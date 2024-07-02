import re
from typing import Annotated, Any

import utils
from _datetime import datetime, timezone
from app.dependencies import get_provider_pricelist, get_transaction_context
from auth.authorization import decode_and_validate_token
from auth.models import User
from auth.schemas import GetPartialUserSchema, GetUserSchema
from auth.use_cases import get_all_users
from fastapi import Depends, HTTPException, Request, Security
from fastapi.responses import JSONResponse
from lato import TransactionContext
from projects.models import AIProvider, Project
from projects.schemas import (
    CreateProjectSchema,
    GetAIProviderPriceSchema,
    GetAIProviderSchema,
    GetPortfolioDetailsSchema,
    GetProjectPortfolioSchema,
    GetProjectSchema,
    UpdateProjectSchema,
)
from projects.use_cases import (
    add_project,
    count_projects,
    delete_project,
    get_all_projects,
    get_project,
    update_project,
)
from seedwork.repositories import DocumentNotFoundException
from settings.use_cases import get_organization_name
from slugify import slugify
from transactions.models import generate_uuid
from transactions.schemas import (
    CreateTransactionSchema,
    GetTransactionLatencyStatisticsWithoutDateSchema,
    GetTransactionPageResponseSchema,
    GetTransactionSchema,
    GetTransactionsLatencyStatisticsSchema,
    GetTransactionStatusStatisticsSchema,
    GetTransactionsUsageStatisticsSchema,
    GetTransactionUsageStatisticsWithoutDateSchema,
    GetTransactionWithProjectSlugSchema,
    StatisticTransactionSchema,
)
from transactions.use_cases import (
    add_transaction,
    count_token_usage_for_project,
    count_transactions,
    count_transactions_for_list,
    delete_multiple_transactions,
    get_all_filtered_and_paginated_transactions,
    get_list_of_filtered_transactions,
    get_transaction,
    get_transactions_for_project,
)

from .app import app


@app.get("/api/auth/whoami", dependencies=[Security(decode_and_validate_token)])
def whoami(
    request: Request, user: User = Depends(decode_and_validate_token)
) -> GetUserSchema:
    return GetUserSchema(
        external_id=user.external_id,
        organization=user.organization,
        email=user.email,
        given_name=user.given_name,
        family_name=user.family_name,
        picture=user.picture,
        issuer=user.issuer,
    )


@app.get("/api/projects", dependencies=[Security(decode_and_validate_token)])
async def get_projects(
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
) -> list[GetProjectSchema]:
    """
    API endpoint to retrieve information about all projects.

    :param ctx: The transaction context dependency.
    :return: A list of GetProjectSchema objects.
    """
    projects = ctx.call(get_all_projects)

    dtos = []
    for project in projects:
        transaction_count = ctx.call(count_transactions, project_id=project.id)
        cost = 0
        if transaction_count > 0:
            transactions = ctx.call(get_transactions_for_project, project_id=project.id)
            for transaction in transactions:
                if transaction.status_code == 200:
                    cost += transaction.total_cost if transaction.total_cost else 0
        dtos.append(
            GetProjectSchema(
                **project.model_dump(),
                total_transactions=transaction_count,
                total_cost=cost,
            )
        )

    return dtos


@app.get(
    "/api/projects/{project_id}",
    response_class=JSONResponse,
    status_code=200,
    dependencies=[Security(decode_and_validate_token)],
)
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
    try:
        project = ctx.call(get_project, project_id=project_id)
    except DocumentNotFoundException:
        raise HTTPException(status_code=404, detail="Project not found")

    transactions = ctx.call(get_transactions_for_project, project_id=project_id)
    cost = 0
    transaction_count = ctx.call(count_transactions, project_id=project_id)
    if transaction_count > 0:
        for transaction in transactions:
            cost += transaction.total_cost if transaction.total_cost else 0

    project = GetProjectSchema(
        **project.model_dump(), total_transactions=transaction_count, total_cost=cost
    )
    return project


@app.post(
    "/api/projects",
    response_class=JSONResponse,
    status_code=201,
    dependencies=[Security(decode_and_validate_token)],
)
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


@app.put(
    "/api/projects/{project_id}",
    response_class=JSONResponse,
    status_code=200,
    dependencies=[Security(decode_and_validate_token)],
)
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


