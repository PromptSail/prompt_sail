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
    project_id: str | None = None
) -> dict:
    query = {}
    if project_id is not None:
        query["project_id"] = project_id
    if tags is not None:
        query["tags"] = {"$all": tags}
    if date_from is not None or date_to is not None:
        query["timestamp"] = {}
    if date_from is not None:
        query["timestamp"]["$gte"] = date_from
    if date_to is not None:
        query["timestamp"]["$lte"] = date_to
    return query
    

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
