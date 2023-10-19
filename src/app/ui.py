from fastapi import Request
from fastapi.responses import HTMLResponse

from app.dependencies import get_transaction_context

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
    return templates.TemplateResponse(
        "projects.html", {"request": request, "projects": project}
    )
