from typing import Any

from pydantic import BaseModel
from seedwork.exceptions import NotFoundException
from utils import deserialize_data, serialize_data
from app.logging import logger


class DocumentNotFoundException(NotFoundException):
    pass


class MongoRepository:
    """
    Generic repository for managing and accessing MongoDB data.

    Provides basic CRUD operations and data retrieval methods.
    """

    model_class = BaseModel

    def __init__(self, db_client, collection_name):
        """
        Initialize the MongoRepository with the MongoDB client and collection name.

        :param db_client: The MongoDB client.
        :param collection_name: The name of the collection in the MongoDB database.
        """
        self._collection = db_client[collection_name]

    def add(self, doc: BaseModel):
        """
        Add a document to the repository.

        :param doc: The BaseModel object to be added.
        :return: The result of the add operation.
        """
        try:
            data = serialize_data(doc.model_dump())
            logger.debug(f"Attempting to insert document into {self._collection.name}")
            result = self._collection.insert_one(data)
            logger.debug(f"MongoDB insert result: {result.inserted_id}")
            return result
        except Exception as e:
            logger.error(f"MongoDB insert error in collection {self._collection.name}: {str(e)}")
            raise

    def update(self, doc: BaseModel):
        """
        Update a document in the repository.

        :param doc: The BaseModel object to be updated.
        :return: The result of the update operation.
        """
        data = serialize_data(doc.model_dump())
        result = self._collection.update_one({"_id": doc.id}, {"$set": data})
        return result

    def delete(self, doc_id: str):
        """
        Delete a document from the repository by its unique identifier.

        :param doc_id: The unique identifier of the document to be deleted.
        :return: The result of the delete operation.
        """
        result = self._collection.delete_one({"_id": doc_id})
        return result

    def delete_many(self, filter_by: dict[str, Any]):
        """
        Delete multiple documents from the repository based on the provided filter.

        :param filter_by: The filter criteria for deleting documents.
        :return: The result of the delete operation.
        """
        result = self._collection.delete_many(filter_by)
        return result

    def find_one(self, filter_by=None):
        """
        Retrieve a single document from the repository based on the provided filter.

        :param filter_by: The filter criteria for retrieving the document.
        :return: The BaseModel object corresponding to the specified filter.
        """
        data = self._collection.find_one(filter_by or {})
        if data is None:
            raise DocumentNotFoundException(f"Document not found: {filter_by}")
        return self.model_class(**deserialize_data(data))

    def find(self, filter_by=None):
        """
        Retrieve a list of documents from the repository based on the provided filter.

        :param filter_by: The filter criteria for retrieving documents.
        :return: A list of BaseModel objects corresponding to the specified filter.
        """
        return [
            self.model_class(**deserialize_data(data))
            for data in self._collection.find(filter_by or {})
        ]

    def get(self, doc_id: str) -> BaseModel:
        """
        Retrieve a document by its unique identifier.

        :param doc_id: The unique identifier of the document to be retrieved.
        :return: The BaseModel object corresponding to the specified identifier.
        """
        return self.find_one({"_id": doc_id})

    def get_all(self, **kwargs):
        """
        Retrieve all documents from the repository.

        :param kwargs: Additional optional parameters for filtering.
        :return: A list of all BaseModel objects stored in the repository.
        """
        return self.find(kwargs)

    def count(self, filter_by=None):
        """
        Count the number of documents in the repository based on the provided filter.

        :param filter_by: The filter criteria for counting documents.
        :return: The count of documents that meet the specified filtering criteria.
        """
        return self._collection.count_documents(filter_by or {})

    def remove_all(self):
        """
        Remove all documents from the repository.

        :return: The result of the delete operation for all documents.
        """
        return self._collection.delete_many({})

    # def exists(self, filter_by=None) -> bool:
    #     return self._collection.find_one(filter_by or {}) is not None
