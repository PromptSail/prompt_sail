from auth.models import User
from auth.repositories import UserRepository


def get_user(external_id: str, user_repository: UserRepository) -> User:
    """
    Retrieve a user by its unique external identifier.

    :param external_id: The unique external identifier of the user to be retrieved.
    :param user_repository: An instance of UserRepository used for accessing user data.
    :return: The User object corresponding to the specified identifier.
    """
    user = user_repository.get_by_external_id(external_id)
    return user


def get_local_user(user_id: str, user_repository: UserRepository) -> User:
    """
    Retrieve a user by its unique internal identifier.

    :param user_id: The unique internal identifier of the user to be retrieved.
    :param user_repository: An instance of UserRepository used for accessing user data.
    :return: The User object corresponding to the specified identifier.
    """
    user = user_repository.get(doc_id=user_id)
    return user


def add_user(user: User, user_repository: UserRepository) -> User:
    """
    Add a new user to the repository.

    :param user: The User object to be added.
    :param user_repository: An instance of UserRepository used for storing user data.
    :return: The newly added User object.
    """
    user_repository.add(user)
    return user


def get_all_users(user_repository: UserRepository) -> list[User]:
    """
    Retrieve all users.

    :param user_repository: An instance of UserRepository used for accessing user data.
    :return: The list of User objects.
    """
    users = user_repository.get_all()
    return users


def check_if_email_exists(user_email: str, user_repository: UserRepository) -> bool:
    """
    Retrieve information whether a user with such an email exists.

    :param user_email: String representing user email.
    :param user_repository: An instance of UserRepository used for accessing user data.
    :return: Boolean value.
    """
    count = user_repository.count({"email": user_email})
    return count == 1


def activate_user(user_id: str, user_repository: UserRepository) -> User:
    """
    Activate user account.

    :param user_id: The unique identifier of the user to be activated.
    :param user_repository: An instance of UserRepository used for accessing user data.
    :return: The updated User object.
    """
    user = user_repository.get(doc_id=user_id)
    user.__dict__.update(is_active=True)
    user_repository.update(user)
    return user
