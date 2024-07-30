from projects.models import Project
from seedwork.exceptions import AlreadyExistsException, NotFoundException
from seedwork.repositories import MongoRepository


class ProjectNotFoundException(NotFoundException):
    """
    Exception raised when a project is not found.
    """


class SlugAlreadyExistsException(AlreadyExistsException):
    """
    Exception raised when a slug already exists for a project.
    """


class ProjectRepository(MongoRepository):
    """
    Repository for managing and accessing project data.

    Inherits from MongoRepository and is specific to the Project model.
    """

    model_class = Project

    def add(self, doc):
        """
        Add a project document to the repository.

        :param doc: The Project object to be added.
        :raise SlugAlreadyExistsException: If the slug already exists in the repository.
        :return: The result of the add operation.
        """
        if self.count({"slug": doc.slug, "org_id": doc.org_id}) > 0:
            raise SlugAlreadyExistsException(f"Slug already exists: {doc.slug}")
        result = super().add(doc)
        return result

    def update(self, doc) -> Project:
        """
        Update a project document in the repository.

        :param doc: The Project object to be updated.
        :raise SlugAlreadyExistsException: If the updated slug already exists in the repository.
        :raise ProjectNotFoundException: If the project with the specified identifier is not found.
        :return: The result of the update operation.
        """
        same_slug = [p for p in self.find({"slug": doc.slug}) if p.id != doc.id]
        if len(same_slug) > 0:
            raise SlugAlreadyExistsException(f"Slug already exists: {doc.slug}")
        if self.count({"_id": doc.id}) == 0:
            raise ProjectNotFoundException(f"Project not found: {doc.id}")
        result = super().update(doc)
        return result

    def get(self, doc_id: str) -> Project:
        """
        Retrieve a project by its unique identifier.

        :param doc_id: The unique identifier of the project to be retrieved.
        :return: The Project object corresponding to the specified identifier.
        """
        project = super().get(doc_id)
        return Project(**project.model_dump())

    def get_by_organization_and_slug(self, slug: str, org_id: str) -> Project:
        """
        Retrieve a project by its slug.

        :param slug: The unique slug of the project to be retrieved.
        :param: org_id: The unique organization id.
        :return: The Project object corresponding to the specified slug.
        """
        return self.find_one({"slug": slug, "org_id": org_id})
