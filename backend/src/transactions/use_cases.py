import json

from _datetime import datetime, timezone
from transactions.models import Transaction
from transactions.repositories import TransactionRepository
from utils import create_transaction_query_from_filters, req_resp_to_transaction_parser


def get_transactions_for_project(
    project_id: str, transaction_repository: TransactionRepository
) -> list[Transaction]:
    """
    Retrieve a list of transactions associated with a specific project.

    :param project_id: The identifier of the project for which transactions are retrieved.
    :param transaction_repository: An instance of TransactionRepository used for accessing transaction data.
    :return: A list of Transaction objects associated with the specified project.
    """
    transactions = transaction_repository.get_for_project(project_id)
    return transactions


def get_transaction(
    transaction_id: str, transaction_repository: TransactionRepository
) -> Transaction:
    """
    Retrieve a specific transaction by its unique identifier.

    :param transaction_id: The unique identifier of the transaction to retrieve.
    :param transaction_repository: An instance of TransactionRepository used for accessing transaction data.
    :return: The Transaction object corresponding to the specified transaction_id.
    """
    transaction = transaction_repository.get_one_by_id(transaction_id)
    return transaction


def get_all_transactions(
    transaction_repository: TransactionRepository,
) -> list[Transaction]:
    """
    Retrieve all transactions from the repository.

    :param transaction_repository: An instance of TransactionRepository used for accessing transaction data.
    :return: A list of all Transaction objects stored in the repository.
    """
    transactions = transaction_repository.get_all()
    return transactions


def count_transactions(
    transaction_repository: TransactionRepository,
    tags: str | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    project_id: str | None = None,
    status_code: int | None = None,
) -> int:
    """
    Count the number of transactions based on specified filters.

    :param transaction_repository: An instance of TransactionRepository used for accessing transaction data.
    :param tags: Optional. List of tags to filter transactions by.
    :param date_from: Optional. Start date for filtering transactions.
    :param date_to: Optional. End date for filtering transactions.
    :param project_id: Optional. Project ID to filter transactions by.
    :param status_code: Optional. Status code to filter transactions by.
    :return: The count of transactions that meet the specified filtering criteria.
    """
    query = create_transaction_query_from_filters(
        tags, date_from, date_to, project_id, status_code
    )
    return transaction_repository.count(query)


def count_token_usage_for_project(
    transaction_repository: TransactionRepository,
    project_id: str | None = None,
) -> int:
    """
    Count the total token usage for transactions associated with a specific project.

    :param transaction_repository: An instance of TransactionRepository used for accessing transaction data.
    :param project_id: Optional. Project ID to filter transactions by.
    :return: The sum of token usage across all transactions for the specified project.
    """
    transactions = transaction_repository.get_for_project(project_id)
    return sum(
        [
            transaction.token_usage
            for transaction in transactions
            if transaction.token_usage is not None
        ]
    )


def get_all_filtered_and_paginated_transactions(
    transaction_repository: TransactionRepository,
    page: int,
    page_size: int,
    tags: str | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    project_id: str | None = None,
    sort_field: str | None = None,
    sort_type: str | None = None,
) -> list[Transaction]:
    """
    Retrieve a paginated and filtered list of transactions based on specified criteria.

    :param transaction_repository: An instance of TransactionRepository used for accessing transaction data.
    :param page: The page number for pagination.
    :param page_size: The number of transactions per page.
    :param tags: Optional. List of tags to filter transactions by.
    :param date_from: Optional. Start date for filtering transactions.
    :param date_to: Optional. End date for filtering transactions.
    :param project_id: Optional. Project ID to filter transactions by.
    :param sort_field: Optional. Field to sort by.
    :param sort_type: Optional. Ordering method (asc or desc).
    :return: A paginated and filtered list of Transaction objects based on the specified criteria.
    """
    query = create_transaction_query_from_filters(tags, date_from, date_to, project_id)
    transactions = transaction_repository.get_paginated_and_filtered(
        page, page_size, query, sort_field, sort_type
    )
    return transactions


