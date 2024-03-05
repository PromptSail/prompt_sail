import json
from collections import OrderedDict
from datetime import datetime
from urllib.parse import parse_qs, unquote, urlparse

import pandas as pd
from transactions.schemas import (
    GetTransactionLatencyStatisticsSchema,
    GetTransactionStatusStatisticsSchema,
    GetTransactionUsageStatisticsSchema,
    StatisticTransactionSchema,
)


def serialize_data(obj):
    obj["_id"] = obj["id"]
    del obj["id"]
    return obj


def deserialize_data(obj):
    obj["id"] = obj["_id"]
    del obj["_id"]
    return obj


def extract_tags_from_url(url_str: str) -> tuple[str, dict[str, str]]:
    """
    Extract tags and relevant information from the provided URL.

    :param url_str: The URL string to extract tags from.
    :return: A tuple containing the modified URL (scheme + netloc) and a dictionary with extracted information.
             The dictionary includes 'model', 'experiment', and 'tags'.
    """
    parsed_url = urlparse(url_str)
    query_params = parse_qs(parsed_url.query)
    model = str(query_params.get("model", [""])[0])
    experiment = str(query_params.get("experiment", [""])[0])
    tags = query_params.get("tags", [""])
    tags = tags[0].split(",") if tags else []
    result_dict = {"model": model, "experiment": experiment, "tags": tags}
    return parsed_url.scheme + "://" + parsed_url.netloc, result_dict


def detect_subdomain(host, base_url) -> str | None:
    """
    Detect and extract the subdomain from the given host and base URL.

    :param host: The host obtained from `request.headers.get("host")`, e.g., mydomain.com:8000.
    :param base_url: The base URL from the configuration, e.g., https://mydomain.com or http://localhost:8000.
    :return: The extracted subdomain, if present; otherwise, returns None.
    """
    host = host.split(":")[0]
    base_name = base_url.split("://")[-1].split(":")[0]
    if host.endswith(base_name):
        subdomain = host.replace(base_name, "").split(".")[0]
        return subdomain or None
    return None


def create_transaction_query_from_filters(
    tags: str | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    project_id: str | None = None,
) -> dict:
    """
    Create a MongoDB query dictionary based on specified filters for transactions.

    :param tags: Optional. List of tags to filter transactions by.
    :param date_from: Optional. Start date for filtering transactions.
    :param date_to: Optional. End date for filtering transactions.
    :param project_id: Optional. Project ID to filter transactions by.
    :return: MongoDB query dictionary representing the specified filters.
    """
    query = {}
    if project_id is not None:
        query["project_id"] = project_id
    if tags is not None:
        query["tags"] = {"$all": tags}
    if date_from is not None or date_to is not None:
        query["response_time"] = {}
    if date_from is not None:
        query["response_time"]["$gte"] = date_from
    if date_to is not None:
        query["response_time"]["$lte"] = date_to
    return query


def parse_headers_to_dict(headers: list[tuple[bytes]]) -> dict:
    """
    Parse a list of header tuples into a dictionary.

    :param headers: List of header tuples where each tuple consists of (name: bytes, value: bytes).
    :return: A dictionary representing the parsed headers with names as keys and values as decoded strings.
    """
    return {header[0].decode("utf8"): header[2].decode("utf8") for header in headers}


def req_resp_to_transaction_parser(request, response, response_content) -> dict:
    """
    Parse information from a request, response, and response content into a dictionary representing a transaction.

    :param request: The request object.
    :param response: The response object.
    :param response_content: The content of the response.
    :return: A dictionary containing parsed information from the request, response, and response content.
    """
    response_headers = parse_headers_to_dict(
        response.__dict__["headers"].__dict__["_list"]
    )
    request_headers = parse_headers_to_dict(
        request.__dict__["headers"].__dict__["_list"]
    )
    request_content = json.loads(request.__dict__["_content"].decode("utf8"))

    transaction_params = {
        "library": request_headers["user-agent"],
        "status_code": response.__dict__["status_code"],
        "model": request_content.get("model", None),
        "input_tokens": None,
        "output_tokens": None,
        "os": request_headers.get("x-stainless-os", None),
        "provider": "Unknown",
    }

    if "usage" in response_content:
        transaction_params["input_tokens"] = response_content["usage"].get(
            "prompt_tokens", 0
        )
        transaction_params["output_tokens"] = response_content["usage"].get(
            "completion_tokens", 0
        )

    url = str(request.__dict__["url"])

    if "openai.azure.com" in url and "embeddings" in url:
        transaction_params["type"] = "embedding"
        transaction_params["provider"] = "Azure"
        if isinstance(request_content["input"], list):
            prompt = (
                "[" + ", ".join(map(lambda x: str(x), request_content["input"])) + "]"
            )
        else:
            prompt = str(request_content["input"])

        transaction_params["prompt"] = prompt
        if response.__dict__["status_code"] > 200:
            transaction_params["error_message"] = response_content["message"]
            transaction_params["message"] = None
        else:
            transaction_params["model"] = response_content["model"]
            if isinstance(response_content["data"][0]["embedding"], list):
                msg = (
                    "["
                    + ", ".join(
                        map(lambda x: str(x), response_content["data"][0]["embedding"])
                    )
                    + "]"
                )
            else:
                msg = str(response_content["data"][0]["embedding"])
            transaction_params["message"] = msg
            transaction_params["error_message"] = None

    if "openai.azure.com" in url and "completions" in url:
        transaction_params["type"] = "chat"
        transaction_params["provider"] = "Azure"
        transaction_params["prompt"] = request_content["messages"][0]["content"]
        if response.__dict__["status_code"] > 200:
            # transaction_params["error_message"] = response_content["message"]
            transaction_params["error_message"] = response_content["error"]["message"]
            transaction_params["message"] = None
        else:
            transaction_params["model"] = response_content["model"]
            transaction_params["message"] = response_content["choices"][0]["message"][
                "content"
            ]
            transaction_params["error_message"] = None

    if "api.openai.com" in url and "completions" in url:
        transaction_params["type"] = "chat"
        transaction_params["provider"] = "OpenAI"
        transaction_params["prompt"] = request_content["messages"][0]["content"]
        if response.__dict__["status_code"] > 200:
            transaction_params["error_message"] = response_content["error"]["message"]
            transaction_params["message"] = None
        else:
            transaction_params["model"] = response_headers["openai-model"]
            transaction_params["message"] = response_content["choices"][0]["message"][
                "content"
            ]
            transaction_params["error_message"] = None

    return transaction_params


