from fastapi import Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from app.dependencies import get_transaction_context
from config import config

from .app import app, templates


@app.get("/ui", response_class=HTMLResponse)
async def dashboard(request: Request):
    ctx = get_transaction_context(request)
    projects = ctx["project_repository"].get_all()
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "projects": projects,
            "build_sha": config.BUILD_SHA,
        },
    )


class CreateProjectSchema(BaseModel):
    id: int
    name: str


class GetProjectSchema(BaseModel):
    id: int
    name: str


@app.post("/api/project", response_class=JSONResponse)
async def add_project(request: Request, data: CreateProjectSchema) -> GetProjectSchema:
    return GetProjectSchema(id=data.id, name=data.name)


@app.get("/ui/project/{project_id}", response_class=HTMLResponse)
async def read_item(request: Request, project_id: str):
    ctx = get_transaction_context(request)
    project = ctx["project_repository"].get(project_id)
    transactions = ctx["transaction_repository"].get_for_project(project_id)
    scheme, host = config.BASE_URL.split("://")
    project_url = f"{scheme}://{project_id}.{host}"
    return templates.TemplateResponse(
        "project.html",
        {
            "request": request,
            "project": project,
            "transactions": transactions,
            "project_url": project_url,
        },
    )


@app.get(
    "/ui/project/{project_id}/transaction/{transacion_id}", response_class=HTMLResponse
)
async def read_sepcific_transaction(
    request: Request, project_id: str, transacion_id: str
):
    ctx = get_transaction_context(request)
    project = ctx["project_repository"].get(project_id)
    transaction = ctx["transaction_repository"].get_one_by_id(transacion_id)
    scheme, host = config.BASE_URL.split("://")
    project_url = f"{scheme}://{project_id}.{host}"
    return templates.TemplateResponse(
        "transaction.html",
        {
            "request": request,
            "project": project,
            "transaction": transaction,
            "project_url": project_url,
        },
    )
