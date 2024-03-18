import re
from typing import Annotated, Any

import utils
from _datetime import datetime, timezone, timedelta
from app.dependencies import get_provider_pricelist, get_transaction_context
from fastapi import Depends, Request
from fastapi.responses import JSONResponse
from lato import TransactionContext
from projects.models import AIProvider, Project
from projects.schemas import (
    CreateProjectSchema,
    GetAIProviderPriceSchema,
    GetAIProviderSchema,
    GetProjectSchema,
    UpdateProjectSchema,
)
from projects.use_cases import (
    add_project,
    delete_project,
    get_all_projects,
    get_project,
    update_project,
)
from settings.schemas import AuthorizeUserSchema
from settings.use_cases import get_organization_name, get_users_for_organization
from slugify import slugify
from transactions.models import generate_uuid
from transactions.schemas import (
    GetTransactionLatencyStatisticsSchema,
    GetTransactionPageResponseSchema,
    GetTransactionStatusStatisticsSchema,
    GetTransactionUsageStatisticsSchema,
    GetTransactionWithProjectSlugSchema,
    StatisticTransactionSchema,
)
from transactions.use_cases import (
    count_token_usage_for_project,
    count_transactions,
    delete_multiple_transactions,
    get_all_filtered_and_paginated_transactions,
    get_list_of_filtered_transactions,
    get_transaction,
)

from .app import app


@app.get("/api/projects")
async def get_projects(
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)]
) -> list[GetProjectSchema]:
    """
    API endpoint to retrieve information about all projects.

    :param ctx: The transaction context dependency.
    :return: A list of GetProjectSchema objects.
    """
    projects = ctx.call(get_all_projects)
    projects = [
        GetProjectSchema(
            **project.model_dump(),
            total_transactions=ctx.call(count_transactions, project_id=project.id),
        )
        for project in projects
    ]
    return projects


@app.get("/api/projects/{project_id}", response_class=JSONResponse, status_code=200)
async def get_project_details(
    project_id: str,
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
) -> GetProjectSchema:
    """
    API endpoint to retrieve details about a specific project.

    :param project_id: The identifier of the project.
    :param ctx: The transaction context dependency.
    :return: A GetProjectSchema object representing the project details.
    """
    project = ctx.call(get_project, project_id=project_id)
    transaction_count = ctx.call(count_transactions, project_id=project_id)
    project = GetProjectSchema(
        **project.model_dump(),
        total_transactions=transaction_count,
    )
    return project


@app.post("/api/projects", response_class=JSONResponse, status_code=201)
async def create_project(
    data: CreateProjectSchema,
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
) -> GetProjectSchema:
    """
    API endpoint to create a new project.

    :param data: The data for creating the project as a CreateProjectSchema object.
    :param ctx: The transaction context dependency.
    :return: A GetProjectSchema object representing the created project.
    """
    project_id = generate_uuid()
    project = Project(
        id=project_id,
        **data.model_dump(),
    )
    project.slug = slugify(data.slug)
    for idx in range(len(project.ai_providers)):
        project.ai_providers[idx].slug = slugify(project.ai_providers[idx].slug)

    ctx.call(add_project, project)
    project = ctx.call(get_project, project_id)
    response = GetProjectSchema(**project.model_dump())
    return response


@app.put("/api/projects/{project_id}", response_class=JSONResponse, status_code=200)
async def update_existing_project(
    project_id: str,
    data: UpdateProjectSchema,
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
) -> GetProjectSchema:
    """
    API endpoint to update an existing project.

    :param project_id: The identifier of the project to be updated.
    :param data: The data for updating the project as an UpdateProjectSchema object.
    :param ctx: The transaction context dependency.
    :return: A GetProjectSchema object representing the updated project.
    """
    data = dict(**data.model_dump(exclude_none=True))
    if "slug" in data:
        data["slug"] = slugify(data["slug"])
    if "ai_providers" in data:
        for idx in range(len(data["ai_providers"])):
            data["ai_providers"][idx] = AIProvider(**data["ai_providers"][idx])
            data["ai_providers"][idx].slug = slugify(data["ai_providers"][idx].slug)
    updated = ctx.call(update_project, project_id=project_id, fields_to_update=data)
    total_tokens_usage = ctx.call(count_token_usage_for_project, project_id=project_id)
    return GetProjectSchema(
        **updated.model_dump(), total_tokens_usage=total_tokens_usage
    )


@app.delete("/api/projects/{project_id}", response_class=JSONResponse, status_code=204)
async def delete_existing_project(
    project_id: str,
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
):
    """
    API endpoint to delete an existing project and its associated transactions.

    :param project_id: The identifier of the project to be deleted.
    :param ctx: The transaction context dependency.
    """
    ctx.call(delete_project, project_id=project_id)
    ctx.call(delete_multiple_transactions, project_id=project_id)


