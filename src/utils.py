from collections import OrderedDict


def serialize_data(obj):
    obj["_id"] = obj["id"]
    del obj["id"]
    return obj


def deserialize_data(obj):
    obj["id"] = obj["_id"]
    del obj["_id"]
    return obj


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
