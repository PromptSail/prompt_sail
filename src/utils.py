from collections import OrderedDict


def serialize_data(obj):
    obj["_id"] = obj["id"]
    del obj["id"]
    return obj


def deserialize_data(obj):
    obj["id"] = obj["_id"]
    del obj["_id"]
    return obj


def detect_subdomain(host, base_url) -> str | None:
    """

    :param host: as in `request.headers.get("host")`, for example mydomain.com:8000
    :param base_url: as in config, for example: https://mydomain.com or http://localhost:8000
    :return: subdomain, if any
    """
    base_name = base_url.split("://")[-1].split(":")[0]
    if host.endswith(base_name):
        subdomain = host.replace(base_name, "").split(".")[0]
        return subdomain or None
    return None


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
