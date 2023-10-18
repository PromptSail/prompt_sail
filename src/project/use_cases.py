from project.models import Project
from project.repositories import ProjectRepository


def get_project(
    project_id: str,
    project_repository: ProjectRepository,
) -> Project:
    project = project_repository.get(project_id)
    return project
