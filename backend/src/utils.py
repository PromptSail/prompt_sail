import json
from collections import OrderedDict
from datetime import datetime
from urllib.parse import parse_qs, urlparse, unquote

from transactions.schemas import GetTransactionUsageStatisticsSchema, GetTransactionStatusStatisticsSchema


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
        transaction_params["input_tokens"] = response_content["usage"].get("prompt_tokens", 0)
        transaction_params["output_tokens"] = response_content["usage"].get("completion_tokens", 0)

    url = str(request.__dict__["url"])

    if "openai.azure.com" in url and "embeddings" in url:
        transaction_params["type"] = "embedding"
        transaction_params["provider"] = "Azure"
        if isinstance(request_content["input"], list):
            prompt = (
                    "["
                    + ", ".join(
                        map(lambda x: str(x), request_content["input"])
                    )
                    + "]"
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
    transactions: list[GetTransactionUsageStatisticsSchema]
) -> list[GetTransactionUsageStatisticsSchema]:
    result = {}
    for transaction in transactions:
        key = (transaction.provider, transaction.model)
        if key in result:
            result[key][0] += transaction.total_input_tokens
            result[key][1] += transaction.total_output_tokens
            result[key][2] += transaction.total_transactions
        else:
            result[key] = [
                transaction.total_input_tokens, 
                transaction.total_output_tokens, 
                transaction.total_transactions
            ]

    result_list = [GetTransactionUsageStatisticsSchema(
        project_id=transactions[0].project_id, 
        provider=provider,
        model=model, 
        total_input_tokens=input_tokens, 
        total_output_tokens=output_tokens,
        total_transactions=total_transactions
    ) for (provider, model), (input_tokens, output_tokens, total_transactions) in result.items()]

    return result_list


def status_counter_for_transactions(
    transactions: list[GetTransactionStatusStatisticsSchema]
) -> list[GetTransactionStatusStatisticsSchema]:
    result = {}
    for transaction in transactions:
        key = (transaction.provider, transaction.model, transaction.status_code)
        if key in result:
            result[key] += 1
        else:
            result[key] = 1

    result_list = [GetTransactionStatusStatisticsSchema(
        project_id=transactions[0].project_id, 
        provider=provider,
        model=model, 
        status_code=status_code,
        total_transactions=total_transactions
    ) for (provider, model, status_code), total_transactions in result.items()]

    return result_list


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


known_ai_providers = [
    {"provider_name": "OpenAI", "api_base_placeholder": "https://api.openai.com/v1"},
    {
        "provider_name": "Azure OpenAI",
        "api_base_placeholder": "https://your-deployment-name.openai.azure.com",
    },
]
