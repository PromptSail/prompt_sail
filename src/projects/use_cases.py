from projects.models import Project
from projects.repositories import ProjectRepository
from projects.schemas import CreateProjectSchema, UpdateProjectSchema


def get_project(
    project_id: str,
    project_repository: ProjectRepository,
) -> Project:
    project = project_repository.get(project_id)
    return project


def get_project_by_slug(
    slug: str,
    project_repository: ProjectRepository,
) -> Project:
    project = project_repository.get_by_slug(slug)
    return project


def get_all_projects(
    project_repository: ProjectRepository
) -> list[Project]:
    projects = project_repository.get_all()
    return projects


def add_project(
    data: CreateProjectSchema,
    project_repository: ProjectRepository,
) -> Project:
    data = Project(**data.model_dump())
    project_repository.add(data)
    project = project_repository.get_by_slug(data.slug)
    return project

def update_project(
    data: UpdateProjectSchema, 
    project_repository: ProjectRepository
) -> Project:
    project_repository.update(data)
    project = project_repository.get(data.id)
    return project

def delete_project(
    project_id: str,
    project_repository: ProjectRepository,
) -> dict:
    project_repository.delete(project_id)
    return {}
