from projects.models import Project
from seedwork.exceptions import AlreadyExistsException, NotFoundException
from seedwork.repositories import MongoRepository


class ProjectNotFoundException(NotFoundException):
    pass


class SlugAlreadyExistsException(AlreadyExistsException):
    pass


class ProjectRepository(MongoRepository):
    model_class = Project

    def add(self, doc):
        if self.count({"slug": doc.slug}) > 0:
            raise SlugAlreadyExistsException(f"Slug already exists: {doc.slug}")
        result = super().add(doc)
        return result

    def update(self, doc) -> Project:
        same_slug = [p for p in self.find({"slug": doc.slug}) if p.id != doc.id]
        if len(same_slug) > 0:
            raise SlugAlreadyExistsException(f"Slug already exists: {doc.slug}")
        if self.count({"_id": doc.id}) == 0:
            raise ProjectNotFoundException(f"Project not found: {doc.id}")
        result = super().update(doc)
        return result

    def get(self, doc_id: str) -> Project:
        project = super().get(doc_id)
        return Project(**project.model_dump())

    def get_by_slug(self, slug: str) -> Project:
        return self.find_one({"slug": slug})
