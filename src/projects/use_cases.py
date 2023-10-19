from projects.models import Project
from projects.repositories import ProjectRepository


def get_project(
    project_id: str,
    project_repository: ProjectRepository,
) -> Project:
    project = project_repository.get(project_id)
    return project
