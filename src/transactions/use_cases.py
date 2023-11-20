import gzip
import json

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
    transaction = transaction_repository.find_one({"_id": transaction_id})
    return transaction


def store_transaction(
    request, response, buffer, project_id, transaction_repository: TransactionRepository
):
    if response.headers.get("content-encoding") == "gzip":
        response_content = gzip.decompress(buffer[0]).decode()
        response_content = json.loads(response_content)
    else:
        chunks = [chunk.decode() for chunk in buffer]
        response_content = None
        for chunk in chunks:
            chunk_data = chunk.split("data:")
            for part_str in chunk_data:
                try:
                    part = json.loads(part_str)
                    if response_content is None:
                        response_content = part
                        response_content["choices"][0]["message"] = dict(
                            content=part["choices"][0]["delta"]["content"],
                            role=part["choices"][0]["delta"]["role"],
                        )
                    else:
                        if "usage" in part_str:
                            raise NotImplementedError()
                        try:
                            if part["choices"][0]["finish_reason"] == "stop":
                                continue
                            else:
                                response_content["choices"][0]["message"][
                                    "content"
                                ] += part["choices"][0]["delta"]["content"]
                        except KeyError:
                            ...
                except json.JSONDecodeError:
                    pass

    if "usage" not in response_content:
        # TODO: check why we don't get usage data with streaming response
        response_content["usage"] = dict(prompt_tokens=0, completion_tokens=0)

    transaction = Transaction(
        project_id=project_id,
        request=dict(
            url=str(request.url),
            host=request.headers.get("host", ""),
            headers=dict(request.headers),
            content=json.loads(request.content),
        ),
        response=dict(
            headers=dict(response.headers),
            is_error=response.is_error,
            is_success=response.is_success,
            status_code=response.status_code,
            content=response_content,
            elapsed=response.elapsed.total_seconds(),
            encoding=response.encoding,
        ),
    )

    transaction_repository.add(transaction)
