from organization.models import Organization
from seedwork.exceptions import NotFoundException
from seedwork.repositories import MongoRepository


class OrganizationNotFoundException(NotFoundException):
    """
    Exception raised when an organization is not found.
    """


class OrganizationRepository(MongoRepository):
    """
    Repository for managing and accessing organization data.

    Inherits from MongoRepository and is specific to the Organization model.
    """

    model_class = Organization

    def add(self, doc):
        """
        Add an organization document to the repository.

        :param doc: The Organization object to be added.
        :return: The result of the add operation.
        """
        result = super().add(doc)
        return result

    def update(self, doc) -> Organization:
        """
        Update an organization document in the repository.

        :param doc: The Organization object to be updated.
        :raise OrganizationNotFoundException: If the organization with the specified identifier is not found.
        :return: The result of the update operation.
        """
        if self.count({"_id": doc.id}) == 0:
            raise OrganizationNotFoundException(f"Organization not found: {doc.id}")
        result = super().update(doc)
        return result

    def get(self, doc_id: str) -> Organization:
        """
        Retrieve an organization by its unique identifier.

        :param doc_id: The unique identifier of the organization to be retrieved.
        :return: The Organization object corresponding to the specified identifier.
        """
        organization = super().get(doc_id)
        return Organization(**organization.model_dump())