def token_counter_for_transactions(
    transactions: list[StatisticTransactionSchema], period
) -> list[GetTransactionUsageStatisticsSchema]:
    """
    Calculate token usage statistics based on a given period.

    This function takes a list of transactions and calculates token usage statistics
    aggregated over the specified period (weekly, monthly, hourly, minutely or daily).

    :param transactions: A list of StatisticTransactionSchema objects representing transactions.
    :param period: A string indicating the aggregation period. 
        Choose from 'weekly', 'monthly' 'hourly', 'minutely' or 'daily'.
    :return: A list of GetTransactionUsageStatisticsSchema objects containing token usage statistics.
    """
    data_dicts = [dto.model_dump() for dto in transactions]
    df = pd.DataFrame(data_dicts)
    df.set_index("date", inplace=True)
    period = pandas_period_from_string(period)
    result = df.groupby(["provider", "model"]).resample(period).sum()

    del result["provider"]
    del result["model"]

    result = result.reset_index()

    data_dicts = result.to_dict(orient="records")

    result_list = [
        GetTransactionUsageStatisticsSchema(
            project_id=str(data["project_id"]),
            provider=data["provider"],
            model=data["model"],
            date=data["date"],
            total_input_tokens=data["total_input_tokens"],
            total_output_tokens=data["total_output_tokens"],
            total_transactions=data["total_transactions"],
            total_cost=0,
        )
        for data in data_dicts
    ]

    return result_list


