import json
from collections import OrderedDict
from datetime import datetime
from urllib.parse import parse_qs, urlparse


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

    :param url_str: string (url) with tags in query params, for example: http://dom.com/?experiment=2&tags=3,4
    :return: tuple[str, dict[str, str]]: tuple of url without tags and dict of tags
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

    :param host: as in `request.headers.get("host")`, for example mydomain.com:8000
    :param base_url: as in config, for example: https://mydomain.com or http://localhost:8000
    :return: subdomain, if any
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
    return {header[0].decode("utf8"): header[2].decode("utf8") for header in headers}


def req_resp_to_transaction_parser(request, response, response_content) -> dict:
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
        "token_usage": None,
        "os": request_headers.get("x-stainless-os", None),
    }

    url = str(request.__dict__["url"])

    if "openai.azure.com" in url and "embeddings" in url:
        transaction_params["type"] = "embedding"
        transaction_params["prompt"] = request_content["input"]
        if response.__dict__["status_code"] > 200:
            transaction_params["error_message"] = response_content["message"]
            transaction_params["message"] = None
        else:
            transaction_params["model"] = response_content["model"]
            transaction_params["token_usage"] = response_content["usage"][
                "total_tokens"
            ]
            msg = (
                "["
                + ", ".join(
                    map(lambda x: str(x), response_content["data"][0]["embedding"])
                )
                + "]"
            )
            transaction_params["message"] = msg
            transaction_params["error_message"] = None

    if "openai.azure.com" in url and "completions" in url:
        transaction_params["type"] = "chat"
        transaction_params["prompt"] = request_content["messages"][0]["content"]
        if response.__dict__["status_code"] > 200:
            transaction_params["error_message"] = response_content["message"]
            transaction_params["message"] = None
        else:
            transaction_params["model"] = response_content["model"]
            transaction_params["token_usage"] = response_content["usage"][
                "total_tokens"
            ]
            transaction_params["message"] = response_content["choices"][0]["message"][
                "content"
            ]
            transaction_params["error_message"] = None

    if "api.openai.com" in url and "completions" in url:
        transaction_params["type"] = "chat"
        transaction_params["prompt"] = request_content["messages"][0]["content"]
        if response.__dict__["status_code"] > 200:
            transaction_params["error_message"] = response_content["error"]["message"]
            transaction_params["message"] = None
        else:
            transaction_params["model"] = response_headers["openai-model"]
            transaction_params["token_usage"] = response_content["usage"][
                "total_tokens"
            ]
            transaction_params["message"] = response_content["choices"][0]["message"][
                "content"
            ]
            transaction_params["error_message"] = None

    return transaction_params


class ApiURLBuilder:
    @staticmethod
    def build(project, deployment_name: str, path: str, target_path: str) -> str:
        api_base = [
            prov.api_base
            for prov in project.ai_providers
            if prov.deployment_name == deployment_name
        ][0]
        if path == "":
            path = target_path if target_path is not None else ""
        return f"{api_base}/{path}"


class OrderedSet(OrderedDict):
    def __init__(self, iterable=None):
        super().__init__()
        if iterable:
            for item in iterable:
                self.add(item)

    def add(self, item):
        self[item] = None

    def update(self, iterable):
        for item in iterable:
            self.add(item)


known_ai_providers = [
    {
        "provider_name": "OpenAI",
        "api_base_placeholder": "https://api.openai.com/v1"
    },
    {
        "provider_name": "Azure OpenAI",
        "api_base_placeholder": "https://your-deployment-name.openai.azure.com"
    }
]
