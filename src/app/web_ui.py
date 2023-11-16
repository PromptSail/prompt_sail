from fastapi import Form, Request
from fastapi.responses import HTMLResponse

from app.dependencies import get_transaction_context
from config import config
from projects.schemas import CreateProjectSchema, UpdateProjectSchema

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


@app.get("/ui/project/add", response_class=HTMLResponse)
async def get_project_form(request: Request):
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
    org_id: str | None = Form(...),
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


@app.post("/ui/project/delete", response_class=HTMLResponse)
async def delete_project_via_ui(request: Request, project_id: str = Form(...)):
    ctx = get_transaction_context(request)
    projects = ctx["project_repository"].get_all()
    project = ctx["project_repository"].get(project_id)
    if project:
        ctx["project_repository"].delete(project_id)
        projects = ctx["project_repository"].get_all()
        return templates.TemplateResponse(
            "dashboard.html",
            {
                "request": request,
                "projects": projects,
                "success": f"Project {project_id} deleted successfully",
                "build_sha": config.BUILD_SHA,
            },
        )
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "projects": projects,
            "error": f"Project {project_id} not found",
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


@app.get("/ui/project/{project_id}/update", response_class=HTMLResponse)
async def get_project_update_form(request: Request, project_id: str):
    ctx = get_transaction_context(request)
    project = ctx["project_repository"].get(project_id)
    return templates.TemplateResponse(
        "project-update-form.html",
        {
            "request": request,
            "project": project,
            "build_sha": config.BUILD_SHA,
        },
    )


@app.post("/ui/project/update", response_class=HTMLResponse)
async def update_project_via_ui(
    request: Request,
    proj_id: str = Form(...),
    name: str = Form(...),
    slug: str = Form(...),
    api_base: str = Form(...),
    org_id: str = Form(...),
):
    ctx = get_transaction_context(request)
    project = ctx["project_repository"].get(proj_id)
    if project:
        data = UpdateProjectSchema(
            id=proj_id, name=name, slug=slug, api_base=api_base, org_id=org_id
        )
        ctx["project_repository"].update(data)
        project = ctx["project_repository"].get(proj_id)
        return templates.TemplateResponse(
            "project-update-form.html",
            {
                "request": request,
                "project": project,
                "success": "Project updated successfully",
                "build_sha": config.BUILD_SHA,
            },
        )
    projects = ctx["project_repository"].get_all()
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "projects": projects,
            "error": "Project not found",
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
