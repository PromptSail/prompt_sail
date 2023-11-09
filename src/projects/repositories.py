from projects.models import Project
from seedwork.exceptions import NotFoundException
from seedwork.repositories import MongoRepository


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

    def get_one_by_id(self, project_id: str) -> Project:
        return self.find_one({"_id": project_id})

    def get_one_by_snippet(self, project_snippet: str) -> Project:
        return self.find({"snippet": project_snippet})
