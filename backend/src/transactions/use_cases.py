import json
import re

import utils
from _datetime import datetime, timezone
from transactions.models import Transaction
from transactions.repositories import TransactionRepository
from transactions.schemas import CreateTransactionSchema
from utils import (
    count_tokens_for_streaming_response,
    create_transaction_query_from_filters,
)


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
    null_generation_speed: bool = True,
    status_codes: list[str] | None = None,
    providers: list[str] | None = None,
    models: list[str] | None = None,
) -> int:
    """
    Count the number of transactions based on specified filters.

    :param transaction_repository: An instance of TransactionRepository used for accessing transaction data.
    :param tags: Optional. List of tags to filter transactions by.
    :param date_from: Optional. Start date for filtering transactions.
    :param date_to: Optional. End date for filtering transactions.
    :param project_id: Optional. Project ID to filter transactions by.
    :param null_generation_speed: Optional. Flag to include transactions with null generation speed.
    :param status_codes: Optional. Status codes to filter transactions by.
    :param providers: Providers to filter transactions by.
    :param models: Models to filter transactions by.
    :return: The count of transactions that meet the specified filtering criteria.
    """
    query = create_transaction_query_from_filters(
        tags,
        date_from,
        date_to,
        project_id,
        null_generation_speed,
        status_codes,
        providers,
        models,
    )
    return transaction_repository.count(query)


def count_transactions_for_list(
    transaction_repository: TransactionRepository,
    tags: str | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    project_id: str | None = None,
    null_generation_speed: bool = True,
    status_codes: list[str] | None = None,
    provider_models: list[dict[str, list[str]]] = None,
) -> int:
    """
    Count the number of transactions based on specified filters.

    :param transaction_repository: An instance of TransactionRepository used for accessing transaction data.
    :param tags: Optional. List of tags to filter transactions by.
    :param date_from: Optional. Start date for filtering transactions.
    :param date_to: Optional. End date for filtering transactions.
    :param project_id: Optional. Project ID to filter transactions by.
    :param null_generation_speed: Optional. Flag to include transactions with null generation speed.
    :param status_codes: Optional. Status codes to filter transactions by.
    :param provider_models: Providers and models to filter transactions by.
    :return: The count of transactions that meet the specified filtering criteria.
    """
    query = utils.create_transaction_list_query_from_filters(
        tags,
        date_from,
        date_to,
        project_id,
        null_generation_speed,
        status_codes,
        provider_models,
    )
    return transaction_repository.count(query)


