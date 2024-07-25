from seedwork.exceptions import AlreadyExistsException, NotFoundException
from seedwork.repositories import MongoRepository
from user_credentials.models import UserCredential


class UserCredentialNotFoundException(NotFoundException):
    """
    Exception raised when a user is not found.
    """

    ...


class UserCredentialAlreadyExistsException(AlreadyExistsException):
    """
    Exception raised when a user already exists in database.
    """

    ...


class UserCredentialRepository(MongoRepository):
    """
    Repository for managing and accessing project data.

    Inherits from MongoRepository and is specific to the Project model.
    """

    model_class = UserCredential

    def add(self, doc):
        """
        Add a user credential document to the repository.

        :param doc: The UserCredential object to be added.
        :raise UserCredentialAlreadyExistsException: If the credential with that username already exists in the repository.
        :return: The result of the add operation.
        """
        if self.count({"user_id": doc.user_id}) > 0:
            raise UserCredentialAlreadyExistsException(
                f"Credential for that user_id already exists: {doc.user_id}"
            )
        result = super().add(doc)
        return result

    def update(self, doc) -> UserCredential:
        """
        Update a user credential document in the repository.

        :param doc: The UserCredential object to be updated.
        :raise UserCredentialNotFoundException: If the credential with the specified identifier is not found.
        :return: The result of the update operation.
        """
        if self.count({"_id": doc.id}) == 0:
            raise UserCredentialNotFoundException(
                f"UserCredential with id: {doc.id} not found."
            )
        result = super().update(doc)
        return result

    def get(self, doc_id: str) -> UserCredential | None:
        """
        Retrieve a user credential by its unique identifier.

        :param doc_id: The unique identifier of the credential to be retrieved.
        :return: The UserCredential object corresponding to the specified identifier.
        """
        if self.count({"_id": doc_id}) == 0:
            raise UserCredentialNotFoundException(
                f"UserCredential with id: {doc_id} not found."
            )
        user = super().get(doc_id)
        return UserCredential(**user.model_dump())

    def get_by_user_id(self, user_id: str) -> UserCredential | None:
        """
        Retrieve a user credential by its unique username.

        :param user_id: The unique username of the credential to be retrieved.
        :return: The UserCredential object corresponding to the specified username.
        """
        if self.count({"user_id": user_id}) == 0:
            raise UserCredentialNotFoundException(
                f"UserCredential with user_id: {user_id} not found."
            )
        user = super().find({"user_id": user_id})[0]
        return UserCredential(**user.model_dump())
