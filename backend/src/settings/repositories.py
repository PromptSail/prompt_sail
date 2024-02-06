from seedwork.exceptions import NotFoundException
from seedwork.repositories import MongoRepository
from settings.models import OrganizationSettings
from transactions.models import Transaction


class SettingsNotFoundException(NotFoundException):
    pass


class SettingsRepository(MongoRepository):
    model_class = OrganizationSettings

    def add(self, doc):
        result = super().add(doc)
        return result
    
    def get(self, doc_id: str) -> OrganizationSettings:
        return self.find_one({"_id": doc_id})
    