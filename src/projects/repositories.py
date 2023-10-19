from projects.models import Project
from seedwork.exceptions import NotFoundException
from seedwork.repositories import MongoRepository


class ProjectNotFoundException(NotFoundException):
    pass


class ProjectRepository(MongoRepository):
    model_class = Project
