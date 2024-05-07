from auth.models import User
from seedwork.exceptions import AlreadyExistsException, NotFoundException
from seedwork.repositories import MongoRepository


class UserNotFoundException(NotFoundException):
    """
    Exception raised when a user is not found.
    """


class UserAlreadyExistsException(AlreadyExistsException):
    """
    Exception raised when a user already exists in database.
    """


class UserRepository(MongoRepository):
    """
    Repository for managing and accessing project data.

    Inherits from MongoRepository and is specific to the Project model.
    """

    model_class = User

    def add(self, doc):
        """
        Add a project document to the repository.

        :param doc: The Project object to be added.
        :raise SlugAlreadyExistsException: If the slug already exists in the repository.
        :return: The result of the add operation.
        """
        if self.count({"_id": doc.id}) > 0:
            raise UserAlreadyExistsException(f"Slug already exists: {doc.slug}")
        result = super().add(doc)
        return result

    def update(self, doc) -> User:
        """
        Update a project document in the repository.

        :param doc: The Project object to be updated.
        :raise SlugAlreadyExistsException: If the updated slug already exists in the repository.
        :raise ProjectNotFoundException: If the project with the specified identifier is not found.
        :return: The result of the update operation.
        """
        if self.count({"_id": doc.id}) == 0:
            raise UserNotFoundException(f"User with id: {doc.id} not found.")
        result = super().update(doc)
        return result

    def get(self, doc_id: str) -> User | None:
        """
        Retrieve a project by its unique identifier.

        :param doc_id: The unique identifier of the project to be retrieved.
        :return: The Project object corresponding to the specified identifier.
        """
        if self.count({"_id": doc_id}) == 0:
            raise UserNotFoundException(f"User with id: {doc_id} not found.")
        user = super().get(doc_id)
        return User(**user.model_dump())
    
    def get_by_external_id(self, external_id: str) -> User | None:
        """
        Retrieve a project by its unique external identifier.

        :param external_id: The unique external identifier of the project to be retrieved.
        :return: The Project object corresponding to the specified identifier.
        """
        if self.count({"external_id": external_id}) == 0:
            return None
        user = super().find_one({"external_id": external_id})
        return User(**user.model_dump())
    
