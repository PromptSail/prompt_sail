from typing import Annotated

from fastapi import Depends, Request
from fastapi.responses import JSONResponse
from lato import TransactionContext

from app.dependencies import get_transaction_context
from projects.models import Project
from projects.schemas import (
    CreateProjectSchema,
    GetProjectSchema,
    GetProjectWithTransactionsSchema,
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
    count_transactions,
    get_all_paginated_transactions,
    get_transaction,
    get_transactions_for_project,
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
) -> GetProjectWithTransactionsSchema:
    transactions = ctx.call(get_transactions_for_project, project_id=project_id)
    project = ctx.call(get_project, project_id=project_id)
    project = GetProjectWithTransactionsSchema(
        transactions=[
            GetTransactionSchema(**transaction.model_dump())
            for transaction in transactions
        ],
        **project.model_dump(),
    )
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
    request: Request,
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
) -> GetTransactionPageResponseSchema:
    query_params = request.query_params.__dict__["_dict"]
    transactions = ctx.call(
        get_all_paginated_transactions,
        page=int(query_params.get("page", 1)),
        page_size=int(query_params.get("page_size", 20)),
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
    count = ctx.call(count_transactions)
    page_response = GetTransactionPageResponseSchema(
        items=transactions,
        page_index=int(query_params.get("page", 1)),
        page_size=int(query_params.get("page_size", 20)),
        total_elements=count,
        total_pages=-(-count // int(query_params.get("page_size", 20))),
    )
    return page_response
