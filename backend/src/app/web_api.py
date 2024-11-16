import re
from collections import defaultdict
from typing import Annotated, Any

import numpy as np
import pandas as pd


import pandas as pd
import utils
from _datetime import datetime, timezone, timedelta
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
    GetProjectsUsageInTimeSchema,
    GetProjectUsageSchema,
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
from raw_transactions.models import TransactionTypeEnum
from raw_transactions.schemas import CreateRawTransactionSchema
from raw_transactions.use_cases import (
    add_raw_transaction,
    get_request_for_transaction,
    get_response_for_transaction,
)
from seedwork.repositories import DocumentNotFoundException
from settings.use_cases import get_organization_name
from slugify import slugify
from transactions.models import Transaction, generate_uuid
from transactions.schemas import (
    CreateTransactionWithRawDataSchema,
    GetTagStatisticsInTime,
    GetTagStatisticsSchema,
    GetTransactionLatencyStatisticsSchema,
    GetTransactionLatencyStatisticsWithoutDateSchema,
    GetTransactionPageResponseSchema,
    GetTransactionSchema,
    GetTransactionsLatencyStatisticsSchema,
    GetTransactionStatusStatisticsSchema,
    GetTransactionsUsageStatisticsSchema,
    GetTransactionUsageStatisticsWithoutDateSchema,
    GetTransactionWithProjectSlugSchema,
    GetTransactionWithRawDataSchema,
    StatisticTransactionSchema,
    TagStatisticTransactionSchema,
)
from transactions.use_cases import (
    add_transaction,
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
    """
    Get the current user's information.

    This endpoint returns the authenticated user's details.

    Parameters:
    - **request**: The incoming request object.
    - **user**: The authenticated user object.

    Returns:
    - A GetUserSchema object containing the user's details.
    """
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
    Retrieve all projects.

    This endpoint returns information about all projects, including transaction counts and total costs.

    Parameters:
    - **ctx**: The transaction context dependency.

    Returns:
    - A list of GetProjectSchema objects representing all projects.
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
    Retrieve details of a specific project.

    This endpoint returns detailed information about a specific project, including transaction count and total cost.

    Parameters:
    - **project_id**: The unique identifier of the project.
    - **ctx**: The transaction context dependency.

    Returns:
    - A GetProjectSchema object representing the project details.

    Raises:
    - HTTPException: 404 error if the project is not found.
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

    Parameters:
    - **data**: The data for creating the project as a CreateProjectSchema object.
    - **ctx**: The transaction context dependency.

    Returns:
    - A GetProjectSchema object representing the created project.
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
    Update an existing project.

    This endpoint updates the details of an existing project.

    Parameters:
    - **project_id**: The unique identifier of the project to be updated.
    - **data**: The UpdateProjectSchema object containing the updated project details.
    - **ctx**: The transaction context dependency.

    Returns:
    - A GetProjectSchema object representing the updated project.
    """
    data = dict(**data.model_dump(exclude_none=True))
    if "slug" in data:
        data["slug"] = slugify(data["slug"])
    if "ai_providers" in data:
        for idx in range(len(data["ai_providers"])):
            data["ai_providers"][idx] = AIProvider(**data["ai_providers"][idx])
            data["ai_providers"][idx].slug = slugify(data["ai_providers"][idx].slug)
    updated = ctx.call(update_project, project_id=project_id, fields_to_update=data)
    return GetProjectSchema(**updated.model_dump())


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
    Delete an existing project and its associated transactions.

    This endpoint deletes a project and all its associated transactions.

    Parameters:
    - **project_id**: The unique identifier of the project to be deleted.
    - **ctx**: The transaction context dependency.

    Returns:
    - No content (204 status code) on successful deletion.
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
) -> GetTransactionWithRawDataSchema:
    """
    Retrieve details of a specific transaction.

    This endpoint returns detailed information about a specific transaction, including raw request and response data.

    Parameters:
    - **transaction_id**: The unique identifier of the transaction.
    - **ctx**: The transaction context dependency.

    Returns:
    - A GetTransactionWithRawDataSchema object representing the transaction details.

    Raises:
    - HTTPException: 404 error if the transaction is not found.
    """
    try:
        transaction = ctx.call(get_transaction, transaction_id=transaction_id)
        request_data = ctx.call(
            get_request_for_transaction, transaction_id=transaction_id
        )
        response_data = ctx.call(
            get_response_for_transaction, transaction_id=transaction_id
        )
    except DocumentNotFoundException:
        raise HTTPException(status_code=404, detail="Transaction not found")
    project = ctx.call(get_project, project_id=transaction.project_id)
    transaction = GetTransactionWithRawDataSchema(
        **transaction.model_dump(),
        project_name=project.name if project else "",
        request=request_data.data,
        response=response_data.data,
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
    Retrieve a paginated list of transactions with filtering options.

    This endpoint returns a paginated list of transactions that can be filtered by various criteria
    such as date range, tags, status codes, and provider models.

    Parameters:
    - **page**: The page number to retrieve (default: 1)
    - **page_size**: Number of transactions per page (default: 20)
    - **tags**: Optional comma-separated list of tags to filter transactions
    - **date_from**: Optional start date for filtering transactions
    - **date_to**: Optional end date for filtering transactions
    - **project_id**: Optional project ID to filter transactions
    - **sort_field**: Optional field name to sort by
    - **sort_type**: Optional sort direction ('asc' or 'desc')
    - **status_codes**: Optional comma-separated list of status codes
    - **provider_models**: Optional comma-separated list of provider.model combinations

    Returns:
    - A GetTransactionPageResponseSchema containing the paginated transactions and metadata
    """
    if tags is not None:
        tags = tags.split(",")
    if status_codes is not None:
        status_codes = list(map(lambda x: int(x), status_codes.split(",")))
    if provider_models is not None:
        provider_models = list(map(lambda x: x.split("."), provider_models.split(",")))
        pairs = {}
        for pair in provider_models:
            if pair[0] not in pairs:
                try:
                    pairs[pair[0]] = (
                        [".".join(pair[1:])] if ".".join(pair[1:]) != "" else []
                    )
                except IndexError:
                    pairs[pair[0]] = []
            else:
                pairs[pair[0]].append(pair[1])
        provider_models = pairs

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
    date_from: str ,
    date_to: str ,
    period: utils.PeriodEnum = utils.PeriodEnum.day,
) -> list[GetTransactionsUsageStatisticsSchema]:
    """
    Calculate cost and usage metrics for transactions within a given time range.
    Only includes successful transactions (status code 200) that occurred between the start and end dates.
    The time range is inclusive - transactions exactly on the start or end date/time will be included.

    Parameters:
    - **ctx**: The transaction context dependency
    - **project_id**: The unique identifier of the project
    - **date_from**: Start date (ISO format: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
    - **date_to**: End date (ISO format: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
    - **period**: Time period for aggregation (year, month, week, day, hour, or 5minutes)

    Returns:
    - A list of GetTransactionsUsageStatisticsSchema objects containing cost and usage statistics
      grouped by the specified period
      
    Raises:
    - HTTPException: 400 error if dates are invalid or in wrong format
    """
    
    
    
    try:
        # Validate date format and convert to datetime
        date_from_dt, date_to_dt = utils.validate_date_range(date_from, date_to)
    except HTTPException as e:
        raise e

    count = ctx.call(
        count_transactions,
        project_id=project_id,
        date_from=date_from_dt,
        date_to=date_to_dt,
        status_codes=[200],
    )
    if count == 0:
        return []

    transactions = ctx.call(
        get_list_of_filtered_transactions,
        project_id=project_id,
        date_from=date_from_dt,
        date_to=date_to_dt,
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
        transactions, period, date_from_dt, date_to_dt
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
    try:
        # Validate date format and convert to datetime
        date_from_dt, date_to_dt = utils.validate_date_range(date_from, date_to)
    except HTTPException as e:
        raise e

    count = ctx.call(
        count_transactions,
        project_id=project_id,
        date_from=date_from_dt,
        date_to=date_to_dt,
    )
    if count == 0:
        return []

    transactions = ctx.call(
        get_list_of_filtered_transactions,
        project_id=project_id,
        date_from=date_from_dt,
        date_to=date_to_dt,
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
        transactions, period, date_from_dt, date_to_dt
    )

    return stats


@app.get(
    "/api/statistics/transactions_speed_old",
    response_class=JSONResponse,
    dependencies=[Security(decode_and_validate_token)],
)
async def get_transactions_speed_statistics_over_time(
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
    project_id: str,
    date_from: str,
    date_to: str,
    period: utils.PeriodEnum = utils.PeriodEnum.day,
) -> list[GetTransactionsLatencyStatisticsSchema]:
    """
    Calculate average generation speed and latency metrics for transactions within a given time range.
    Only includes successful transactions (status code 200) that occurred between the start and end dates.
    The time range is inclusive - transactions exactly on the start or end date/time will be included.

    Parameters:
    - **ctx**: The transaction context dependency
    - **project_id**: The unique identifier of the project
    - **date_from**: Start date (ISO format: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
    - **date_to**: End date (ISO format: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
    - **period**: Time period for aggregation (year, month, week, day, hour, or 5minutes)

    Returns:
    - A list of GetTransactionLatencyStatisticsSchema objects containing latency and speed statistics
      grouped by the specified period
      
    Raises:
    - HTTPException: 400 error if dates are invalid or in wrong format
    """
    try:
        # Validate date format and convert to datetime
        date_from, date_to = utils.validate_date_range(date_from, date_to)
    except HTTPException as e:
        raise e

    # Continue with existing logic
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

    transactions: list[Transaction] = ctx.call(
        get_list_of_filtered_transactions,
        project_id=project_id,
        date_from=date_from,
        date_to=date_to,
        status_codes=[200],
        null_generation_speed=False,
    )
    
    transactions: list[StatisticTransactionSchema] = [
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
    "/api/statistics/transactions_speed",
    response_class=JSONResponse,
    dependencies=[Security(decode_and_validate_token)],
)
async def get_transactions_speed_statistics_over_time_refactored(
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
    project_id: str,
    date_from: str,
    date_to: str,
    period: utils.PeriodEnum = utils.PeriodEnum.day,
) -> list[GetTransactionsLatencyStatisticsSchema]:
    """
    Calculate average generation speed and latency metrics for transactions within a given time range.
    Only includes successful transactions (status code 200) that occurred between the start and end dates.
    The time range is inclusive - transactions exactly on the start or end date/time will be included.

    Parameters:
    - **ctx**: The transaction context dependency
    - **project_id**: The unique identifier of the project
    - **date_from**: Start date (ISO format: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
    - **date_to**: End date (ISO format: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
    - **period**: Time period for aggregation (year, month, week, day, hour, or 5minutes)

    Returns:
    - A list of GetTransactionLatencyStatisticsSchema objects containing latency and speed statistics
      grouped by the specified period
      
    Raises:
    - HTTPException: 400 error if dates are invalid or in wrong format
    """
    try:
        # Validate date format and convert to datetime
        date_from_dt, date_to_dt = utils.validate_date_range(date_from, date_to)
    except HTTPException as e:
        raise e

    # Continue with existing logic
    count = ctx.call(
        count_transactions,
        project_id=project_id,
        date_from=date_from_dt,
        date_to=date_to_dt,
        status_codes=[200],
        null_generation_speed=False,
    )
    
    if count == 0:
        return []

    transactions: list[Transaction] = ctx.call(
        get_list_of_filtered_transactions,
        project_id=project_id,
        date_from=date_from_dt,
        date_to=date_to_dt,
        status_codes=[200],
        null_generation_speed=False,
    )
    # Transform and calculate statistics
    df = utils.prepare_transaction_dataframe(transactions, date_from_dt, date_to_dt)
    stats_df = utils.calculate_speed_statistics(df, utils.pandas_period_from_string(period))
    
    # Format response
    return utils.format_statistics_response(stats_df)


@app.get(
    "/api/portfolio/details",
    response_class=JSONResponse,
    dependencies=[Security(decode_and_validate_token)],
)
async def get_portfolio_details(
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)]
) -> GetPortfolioDetailsSchema:
    """
    Retrieve portfolio-wide statistics and details.

    This endpoint provides an overview of all projects in the portfolio, including
    aggregated statistics such as total costs, total transactions, and individual
    project metrics.

    Parameters:
    - **ctx**: The transaction context dependency

    Returns:
    - A GetPortfolioDetailsSchema containing portfolio-wide statistics and project details
    """
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
    "/api/portfolio/usage_in_time",
    response_class=JSONResponse,
    dependencies=[Security(decode_and_validate_token)],
)
async def get_portfolio_usage_in_time(
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
    date_from: datetime | str | None = None,
    date_to: datetime | str | None = None,
    period: utils.PeriodEnum = utils.PeriodEnum.day,
) -> list[GetProjectsUsageInTimeSchema]:
    """
    Retrieve portfolio usage statistics over time.

    This endpoint provides detailed statistics about portfolio-wide usage patterns,
    including token consumption and costs across all projects over time.

    Parameters:
    - **ctx**: The transaction context dependency
    - **date_from**: Optional start date (format: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
    - **date_to**: Optional end date (format: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
    - **period**: Time period for aggregation (year, month, week, day, hour, or 5minutes)

    Returns:
    - A list of GetProjectsUsageInTimeSchema objects containing usage statistics
      grouped by the specified period
    """
    project_count = ctx.call(count_projects)
    projects_usage_in_time = []
    results = {}
    if project_count > 0:
        projects = ctx.call(get_all_projects)
        project_ids = [project.id for project in projects]
        for idx in project_ids:
            if not date_from:
                date_from = [
                    project.created_at for project in projects if project.id == idx
                ][0]
            if not date_to:
                date_to = datetime.now()
            date_from, date_to = utils.check_dates_for_statistics(date_from, date_to)

            count = ctx.call(
                count_transactions,
                project_id=idx,
                date_from=date_from,
                date_to=date_to,
                status_codes=[200],
            )
            if count == 0:
                results[idx] = []

            transactions = ctx.call(
                get_list_of_filtered_transactions,
                project_id=idx,
                date_from=date_from,
                date_to=date_to,
                status_codes=[200],
            )
            transactions = [
                StatisticTransactionSchema(
                    project_id=idx,
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

            if len(transactions) > 0:
                stats = utils.token_counter_for_transactions(
                    transactions, period, date_from, date_to, False
                )
                results[idx] = stats

        if sum([len(stat) for stat in results.items()]) == 0:
            return []

        aggregated_data = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

        for project_id, records in results.items():
            if len(records) > 0:
                for record in records:
                    date = record.date
                    aggregated_data[date][project_id][
                        "total_input_tokens"
                    ] += record.total_input_tokens
                    aggregated_data[date][project_id][
                        "total_output_tokens"
                    ] += record.total_output_tokens
                    aggregated_data[date][project_id][
                        "input_cumulative_total"
                    ] += record.input_cumulative_total
                    aggregated_data[date][project_id][
                        "output_cumulative_total"
                    ] += record.output_cumulative_total
                    aggregated_data[date][project_id][
                        "total_transactions"
                    ] += record.total_transactions
                    aggregated_data[date][project_id]["total_cost"] += record.total_cost

        result = []

        for date, statistics in aggregated_data.items():
            date_record = {"date": date, "records": []}
            for project_id, stats in statistics.items():
                record = {
                    "project_id": project_id,
                    "total_input_tokens": stats["total_input_tokens"],
                    "total_output_tokens": stats["total_output_tokens"],
                    "input_cumulative_total": stats["input_cumulative_total"],
                    "output_cumulative_total": stats["output_cumulative_total"],
                    "total_transactions": stats["total_transactions"],
                    "total_cost": stats["total_cost"],
                }
                date_record["records"].append(record)
            result.append(date_record)

        for usage in result:
            records = []
            for record in usage["records"]:
                project_name = [
                    project.name
                    for project in projects
                    if project.id == record["project_id"]
                ][0]
                records.append(
                    GetProjectUsageSchema(**record, project_name=project_name)
                )
            projects_usage_in_time.append(
                GetProjectsUsageInTimeSchema(date=usage["date"], records=records)
            )

    return projects_usage_in_time


@app.get(
    "/api/portfolio/costs_by_tag",
    response_class=JSONResponse,
    dependencies=[Security(decode_and_validate_token)],
)
async def get_portfolio_costs_by_tag(
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
    date_from: datetime | str | None = None,
    date_to: datetime | str | None = None,
    period: utils.PeriodEnum = utils.PeriodEnum.day,
) -> list[GetTagStatisticsInTime]:
    """
    Retrieve cost statistics grouped by tags over time.

    This endpoint calculates and returns cost statistics for transactions,
    grouped by their tags and aggregated over the specified time period.

    Parameters:
    - **ctx**: The transaction context dependency
    - **date_from**: Optional start date (format: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
    - **date_to**: Optional end date (format: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
    - **period**: Time period for aggregation (year, month, week, day, hour, or 5minutes)

    Returns:
    - A list of GetTagStatisticsInTime objects containing cost statistics by tag
      grouped by the specified period
    """
    date_from, date_to = utils.check_dates_for_statistics(date_from, date_to)
    count = ctx.call(
        count_transactions,
        date_from=date_from,
        date_to=date_to,
        status_codes=[200],
    )
    if count == 0:
        return []

    transactions = ctx.call(
        get_list_of_filtered_transactions,
        date_from=date_from,
        date_to=date_to,
        status_codes=[200],
    )

    transactions_multiplied = []
    for transaction in transactions:
        if len(transaction.tags) == 0:
            transactions_multiplied.append(
                Transaction(
                    id=transaction.id,
                    project_id=transaction.project_id,
                    tags=["untagged-transactions"],
                    provider=transaction.provider,
                    model=transaction.model,
                    type=transaction.type,
                    os=transaction.os,
                    input_tokens=transaction.input_tokens,
                    output_tokens=transaction.output_tokens,
                    library=transaction.library,
                    status_code=transaction.status_code,
                    messages=transaction.messages,
                    last_message=transaction.last_message,
                    prompt=transaction.prompt,
                    error_message=transaction.error_message,
                    generation_speed=transaction.generation_speed,
                    input_cost=transaction.input_cost,
                    output_cost=transaction.output_cost,
                    total_cost=transaction.total_cost,
                    request_time=transaction.request_time,
                    response_time=transaction.response_time,
                )
            )
        else:
            for tag in transaction.tags:
                transactions_multiplied.append(
                    Transaction(
                        id=transaction.id,
                        project_id=transaction.project_id,
                        tags=[tag],
                        provider=transaction.provider,
                        model=transaction.model,
                        type=transaction.type,
                        os=transaction.os,
                        input_tokens=transaction.input_tokens,
                        output_tokens=transaction.output_tokens,
                        library=transaction.library,
                        status_code=transaction.status_code,
                        messages=transaction.messages,
                        last_message=transaction.last_message,
                        prompt=transaction.prompt,
                        error_message=transaction.error_message,
                        generation_speed=transaction.generation_speed,
                        input_cost=transaction.input_cost,
                        output_cost=transaction.output_cost,
                        total_cost=transaction.total_cost,
                        request_time=transaction.request_time,
                        response_time=transaction.response_time,
                    )
                )

    transactions = [
        TagStatisticTransactionSchema(
            tag=transaction.tags[0],
            total_input_tokens=transaction.input_tokens or 0,
            total_output_tokens=transaction.output_tokens or 0,
            total_input_cost=transaction.input_cost or 0,
            total_output_cost=transaction.output_cost or 0,
            total_cost=transaction.total_cost or 0,
            date=transaction.response_time,
            total_transactions=1,
        )
        for transaction in transactions_multiplied
    ]

    if len(transactions) > 0:
        stats = utils.token_counter_for_transactions_by_tag(
            transactions, period, date_from, date_to, False
        )
        df = pd.DataFrame([stat.model_dump() for stat in stats])
        grouped = (
            df.groupby("date")
            .apply(lambda x: x.to_dict(orient="records"))
            .reset_index(name="records")
        )
        output = grouped.to_dict(orient="records")

        response = []
        for row in output:
            records = []
            for record in row["records"]:
                records.append(GetTagStatisticsSchema(**record))
            response.append(GetTagStatisticsInTime(date=row["date"], records=records))
        return response

    return []


@app.get(
    "/api/statistics/pricelist",
    response_class=JSONResponse,
    dependencies=[Security(decode_and_validate_token)],
)
async def fetch_provider_pricelist(request: Request) -> list[GetAIProviderPriceSchema]:
    """
    Retrieve the price list for all AI providers.

    This endpoint returns the current price list for all active AI providers,
    including their models and associated costs.

    Parameters:
    - **request**: The incoming request object

    Returns:
    - A list of GetAIProviderPriceSchema objects containing pricing information
      for each active provider and model
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
    Retrieve the list of supported AI providers.

    This endpoint returns information about all supported AI providers,
    including their names and API base URLs.

    Parameters:
    - **request**: The incoming request object

    Returns:
    - A list of GetAIProviderSchema objects containing provider information
    """
    return [GetAIProviderSchema(**provider) for provider in utils.known_ai_providers]


@app.get("/api/config", response_class=JSONResponse)
async def get_config(
    request: Request,
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
) -> dict[str, str | bool]:
    """
    Retrieve application configuration settings.

    This endpoint returns the current application configuration, including
    organization name and authentication settings (SSO, Azure, Google).

    Parameters:
    - **request**: The incoming request object
    - **ctx**: The transaction context dependency

    Returns:
    - A dictionary containing configuration settings including:
      - organization: Organization name
      - authorization: SSO authentication status
      - azure_auth: Azure authentication availability
      - google_auth: Google authentication availability
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
    """
    Retrieve a list of all users.

    This endpoint returns a list of all users, with the authenticated user always
    appearing first in the list. Each user's information includes their ID, email,
    full name, and profile picture.

    Parameters:
    - **ctx**: The transaction context dependency
    - **auth_user**: The authenticated user making the request

    Returns:
    - A list of GetPartialUserSchema objects containing user information
    """
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
    request_object: Request,
    data: CreateTransactionWithRawDataSchema,
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
) -> GetTransactionSchema:
    """
    Create a new transaction.

    This endpoint creates a new transaction based on the provided data. It calculates the cost
    of the transaction if not provided, using the price list for the specified model and provider.

    Parameters:
    - **request_object**: The incoming fastapirequest object.
    - **data**: The data for creating the transaction as a CreateTransactionWithRawDataSchema object.
    - **ctx**: The transaction context dependency.

    Returns:
    - A GetTransactionWithRawDataSchema object representing the created transaction.
    """
    if ((data.status_code == 200) and data.model and data.provider) and not (
        data.input_cost or data.output_cost or data.total_cost
    ):
        pricelist = get_provider_pricelist(request_object)
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
            time_elapsed = data.response_time - data.request_time
            data.generation_speed = (data.output_tokens + 0.0) / (
                time_elapsed.total_seconds() + 0.000001
            )

        elif data.output_tokens == 0:
            data.generation_speed = None
        else:
            data.generation_speed = 0

    created_transaction = ctx.call(add_transaction, data=data)

    request_data = CreateRawTransactionSchema(
        transaction_id=created_transaction.id,
        type=TransactionTypeEnum.request,
        data=data.request_json,
    )

    response_data = CreateRawTransactionSchema(
        transaction_id=created_transaction.id,
        type=TransactionTypeEnum.response,
        data=data.response_json,
    )

    raw_transaction_request = ctx.call(add_raw_transaction, data=request_data)
    raw_transaction_response = ctx.call(add_raw_transaction, data=response_data)

    project = ctx.call(get_project, project_id=created_transaction.project_id)

    return GetTransactionWithRawDataSchema(
        **created_transaction.model_dump(),
        project_name=project.name,
        request=raw_transaction_request.data,
        response=raw_transaction_response.data,
    )


@app.post("/api/only_for_purpose/mock_transactions", response_class=JSONResponse)
async def mock_transactions(
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
    count: int,
    date_from: datetime,
    date_to: datetime,
) -> dict[str, Any]:
    """
    Generate mock transactions for testing purposes.

    This endpoint creates a specified number of mock transactions within a given date range.
    Warning: This endpoint is only for testing purposes and will delete existing test transactions in the "project-test" project.

    Parameters:
    - **ctx**: The transaction context dependency
    - **count**: Number of mock transactions to generate
    - **date_from**: Start date for the mock transactions (format: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
    - **date_to**: End date for the mock transactions (format: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)

    Returns:
    - A dictionary containing the status code and execution time information
    """
    time_start = datetime.now(tz=timezone.utc)
    transactions_repo = ctx["transaction_repository"]

    # Delete all transactions for project-test in order to avoid duplicates transactions keys
    transactions_repo.delete_cascade(project_id="project-test")

    # generate random transactions, with different models and providers
    mocked_transactions = utils.generate_mock_transactions(count, date_from, date_to)
    for transaction in mocked_transactions:
        transactions_repo.add(transaction)
    time_stop = datetime.now(tz=timezone.utc)

    return {
        "status_code": 200,
        "message": f"{count} transactions added in {(time_stop-time_start).total_seconds()} seconds.",
    }


@app.post(
    "/api/only_for_purpose/remove_mocked_transactions", response_class=JSONResponse
)
async def remove_mocked_transactions(
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
) -> dict[str, Any]:
    """
    Remove mocked transactions.

    This endpoint removes all mocked transactions for the 'project-test' project. 
    Warning: This endpoint is only for testing purposes.

    Parameters:
    - **ctx**: The transaction context dependency.

    Returns:
    - A dictionary containing the status code and a message confirming the removal of mocked transactions.
    """
    transactions_repo = ctx["transaction_repository"]
    transactions_repo.delete_cascade(project_id="project-test")

    return {
        "status_code": 200,
        "message": f"Mocked transactions removed",
    }
