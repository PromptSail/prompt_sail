from seedwork.exceptions import NotFoundException
from seedwork.repositories import MongoRepository
from settings.models import OrganizationSettings


class SettingsNotFoundException(NotFoundException):
    """
    Exception raised when organization settings are not found.
    """
    pass


class SettingsRepository(MongoRepository):
    """
    Repository for managing and accessing organization settings.
    
    Inherits from MongoRepository and is specific to the OrganizationSettings model.
    """
    model_class = OrganizationSettings

    def add(self, doc):
        """
        Add organization settings to the repository.

        :param doc: The OrganizationSettings object to be added.
        :return: The result of the add operation.
        """
        result = super().add(doc)
        return result

    def get(self, doc_id: str) -> OrganizationSettings:
        """
        Retrieve organization settings by its unique identifier.

        :param doc_id: The unique identifier of the organization settings to retrieve.
        :return: The OrganizationSettings object corresponding to the specified identifier.
        """
        return self.find_one({"_id": doc_id})
