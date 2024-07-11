from raw_transactions.models import RawTransaction, TransactionTypeEnum
from seedwork.exceptions import NotFoundException
from seedwork.repositories import MongoRepository


class RawTransactionNotFoundException(NotFoundException):
    """
    Exception raised when a raw transaction is not found.
    """

    ...


class RawTransactionRepository(MongoRepository):
    """
    Repository for managing and accessing raw transaction data.

    Inherits from MongoRepository and is specific to the RawTransaction model.
    """

    model_class = RawTransaction

    def add(self, doc):
        """
        Add a document to the repository.

        :param doc: The document to be added to the repository.
        :return: The result of the add operation.
        """
        result = super().add(doc)
        return result

    def get_for_transaction(self, transaction_id: str) -> list[RawTransaction]:
        """
        Retrieve a list of transactions associated with a specific project.

        :param transaction_id: The identifier of the transaction for which raw transactions are retrieved.
        :return: A list of RawTransaction objects associated with the specified transaction.
        """
        return self.find({"transaction_id": transaction_id})

    def get_request_by_transaction_id(self, transaction_id: str) -> RawTransaction:
        """
        Retrieve a specific transaction by its unique identifier.

        :param transaction_id: The unique identifier of the transaction to retrieve.
        :return: The RawTransaction object (type - request) corresponding to the specified transaction_id.
        """
        return self.find_one(
            {"transaction_id": transaction_id, "type": TransactionTypeEnum.request}
        )

    def get_response_by_transaction_id(self, transaction_id: str) -> RawTransaction:
        """
        Retrieve a specific transaction by its unique identifier.

        :param transaction_id: The unique identifier of the transaction to retrieve.
        :return: The RawTransaction object (type - request) corresponding to the specified transaction_id.
        """
        return self.find_one(
            {"transaction_id": transaction_id, "type": TransactionTypeEnum.response}
        )

    def delete_cascade(self, transaction_id: str):
        """
        Delete multiple raw transactions and related data for a specific project using cascading deletion.

        :param transaction_id: The Project ID for which transactions and related data will be deleted.
        :return: The result of the cascading deletion operation.
        """
        return self.delete_many(filter_by={"transaction_id": transaction_id})
