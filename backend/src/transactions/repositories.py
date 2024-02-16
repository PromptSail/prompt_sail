from datetime import datetime

from seedwork.exceptions import NotFoundException
from seedwork.repositories import MongoRepository
from transactions.models import Transaction


class TransactionNotFoundException(NotFoundException):
    """
    Exception raised when a transaction is not found.
    """
    pass


class TransactionRepository(MongoRepository):
    """
    Repository for managing and accessing transaction data.

    Inherits from MongoRepository and is specific to the Transaction model.
    """
    model_class = Transaction

    def add(self, doc):
        """
        Add a document to the repository.
        
        :param doc: The document to be added to the repository.
        :return: The result of the add operation.
        """
        result = super().add(doc)
        return result

    def get_for_project(self, project_id: str) -> list[Transaction]:
        """
        Retrieve a list of transactions associated with a specific project.

        :param project_id: The identifier of the project for which transactions are retrieved.
        :return: A list of Transaction objects associated with the specified project. 
        """
        return self.find({"project_id": project_id})

    def get_one_by_id(self, transaction_id: str) -> Transaction:
        """
        Retrieve a specific transaction by its unique identifier.

        :param transaction_id: The unique identifier of the transaction to retrieve.
        :return: The Transaction object corresponding to the specified transaction_id.
        """
        return self.find_one({"_id": transaction_id})

    def get_paginated_and_filtered(
        self, page: int, page_size: int, query: dict[str, str | datetime | None] = None
    ) -> list[Transaction]:
        """
        Retrieve a paginated and filtered list of transactions from the repository.

        :param page: The page number for pagination.
        :param page_size: The number of transactions per page.
        :param query: Optional query parameters to filter transactions.
        :return: A paginated and filtered list of Transaction objects based on the specified criteria.
        """
        return self.find(query)[::-1][
            (page - 1) * page_size : (page - 1) * page_size + page_size
        ]

    def delete_cascade(self, project_id: str):
        """
        Delete multiple transactions and related data for a specific project using cascading deletion.
        
        :param project_id: The Project ID for which transactions and related data will be deleted.
        :return: The result of the cascading deletion operation.
        """
        return self.delete_many(filter_by={"project_id": project_id})
