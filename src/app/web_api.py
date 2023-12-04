from fastapi import Request
from fastapi.responses import JSONResponse

from app.dependencies import get_transaction_context
from projects.schemas import CreateProjectSchema, UpdateProjectSchema, GetProjectSchema, \
    GetProjectWithTransactionsSchema
from projects.use_cases import get_all_projects, add_project, update_project, delete_project, get_project
from transactions.schemas import GetTransactionSchema
from transactions.use_cases import get_transactions_for_project

from .app import app


@app.get("/api/projects", response_class=JSONResponse, status_code=200)
async def get_projects(request: Request) -> list[GetProjectSchema]:
    ctx = get_transaction_context(request)
    projects = ctx.call(get_all_projects)
    return projects


@app.get("/api/projects/{project_id}", response_class=JSONResponse, status_code=200)
async def get_project_details(request: Request, project_id: str) -> GetProjectWithTransactionsSchema:
    ctx = get_transaction_context(request)
    transactions = ctx.call(get_transactions_for_project, project_id=project_id)
    project = ctx.call(get_project, project_id=project_id)
    project = GetProjectWithTransactionsSchema(transactions=[GetTransactionSchema(**transaction.model_dump()) 
                                                             for transaction in transactions], **project.model_dump())
    return project


@app.post("/api/projects", response_class=JSONResponse, status_code=201)
async def create_project(request: Request, data: CreateProjectSchema) -> GetProjectSchema:
    ctx = get_transaction_context(request)
    project = ctx.call(add_project, data=data)
    project = GetProjectSchema(**project.model_dump())
    return project


@app.put("/api/projects/{project_id}", response_class=JSONResponse, status_code=200)
async def update_existing_project(request: Request, project_id: str, data: UpdateProjectSchema) -> GetProjectSchema:
    ctx = get_transaction_context(request)
    data = GetProjectSchema(**data.model_dump(), id=project_id)
    updated = ctx.call(update_project, data=data)
    return updated


@app.delete("/api/projects/{project_id}", response_class=JSONResponse, status_code=204)
async def delete_existing_project(request: Request, project_id: str):
    ctx = get_transaction_context(request)
    ctx.call(delete_project, project_id=project_id)
