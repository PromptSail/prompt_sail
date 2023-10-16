from pydantic import BaseModel, Field
from config import config


class Project(BaseModel):
    id: str = Field(default_factory=str)
    api_base: str = Field(default_factory=str)


class ProjectNotFoundException(Exception):
    pass


class ProjectRepository:
    def __init__(self):
        self._projects = {}

    def add(self, project: Project):
        self._projects[project.id] = project

    def get(self, project_id: str) -> Project:
        try:
            return self._projects[project_id]
        except KeyError:
            raise ProjectNotFoundException(project_id)


project_repository = ProjectRepository()
project_repository.add(Project(id="project1", api_base="https://api.openai.com/v1"))
project_repository.add(Project(id="project2", api_base="https://api.openai.com/v1"))
