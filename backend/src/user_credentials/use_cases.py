from user_credentials.models import UserCredential
from user_credentials.repositories import UserCredentialRepository


def get_user_credential(
    user_id: str, credential_repository: UserCredentialRepository
) -> UserCredential:
    """
    Retrieve a user credential by its unique external identifier.

    :param user_id: The unique user_id of the user credential to be retrieved.
    :param credential_repository: An instance of UserCredentialRepository used for accessing user data.
    :return: The UserCredential object corresponding to the specified username.
    """
    user = credential_repository.get_by_user_id(user_id)
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


def update_user_credential_password(
    credential_id: str, password: str, credential_repository: UserCredentialRepository
) -> UserCredential:
    """

    :param credential_id: The unique credential_id of object to be retrieved.
    :param password: The new password hash.
    :param credential_repository: An instance of UserCredentialRepository used for storing user credential data.
    :return: The updated UserCredential object.
    """
    credential = credential_repository.get(credential_id)
    credential.__dict__.update(password=password)
    credential_repository.update(credential)
    return credential
