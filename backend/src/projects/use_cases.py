from projects.models import Project
from projects.repositories import ProjectRepository


def get_project(
    project_id: str,
    project_repository: ProjectRepository,
) -> Project:
    """
    Retrieve a project by its unique identifier.

    :param project_id: The unique identifier of the project to be retrieved.
    :param project_repository: An instance of ProjectRepository used for accessing project data.
    :return: The Project object corresponding to the specified identifier.
    """
    project = project_repository.find_one({"_id": project_id})
    return project


def get_project_by_slug(
    slug: str,
    project_repository: ProjectRepository,
) -> Project:
    """
    Retrieve a project by its slug.

    :param slug: The unique slug of the project to be retrieved.
    :param project_repository: An instance of ProjectRepository used for accessing project data.
    :return: The Project object corresponding to the specified slug.
    """
    project = project_repository.get_by_slug(slug)
    return project


def get_all_projects(project_repository: ProjectRepository) -> list[Project]:
    """
    Retrieve a list of all projects.

    :param project_repository: An instance of ProjectRepository used for accessing project data.
    :return: A list of all Project objects stored in the repository.
    """
    projects = project_repository.get_all()
    return projects


def add_project(
    project: Project,
    project_repository: ProjectRepository,
) -> Project:
    """
    Add a new project to the repository.

    :param project: The Project object to be added.
    :param project_repository: An instance of ProjectRepository used for storing project data.
    :return: The newly added Project object.
    """
    project_repository.add(project)
    return project


def update_project(
    project_repository: ProjectRepository, project_id: str, fields_to_update: dict
) -> Project:
    """
    Update a project with specified fields.

    :param project_repository: An instance of ProjectRepository used for accessing project data.
    :param project_id: The unique identifier of the project to be updated.
    :param fields_to_update: A dictionary containing the fields and values to update in the project.
    :return: The updated Project object.
    """
    project = project_repository.get(project_id)
    project.__dict__.update(**fields_to_update)
    project_repository.update(project)
    return project


def delete_project(
    project_id: str,
    project_repository: ProjectRepository,
) -> None:
    """
    Delete a project and associated data.

    :param project_id: The unique identifier of the project to be deleted.
    :param project_repository: An instance of ProjectRepository used for accessing project data.
    :return: None
    """
    project_repository.delete(project_id)


def count_projects(project_repository: ProjectRepository) -> int:
    return project_repository.count()
