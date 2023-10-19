from fastapi import Request
from fastapi.responses import HTMLResponse

from app.dependencies import get_transaction_context
from config import config

from .app import app, templates


@app.get("/ui", response_class=HTMLResponse)
async def dashboard(request: Request):
    ctx = get_transaction_context(request)
    projects = ctx["project_repository"].get_all()
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "projects": projects}
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
        },
    )
