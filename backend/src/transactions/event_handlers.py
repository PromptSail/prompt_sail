from app.messages import ProjectWasDeleted
from lato import TransactionContext

from transactions import transactions


@transactions.on(ProjectWasDeleted)
def on_project_was_deleted(event: ProjectWasDeleted, ctx: TransactionContext):
    print(f"Project {event.project_id} was deleted")
    # TODO: delete transactions
    # transaction_repository.remove(...)
