from datetime import datetime
from operator import attrgetter
import json

from seedwork.exceptions import NotFoundException
from seedwork.repositories import MongoRepository, deserialize_data
from transactions.models import Transaction
from app.logging import logger


class TransactionNotFoundException(NotFoundException):
    """
    Exception raised when a transaction is not found.
    """


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
        try:
            result = super().add(doc)
            logger.debug(f"Successfully added transaction to MongoDB: {doc.id}")
            return result
        except Exception as e:
            logger.error(f"Failed to add transaction to MongoDB: {str(e)}")
            raise

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
        self,
        page: int,
        page_size: int,
        query: dict[str, str | datetime | None] = None,
        sort_field: str | None = None,
        sort_type: str | None = None,
    ) -> list[Transaction]:
        """
        Retrieve a paginated and filtered list of transactions from the repository.

        :param page: The page number for pagination.
        :param page_size: The number of transactions per page.
        :param query: Optional query parameters to filter transactions.
        :param sort_field: Optional. Field to sort by.
        :param sort_type: Optional. Ordering method (asc or desc).
        :return: A paginated and filtered list of Transaction objects based on the specified criteria.
        """
        transactions = self.find(query)
        sort = False if sort_type == "asc" else True
        if sort_field:
            transactions_to_sort = [
                transaction
                for transaction in transactions
                if getattr(transaction, sort_field) is not None
            ]
            transactions_rest = [
                transaction
                for transaction in transactions
                if getattr(transaction, sort_field) is None
            ]
            sorted_transactions = sorted(
                transactions_to_sort, key=attrgetter(sort_field), reverse=sort
            )
            sorted_transactions += transactions_rest
        else:
            sorted_transactions = transactions[::-1]

        paginated = sorted_transactions[
            (page - 1) * page_size : (page - 1) * page_size + page_size
        ]
        return paginated

    def get_filtered(self, query: dict) -> list[Transaction]:
        """Get transactions based on filter query."""
        logger.debug(f"Getting filtered transactions with query: {query}")
        transactions = list(self._collection.find(query))
        logger.debug(f"Found {len(transactions)} transactions")
        
        # Transform transactions to include required frontend fields
        transformed = []
        for t in transactions:
            t = deserialize_data(t)
            try:
                # Extract prompt from request content
                request_content = json.loads(t.get('request_content', '{}'))
                messages = request_content.get('messages', [])
                prompt = messages[-1].get('content', '') if messages else ''
                
                # Extract last message from response content
                response_content = json.loads(t.get('response_content', '{}'))
                last_message = response_content.get('choices', [{}])[0].get('message', {}).get('content', '')
                
                # Add these to the transaction data
                t['prompt'] = prompt
                t['last_message'] = last_message
                
            except (json.JSONDecodeError, IndexError, KeyError) as e:
                logger.error(f"Error extracting messages: {str(e)}")
                t['prompt'] = ''
                t['last_message'] = ''
                
            transformed.append(t)
        
        return [Transaction(**t) for t in transformed]

    def delete_cascade(self, project_id: str):
        """
        Delete multiple transactions and related data for a specific project using cascading deletion.

        :param project_id: The Project ID for which transactions and related data will be deleted.
        :return: The result of the cascading deletion operation.
        """
        return self.delete_many(filter_by={"project_id": project_id})
