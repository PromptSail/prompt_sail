from pydantic import BaseModel

from seedwork.exceptions import NotFoundException
from utils import deserialize_data, serialize_data


class DocumentNotFoundException(NotFoundException):
    pass


class MongoRepository:
    model_class = BaseModel

    def __init__(self, db_client, collection_name):
        self._collection = db_client[collection_name]

    def add(self, doc: BaseModel):
        data = serialize_data(doc.model_dump())
        result = self._collection.insert_one(data)
        return result

    def update(self, doc: BaseModel):
        data = serialize_data(doc.model_dump())
        result = self._collection.update_one({"_id": doc.id}, {"$set": data})
        return result

    def delete(self, doc_id: str):
        result = self._collection.delete_one({"_id": doc_id})
        return result

    def find_one(self, filter_by=None):
        data = self._collection.find_one(filter_by or {})
        if data is None:
            raise DocumentNotFoundException(f"Document not found: {filter_by}")
        return self.model_class(**deserialize_data(data))

    def find(self, filter_by=None):
        return [
            self.model_class(**deserialize_data(data))
            for data in self._collection.find(filter_by or {})
        ]

    def get(self, doc_id: str) -> BaseModel:
        return self.find_one({"_id": doc_id})

    def get_all(self, **kwargs):
        return self.find(kwargs)

    def count(self, filter_by=None):
        return self._collection.count_documents(filter_by or {})

    # def exists(self, filter_by=None) -> bool:
    #     return self._collection.find_one(filter_by or {}) is not None

    def remove_all(self):
        return self._collection.delete_many({})
