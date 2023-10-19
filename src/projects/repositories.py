from projects.models import Project


class ProjectNotFoundException(Exception):
    pass


class ProjectRepository:
    def __init__(self):
        self._projects = {}
        self.add(
            Project(
                id="project1", name="Project 1", api_base="https://api.openai.com/v1"
            )
        )
        self.add(
            Project(
                id="project2", name="Project 2", api_base="https://api.openai.com/v1"
            )
        )

    def add(self, project: Project):
        self._projects[project.id] = project

    def get(self, project_id: str) -> Project:
        try:
            return self._projects[project_id]
        except KeyError:
            raise ProjectNotFoundException(project_id)

    def get_all(self):
        return self._projects.values()