@app.get(
    "/api/transactions/{transaction_id}", response_class=JSONResponse, status_code=200
)
async def get_transaction_details(
    request: Request,
    transaction_id: str,
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
) -> GetTransactionWithProjectSlugSchema:
    """
    API endpoint to retrieve details of a specific transaction.

    :param request: The incoming request.
    :param transaction_id: The identifier of the transaction.
    :param ctx: The transaction context dependency.
    """
    price_list = get_provider_pricelist(request)
    transaction = ctx.call(get_transaction, transaction_id=transaction_id)
    price = [price for price in price_list if re.match(price.match_pattern, transaction.model)]
    if len(price) > 0:
        price = price[0]
        if price.total_price > 0:
            input_cost, output_cost = 0, 0
            total_cost = ((transaction.input_tokens / 1000) + (transaction.output_tokens / 1000)) * price.total_price if transaction.input_tokens > 0 and transaction.output_tokens > 0 else 0
        else:
            input_cost = (transaction.input_tokens / 1000) * price.input_price if transaction.input_tokens > 0 and price.input_price > 0 else 0
            output_cost = (transaction.output_tokens / 1000) * price.output_price if transaction.output_tokens > 0 and price.output_price > 0 else 0
            total_cost = input_cost + output_cost
    else:
        input_cost, output_cost, total_cost = 0, 0, 0
    project = ctx.call(get_project, project_id=transaction.project_id)
    transaction = GetTransactionWithProjectSlugSchema(**transaction.model_dump(), project_name=project.name, input_cost=input_cost, output_cost=output_cost, total_cost=total_cost)
    return transaction


