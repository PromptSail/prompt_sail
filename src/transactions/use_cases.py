import json

from transactions.models import QueryParams
from transactions.repositories import Transaction, TransactionRepository


def get_transactions_for_project(
    project_id: str, transaction_repository: TransactionRepository
) -> list[Transaction]:
    transactions = transaction_repository.get_for_project(project_id)
    return transactions


def get_transaction(
    transaction_id: str, transaction_repository: TransactionRepository
) -> Transaction:
    transaction = transaction_repository.get_one_by_id(transaction_id)
    return transaction


def get_all_transactions(
    transaction_repository: TransactionRepository,
) -> list[Transaction]:
    transactions = transaction_repository.get_all()
    return transactions


def store_transaction(
    request,
    response,
    buffer,
    project_id,
    query_params,
    transaction_repository: TransactionRepository,
):
    response_content = "".join(buffer)
    response_content = json.loads(response_content)

    if "usage" not in response_content:
        # TODO: check why we don't get usage data with streaming response
        response_content["usage"] = dict(prompt_tokens=0, completion_tokens=0)

    transaction = Transaction(
        project_id=project_id,
        request=dict(
            method=request.method,
            url=str(request.url),
            host=request.headers.get("host", ""),
            headers=dict(request.headers),
            extensions=dict(request.extensions),
            content=json.loads(request.content),
        ),
        response=dict(
            status_code=response.status_code,
            headers=dict(response.headers),
            next_requset=response.next_request,
            is_error=response.is_error,
            is_success=response.is_success,
            content=response_content,
            elapsed=response.elapsed.total_seconds(),
            encoding=response.encoding,
        ),
        query_params=QueryParams(
            model=query_params["model"] if "model" in query_params.keys() else None,
            experiment=query_params["experiment"]
            if "experiment" in query_params.keys()
            else None,
            tags=query_params["tags"] if "tags" in query_params.keys() else [],
        ),
    )

    transaction_repository.add(transaction)