def delete_multiple_transactions(
    transaction_repository: TransactionRepository, project_id: str
) -> None:
    """
     Delete multiple transactions and related data for a specific project.

    :param transaction_repository: An instance of TransactionRepository used for accessing transaction data.
    :param project_id: The Project ID for which transactions and related data will be deleted.
    :return: None
    """
    transaction_repository.delete_cascade(project_id=project_id)


def store_transaction(
    request,
    response,
    buffer,
    project_id,
    tags,
    ai_model_version,
    request_time,
    transaction_repository: TransactionRepository,
):
    """
    Store a transaction in the repository based on request, response, and additional information.

    :param request: The request object.
    :param response: The response object.
    :param buffer: The buffer containing the response content.
    :param project_id: The Project ID associated with the transaction.
    :param tags: The tags associated with the transaction.
    :param request_time: The timestamp of the request.
    :param ai_model_version: Optional. Specific tag for AI model. Helps with cost count.
    :param transaction_repository: An instance of TransactionRepository used for storing transaction data.
    :return: None
    """
    decoder = response._get_content_decoder()
    buf = b"".join(buffer)
    
    try:
        response_content = decoder.decode(buf)
        response_content = json.loads(response_content)
    except json.JSONDecodeError:
        content = []
        chunks = buf.decode().replace('data: ', '').split("\n\n")[::-1][3:][::-1]
        for i in chunks:
            content.append(json.loads(i)['choices'][0]['delta']['content'].replace('\n', ' '))
        content = "".join(content)
        example = json.loads(chunks[0])
        response_content = dict(
            id=example["id"], 
            object="chat.completion", 
            created=example["created"], 
            model=example["model"],
            choices=[
                dict(
                    index=0,
                    message=dict(role="assistant",content=content),
                    logprobs=None,
                    finish_reason="stop",
                )
            ],
            system_fingerprint=example["system_fingerprint"],
        )
    
    params = req_resp_to_transaction_parser(request, response, response_content)

    if "usage" not in response_content:
        # TODO: check why we don't get usage data with streaming response
        response_content["usage"] = dict(prompt_tokens=0, completion_tokens=0, total_tokens=0)

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
        provider=params["provider"],
        model=ai_model_version if ai_model_version is not None else params["model"],
        prompt=params["prompt"],
        type=params["type"],
        os=params["os"],
        input_tokens=params["input_tokens"],
        output_tokens=params["output_tokens"],
        library=params["library"],
        status_code=params["status_code"],
        messages=params["messages"],
        last_message=params["last_message"],
        error_message=params["error_message"],
        request_time=request_time,
        generation_speed=params["output_tokens"]
        / (datetime.now(tz=timezone.utc) - request_time).total_seconds()
        if (params["output_tokens"] is not None and params["output_tokens"] > 0)
        else 0,
    )

    transaction_repository.add(transaction)


def get_list_of_filtered_transactions(
    project_id: str,
    date_from: datetime,
    date_to: datetime,
    transaction_repository: TransactionRepository,
    status_code: int | None = None,
) -> list[Transaction]:
    """
    Retrieve a list of transactions filtered by project ID and date range.

    This function queries the transaction repository using the specified project ID
    and date range to retrieve a list of transactions that match the given criteria.

    :param project_id: The unique identifier of the project.
    :param date_from: The starting date for the filter.
    :param date_to: The ending date for the filter.
    :param transaction_repository: An instance of TransactionRepository for data retrieval.
    :param status_code: The transactions' status code.
    :return: A list of Transaction objects that meet the specified criteria.
    """
    query = create_transaction_query_from_filters(
        date_from=date_from,
        date_to=date_to,
        project_id=project_id,
        status_code=status_code,
    )
    transactions = transaction_repository.get_filtered(query)
    return transactions
