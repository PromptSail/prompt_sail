from typing import Annotated

from fastapi import Request, Depends
from fastapi.responses import JSONResponse

from app.dependencies import get_transaction_context
from projects.models import Project
from projects.schemas import CreateProjectSchema, UpdateProjectSchema, GetProjectSchema, \
    GetProjectWithTransactionsSchema
from projects.use_cases import get_all_projects, add_project, update_project, delete_project, get_project
from transactions.models import generate_uuid
from transactions.schemas import GetTransactionSchema
from transactions.use_cases import get_transactions_for_project
from lato import TransactionContext
from .app import app


@app.get("/api/projects")
async def get_projects(ctx: Annotated[TransactionContext, Depends(get_transaction_context)]) -> list[GetProjectSchema]:
    projects = ctx.call(get_all_projects)
    return projects


@app.get("/api/projects/{project_id}", response_class=JSONResponse, status_code=200)
async def get_project_details(
    project_id: str, 
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)]
) -> GetProjectWithTransactionsSchema:
    transactions = ctx.call(get_transactions_for_project, project_id=project_id)
    project = ctx.call(get_project, project_id=project_id)
    project = GetProjectWithTransactionsSchema(transactions=[GetTransactionSchema(**transaction.model_dump()) 
                                                             for transaction in transactions], **project.model_dump())
    return project


@app.post("/api/projects", response_class=JSONResponse, status_code=201)
async def create_project(
    data: CreateProjectSchema, 
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)]
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
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)]
) -> GetProjectSchema:
    data = dict(**data.model_dump(exclude_none=True))
    updated = ctx.call(update_project, project_id=project_id, fields_to_update=data)
    return updated


@app.delete("/api/projects/{project_id}", response_class=JSONResponse, status_code=204)
async def delete_existing_project(
    project_id: str,
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)]
):
    ctx.call(delete_project, project_id=project_id)
