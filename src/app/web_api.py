from fastapi import Request
from fastapi.responses import JSONResponse

from app.dependencies import get_transaction_context
from projects.schemas import CreateProjectSchema, UpdateProjectSchema
from projects.use_cases import (get_all_projects, add_project, update_project, delete_project, 
                                get_project, get_project_by_slug)
from transactions.use_cases import get_transactions_for_project

from .app import app


@app.get("/api/projects", response_class=JSONResponse)
async def get_projects(request: Request):
    ctx = get_transaction_context(request)
    projects = ctx.call(get_all_projects)
    return projects


@app.get("/api/projects/{project_id}", response_class=JSONResponse)
async def get_specific_project(request: Request, project_id: str):
    ctx = get_transaction_context(request)
    transactions = ctx.call(get_transactions_for_project, project_id=project_id)
    project = ctx.call(get_project, project_id=project_id)
    if project is None:
        return JSONResponse({"error": "Project not found"}, status_code=404)
    project = project.model_dump()  # convert to dict to append transactions
    project["transactions"] = transactions
    return project


@app.post("/api/projects", response_class=JSONResponse)
async def create_project(request: Request, data: CreateProjectSchema):
    ctx = get_transaction_context(request)
    project = ctx.call(add_project, data=data)
    if project is None:
        return JSONResponse({"error": "Project already exists"}, status_code=400)
    return JSONResponse(data.model_dump(), status_code=200)


@app.put("/api/projects", response_class=JSONResponse)
async def update_existing_project(request: Request, data: UpdateProjectSchema):
    ctx = get_transaction_context(request)
    updated = ctx.call(update_project, data=data)
    if updated:
        return JSONResponse(data.model_dump(), status_code=200)
    return JSONResponse({"error": "Project not found"}, status_code=404)


@app.delete("/api/projects/{project_id}", response_class=JSONResponse)
async def delete_existing_project(request: Request, project_id: str):
    ctx = get_transaction_context(request)
    deleted = ctx.call(delete_project, project_id=project_id)
    if deleted:
        return JSONResponse({"success": "Project deleted successfully"}, status_code=200) 
    return JSONResponse({"error": "Project not found"}, status_code=404)
