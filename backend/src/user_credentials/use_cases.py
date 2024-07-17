from user_credentials.models import UserCredential
from user_credentials.repositories import UserCredentialRepository


def get_user_credential(
    username: str, credential_repository: UserCredentialRepository
) -> UserCredential:
    """
    Retrieve a user credential by its unique external identifier.

    :param username: The unique username of the user credential to be retrieved.
    :param credential_repository: An instance of UserCredentialRepository used for accessing user data.
    :return: The UserCredential object corresponding to the specified username.
    """
    user = credential_repository.get_by_username(username)
    return user


def add_user_credential(
    user_credential: UserCredential, credential_repository: UserCredentialRepository
) -> UserCredential:
    """
    Add a new user credential to the repository.

    :param user_credential: The UserCredential object to be added.
    :param credential_repository: An instance of UserCredentialRepository used for storing user credential data.
    :return: The newly added UserCredential object.
    """
    credential = credential_repository.add(user_credential)
    return credential


def check_if_username_exists(
    username: str, credential_repository: UserCredentialRepository
) -> bool:
    """
    Retrieve information whether a user credential with such a username exists.

    :param username: String representing user credential username.
    :param credential_repository: An instance of UserCredentialRepository used for accessing user credential data.
    :return: Boolean value.
    """
    count = credential_repository.count({"username": username})
    return count > 0