def get_all_filtered_and_paginated_transactions(
    transaction_repository: TransactionRepository,
    page: int,
    page_size: int,
    tags: list[str] | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    project_id: str | None = None,
    sort_field: str | None = None,
    sort_type: str | None = None,
    status_codes: list[int] | None = None,
    provider_models: list[dict[str, list[str]]] = None,
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
    :param status_codes: The transactions' status codes.
    :param provider_models: The transactions' providers and models.
    :return: A paginated and filtered list of Transaction objects based on the specified criteria.
    """
    query = utils.create_transaction_list_query_from_filters(
        tags, date_from, date_to, project_id, True, status_codes, provider_models
    )

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
    pricelist,
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
    :param pricelist: The pricelist for the models.
    :param transaction_repository: An instance of TransactionRepository used for storing transaction data.
    :return: None
    """
    decoder = response._get_content_decoder()
    buf = b"".join(buffer)

    if "localhost" in str(request.__dict__["url"]) or "host.docker.internal" in str(request.__dict__["url"]):
        content = buf.decode("utf-8").split("\n")
        rest, content = content[-2], content[:-2]
        response_content = {
            pair.split(":")[0]: pair.split(":")[1]
            for pair in rest.split(',"context"')[0][1:].replace('"', "").split(",")
        }
        content = "".join(
            list(
                map(
                    lambda msg: [
                        text
                        for text in [text for text in msg[1:-1].split('response":"')][
                            1
                        ].split('"')
                    ][0],
                    content,
                )
            )
        )
        response_content["response"] = content
    else:
        try:
            response_content = decoder.decode(buf)
            response_content = json.loads(response_content)
        except json.JSONDecodeError:
            content = []
            for i in (
                chunks := buf.decode()
                .replace("data: ", "")
                .split("\n\n")[::-1][3:][::-1]
            ):
                content.append(
                    json.loads(i)["choices"][0]["delta"]["content"].replace("\n", " ")
                )
            content = "".join(content)
            example = json.loads(chunks[0])
            messages = [
                message
                for message in json.loads(request.__dict__["_content"].decode("utf8"))[
                    "messages"
                ]
            ]
            input_tokens = count_tokens_for_streaming_response(
                messages, example["model"]
            )
            output_tokens = count_tokens_for_streaming_response(
                content, example["model"]
            )
            response_content = dict(
                id=example["id"],
                object="chat.completion",
                created=example["created"],
                model=example["model"],
                choices=[
                    dict(
                        index=0,
                        message=dict(role="assistant", content=content),
                        logprobs=None,
                        finish_reason="stop",
                    )
                ],
                system_fingerprint=example["system_fingerprint"],
                usage=dict(
                    prompt_tokens=input_tokens,
                    completion_tokens=output_tokens,
                    total_tokens=input_tokens + output_tokens,
                ),
            )

    if isinstance(response_content, list):
        response_content = response_content[0]

    if "usage" not in response_content:
        response_content["usage"] = dict(
            prompt_tokens=0, completion_tokens=0, total_tokens=0
        )

    param_extractor = utils.TransactionParamExtractor(
        request, response, response_content
    )
    params = param_extractor.extract()

    ai_model_version = (
        ai_model_version if ai_model_version is not None else params["model"]
    )

    pricelist = [
        item
        for item in pricelist
        if item.provider == params["provider"]
        and re.match(item.match_pattern, ai_model_version)
    ]

    if (
        params["status_code"] == 200
        and params["input_tokens"] is not None
        and params["output_tokens"] is not None
    ):
        if len(pricelist) > 0:
            if pricelist[0].mode == "image_generation":
                input_cost = 0
                output_cost = (
                    int(param_extractor.request_content["n"]) * pricelist[0].total_price
                )
                total_cost = output_cost
            else:
                if pricelist[0].input_price == 0:
                    input_cost, output_cost = 0, 0
                    total_cost = (
                        (params["input_tokens"] + params["output_tokens"])
                        / 1000
                        * pricelist[0].total_price
                    )
                else:
                    input_cost = pricelist[0].input_price * (
                        params["input_tokens"] / 1000
                    )
                    output_cost = pricelist[0].output_price * (
                        params["output_tokens"] / 1000
                    )
                    total_cost = input_cost + output_cost
        else:
            input_cost, output_cost, total_cost = None, None, None
    else:
        input_cost, output_cost, total_cost = 0, 0, 0

    if params["output_tokens"] is not None and params["output_tokens"] > 0:
        generation_speed = (
            params["output_tokens"]
            / (datetime.now(tz=timezone.utc) - request_time).total_seconds()
        )
    elif params["output_tokens"] == 0:
        generation_speed = None
    else:
        generation_speed = 0

    try:
        content = json.loads(request.content)
    except UnicodeDecodeError:
        content = param_extractor.request_content

    transaction = Transaction(
        project_id=project_id,
        request=dict(
            method=request.method,
            url=str(request.url),
            host=request.headers.get("host", ""),
            headers=dict(request.headers),
            extensions=dict(request.extensions),
            content=param_extractor.request_content,
        ),
        response=dict(
            status_code=response.status_code,
            headers=dict(response.headers),
            next_requset=response.next_request,
            is_error=response.is_error,
            is_success=response.is_success,
            content=param_extractor.response_content,
            elapsed=response.elapsed.total_seconds(),
            encoding=response.encoding,
        ),
        tags=tags,
        provider=params["provider"],
        model=ai_model_version,
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
        input_cost=input_cost,
        output_cost=output_cost,
        total_cost=total_cost,
        request_time=request_time,
        generation_speed=generation_speed,
    )
    transaction_repository.add(transaction)


def get_list_of_filtered_transactions(
    project_id: str,
    date_from: datetime,
    date_to: datetime,
    transaction_repository: TransactionRepository,
    null_generation_speed: bool = True,
    status_codes: list[str] | None = None,
    providers: list[str] | None = None,
    models: list[str] | None = None,
) -> list[Transaction]:
    """
    Retrieve a list of transactions filtered by project ID and date range.

    This function queries the transaction repository using the specified project ID
    and date range to retrieve a list of transactions that match the given criteria.

    :param project_id: The unique identifier of the project.
    :param date_from: The starting date for the filter.
    :param date_to: The ending date for the filter.
    :param transaction_repository: An instance of TransactionRepository for data retrieval.
    :param null_generation_speed: Optional. Flag to include transactions with null generation speed.
    :param status_codes: The transactions' status codes.
    :param providers: The transactions' providers.
    :param models: The transactions' models.
    :return: A list of Transaction objects that meet the specified criteria.
    """
    query = create_transaction_query_from_filters(
        date_from=date_from,
        date_to=date_to,
        project_id=project_id,
        null_generation_speed=null_generation_speed,
        status_codes=status_codes,
        providers=providers,
        models=models,
    )
    transactions = transaction_repository.get_filtered(query)
    return transactions


def add_transaction(
    data: CreateTransactionSchema, transaction_repository: TransactionRepository
) -> Transaction:
    transaction = Transaction(**data.model_dump())
    transaction_repository.add(transaction)
    return transaction
