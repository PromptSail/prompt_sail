import gzip
import json

# from transactions.models import Tags
from transactions.repositories import Transaction, TransactionRepository


def get_transactions_for_project(
    project_id: str, 
    transaction_repository: TransactionRepository
) -> list[Transaction]:
    transactions = transaction_repository.get_for_project(project_id)
    return transactions


def get_transaction(
    transaction_id: str, 
    transaction_repository: TransactionRepository
) -> Transaction:
    transaction = transaction_repository.get_one_by_id(transaction_id)
    return transaction


def get_all_transactions(
    transaction_repository: TransactionRepository
) -> list[Transaction]:
    transactions = transaction_repository.get_all()
    return transactions


def store_transaction(
    request, 
    response, 
    buffer,
    project_id, 
    # tags,
    transaction_repository: TransactionRepository
):
    if response.headers.get("content-encoding") == "gzip":
        response_content = gzip.decompress(buffer[0]).decode()
        response_content = json.loads(response_content)
    else:
        chunks = [chunk.decode() for chunk in buffer]
        response_content = [json.loads(chunk.split("data:")) for chunk in chunks if len(chunk) > 0]

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
        # tags=Tags(
        #     model=tags.model,
        #     experiment=tags.experiment,
        #     tags=tags.tags
        # )
    )

    transaction_repository.add(transaction)
