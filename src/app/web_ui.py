from fastapi import Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from app.dependencies import get_transaction_context
from config import config

from .app import app, templates


class CreateProjectSchema(BaseModel):
    id: str
    name: str
    slug: str
    api_base: str
    org_id: str


class GetProjectSchema(BaseModel):
    id: str
    name: str
    slug: str
    api_base: str
    org_id: str


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


@app.get("/api/projects", response_class=JSONResponse)
async def get_projects(request: Request):
    ctx = get_transaction_context(request)
    projects = ctx["project_repository"].get_all()
    return projects


@app.post("/api/project", response_class=JSONResponse)
async def add_project(request: Request, data: CreateProjectSchema) -> GetProjectSchema:
    return GetProjectSchema(
        id=1, name=data.name, slug=data.slug, api_base=data.api_base, org_id=data.org_id
    )


@app.get("/ui/project", response_class=HTMLResponse)
async def get_project_form(request: Request):
    ctx = get_transaction_context(request)
    return templates.TemplateResponse(
        "project-form.html",
        {
            "request": request,
            "build_sha": config.BUILD_SHA,
        },
    )


@app.post("/ui/project", response_class=HTMLResponse)
async def add_project_via_ui(
    request: Request,
    proj_id: str = Form(...),
    name: str = Form(...),
    slug: str = Form(...),
    api_base: str = Form(default="https://api.openai.com/v1"),
    org_id: str = Form(default="none"),
):
    ctx = get_transaction_context(request)
    if ctx["project_repository"].find_one({"_id": proj_id}) or ctx[
        "project_repository"
    ].find_one({"slug": slug}):
        return templates.TemplateResponse(
            "project-form.html",
            {
                "request": request,
                "error": "Project already exists",
                "build_sha": config.BUILD_SHA,
            },
        )

    if api_base == "":
        api_base = "https://api.openai.com/v1"
    if org_id == "":
        org_id = "none"

    data = CreateProjectSchema(
        id=proj_id, name=name, slug=slug, api_base=api_base, org_id=org_id
    )
    project = ctx["project_repository"].add(data)
    return templates.TemplateResponse(
        "project-form.html",
        {
            "request": request,
            "project": project,
            "success": "Project added successfully",
            "build_sha": config.BUILD_SHA,
        },
    )


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
            "build_sha": config.BUILD_SHA,
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
            "build_sha": config.BUILD_SHA,
        },
    )
