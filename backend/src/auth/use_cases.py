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
