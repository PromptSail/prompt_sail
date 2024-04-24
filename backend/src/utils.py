import json
import random
import re
from collections import OrderedDict
from enum import Enum
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

import numpy as np
import pandas as pd
from _datetime import datetime, timedelta
from transactions.models import Transaction
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
    status_code: int | None = None,
) -> dict:
    """
    Create a MongoDB query dictionary based on specified filters for transactions.

    :param tags: Optional. List of tags to filter transactions by.
    :param date_from: Optional. Start date for filtering transactions.
    :param date_to: Optional. End date for filtering transactions.
    :param project_id: Optional. Project ID to filter transactions by.
    :param status_code: Optional. Status code of the transactions.
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
    if status_code is not None:
        query["status_code"] = status_code
    return query


def parse_headers_to_dict(headers: list[tuple[bytes]]) -> dict:
    """
    Parse a list of header tuples into a dictionary.

    :param headers: List of header tuples where each tuple consists of (name: bytes, value: bytes).
    :return: A dictionary representing the parsed headers with names as keys and values as decoded strings.
    """
    return {header[0].decode("utf8"): header[2].decode("utf8") for header in headers}


class TransactionParamsBuilder:
    library: str | None = None
    status_code: int | None = None
    model: str | None = None
    model_type: str | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    prompt: str | None = None
    os: str | None = None
    provider: str | None = None
    messages: list[dict[str, Any]] | str | None = None
    last_message: str | None = None
    error_message: str | None = None

    def add_library(self, library: str):
        self.library = library
        return self

    def add_status_code(self, status_code: int):
        self.status_code = status_code
        return self

    def add_model(self, model: str):
        self.model = model
        return self

    def add_type(self, model_type: str):
        self.model_type = model_type
        return self

    def add_prompt(self, prompt: str):
        self.prompt = prompt
        return self

    def add_input_tokens(self, input_tokens: int):
        self.input_tokens = input_tokens
        return self

    def add_output_tokens(self, output_tokens: int):
        self.output_tokens = output_tokens
        return self

    def add_os(self, os: str | None):
        self.os = os
        return self

    def add_provider(self, provider: str):
        self.provider = provider
        return self

    def add_messages(self, messages: list[dict[str, str]]):
        self.messages = messages
        return self

    def add_last_message(self, last_message: str | None):
        self.last_message = last_message
        return self

    def add_error_message(self, error_message: str):
        self.error_message = error_message
        return self

    def build(self):
        return {
            "library": self.library,
            "status_code": self.status_code,
            "model": self.model,
            "type": self.model_type,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "prompt": self.prompt,
            "os": self.os,
            "provider": self.provider,
            "messages": self.messages,
            "last_message": self.last_message,
            "error_message": self.error_message,
        }


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
    url = str(request.__dict__["url"])

    azure_embeddings_pattern = re.compile(r".*openai\.azure\.com.*embeddings.*")
    azure_completions_pattern = re.compile(r".*openai\.azure\.com.*completions.*")
    openai_chat_completions_pattern = re.compile(
        r".*api\.openai\.com.*chat.*completions.*"
    )
    openai_completions_pattern = re.compile(
        r".*api\.openai\.com(?!.*chat).*\/completions.*"
    )
    openai_embeddings_pattern = re.compile(r".*api\.openai\.com.*embeddings.*")

    transaction_params = TransactionParamsBuilder()
    transaction_params.add_library(request_headers["user-agent"]).add_status_code(
        response.__dict__["status_code"]
    ).add_model(request_content.get("model", None)).add_os(
        request_headers.get("x-stainless-os", None)
    )

    if "usage" in response_content:
        transaction_params.add_input_tokens(
            response_content["usage"].get("prompt_tokens", 0)
        ).add_output_tokens(response_content["usage"].get("completion_tokens", 0))

    if azure_embeddings_pattern.match(url):
        transaction_params.add_type("embedding").add_provider("Azure OpenAI")
        if isinstance(request_content["input"], list):
            transaction_params.add_prompt(
                "[" + ", ".join(map(lambda x: str(x), request_content["input"])) + "]"
            )
        else:
            transaction_params.add_prompt(request_content["input"])
        if response.__dict__["status_code"] > 200:
            transaction_params.add_error_message(response_content["message"])
        else:
            transaction_params.add_model(response_content["model"])
            if isinstance(response_content["data"][0]["embedding"], list):
                transaction_params.add_last_message(
                    "["
                    + ", ".join(
                        map(lambda x: str(x), response_content["data"][0]["embedding"])
                    )
                    + "]"
                )
            else:
                transaction_params.add_last_message(
                    response_content["data"][0]["embedding"]
                )

    if azure_completions_pattern.match(url):
        prompt = [
            message["content"]
            for message in request_content["messages"]
            if message["role"] == "user"
        ][::-1][0]
        transaction_params.add_type("completions").add_provider(
            "Azure OpenAI"
        ).add_prompt(prompt if prompt else request_content["messages"][0]["content"])
        messages = request_content["messages"]
        if response.__dict__["status_code"] > 200:
            messages.append(
                {
                    "role": "error",
                    "content": response_content["error"]["message"]
                    if "error" in response_content.keys()
                    else response_content["message"],
                }
            )

            transaction_params.add_error_message(
                response_content["error"]["message"]
                if "error" in response_content.keys()
                else response_content["message"]
            ).add_last_message(
                response_content["error"]["message"]
                if "error" in response_content.keys()
                else response_content["message"]
            ).add_messages(
                messages
            )
        else:
            messages.append(response_content["choices"][0]["message"])

            transaction_params.add_messages(messages).add_model(
                response_content["model"]
            ).add_last_message(response_content["choices"][0]["message"]["content"])

    if openai_chat_completions_pattern.match(url):
        prompt = [
            message["content"]
            for message in request_content["messages"]
            if message["role"] == "user"
        ][::-1][0]
        transaction_params.add_type("chat completions").add_provider(
            "OpenAI"
        ).add_prompt(prompt if prompt else request_content["messages"][0]["content"])
        messages = request_content["messages"]
        if response.__dict__["status_code"] > 200:
            messages.append(
                {"role": "error", "content": response_content["error"]["message"]}
            )
            transaction_params.add_error_message(
                response_content["error"]["message"]
            ).add_last_message(response_content["error"]["message"]).add_messages(
                messages
            )
        else:
            messages.append(response_content["choices"][0]["message"])
            transaction_params.add_messages(messages).add_model(
                response_headers["openai-model"]
                if "openai-model" in response_headers
                else response_content["model"]
            ).add_last_message(response_content["choices"][0]["message"]["content"])

    if openai_completions_pattern.match(url):
        transaction_params.add_type("completions").add_provider("OpenAI").add_prompt(
            request_content["prompt"]
        )
        messages = [{"role": "user", "content": request_content["prompt"]}]
        if response.__dict__["status_code"] > 200:
            messages.append(
                {"role": "error", "content": response_content["error"]["message"]}
            )
            transaction_params.add_error_message(
                response_content["error"]["message"]
            ).add_last_message(response_content["error"]["message"]).add_messages(
                messages
            )
        else:
            messages.append(response_content["choices"][0]["message"])
            transaction_params.add_messages(messages).add_model(
                response_headers["openai-model"]
                if "openai-model" in response_headers
                else response_content["model"]
            ).add_last_message(response_content["choices"][0]["message"]["content"])

    if openai_embeddings_pattern.match(url):
        transaction_params.add_type("embedding").add_provider("OpenAI")
        if isinstance(request_content["input"], list):
            transaction_params.add_prompt(
                "[" + ", ".join(map(lambda x: str(x), request_content["input"])) + "]"
            )
        else:
            transaction_params.add_prompt(request_content["input"])
        if response.__dict__["status_code"] > 200:
            transaction_params.add_error_message(
                response_content["error"]["message"]
            ).add_last_message(None)
        else:
            transaction_params.add_model(response_content["model"])
            if isinstance(response_content["data"][0]["embedding"], list):
                transaction_params.add_last_message(
                    "["
                    + ", ".join(
                        map(lambda x: str(x), response_content["data"][0]["embedding"])
                    )
                    + "]"
                )
            else:
                transaction_params.add_last_message(
                    response_content["data"][0]["embedding"]
                )

    return transaction_params.build()


def token_counter_for_transactions(
    transactions: list[StatisticTransactionSchema],
    period: str,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
) -> list[GetTransactionUsageStatisticsSchema]:
    """
    Calculate token usage statistics based on a given period.

    This function takes a list of transactions and calculates token usage statistics
    aggregated over the specified period (weekly, monthly, hourly, minutely or daily).

    :param transactions: A list of StatisticTransactionSchema objects representing transactions.
    :param period: A string indicating the aggregation period.
        Choose from 'weekly', 'monthly' 'hourly', 'minutely' or 'daily'.
    :param date_from: The starting date for the filter.
    :param date_to: The ending date for the filter.
    :return: A list of GetTransactionUsageStatisticsSchema objects containing token usage statistics.
    """
    data_dicts = [dto.model_dump() for dto in transactions]
    df = pd.DataFrame(data_dicts)
    project_id = data_dicts[0]["project_id"]
    pairs = list(set([(data["provider"], data["model"]) for data in data_dicts]))
    if date_from:
        for pair_idx in range(len(pairs)):
            df.loc[len(df)] = {
                "date": pd.Timestamp(date_from),
                "project_id": project_id,
                "provider": pairs[pair_idx][0],
                "model": pairs[pair_idx][1],
                "total_input_tokens": 0,
                "total_output_tokens": 0,
                "total_input_cost": 0,
                "total_output_cost": 0,
                "total_cost": 0,
                "status_code": 0,
                "latency": timedelta(0),
                "total_transactions": 0,
                "generation_speed": 0,
            }
    if date_to:
        for pair in pairs:
            df.loc[len(df)] = {
                "date": pd.Timestamp(date_to),
                "project_id": project_id,
                "provider": pair[0],
                "model": pair[1],
                "total_input_tokens": 0,
                "total_output_tokens": 0,
                "total_input_cost": 0,
                "total_output_cost": 0,
                "total_cost": 0,
                "status_code": 0,
                "latency": timedelta(0),
                "total_transactions": 0,
                "generation_speed": 0,
            }

    df.set_index("date", inplace=True)
    period = pandas_period_from_string(period)
    result = (
        df.groupby(["provider", "model"])
        .resample(period)
        .agg(
            {
                "project_id": "first",
                "provider": "first",
                "model": "first",
                "total_input_tokens": "sum",
                "total_output_tokens": "sum",
                "total_input_cost": "sum",
                "total_output_cost": "sum",
                "total_cost": "sum",
                "status_code": "sum",
                "latency": "sum",
                "total_transactions": "sum",
                "generation_speed": "sum",
            }
        )
    )

    del result["provider"]
    del result["model"]

    result = result.reset_index()

    result["output_cumulative_total"] = result.groupby(["provider", "model"])[
        "total_output_tokens"
    ].cumsum()
    result["input_cumulative_total"] = result.groupby(["provider", "model"])[
        "total_input_tokens"
    ].cumsum()

    data_dicts = result.to_dict(orient="records")

    result_list = [
        GetTransactionUsageStatisticsSchema(
            provider=data["provider"],
            model=data["model"],
            date=data["date"],
            total_input_tokens=data["total_input_tokens"],
            total_output_tokens=data["total_output_tokens"],
            input_cumulative_total=data["input_cumulative_total"],
            output_cumulative_total=data["output_cumulative_total"],
            total_transactions=data["total_transactions"],
            total_cost=data["total_cost"],
        )
        for data in data_dicts
    ]

    return result_list


def status_counter_for_transactions(
    transactions: list[StatisticTransactionSchema],
    period: str,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
) -> list[GetTransactionStatusStatisticsSchema]:
    """
    Calculate transaction status statistics based on a given period.

    This function takes a list of transactions and calculates statistics
    on transaction statuses aggregated over the specified period (weekly, monthly, hourly, minutely or daily).

    :param transactions: A list of StatisticTransactionSchema objects representing transactions.
    :param period: A string indicating the aggregation period.
        Choose from 'weekly', 'monthly' 'hourly', 'minutely' or 'daily'.
    :param date_from: The starting date for the filter.
    :param date_to: The ending date for the filter.
    :return: A list of GetTransactionStatusStatisticsSchema objects containing status statistics.
    """
    data_dicts = [dto.model_dump() for dto in transactions]
    for x in range(len(data_dicts)):
        data_dicts[x]["status_code"] = (data_dicts[x]["status_code"] // 100) * 100
    df = pd.DataFrame(data_dicts)
    df.set_index("date", inplace=True)

    if date_from:
        date_from = str(date_from)
        df.loc[pd.Timestamp(date_from)] = pd.NA
    if date_to:
        date_to = str(date_to)
        df.loc[pd.Timestamp(date_to)] = pd.NA

    period = pandas_period_from_string(period)

    result = df.resample(period).agg(
        {
            "project_id": "first",
            "provider": "first",
            "model": "first",
            "total_input_tokens": "sum",
            "total_output_tokens": "sum",
            "total_input_cost": "sum",
            "total_output_cost": "sum",
            "total_cost": "sum",
            "status_code": [
                ("status_200", lambda code: (code == 200).sum()),
                ("status_300", lambda code: (code == 300).sum()),
                ("status_400", lambda code: (code == 400).sum()),
                ("status_500", lambda code: (code == 500).sum()),
            ],
            "latency": "sum",
            "total_transactions": "sum",
            "generation_speed": "sum",
        }
    )
    result = result.reset_index()

    data_dicts = result.to_dict(orient="records")

    new_data_dicts = []
    for data in data_dicts:
        new_data = {}
        for key, value in data.items():
            if key[0] == "status_code":
                new_key = key[1]
            else:
                new_key = key[0]
            new_data[new_key] = value
        new_data_dicts.append(new_data)

    result_list = [
        GetTransactionStatusStatisticsSchema(
            date=data["date"],
            status_200=data["status_200"],
            status_300=data["status_300"],
            status_400=data["status_400"],
            status_500=data["status_500"],
            total_transactions=data["total_transactions"],
        )
        for data in new_data_dicts
    ]

    return result_list


def speed_counter_for_transactions(
    transactions: list[StatisticTransactionSchema],
    period: str,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
) -> list[GetTransactionLatencyStatisticsSchema]:
    """
    Calculate transaction latency statistics based on a given period.

    This function takes a list of transactions and calculates statistics
    on transaction latency aggregated over the specified period (weekly, monthly, hourly, minutely or daily).

    :param transactions: A list of StatisticTransactionSchema objects representing transactions.
    :param period: A string indicating the aggregation period.
        Choose from 'weekly', 'monthly' 'hourly', 'minutely' or 'daily'.
    :param date_from: The starting date for the filter.
    :param date_to: The ending date for the filter.
    :return: A list of GetTransactionLatencyStatisticsSchema objects containing latency statistics.
    """
    data_dicts = [dto.model_dump() for dto in transactions]
    df = pd.DataFrame(data_dicts)
    project_id = data_dicts[0]["project_id"]
    pairs = set([(data["provider"], data["model"]) for data in data_dicts])
    if date_from:
        for pair in pairs:
            df.loc[len(df)] = {
                "date": pd.Timestamp(date_from),
                "project_id": project_id,
                "provider": pair[0],
                "model": pair[1],
                "total_input_tokens": 0,
                "total_output_tokens": 0,
                "total_input_cost": 0,
                "total_output_cost": 0,
                "total_cost": 0,
                "status_code": 0,
                "latency": timedelta(0),
                "total_transactions": 0,
                "generation_speed": 0,
            }
    if date_to:
        for pair in pairs:
            df.loc[len(df)] = {
                "date": pd.Timestamp(date_to),
                "project_id": project_id,
                "provider": pair[0],
                "model": pair[1],
                "total_input_tokens": 0,
                "total_output_tokens": 0,
                "total_input_cost": 0,
                "total_output_cost": 0,
                "total_cost": 0,
                "status_code": 0,
                "latency": timedelta(0),
                "total_transactions": 0,
                "generation_speed": 0,
            }
    df.set_index("date", inplace=True)
    period = pandas_period_from_string(period)
    result = (
        df.assign(
            transactions_code_200=lambda x: np.where(x["status_code"] == 200, 1, 0)
        )
        .groupby(["provider", "model"])
        .resample(period)
        .agg(
            {
                "project_id": "first",
                "provider": "first",
                "model": "first",
                "total_input_tokens": "sum",
                "total_output_tokens": "sum",
                "total_input_cost": "sum",
                "total_output_cost": "sum",
                "total_cost": "sum",
                "status_code": "first",
                "latency": "sum",
                "total_transactions": "sum",
                "generation_speed": "sum",
                "transactions_code_200": "sum",
            }
        )
    )

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
            tokens_per_second=data["generation_speed"] / data["transactions_code_200"]
            if data["generation_speed"] > 0 and data["transactions_code_200"] > 0
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
        provider: str,
        start_date: datetime | str | None,
        match_pattern: str,
        input_price: int | float,
        output_price: int | float,
        total_price: int | float,
        is_active: bool,
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
        self.provider = provider
        self.start_date = (
            datetime.strptime(start_date, "%Y-%m-%d") if start_date != "" else None
        )
        self.match_pattern = match_pattern
        self.input_price = input_price
        self.output_price = output_price
        self.total_price = total_price
        self.is_active = is_active

    def __repr__(self):
        """
        Return a string representation of the ProviderPrice object.

        :return: A string representation of the object.
        """
        return (
            "{"
            + f"model_name: {self.model_name}, provider: {self.provider}, start_date: {self.start_date}, match_pattern: {self.match_pattern}, input_price: {self.input_price}, output_price: {self.output_price}, total_price: {self.total_price}"
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
            path = unquote(unquote(target_path)) if target_path is not None else ""
            if len(path.split("/")[1:]) > 5:
                new_path = path.split("/")[1:]
                new_path = new_path[0:3] + new_path[5:7]
                path = "/" + "/".join(new_path)

        url = api_base + f"/{path}".replace("//", "/")
        if api_base.endswith("/"):
            url = api_base + f"{path}".replace("//", "/")

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
    if period == PeriodEnum.week:
        return "W-Mon"
    if period == PeriodEnum.month:
        return "ME"
    if period == PeriodEnum.year:
        return "YE"
    if period == PeriodEnum.hour:
        return "h"
    if period == PeriodEnum.minutes:
        return "5min"
    return "D"


def generate_mock_transactions(n: int, date_from: datetime, date_to: datetime):
    """
    Generate a list of mock transactions.

    This function creates a list of transaction objects for testing purposes.
    The transactions are either successful (status code 200) with randomly
    generated input and output tokens or unsuccessful with no input/output tokens.

    Parameters:
    n (int): The number of transactions to generate.
    date_from (datetime): The start date from which transactions should be added.
    date_to (datetime): The end date till which transactions should be added.

    Returns:
    list: A list of Transaction objects.

    """
    providers = ["Azure", "OpenAI"]
    models = ["gpt-3.5-turbo", "gpt-4", "text-davinci-001"]
    status_codes = [200, 300, 400, 500]

    transactions = []

    for x in range(0, n):
        transaction_id = f"transaction-{x}"
        input_tokens = random.randint(5, 25)
        output_tokens = random.randint(200, 800)

        # Generate random date within date_from and date_to
        time_between_dates = date_to - date_from
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = date_from + timedelta(days=random_number_of_days)
        start_date = random_date
        stop_date = start_date + timedelta(
            seconds=random.randint(1, 6), milliseconds=random.randint(0, 999)
        )

        # Generate random status code according to the distribution, the most common status code is 200, rest is less probable
        status = random.choices(status_codes, [0.75, 0.15, 0.05, 0.05])[0]

        # If status is not 200, set input/output tokens to 0 and error message to "Error"
        error_message = None if status == 200 else "Error"
        generation_speed = (
            output_tokens / (stop_date - start_date).total_seconds()
            if status == 200
            else 0
        )
        output_tokens = output_tokens if status == 200 else 0

        transactions.append(
            Transaction(
                id=transaction_id,
                project_id="project-test",
                request={},
                response={},
                tags=["tag1", "tag2", "tag3"],
                provider=random.choice(providers),
                model=random.choice(models),
                type="chat",
                os=None,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                library="PostmanRuntime/7.36.3",
                status_code=status,
                messages=None,
                prompt="",
                last_message="",
                error_message=error_message,
                request_time=start_date,
                response_time=stop_date,
                generation_speed=generation_speed,
            )
        )

    return transactions


def check_dates_for_statistics(
    date_from: datetime | str | None, date_to: datetime | str | None
) -> tuple[datetime | None, datetime | None]:
    if isinstance(date_from, str):
        if len(date_from) == 10:
            date_from = datetime.fromisoformat(str(date_from) + "T00:00:00")
        elif date_from.endswith("Z"):
            date_from = datetime.fromisoformat(str(date_from)[:-1])
        else:
            date_from = datetime.fromisoformat(date_from)
    if isinstance(date_to, str):
        if len(date_to) == 10:
            date_to = datetime.fromisoformat(date_to + "T23:59:59")
        elif date_to.endswith("Z"):
            date_to = datetime.fromisoformat(str(date_to)[:-1])
        else:
            date_to = datetime.fromisoformat(date_to)

    if date_from is not None and date_to is not None and date_from == date_to:
        date_to = date_to + timedelta(days=1) - timedelta(seconds=1)

    return date_from, date_to


def read_transactions_from_csv(
    path: str = "../test_transactions.csv",
) -> list[Transaction]:
    df = pd.read_csv(path, sep=";")
    data = df.to_dict(orient="records")
    transactions = []
    for idx, obj in enumerate(data):
        transaction_id = f"test-transaction-{idx}"
        request_time = datetime.fromisoformat(
            obj["request_time"].replace("Z", "+00:00")
        )
        response_time = datetime.fromisoformat(
            obj["response_time"].replace("Z", "+00:00")
        )
        latency = response_time - request_time
        if obj["status_code"] == 200:
            transactions.append(
                Transaction(
                    id=transaction_id,
                    project_id="project-test",
                    request={},
                    response={},
                    tags=["tag"],
                    provider=obj["provider"],
                    model=obj["model"],
                    type="chat",
                    os=None,
                    input_tokens=obj["input_tokens"],
                    output_tokens=obj["output_tokens"],
                    library="PostmanRuntime/7.36.3",
                    status_code=obj["status_code"],
                    messages=None,
                    prompt="",
                    last_message="",
                    error_message=None,
                    request_time=request_time,
                    response_time=response_time,
                    generation_speed=obj["output_tokens"] / latency.total_seconds()
                    if latency.total_seconds() > 0
                    else 0,
                    input_cost=None,
                    output_cost=None,
                    total_cost=None,
                )
            )
        else:
            transactions.append(
                Transaction(
                    id=transaction_id,
                    project_id="project-test",
                    request={},
                    response={},
                    tags=["tag"],
                    provider=obj["provider"],
                    model=obj["model"],
                    type="chat",
                    os=None,
                    input_tokens=0,
                    output_tokens=0,
                    library="PostmanRuntime/7.36.3",
                    status_code=obj["status_code"],
                    messages=None,
                    prompt="",
                    last_message="",
                    error_message="Error",
                    request_time=request_time,
                    response_time=response_time,
                    generation_speed=0,
                    input_cost=None,
                    output_cost=None,
                    total_cost=None,
                )
            )
    return transactions


class PeriodEnum(str, Enum):
    week = "week"
    year = "year"
    month = "month"
    day = "day"
    hour = "hour"
    minutes = "5minutes"


known_ai_providers = [
    {"provider_name": "OpenAI", "api_base_placeholder": "https://api.openai.com/v1"},
    {
        "provider_name": "Azure OpenAI",
        "api_base_placeholder": "https://your-deployment-name.openai.azure.com",
    },
    {
        "provider_name": "Anthropic",
        "api_base_placeholder": "https://api.anthropic.com/v1",
    },
    {
        "provider_name": "Other",
        "api_base_placeholder": "https://llmapi.provider.com/v1",
    },
]
