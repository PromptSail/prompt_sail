from fastapi import Request
from fastapi.responses import JSONResponse

from app.dependencies import get_transaction_context
from projects.schemas import CreateProjectSchema, UpdateProjectSchema

from .app import app


@app.get("/api/projects", response_class=JSONResponse)
async def get_projects(request: Request):
    ctx = get_transaction_context(request)
    projects = ctx["project_repository"].get_all()
    return projects


@app.get("/api/project/{project_id}", response_class=JSONResponse)
async def get_project(request: Request, project_id: str):
    ctx = get_transaction_context(request)
    transactions = ctx["transaction_repository"].get_for_project(project_id)
    project = ctx["project_repository"].get(project_id)
    project = project.model_dump()  # convert to dict to append transactions
    project["transactions"] = transactions
    return project


@app.post("/api/project", response_class=JSONResponse)
async def add_project(request: Request, data: CreateProjectSchema):
    ctx = get_transaction_context(request)
    if ctx["project_repository"].get(data.id) or ctx[
        "project_repository"
    ].find_one({"slug": data.slug}):
        return JSONResponse({"error": "Project already exists"}, status_code=400)
    ctx["project_repository"].add(data)
    return JSONResponse(data.model_dump(), status_code=200)


@app.put("/api/project/{project_id}", response_class=JSONResponse)
async def update_project(request: Request, project_id: str, data: UpdateProjectSchema):
    ctx = get_transaction_context(request)
    if ctx["project_repository"].get(project_id) or ctx[
        "project_repository"
    ].find_one({"slug": data.slug}):
        ctx["project_repository"].update(data)
        return JSONResponse({"success": "Project updated successfully"}, status_code=200)
    return JSONResponse({"error": "Project not found"}, status_code=404)


@app.delete("/api/project/{project_id}", response_class=JSONResponse)
async def delete_project(request: Request, project_id: str):
    ctx = get_transaction_context(request)
    project = ctx["project_repository"].get(project_id)
    if project:
        ctx["project_repository"].delete(project_id)
        return JSONResponse({"success": "Project deleted successfully"}, status_code=200) 
    return JSONResponse({"error": "Project not found"}, status_code=404)
