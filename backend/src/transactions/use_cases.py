from datetime import datetime
import json

from transactions.models import Transaction
from transactions.repositories import TransactionRepository


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


def count_transactions(
    transaction_repository: TransactionRepository
) -> int:
    return transaction_repository.count()


def get_all_filtered_and_paginated_transactions(
    transaction_repository: TransactionRepository,
    page: int,
    page_size: int,
    tags: str | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    project_id: str | None = None
) -> list[Transaction]:
    query = {}
    if project_id is not None:
        query["project_id"] = project_id
    if tags is not None:
        query["tags"] = {"$all": tags}
    if date_from is not None and date_to is None:
        query["timestamp"] = {"$gt": date_from}
    elif date_to is not None and date_from is None:
        query["timestamp"] = {"$lt": date_to}
    elif date_from is not None and date_to is None:
        query["timestamp"] = {"$gte": date_from, "$lte": date_to}

    transactions = transaction_repository.get_paginated_and_filtered(
        page, 
        page_size, 
        query
    )
    return transactions


def store_transaction(
    request,
    response,
    buffer,
    project_id,
    tags,
    transaction_repository: TransactionRepository,
):
    decoder = response._get_content_decoder()
    buf = b"".join(buffer)
    response_content = decoder.decode(buf)

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
        tags=tags,
    )

    transaction_repository.add(transaction)