@app.get("/api/transactions", response_class=JSONResponse, status_code=200)
async def get_paginated_transactions(
    request: Request,
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
    page: int = 1,
    page_size: int = 20,
    tags: str | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    project_id: str | None = None,
) -> GetTransactionPageResponseSchema:
    """
    API endpoint to retrieve a paginated list of transactions based on specified filters.

    :param request: The incoming request.
    :param ctx: The transaction context dependency.
    :param page: The page number for pagination.
    :param page_size: The number of transactions per page.
    :param tags: Optional. List of tags to filter transactions by.
    :param date_from: Optional. Start date for filtering transactions.
    :param date_to: Optional. End date for filtering transactions.
    :param project_id: Optional. Project ID to filter transactions by.
    """
    if tags is not None:
        tags = tags.split(",")

    transactions = ctx.call(
        get_all_filtered_and_paginated_transactions,
        page=page,
        page_size=page_size,
        tags=tags,
        date_from=date_from,
        date_to=date_to,
        project_id=project_id,
    )
    
    price_list = get_provider_pricelist(request)
    projects = ctx.call(get_all_projects)
    project_id_name_map = {project.id: project.name for project in projects}
    new_transactions = []
    for transaction in transactions:
        price = [price for price in price_list if re.match(price.match_pattern, transaction.model)]
        if len(price) > 0:
            price = price[0]
            if price.total_price > 0:
                input_cost, output_cost = 0, 0
                total_cost = ((transaction.input_tokens / 1000) + (transaction.output_tokens / 1000)) * price.total_price if transaction.input_tokens > 0 and transaction.output_tokens > 0 else 0
            else:
                input_cost = (transaction.input_tokens / 1000) * price.input_price if transaction.input_tokens > 0 and price.input_price > 0 else 0
                output_cost = (transaction.output_tokens / 1000) * price.output_price if transaction.output_tokens > 0 and price.output_price > 0 else 0
                total_cost = input_cost + output_cost
        else:
            input_cost, output_cost, total_cost = 0, 0, 0
        new_transactions.append(
            GetTransactionWithProjectSlugSchema(
                **transaction.model_dump(),
                project_name=project_id_name_map.get(transaction.project_id, None),
                input_cost=input_cost,
                output_cost=output_cost,
                total_cost=total_cost
            )
        )
    
    # transactions = [
    #     GetTransactionWithProjectSlugSchema(
    #         **transaction.model_dump(),
    #         project_name=project_id_name_map.get(transaction.project_id, None),
    #     )
    #     for transaction in transactions
    # ]
    count = ctx.call(
        count_transactions,
        tags=tags,
        date_from=date_from,
        date_to=date_to,
        project_id=project_id,
    )
    page_response = GetTransactionPageResponseSchema(
        items=new_transactions,
        page_index=page,
        page_size=page_size,
        total_elements=count,
        total_pages=-(-count // page_size),
    )
    return page_response


@app.get("/api/statistics/transactions_cost", response_class=JSONResponse)
async def get_transaction_usage_statistics_over_time(
    request: Request,
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
    project_id: str,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    period: str | None = "daily",
) -> list[GetTransactionUsageStatisticsSchema] | dict[str, str]:
    """
    Retrieve transaction usage statistics over a specified time period.\n

    This endpoint fetches transaction data based on the specified project ID,
    date range, and period. It then processes the data to generate usage statistics
    including total input tokens, total output tokens, cumulative input tokens, cumulative output tokens as well as
    total cost calculated based on cumulative values for the best possible representation of costs over time.\n

    :param request: The FastAPI Request object (automatically applied).\n
    :param ctx: The transaction context, providing access to dependencies (automatically applied).\n
    :param project_id: The unique identifier of the project.\n
    :param date_from: Starting point of the time interval (optional - when empty, then the scope is counted from the
        beginning of the project's existence).\n
    :param date_to: End point of the time interval (optional - when empty, then the interval is counted up to the
        present time).\n
    :param period: The time period for grouping statistics - can be yearly, monthly, weekly, daily, hourly or minutely.
        (default is "daily").\n
    :return: A list of GetTransactionUsageStatisticsSchema (provider, model, date, total_input_tokens,
        total_output_tokens, input_cumulative_total, output_cumulative_total, total_transactions, total_cost)
        representing the usage statistics.\n
    """

    try:
        if date_from is not None and date_to is not None and date_from == date_to:
            date_to = date_to + timedelta(days=1) - timedelta(seconds=1)
        
        transactions = ctx.call(
            get_list_of_filtered_transactions,
            project_id=project_id,
            date_from=date_from,
            date_to=date_to,
        )        
        transactions = [
            StatisticTransactionSchema(
                project_id=project_id,
                provider=transaction.provider,
                model=transaction.model,
                total_input_tokens=transaction.input_tokens or 0,
                total_output_tokens=transaction.output_tokens or 0,
                status_code=transaction.status_code,
                date=transaction.response_time,
                latency=(
                    transaction.response_time - transaction.request_time
                ).total_seconds(),
                generation_speed=transaction.generation_speed,
                total_transactions=1,
            )
            for transaction in transactions
        ]
        stats = utils.token_counter_for_transactions(transactions, period)
        pricelist = get_provider_pricelist(request)

        for stat in stats:
            possible_prices = [
                price
                for price in pricelist
                if re.match(price.match_pattern, stat.model)
            ]
            if len(possible_prices) > 0:
                # TODO: Counting by date instead of by lastest
                lastest = max(
                    possible_prices,
                    key=lambda x: x.start_date if x.start_date else datetime.min,
                )
                if lastest.input_price > 0 and lastest.output_price > 0:
                    stat.total_cost += (
                        (stat.input_cumulative_total / 1000)
                        * lastest.input_price
                    )
                    stat.total_cost += (
                        (stat.output_cumulative_total / 1000)
                        * lastest.output_price
                    )
                else:
                    stat.total_cost = (
                        (stat.input_cumulative_total + stat.output_cumulative_total)
                        / 1000
                    ) * lastest.total_price

        return stats
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/statistics/transactions_count", response_class=JSONResponse)
async def get_transaction_status_statistics_over_time(
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
    project_id: str,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    period: str | None = "daily",
) -> list[GetTransactionStatusStatisticsSchema] | dict[str, str]:
    """
    Retrieve transaction status statistics over a specified time period.\n

    This endpoint fetches transaction data based on the specified project ID,
    date range, and period. It then processes the data to generate status statistics
    including total transactions and the distribution of status codes over time.\n

    :param ctx: The transaction context, providing access to dependencies (automatically applied).\n
    :param project_id: The unique identifier of the project.\n
    :param date_from: Starting point of the time interval (optional - when empty, then the scope is counted from the
        beginning of the project's existence).\n
    :param date_to: End point of the time interval (optional - when empty, then the interval is counted up to the
        present time).\n
    :param period: The time period for grouping statistics - can be yearly, monthly, weekly, daily, hourly or minutely.
        (default is "daily").\n
    :return: A list of GetTransactionStatusStatisticsSchema (date, status_code, total_transactions) representing the
        status statistics.\n
    """
    try:
        if date_from is not None and date_to is not None and date_from == date_to:
            date_to = date_to + timedelta(days=1) - timedelta(seconds=1)
            
        transactions = ctx.call(
            get_list_of_filtered_transactions,
            project_id=project_id,
            date_from=date_from,
            date_to=date_to,
        )
        transactions = [
            StatisticTransactionSchema(
                project_id=project_id,
                provider=transaction.provider,
                model=transaction.model,
                total_input_tokens=transaction.input_tokens or 0,
                total_output_tokens=transaction.output_tokens or 0,
                status_code=transaction.status_code,
                date=transaction.response_time,
                latency=(
                    transaction.response_time - transaction.request_time
                ).total_seconds(),
                generation_speed=transaction.generation_speed,
                total_transactions=1,
            )
            for transaction in transactions
        ]
        stats = utils.status_counter_for_transactions(transactions, period)

        return stats
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/statistics/transactions_speed", response_class=JSONResponse)
async def get_transaction_latency_statistics_over_time(
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
    project_id: str,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    period: str | None = "daily",
) -> list[GetTransactionLatencyStatisticsSchema] | dict[str, str]:
    """
    Retrieve transaction generation speed and latency statistics over a specified time period.\n

    This endpoint fetches transaction data based on the specified project ID,
    date range, and period. It then processes the data to generate values of latency and generation speed.\n

    :param ctx: The transaction context, providing access to dependencies (automatically applied).\n
    :param project_id: The unique identifier of the project.\n
    :param date_from: Starting point of the time interval (optional - when empty, then the scope is counted from the
        beginning of the project's existence).\n
    :param date_to: End point of the time interval (optional - when empty, then the interval is counted up to the
        present time).\n
    :param period: The time period for grouping statistics - can be yearly, monthly, weekly, daily, hourly or minutely.
        (default is "daily").\n
    :return: A list of GetTransactionLatencyStatisticsSchema (provider, model, date, mean_latency, tokens_per_second,
        total_transactions) representing the generation speed and latency statistics.\n
    """
    try:
        if date_from is not None and date_to is not None and date_from == date_to:
            date_to = date_to + timedelta(days=1) - timedelta(seconds=1)
            
        transactions = ctx.call(
            get_list_of_filtered_transactions,
            project_id=project_id,
            date_from=date_from,
            date_to=date_to,
        )
        transactions = [
            StatisticTransactionSchema(
                project_id=project_id,
                provider=transaction.provider,
                model=transaction.model,
                total_input_tokens=transaction.input_tokens or 0,
                total_output_tokens=transaction.output_tokens or 0,
                status_code=transaction.status_code,
                date=transaction.response_time,
                latency=(
                    transaction.response_time - transaction.request_time
                ).total_seconds(),
                generation_speed=transaction.generation_speed,
                total_transactions=1,
            )
            for transaction in transactions
        ]
        stats = utils.latency_counter_for_transactions(transactions, period)

        return stats
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/statistics/pricelist", response_class=JSONResponse)
async def fetch_provider_pricelist(request: Request) -> list[GetAIProviderPriceSchema]:
    """
    API endpoint to retrieve a price list of AI providers.

    :param request: The incoming request.
    """
    price_list = get_provider_pricelist(request)
    return [GetAIProviderPriceSchema(**price.__dict__) for price in price_list]


@app.get("/api/providers", response_class=JSONResponse)
async def get_providers(request: Request) -> list[GetAIProviderSchema]:
    """
    API endpoint to retrieve a list of AI providers.

    :param request: The incoming request.
    """
    return [GetAIProviderSchema(**provider) for provider in utils.known_ai_providers]


@app.get("/api/organization", response_class=JSONResponse)
async def get_organization(
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)]
) -> str:
    """
    API endpoint to retrieve the organization name.

    :param ctx: The transaction context dependency.
    """
    organization_name = ctx.call(get_organization_name)
    return str(organization_name)


