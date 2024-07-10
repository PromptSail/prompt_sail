from .models import RawTransaction, TransactionTypeEnum
from .repositories import RawTransactionRepository
import utils
import json

def get_raw_transaction_for_transaction(
    transaction_id: str, raw_transaction_repository: RawTransactionRepository
) -> list[RawTransaction]:
    """
    Retrieve a list of transactions associated with a specific project.

    :param transaction_id: The identifier of the transaction for which raw transactions are retrieved.
    :param raw_transaction_repository: An instance of RawTransactionRepository used for accessing transaction data.
    :return: A list of Transaction objects associated with the specified project.
    """
    raw_transactions = raw_transaction_repository.get_for_transaction(transaction_id)
    return raw_transactions


def get_request_for_transaction(
    transaction_id: str, raw_transaction_repository: RawTransactionRepository
) -> RawTransaction:
    """
    Retrieve a specific raw transaction (type - request) by transaction unique identifier.

    :param transaction_id: The unique identifier of the transaction to retrieve.
    :param raw_transaction_repository: An instance of TransactionRepository used for accessing transaction data.
    :return: The Transaction object corresponding to the specified transaction_id.
    """
    request = raw_transaction_repository.get_request_by_transaction_id(transaction_id)
    return request


def get_response_for_transaction(
    transaction_id: str, raw_transaction_repository: RawTransactionRepository
) -> RawTransaction:
    """
    Retrieve a specific raw transaction (type - response) by transaction unique identifier.

    :param transaction_id: The unique identifier of the transaction to retrieve.
    :param raw_transaction_repository: An instance of TransactionRepository used for accessing transaction data.
    :return: The Transaction object corresponding to the specified transaction_id.
    """
    response = raw_transaction_repository.get_response_by_transaction_id(transaction_id)
    return response


def delete_raw_transactions(
    transaction_id: str, raw_transaction_repository: RawTransactionRepository
) -> None:
    """
     Delete multiple raw transactions (request and response) for a specific transaction.

    :param transaction_id: The Transaction ID for which raw transactions will be deleted.
    :param raw_transaction_repository: An instance of RawTransactionRepository used for accessing transaction data.
    :return: None
    """
    raw_transaction_repository.delete_cascade(transaction_id=transaction_id)
    

def store_raw_transactions(
    request, request_content, response, response_content, 
    transaction_id: str, 
    raw_transaction_repository: RawTransactionRepository
):
    request_data = RawTransaction(
        transaction_id=transaction_id,
        type=TransactionTypeEnum.request,
        data=dict(
            method=request.method,
            url=str(request.url),
            host=request.headers.get("host", ""),
            headers=dict(request.headers),
            extensions=dict(request.extensions),
            content=request_content,
        )
    )
    response_data = RawTransaction(
        transaction_id=transaction_id,
        type=TransactionTypeEnum.response,
        data=dict(
            status_code=response.status_code,
            headers=dict(response.headers),
            next_requset=response.next_request,
            is_error=response.is_error,
            is_success=response.is_success,
            content=response_content,
            elapsed=response.elapsed.total_seconds(),
            encoding=response.encoding,
        )
    )
    raw_transaction_repository.add(request_data)
    raw_transaction_repository.add(response_data)
    