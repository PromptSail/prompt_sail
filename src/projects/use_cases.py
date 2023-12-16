from projects.models import Project
from projects.repositories import ProjectRepository
from projects.schemas import CreateProjectSchema, UpdateProjectSchema


def get_project(
    project_id: str,
    project_repository: ProjectRepository,
) -> Project:
    project = project_repository.find_one({"_id": project_id})
    return project


def get_project_by_slug(
    slug: str,
    project_repository: ProjectRepository,
) -> Project:
    project = project_repository.get_by_slug(slug)
    return project


def get_all_projects(project_repository: ProjectRepository) -> list[Project]:
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


def delete_project(
    project_id: str,
    project_repository: ProjectRepository,
) -> None:
    project_repository.delete(project_id)