def status_counter_for_transactions(
    transactions: list[StatisticTransactionSchema], period
) -> list[GetTransactionStatusStatisticsSchema]:
    """
    Calculate transaction status statistics based on a given period.

    This function takes a list of transactions and calculates statistics
    on transaction statuses aggregated over the specified period (weekly, monthly, hourly, minutely or daily).

    :param transactions: A list of StatisticTransactionSchema objects representing transactions.
    :param period: A string indicating the aggregation period. 
        Choose from 'weekly', 'monthly' 'hourly', 'minutely' or 'daily'.
    :return: A list of GetTransactionStatusStatisticsSchema objects containing status statistics.
    """
    data_dicts = [dto.model_dump() for dto in transactions]
    for x in range(len(data_dicts)):
        data_dicts[x]["status_code"] = (data_dicts[x]["status_code"] // 100) * 100
    df = pd.DataFrame(data_dicts)
    df.set_index("date", inplace=True)
    period = pandas_period_from_string(period)
        
    result = df.groupby(["status_code"]).resample(period).agg({
        'project_id': 'first',
        'provider': 'first',
        'model': 'first',
        'total_input_tokens': 'sum',
        'total_output_tokens': 'sum',
        'status_code': 'first',
        'latency': 'sum',
        'total_transactions': 'sum'
    })

    del result["status_code"]

    result = result.reset_index()

    data_dicts = result.to_dict(orient="records")

    result_list = [
        GetTransactionStatusStatisticsSchema(
            date=data["date"],
            status_code=data["status_code"],
            total_transactions=data["total_transactions"],
        )
        for data in data_dicts
    ]

    return result_list


def latency_counter_for_transactions(
    transactions: list[StatisticTransactionSchema], period
) -> list[GetTransactionLatencyStatisticsSchema]:
    """
    Calculate transaction latency statistics based on a given period.

    This function takes a list of transactions and calculates statistics
    on transaction latency aggregated over the specified period (weekly, monthly, hourly, minutely or daily).

    :param transactions: A list of StatisticTransactionSchema objects representing transactions.
    :param period: A string indicating the aggregation period. 
        Choose from 'weekly', 'monthly' 'hourly', 'minutely' or 'daily'.
    :return: A list of GetTransactionLatencyStatisticsSchema objects containing latency statistics.
    """
    data_dicts = [dto.model_dump() for dto in transactions]
    df = pd.DataFrame(data_dicts)
    df.set_index("date", inplace=True)
    period = pandas_period_from_string(period)
    result = df.groupby(["provider", "model"]).resample(period).agg({
        'project_id': 'first',
        'provider': 'first',
        'model': 'first',
        'total_input_tokens': 'sum',
        'total_output_tokens': 'sum',
        'status_code': 'first',
        'latency': 'sum',
        'total_transactions': 'sum'
    })

    del result["provider"]
    del result["model"]

    result = result.reset_index()

    data_dicts = result.to_dict(orient="records")
    result_list = [
        GetTransactionLatencyStatisticsSchema(
            provider=data["provider"],
            model=data["model"],
            date=data["date"],
            mean_latency=data["latency"].total_seconds() / data["total_transactions"]
            if data["latency"].total_seconds() > 0
            else 0,
            tokens_per_second=data['total_output_tokens'] / data["latency"].total_seconds()
            if data["latency"].total_seconds() != 0 and data['total_output_tokens'] != 0
            else 0,
            total_transactions=data["total_transactions"],
        )
        for data in data_dicts
    ]

    return result_list


class ProviderPrice:
    def __init__(
        self,
        model_name: str,
        start_date: datetime | str | None,
        match_pattern: str,
        input_price: int | float,
        output_price: int | float,
        total_price: int | float,
    ) -> None:
        """
        Initialize a ProviderPrice object.

        :param model_name: The name of the AI model.
        :param start_date: The start date for the price information.
        :param match_pattern: The match pattern for the price information.
        :param input_price: The price for input usage.
        :param output_price: The price for output usage.
        :param total_price: The total price for usage.
        """
        self.model_name = model_name
        self.start_date = (
            datetime.strptime(start_date, "%Y-%m-%d") if start_date != "" else None
        )
        self.match_pattern = match_pattern
        self.input_price = input_price
        self.output_price = output_price
        self.total_price = total_price

    def __repr__(self):
        """
        Return a string representation of the ProviderPrice object.

        :return: A string representation of the object.
        """
        return (
            "{"
            + f"model_name: {self.model_name}, start_date: {self.start_date}, match_pattern: {self.match_pattern}, input_price: {self.input_price}, output_price: {self.output_price}, total_price: {self.total_price}"
            + "}"
        )


def read_provider_pricelist(
    path: str = "../provider_price_list.json",
) -> list[ProviderPrice]:
    """
    Read the provider price list from a JSON file.

    :param path: The path to the JSON file containing provider prices.
    :return: A list of ProviderPrice objects.
    """
    with open(path, "r") as f:
        data = json.load(f)
    prices = [ProviderPrice(**provider) for provider in data]
    return prices


class ApiURLBuilder:
    @staticmethod
    def build(project, deployment_slug: str, path: str, target_path: str) -> str:
        """
        Build an API URL using the specified project, deployment slug, path, and target path.

        :param project: The project object containing AI providers.
        :param deployment_slug: The deployment slug to identify the AI provider.
        :param path: The base path for the API URL.
        :param target_path: The target path to be appended to the base path.
        :return: The constructed API URL.
        """
        api_base = [
            prov.api_base
            for prov in project.ai_providers
            if prov.slug == deployment_slug
        ][0]
        if path == "":
            path = unquote(target_path) if target_path is not None else ""
        url = api_base + f"/{path}".replace("//", "/")
        return url


class OrderedSet(OrderedDict):
    def __init__(self, iterable=None):
        """
        Create an ordered set, a set that maintains the order of element insertion.

        :param iterable: Optional iterable to initialize the ordered set.
        """
        super().__init__()
        if iterable:
            for item in iterable:
                self.add(item)

    def add(self, item):
        """
        Add an item to the ordered set.

        :param item: The item to add to the set.
        """
        self[item] = None

    def update(self, iterable):
        """
        Update the ordered set with elements from the provided iterable.

        :param iterable: The iterable containing elements to be added to the ordered set.
        """
        for item in iterable:
            self.add(item)


def pandas_period_from_string(period: str):
    if period == "weekly":
        return "W-Mon"
    if period == "monthly":
        return "ME"
    if period == "yearly":
        return "YE"
    if period == "hourly":
        return "H"
    if period == "minutely":
        return "5T"
    return "D"


known_ai_providers = [
    {"provider_name": "OpenAI", "api_base_placeholder": "https://api.openai.com/v1"},
    {
        "provider_name": "Azure OpenAI",
        "api_base_placeholder": "https://your-deployment-name.openai.azure.com",
    },
]