@app.delete(
    "/api/projects/{project_id}",
    response_class=JSONResponse,
    status_code=204,
    dependencies=[Security(decode_and_validate_token)],
)
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
    "/api/transactions/{transaction_id}",
    response_class=JSONResponse,
    status_code=200,
    dependencies=[Security(decode_and_validate_token)],
)
async def get_transaction_details(
    transaction_id: str,
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
) -> GetTransactionWithProjectSlugSchema:
    """
    API endpoint to retrieve details of a specific transaction.

    :param transaction_id: The identifier of the transaction.
    :param ctx: The transaction context dependency.
    """
    try:
        transaction = ctx.call(get_transaction, transaction_id=transaction_id)
    except DocumentNotFoundException:
        raise HTTPException(status_code=404, detail="Transaction not found")
    project = ctx.call(get_project, project_id=transaction.project_id)
    transaction = GetTransactionWithProjectSlugSchema(
        **transaction.model_dump(),
        project_name=project.name if project else "",
        total_tokens=transaction.input_tokens + transaction.output_tokens
        if transaction.input_tokens and transaction.output_tokens
        else None,
    )
    return transaction


@app.get(
    "/api/transactions",
    response_class=JSONResponse,
    status_code=200,
    dependencies=[Security(decode_and_validate_token)],
)
async def get_paginated_transactions(
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
    page: int = 1,
    page_size: int = 20,
    tags: str | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    project_id: str | None = None,
    sort_field: str | None = None,
    sort_type: str | None = None,
    status_codes: str | None = None,
    provider_models: str | None = None,
) -> GetTransactionPageResponseSchema:
    """
    API endpoint to retrieve a paginated list of transactions based on specified filters.

    :param ctx: The transaction context dependency.
    :param page: The page number for pagination.
    :param page_size: The number of transactions per page.
    :param tags: Optional. List of tags to filter transactions by.
    :param date_from: Optional. Start date for filtering transactions.
    :param date_to: Optional. End date for filtering transactions.
    :param project_id: Optional. Project ID to filter transactions by.
    :param sort_field: Optional. Field to sort by.
    :param sort_type: Optional. Ordering method (asc or desc).
    :param status_codes: Optional. List of status codes for filtering transactions.
    :param provider_models: Optional. List of providers and models for filtering transactions.
    """
    if tags is not None:
        tags = tags.split(",")
    if status_codes is not None:
        status_codes = list(map(lambda x: int(x), status_codes.split(",")))
    if provider_models is not None:
        if provider_models is not None:
            provider_models = list(
                map(lambda x: x.split("."), provider_models.split(","))
            )
            pairs = {}
            for pair in provider_models:
                if pair[0] not in pairs:
                    try:
                        pairs[pair[0]] = [".".join(pair[1:])] if ".".join(pair[1:]) is not "" else []
                    except IndexError:
                        pairs[pair[0]] = []
                else:
                    pairs[pair[0]].append(pair[1])
            provider_models = pairs
    print(provider_models)
    transactions = ctx.call(
        get_all_filtered_and_paginated_transactions,
        page=page,
        page_size=page_size,
        tags=tags,
        date_from=date_from,
        date_to=date_to,
        project_id=project_id,
        sort_field=sort_field,
        sort_type=sort_type,
        status_codes=status_codes,
        provider_models=provider_models,
    )

    projects = ctx.call(get_all_projects)
    project_id_name_map = {project.id: project.name for project in projects}
    new_transactions = []
    for transaction in transactions:
        new_transactions.append(
            GetTransactionWithProjectSlugSchema(
                **transaction.model_dump(),
                project_name=project_id_name_map.get(transaction.project_id, ""),
                total_tokens=transaction.input_tokens + transaction.output_tokens
                if transaction.input_tokens and transaction.output_tokens
                else None,
            )
        )

    count = ctx.call(
        count_transactions_for_list,
        tags=tags,
        date_from=date_from,
        date_to=date_to,
        project_id=project_id,
        status_codes=status_codes,
        provider_models=provider_models,
    )
    page_response = GetTransactionPageResponseSchema(
        items=new_transactions,
        page_index=page,
        page_size=page_size,
        total_elements=count,
        total_pages=-(-count // page_size),
    )
    return page_response


@app.get(
    "/api/statistics/transactions_cost",
    response_class=JSONResponse,
    dependencies=[Security(decode_and_validate_token)],
)
async def get_transaction_usage_statistics_over_time(
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
    project_id: str,
    date_from: datetime | str | None = None,
    date_to: datetime | str | None = None,
    period: utils.PeriodEnum = utils.PeriodEnum.day,
) -> list[GetTransactionsUsageStatisticsSchema]:
    """
    Retrieve transaction usage statistics over a specified time period.\n

    This endpoint fetches transaction data based on the specified project ID,
    date range, and period. It then processes the data to generate usage statistics
    including total input tokens, total output tokens, cumulative input tokens, cumulative output tokens as well as
    total cost calculated based on cumulative values for the best possible representation of costs over time.\n

    :param ctx: The transaction context, providing access to dependencies (automatically applied).\n
    :param project_id: The unique identifier of the project.\n
    :param date_from: Starting point of the time interval (optional - when empty, then the scope is counted from the
        beginning of the project's existence).\n
    :param date_to: End point of the time interval (optional - when empty, then the interval is counted up to the
        present time).\n
    :param period: The time period for grouping statistics - can be year, month, week, day, hour or minute (5 minutes).
        (default is "day").\n
    :return: A list of GetTransactionUsageStatisticsSchema (provider, model, date, total_input_tokens,
        total_output_tokens, input_cumulative_total, output_cumulative_total, total_transactions, total_cost)
        representing the usage statistics.\n
    """
    date_from, date_to = utils.check_dates_for_statistics(date_from, date_to)

    count = ctx.call(
        count_transactions,
        project_id=project_id,
        date_from=date_from,
        date_to=date_to,
        status_codes=[200],
    )
    if count == 0:
        return []

    transactions = ctx.call(
        get_list_of_filtered_transactions,
        project_id=project_id,
        date_from=date_from,
        date_to=date_to,
        status_codes=[200],
    )
    transactions = [
        StatisticTransactionSchema(
            project_id=project_id,
            provider=transaction.provider,
            model=transaction.model,
            total_input_tokens=transaction.input_tokens or 0,
            total_output_tokens=transaction.output_tokens or 0,
            total_input_cost=transaction.input_cost or 0,
            total_output_cost=transaction.output_cost or 0,
            total_cost=transaction.total_cost or 0,
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
    stats = utils.token_counter_for_transactions(
        transactions, period, date_from, date_to
    )
    dates = []
    for stat in stats:
        dates.append(stat.date)
    new_stats = []
    for date in set(dates):
        for_date = []
        for stat in stats:
            if stat.date == date:
                for_date.append(
                    GetTransactionUsageStatisticsWithoutDateSchema(
                        provider=stat.provider,
                        model=stat.model,
                        total_input_tokens=stat.total_input_tokens,
                        total_output_tokens=stat.total_output_tokens,
                        input_cumulative_total=stat.input_cumulative_total,
                        output_cumulative_total=stat.output_cumulative_total,
                        total_transactions=stat.total_transactions,
                        total_cost=stat.total_cost,
                    )
                )
        new_stats.append(
            GetTransactionsUsageStatisticsSchema(date=date, records=for_date)
        )
    new_stats.sort(key=lambda statistic: statistic.date)

    return new_stats


@app.get(
    "/api/statistics/transactions_count",
    response_class=JSONResponse,
    dependencies=[Security(decode_and_validate_token)],
)
async def get_transaction_status_statistics_over_time(
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
    project_id: str,
    date_from: datetime | str | None = None,
    date_to: datetime | str | None = None,
    period: utils.PeriodEnum = utils.PeriodEnum.day,
) -> list[GetTransactionStatusStatisticsSchema]:
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
    :param period: The time period for grouping statistics - can be year, month, week, day, hour or minute (5 minutes).
        (default is "day").\n
    :return: A list of GetTransactionStatusStatisticsSchema (date, status_code, total_transactions) representing the
        status statistics.\n
    """
    date_from, date_to = utils.check_dates_for_statistics(date_from, date_to)

    count = ctx.call(
        count_transactions,
        project_id=project_id,
        date_from=date_from,
        date_to=date_to,
    )
    if count == 0:
        return []

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
            total_input_cost=transaction.input_cost or 0,
            total_output_cost=transaction.output_cost or 0,
            total_cost=transaction.total_cost or 0,
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
    stats = utils.status_counter_for_transactions(
        transactions, period, date_from, date_to
    )

    return stats


@app.get(
    "/api/statistics/transactions_speed",
    response_class=JSONResponse,
    dependencies=[Security(decode_and_validate_token)],
)
async def get_transaction_latency_statistics_over_time(
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
    project_id: str,
    date_from: datetime | str | None = None,
    date_to: datetime | str | None = None,
    period: utils.PeriodEnum = utils.PeriodEnum.day,
) -> list[GetTransactionsLatencyStatisticsSchema]:
    """
    Compute mean transactions generation speed and latency statistics over a specified time period.\n

    Endpoint fetches transaction data for the project (project ID) and specified date range (date from, date to). Next, it aggregates the generation speed by the provided granularity (monthly, weekly, daily, hourly or by minutes).\n

    :param ctx: The transaction context, providing access to dependencies (automatically applied).\n
    :param project_id: The unique identifier of the project.\n
    :param date_from: Starting point of the time interval (optional - when empty, then the scope is counted from the
        beginning of the project's existence).\n
    :param date_to: End point of the time interval (optional - when empty, then the interval is counted up to the
        present time).\n
    :param period: The time period for grouping statistics - can be year, month, week, day, hour or minute (5 minutes).
        (default is "day").\n
    :return: A list of GetTransactionLatencyStatisticsSchema (provider, model, date, mean_latency, tokens_per_second,
        total_transactions) representing the generation speed and latency statistics.\n
    """
    date_from, date_to = utils.check_dates_for_statistics(date_from, date_to)

    count = ctx.call(
        count_transactions,
        project_id=project_id,
        date_from=date_from,
        date_to=date_to,
        status_codes=[200],
        null_generation_speed=False,
    )
    if count == 0:
        return []

    transactions = ctx.call(
        get_list_of_filtered_transactions,
        project_id=project_id,
        date_from=date_from,
        date_to=date_to,
        status_codes=[200],
        null_generation_speed=False,
    )
    transactions = [
        StatisticTransactionSchema(
            project_id=project_id,
            provider=transaction.provider,
            model=transaction.model,
            total_input_tokens=transaction.input_tokens or 0,
            total_output_tokens=transaction.output_tokens or 0,
            total_input_cost=transaction.input_cost or 0,
            total_output_cost=transaction.output_cost or 0,
            total_cost=transaction.total_cost or 0,
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
    stats = utils.speed_counter_for_transactions(
        transactions, period, date_from, date_to
    )

    dates = [stat.date for stat in stats]
    new_stats = []
    for date in set(dates):
        for_date = []
        for stat in stats:
            if stat.date == date:
                for_date.append(
                    GetTransactionLatencyStatisticsWithoutDateSchema(
                        provider=stat.provider,
                        model=stat.model,
                        mean_latency=stat.mean_latency,
                        tokens_per_second=stat.tokens_per_second,
                        total_transactions=stat.total_transactions,
                    )
                )
        new_stats.append(
            GetTransactionsLatencyStatisticsSchema(date=date, records=for_date)
        )
    new_stats.sort(key=lambda statistic: statistic.date)

    return new_stats


@app.get(
    "/api/portfolio/details",
    response_class=JSONResponse,
    dependencies=[Security(decode_and_validate_token)],
)
async def get_portfolio_details(
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)]
) -> GetPortfolioDetailsSchema:
    project_count = ctx.call(count_projects)
    total_cost_per_project, total_transactions_per_project = {}, {}
    total_cost, total_transactions = 0, 0
    projects = []
    if project_count > 0:
        projects = ctx.call(get_all_projects)
        projects_ids = [project.id for project in projects]
        for idx in projects_ids:
            transactions = ctx.call(get_transactions_for_project, project_id=idx)
            cost = sum(
                [
                    transaction.total_cost if transaction.total_cost is not None else 0
                    for transaction in transactions
                ]
            )
            total_cost_per_project[idx] = cost
            total_cost += cost
            count = len(transactions)
            total_transactions_per_project[idx] = count
            total_transactions += count
        projects = [
            GetProjectPortfolioSchema(
                **project.model_dump(),
                total_transactions=total_transactions_per_project[project.id],
                total_cost=total_cost_per_project[project.id],
            )
            for project in projects
        ]

    return GetPortfolioDetailsSchema(
        total_cost=total_cost, total_transactions=total_transactions, projects=projects
    )


@app.get(
    "/api/statistics/pricelist",
    response_class=JSONResponse,
    dependencies=[Security(decode_and_validate_token)],
)
async def fetch_provider_pricelist(request: Request) -> list[GetAIProviderPriceSchema]:
    """
    API endpoint to retrieve a price list of AI providers.

    :param request: The incoming request.
    """
    price_list = [
        price for price in get_provider_pricelist(request) if price.is_active is True
    ]
    return [GetAIProviderPriceSchema(**price.__dict__) for price in price_list]


@app.get(
    "/api/providers",
    response_class=JSONResponse,
    dependencies=[Security(decode_and_validate_token)],
)
async def get_providers(request: Request) -> list[GetAIProviderSchema]:
    """
    API endpoint to retrieve a list of AI providers.

    :param request: The incoming request.
    """
    return [GetAIProviderSchema(**provider) for provider in utils.known_ai_providers]


@app.get("/api/config", response_class=JSONResponse)
async def get_config(
    request: Request,
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
) -> dict[str, str | bool]:
    """
    API endpoint to retrieve the config.

    :param ctx: The transaction context dependency.
    """
    config = request.app.container.config()
    organization_name = ctx.call(get_organization_name)

    return {
        "organization": str(organization_name),
        "authorization": config.SSO_AUTH,
        "azure_auth": config.AZURE_CLIENT_ID is not None,
        "google_auth": config.GOOGLE_CLIENT_ID is not None,
    }


@app.get("/api/users", dependencies=[Security(decode_and_validate_token)])
async def get_users(
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
    auth_user: User = Depends(decode_and_validate_token),
) -> list[GetPartialUserSchema]:
    users = ctx.call(get_all_users)
    idx = next(
        (i for i, usr in enumerate(users) if usr.external_id == auth_user.external_id),
        None,
    )
    if idx is not None:
        temp = users.pop(idx)
        users.insert(0, temp)
    else:
        users.insert(0, User(**auth_user.model_dump()))

    parsed_users = map(
        lambda user: GetPartialUserSchema(
            id=user.id,
            email=user.email,
            full_name=str(user.given_name + " " + user.family_name),
            picture=user.picture,
        ),
        users,
    )
    return list(parsed_users)


@app.post(
    "/api/transactions",
    response_class=JSONResponse,
    status_code=201,
    dependencies=[Security(decode_and_validate_token)],
)
def create_transaction(
    request: Request,
    data: CreateTransactionSchema,
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
) -> GetTransactionSchema:
    if ((data.status_code == 200) and data.model and data.provider) and not (
        data.input_cost or data.output_cost or data.total_cost
    ):
        pricelist = get_provider_pricelist(request)
        pricelist = [
            item
            for item in pricelist
            if item.provider == data.provider
            and re.match(item.match_pattern, data.model)
        ]
        if len(pricelist) > 0:
            if pricelist[0].input_price == 0:
                data.input_cost, data.output_cost = 0, 0
                data.total_cost = (
                    (data.input_tokens + data.output_tokens)
                    / 1000
                    * pricelist[0].total_price
                )
            else:
                data.input_cost = pricelist[0].input_price * (data.input_tokens / 1000)
                data.output_cost = pricelist[0].output_price * (
                    data.output_tokens / 1000
                )
                data.total_cost = data.input_cost + data.output_cost
        else:
            data.input_cost, data.output_cost, data.total_cost = None, None, None

    if not data.generation_speed:
        if data.output_tokens is not None and (data.output_tokens > 0):
            data.generation_speed = (
                data.output_tokens
                / (datetime.now(tz=timezone.utc) - data.request_time).total_seconds()
            )
        elif data.output_tokens == 0:
            data.generation_speed = None
        else:
            data.generation_speed = 0

    created_transaction = ctx.call(add_transaction, data=data)
    return GetTransactionSchema(**created_transaction.model_dump())


@app.post("/api/only_for_purpose/mock_transactions", response_class=JSONResponse)
async def mock_transactions(
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
    count: int,
    date_from: datetime,
    date_to: datetime,
) -> dict[str, Any]:
    """
    API endpoint to generate a set of mock transactions. Warining! This endpoint is only for testing purposes and will delete all transactions for project-test.

    :param count: How many transactions you want to mock.
    :param date_from: The start date from which transactions should be added.
    :param date_to: The end date till which transactions should be added.
    :param ctx: The transaction context dependency.
    :return: A dictionary containing the status and message (code and latency).
    """
    time_start = datetime.now(tz=timezone.utc)
    repo = ctx["transaction_repository"]

    # Delete all transactions for project-test in order to avoid duplicates transations keys
    repo.delete_cascade(project_id="project-test")

    # generate random transactions, with different models and providers
    mocked_transactions = utils.generate_mock_transactions(count, date_from, date_to)
    for transaction in mocked_transactions:
        repo.add(transaction)
    time_stop = datetime.now(tz=timezone.utc)

    return {
        "status_code": 200,
        "message": f"{count} transactions added in {(time_stop-time_start).total_seconds()} seconds.",
    }