@app.post("/api/authorize", response_class=JSONResponse)
async def authorize_user(
    data: AuthorizeUserSchema,
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
) -> dict[str, Any]:
    """
    API endpoint to authorize a user.

    :param data: The data containing user information.
    :param ctx: The transaction context dependency.
    :return: A dictionary containing the authorization status and message.
    """
    if AuthorizeUserSchema(**data.model_dump()) in [
        AuthorizeUserSchema(**data.model_dump())
        for data in ctx.call(get_users_for_organization)
    ]:
        return {"status": 200, "message": "OK"}
    return {"status": 404, "message": "Not Found"}


@app.post("/api/only_for_purpose/mock_transactions", response_class=JSONResponse)
async def mock_transactions(
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
    count: int,
    days_back: int = 30,
) -> dict[str, Any]:
    """
    API endpoint to mock transactions.

    :param count: How many transactions you want to mock.
    :param days_back: How many days back from now transactions should be added. 
    :param ctx: The transaction context dependency.
    :return: A dictionary containing the status and message (code and latency).
    """
    try:
        time_start = datetime.now(tz=timezone.utc)
        repo = ctx['transaction_repository']
        mocked_transactions = utils.generate_mock_transactions(count, days_back)
        for transaction in mocked_transactions:
            repo.add(transaction)
        time_stop = datetime.now(tz=timezone.utc)
        
        return {"status_code": 200, "message": f"{count} transactions added in {(time_stop-time_start).total_seconds()} seconds."}
        
    except Exception as e:
        return {"status_code": 500, "message": str(e)}
    
    
    