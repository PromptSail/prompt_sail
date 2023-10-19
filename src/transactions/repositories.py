from seedwork.exceptions import NotFoundException
from seedwork.repositories import MongoRepository
from transactions.models import Transaction


class TransactionNotFoundException(NotFoundException):
    pass


class TransactionRepository(MongoRepository):
    model_class = Transaction

    def add(self, doc):
        result = super().add(doc)
        return result

    def get_for_project(self, project_id: str) -> list[Transaction]:
        return self.find({"project_id": project_id})
