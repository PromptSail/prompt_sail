from typing import Annotated
from datetime import datetime
from fastapi import Depends
from fastapi.responses import JSONResponse
from lato import TransactionContext

from app.dependencies import get_transaction_context
from projects.models import Project
from projects.schemas import (
    CreateProjectSchema,
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
from transactions.models import generate_uuid
from transactions.schemas import (
    GetTransactionPageResponseSchema,
    GetTransactionSchema,
    GetTransactionWithProjectSlugSchema,
)
from transactions.use_cases import (
    get_all_filtered_and_paginated_transactions,
    get_transaction,
    count_transactions
)

from .app import app


@app.get("/api/projects")
async def get_projects(
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)]
) -> list[GetProjectSchema]:
    projects = ctx.call(get_all_projects)
    return projects


@app.get("/api/projects/{project_id}", response_class=JSONResponse, status_code=200)
async def get_project_details(
    project_id: str,
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
) -> GetProjectSchema:
    project = ctx.call(get_project, project_id=project_id)
    project = GetProjectSchema(**project.model_dump())
    return project


@app.post("/api/projects", response_class=JSONResponse, status_code=201)
async def create_project(
    data: CreateProjectSchema,
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
) -> GetProjectSchema:
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
    data = dict(**data.model_dump(exclude_none=True))
    updated = ctx.call(update_project, project_id=project_id, fields_to_update=data)
    return updated


@app.delete("/api/projects/{project_id}", response_class=JSONResponse, status_code=204)
async def delete_existing_project(
    project_id: str,
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
):
    ctx.call(delete_project, project_id=project_id)


@app.get(
    "/api/transactions/{transaction_id}", response_class=JSONResponse, status_code=200
)
async def get_transaction_details(
    transaction_id: str,
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
) -> GetTransactionSchema:
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
    project_id: str | None = None
) -> GetTransactionPageResponseSchema:
    if tags is not None:
        tags = tags.split(',')
    
    transactions = ctx.call(
        get_all_filtered_and_paginated_transactions,
        page=page,
        page_size=page_size,
        tags=tags,
        date_from=date_from,
        date_to=date_to,
        project_id=project_id
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
    count = ctx.call(count_transactions, tags=tags, date_from=date_from, date_to=date_to, project_id=project_id)
    page_response = GetTransactionPageResponseSchema(
        items=transactions,
        page_index=page,
        page_size=page_size,
        total_elements=count,
        total_pages=-(-count // page_size),
    )
    return page_response