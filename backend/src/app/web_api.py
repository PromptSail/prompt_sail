from datetime import datetime
from typing import Annotated, Any

import utils
from app.dependencies import get_transaction_context
from fastapi import Depends
from fastapi.responses import JSONResponse
from lato import TransactionContext
from projects.models import Project
from projects.schemas import (
    CreateProjectSchema,
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
from transactions.models import generate_uuid
from transactions.schemas import (
    GetTransactionPageResponseSchema,
    GetTransactionSchema,
    GetTransactionWithProjectSlugSchema,
)
from transactions.use_cases import (
    count_token_usage_for_project,
    count_transactions,
    delete_multiple_transactions,
    get_all_filtered_and_paginated_transactions,
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
    transactions_count = {}
    total_tokens_usage = {}
    for project in projects:
        transactions_count[project.id] = ctx.call(
            count_transactions, project_id=project.id
        )
        total_tokens_usage[project.id] = ctx.call(
            count_token_usage_for_project, project_id=project.id
        )
    projects = [
        GetProjectSchema(
            **project.model_dump(),
            total_transactions=transactions_count[project.id],
            total_tokens_usage=total_tokens_usage[project.id],
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
    total_tokens_usage = ctx.call(count_token_usage_for_project, project_id=project_id)
    project = GetProjectSchema(
        **project.model_dump(),
        total_transactions=transaction_count,
        total_tokens_usage=total_tokens_usage,
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
    updated = ctx.call(update_project, project_id=project_id, fields_to_update=data)
    total_tokens_usage = ctx.call(count_token_usage_for_project, project_id=project_id)
    return GetProjectSchema(**updated.model_dump(), total_tokens_usage=total_tokens_usage)


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
    transaction_id: str,
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
) -> GetTransactionSchema:
    """
    API endpoint to retrieve details of a specific transaction.

    :param transaction_id: The identifier of the transaction.
    :param ctx: The transaction context dependency.
    """
    transaction = ctx.call(get_transaction, transaction_id=transaction_id)
    transaction = GetTransactionSchema(**transaction.model_dump())
    return transaction


@app.get("/api/transactions", response_class=JSONResponse, status_code=200)
async def get_paginated_transactions(
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
    projects = ctx.call(get_all_projects)
    project_id_name_map = {project.id: project.name for project in projects}
    transactions = [
        GetTransactionWithProjectSlugSchema(
            **transaction.model_dump(),
            project_name=project_id_name_map.get(transaction.project_id, None),
        )
        for transaction in transactions
    ]
    count = ctx.call(
        count_transactions,
        tags=tags,
        date_from=date_from,
        date_to=date_to,
        project_id=project_id,
    )
    page_response = GetTransactionPageResponseSchema(
        items=transactions,
        page_index=page,
        page_size=page_size,
        total_elements=count,
        total_pages=-(-count // page_size),
    )
    return page_response


@app.get("/api/providers", response_class=JSONResponse)
async def get_providers(
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)]
) -> list[GetAIProviderSchema]:
    """
    API endpoint to retrieve a list of AI providers.

    :param ctx: The transaction context dependency.
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
