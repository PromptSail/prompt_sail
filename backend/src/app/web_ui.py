from fastapi import Request #, Form
from fastapi.responses import HTMLResponse

from app.dependencies import get_transaction_context
from config import config
# from projects.schemas import (
#     CreateProjectSchema,
#     GetProjectSchema,
#     ProjectAIProviderSchema,
# )
from projects.use_cases import (
    # add_project,
    # delete_project,
    get_all_projects,
    # get_project,
    # update_project,
)
# from transactions.use_cases import get_transaction, get_transactions_for_project

from .app import app, templates


@app.get("/ui", response_class=HTMLResponse)
async def dashboard(request: Request):
    ctx = get_transaction_context(request)
    projects = ctx.call(get_all_projects)
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "projects": projects,
            "build_sha": config.BUILD_SHA,
        },
    )


# @app.get("/ui/project/add", response_class=HTMLResponse)
# async def get_project_form(request: Request):
#     provider_names = [
#         "OpenAI",
#         "Azure OpenAI",
#         "Google Palm",
#         "Anthropic Cloud",
#         "Meta LLama",
#         "HuggingFace",
#         "Custom",
#     ]
#     return templates.TemplateResponse(
#         "project-form.html",
#         {
#             "request": request,
#             "provider_names": provider_names,
#             "build_sha": config.BUILD_SHA,
#         },
#     )


# @app.post("/ui/project", response_class=HTMLResponse)
# async def add_project_via_ui(
#     request: Request,
#     name: str = Form(...),
#     slug: str = Form(...),
#     description: str = Form(...),
#     api_base: str = Form(...),
#     provider_name: str = Form(...),
#     ai_model_name: str = Form(...),
#     tags: str = Form(...),
#     org_id: str | None = Form(...),
# ):
#     ctx = get_transaction_context(request)
#     tags = tags.replace(" ", "").split(",")
#     data = CreateProjectSchema(
#         name=name,
#         slug=slug,
#         description=description,
#         ai_providers=[
#             ProjectAIProviderSchema(
#                 api_base=api_base,
#                 provider_name=provider_name,
#                 ai_model_name=ai_model_name,
#             )
#         ],
#         tags=tags,
#         org_id=org_id,
#     )
#     project = ctx.call(add_project, data)
# 
#     if project is None:
#         return templates.TemplateResponse(
#             "project-form.html",
#             {
#                 "request": request,
#                 "error": "Project already exists",
#                 "build_sha": config.BUILD_SHA,
#             },
#         )
#     return templates.TemplateResponse(
#         "project-form.html",
#         {
#             "request": request,
#             "project": project,
#             "success": "Project added successfully",
#             "build_sha": config.BUILD_SHA,
#         },
#     )


# @app.post("/ui/project/delete", response_class=HTMLResponse)
# async def delete_project_via_ui(request: Request, project_id: str = Form(...)):
#     ctx = get_transaction_context(request)
#     projects = ctx.call(get_all_projects)
#     deleted = ctx.call(delete_project, project_id=project_id)
# 
#     if deleted:
#         projects = ctx.call(get_all_projects)
#         return templates.TemplateResponse(
#             "dashboard.html",
#             {
#                 "request": request,
#                 "projects": projects,
#                 "success": f"Project {project_id} deleted successfully",
#                 "build_sha": config.BUILD_SHA,
#             },
#         )
#     return templates.TemplateResponse(
#         "dashboard.html",
#         {
#             "request": request,
#             "projects": projects,
#             "error": f"Project {project_id} not found",
#             "build_sha": config.BUILD_SHA,
#         },
#     )


# @app.get("/ui/project/{project_id}", response_class=HTMLResponse)
# async def read_item(request: Request, project_id: str):
#     ctx = get_transaction_context(request)
#     project = ctx.call(get_project, project_id=project_id)
#     transactions = ctx.call(get_transactions_for_project, project_id=project_id)
#     scheme, host = config.BASE_URL.split("://")
#     project_url = f"{scheme}://{project.slug}.{host}"
#     return templates.TemplateResponse(
#         "project.html",
#         {
#             "request": request,
#             "project": project,
#             "transactions": transactions,
#             "project_url": project_url,
#             "build_sha": config.BUILD_SHA,
#         },
#     )


# @app.get("/ui/project/{project_id}/update", response_class=HTMLResponse)
# async def get_project_update_form(request: Request, project_id: str):
#     ctx = get_transaction_context(request)
#     project = ctx.call(get_project, project_id=project_id)
#     provider_names = [
#         "OpenAI",
#         "Azure OpenAI",
#         "Google Palm",
#         "Anthropic Cloud",
#         "Meta LLama",
#         "HuggingFace",
#         "Custom",
#     ]
#     return templates.TemplateResponse(
#         "project-update-form.html",
#         {
#             "request": request,
#             "project": project,
#             "provider_names": provider_names,
#             "build_sha": config.BUILD_SHA,
#         },
#     )


# @app.post("/ui/project/update", response_class=HTMLResponse)
# async def update_project_via_ui(
#     request: Request,
#     proj_id: str = Form(...),
#     name: str = Form(...),
#     slug: str = Form(...),
#     description: str = Form(...),
#     api_base: str = Form(...),
#     provider_name: str = Form(...),
#     ai_model_name: str = Form(...),
#     tags: str = Form(...),
#     org_id: str | None = Form(...),
# ):
#     ctx = get_transaction_context(request)
# 
#     tags = tags.replace(" ", "").split(",")
# 
#     tags = (
#         tags[0 : len(tags) - 2] if tags[len(tags) - 1] == " " else tags
#     )  # remove empty tag if exists
#     data = GetProjectSchema(
#         id=proj_id,
#         name=name,
#         slug=slug,
#         description=description,
#         ai_providers=[
#             ProjectAIProviderSchema(
#                 api_base=api_base,
#                 provider_name=provider_name,
#                 ai_model_name=ai_model_name,
#             )
#         ],
#         tags=tags,
#         org_id=org_id,
#     )
#     updated = ctx.call(update_project, data=data)
#     if updated:
#         project = ctx.call(get_project, project_id=proj_id)
#         return templates.TemplateResponse(
#             "project-update-form.html",
#             {
#                 "request": request,
#                 "project": project,
#                 "success": "Project updated successfully",
#                 "build_sha": config.BUILD_SHA,
#             },
#         )
#     projects = ctx.call(get_all_projects)
#     return templates.TemplateResponse(
#         "dashboard.html",
#         {
#             "request": request,
#             "projects": projects,
#             "error": "Project not found",
#             "build_sha": config.BUILD_SHA,
#         },
#     )


# @app.get(
#     "/ui/project/{project_id}/transaction/{transacion_id}", response_class=HTMLResponse
# )
# async def read_sepcific_transaction(
#     request: Request, project_id: str, transacion_id: str
# ):
#     ctx = get_transaction_context(request)
#     project = ctx.call(get_project, project_id=project_id)
#     transaction = ctx.call(get_transaction, transaction_id=transacion_id)
#     scheme, host = config.BASE_URL.split("://")
#     project_url = f"{scheme}://{project_id}.{host}"
#     return templates.TemplateResponse(
#         "transaction.html",
#         {
#             "request": request,
#             "project": project,
#             "transaction": transaction,
#             "project_url": project_url,
#             "build_sha": config.BUILD_SHA,
#         },
#     )
