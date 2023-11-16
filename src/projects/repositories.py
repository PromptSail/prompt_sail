from projects.models import Project
from seedwork.exceptions import NotFoundException
from seedwork.repositories import MongoRepository
from utils import deserialize_data


class ProjectNotFoundException(NotFoundException):
    pass


class ProjectRepository(MongoRepository):
    model_class = Project

    def add(self, doc):
        result = super().add(doc)
        return result

    def update(self, doc):
        result = super().update(doc)
        return result

    def find_one(self, filter_by=None):
        data = self._collection.find_one(filter_by or {})
        if data is None:
            return None
        return self.model_class(**deserialize_data(data))
