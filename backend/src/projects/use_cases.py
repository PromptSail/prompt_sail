from app.messages import (
    DeleteProject,
    GetAllProjects,
    GetProject,
    GetProjectBySlug,
    ProjectWasDeleted,
)
from lato import TransactionContext
from projects.models import Project
from projects.repositories import ProjectRepository

from projects import projects


@projects.handler(GetProject)
def get_project(
    query: GetProject,
    project_repository: ProjectRepository,
) -> dict:
    project = project_repository.find_one({"_id": query.project_id})
    return project.model_dump()


@projects.handler(GetProjectBySlug)
def get_project_by_slug(
    query: GetProjectBySlug,
    project_repository: ProjectRepository,
) -> Project:
    project = project_repository.get_by_slug(query.slug)
    return project


@projects.handler(GetAllProjects)
def get_all_projects(
    query: GetAllProjects, project_repository: ProjectRepository
) -> list[Project]:
    projects = project_repository.get_all()
    return projects


def add_project(
    project: Project,
    project_repository: ProjectRepository,
) -> Project:
    project_repository.add(project)
    return project


def update_project(
    project_repository: ProjectRepository, project_id: str, fields_to_update: dict
) -> Project:
    project = project_repository.get(project_id)
    project.__dict__.update(**fields_to_update)
    project_repository.update(project)
    return project


@projects.handler(DeleteProject)
def delete_project(
    command: DeleteProject,
    project_repository: ProjectRepository,
    ctx: TransactionContext,
) -> None:
    project_repository.delete(command.project_id)
    ctx.emit(ProjectWasDeleted(project_id=command.project_id))
