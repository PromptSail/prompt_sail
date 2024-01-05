from datetime import datetime

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

    def get_one_by_id(self, transaction_id: str) -> Transaction:
        return self.find_one({"_id": transaction_id})

    def get_paginated_and_filtered(
        self, 
        page: int, 
        page_size: int, 
        query: dict[str, str | datetime | None] = None
    ) -> list[Transaction]:
        return self.find(query)[
            (page - 1) * page_size : (page - 1) * page_size + page_size
        ][::-1]
