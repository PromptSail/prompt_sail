from lato import Event, Task


class GetProject(Task):
    project_id: str
    include_transactions: bool = True


class GetProjectBySlug(Task):
    slug: str


class GetAllProjects(Task):
    pass


class DeleteProject(Task):
    project_id: str


class ProjectWasDeleted(Event):
    project_id: str
