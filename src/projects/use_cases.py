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
    project = project_repository.find_one({"slug": slug})
    return project


def get_all_projects(
    project_repository: ProjectRepository
) -> list[Project]:
    projects = project_repository.get_all()
    return projects


def add_project(
    data: CreateProjectSchema,
    project_repository: ProjectRepository,
) -> Project | None:
    if project_repository.find_one({"slug": data.slug}):
        return None
    data = Project(**data.model_dump())
    project = project_repository.add(data)
    return project


def update_project(
    data: UpdateProjectSchema, 
    project_repository: ProjectRepository
) -> bool:
    update_result = project_repository.update(data)
    if update_result.modified_count == 0:
        return False
    return True


def delete_project(
    project_id: str,
    project_repository: ProjectRepository,
) -> bool:
    delete_result = project_repository.delete(project_id)
    if delete_result.deleted_count == 0:
        return False
    return True
