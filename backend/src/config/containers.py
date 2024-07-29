import copy
import inspect
import json
import uuid
from logging import Logger
from typing import Optional
from uuid import UUID

import pymongo
from app.logging import logger, logging_context
from auth.repositories import UserRepository
from dependency_injector import containers, providers
from dependency_injector.containers import Container
from dependency_injector.providers import Dependency, Factory, Provider, Singleton
from dependency_injector.wiring import Provide, inject  # noqa
from lato import Application, DependencyProvider, TransactionContext
from organization.repositories import OrganizationRepository
from projects.repositories import ProjectRepository
from raw_transactions.repositories import RawTransactionRepository
from settings.repositories import SettingsRepository
from transactions.repositories import TransactionRepository
from user_credentials.repositories import UserCredentialRepository
from utils import read_provider_pricelist

# logger = logging.getLogger("ps")
# logger.setLevel(logging.DEBUG)
#
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.DEBUG)
# formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# console_handler.setFormatter(formatter)
# logger.addHandler(console_handler)


def resolve_provider_by_type(container: Container, cls: type) -> Optional[Provider]:
    """
    Resolve a provider from the container based on the specified type.

    :param container: The dependency injection container.
    :param cls: The type for which to resolve a provider.
    :return: The resolved Provider object, or None if no matching provider is found.
    :raises ValueError: If multiple matching providers are found.
    """

    def inspect_provider(provider: Provider) -> bool:
        if isinstance(provider, (Factory, Singleton)):
            return issubclass(provider.cls, cls)
        elif isinstance(provider, Dependency):
            return issubclass(provider.instance_of, cls)

        return False

    matching_providers = inspect.getmembers(
        container,
        inspect_provider,
    )
    if matching_providers:
        if len(matching_providers) > 1:
            raise ValueError(
                f"Cannot uniquely resolve {cls}. Found {len(providers)} matching resources."
            )
        return matching_providers[0][1]
    return None


def _default(val):
    """
    Convert a value to its default representation.

    Handles the conversion of UUID objects to strings.

    :param val: The value to be converted.
    :return: The default representation of the value.
    :raises TypeError: If the value is not of a supported type.
    """
    import uuid

    if isinstance(val, uuid.UUID):
        return str(val)
    raise TypeError()


def dumps(d):
    """
    Serialize a Python object to a JSON-formatted string.

    :param d: The Python object to be serialized.
    :return: A JSON-formatted string representing the serialized object.
    """
    return json.dumps(d, default=_default)


class ContainerProvider(DependencyProvider):
    """
    Dependency provider for integrating a dependency injection container.

    This provider interacts with the specified container to manage dependencies.
    """

    def __init__(self, container: Container):
        """
        Initialize the ContainerProvider with a dependency injection container.

        :param container: The dependency injection container.
        """
        self.container = container
        self.counter = 0

    def has_dependency(self, identifier: str | type) -> bool:
        """
        Check if the container has a dependency identified by the specified identifier.

        :param identifier: The identifier (either a string or a type) of the dependency.
        :return: True if the dependency is found, False otherwise.
        """
        if isinstance(identifier, type) and resolve_provider_by_type(
            self.container, identifier
        ):
            return True
        if type(identifier) is str:
            return identifier in self.container.providers

    def register_dependency(self, identifier, dependency_instance):
        """
        Register a dependency in the container.

        :param identifier: The identifier for the dependency.
        :param dependency_instance: The instance of the dependency to be registered.
        """
        pr = providers.Object(dependency_instance)
        try:
            setattr(self.container, identifier, pr)
        except TypeError:
            setattr(self.container, f"{str(identifier)}-{self.counter}", pr)
            self.counter += 1

    def get_dependency(self, identifier):
        """
        Get the instance of a dependency from the container.

        :param identifier: The identifier of the dependency to be retrieved.
        :return: The instance of the dependency.
        """
        try:
            if isinstance(identifier, type):
                provider = resolve_provider_by_type(self.container, identifier)
            else:
                provider = getattr(self.container, identifier)
            instance = provider()
        except Exception as e:
            raise e
        return instance

    def copy(self, *args, **kwargs):
        """
        Create a copy of the ContainerProvider with updated parameters.

        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        :return: A new instance of ContainerProvider with updated parameters.
        """
        dp = ContainerProvider(copy.copy(self.container))
        dp.update(*args, **kwargs)
        return dp


def create_application(container, **kwargs):
    """
    Create and configure an application with a dependency injection container.

    :param container: The dependency injection container.
    :param kwargs: Additional keyword arguments for configuring the application.
    :return: An instance of the configured Application.
    """
    application = Application(
        name="PromptSail",
        dependency_provider=ContainerProvider(container),
        **kwargs,
    )
    # application.include_module(...)
    # application.include_module(...)

    @application.on_create_transaction_context
    def on_create_transaction_context():
        """
        Event handler for creating a transaction context.

        :return: A new TransactionContext.
        """
        correlation_id = uuid.uuid4()
        transaction_level_container = TransactionContainer(
            correlation_id=correlation_id,
            logger=logger,
            db_client=container.db_client,
            app=application,
        )
        transaction_level_provider = ContainerProvider(transaction_level_container)
        return TransactionContext(dependency_provider=transaction_level_provider)

    @application.on_enter_transaction_context
    def on_enter_transaction_context(ctx: TransactionContext):
        """
        Event handler for entering a transaction context.

        :param ctx: The TransactionContext.
        """
        logging_context.correlation_id = ctx["correlation_id"]
        logger.debug(f"transaction started")

    @application.on_exit_transaction_context
    def on_exit_transaction_context(ctx: TransactionContext, exception):
        """
        Event handler for exiting a transaction context.

        :param ctx: The TransactionContext.
        :param exception: The exception (if any) that occurred during the transaction.
        """
        logger.debug(f"transaction ended ")
        logging_context.correlation_id = None

    # @application.transaction_middleware
    # def null_middleware(ctx: TransactionContext, call_next):
    #     result = call_next()
    #     return result

    return application


class TopLevelContainer(containers.DeclarativeContainer):
    """
    Top-level dependency injection container for the application.

    Inherits from containers.DeclarativeContainer.
    """

    __self__ = providers.Self()
    config = providers.Configuration()
    logger = providers.Object(logger)
    db_client = providers.Singleton(
        lambda config: pymongo.MongoClient(config.MONGO_URL).get_database(
            config.DATABASE_NAME
        ),
        config=config,
    )
    application: Application = providers.Singleton(
        create_application,
        db_client=db_client,
        logger=logger,
        container=__self__,
    )
    provider_pricelist = providers.Singleton(read_provider_pricelist)


class TransactionContainer(containers.DeclarativeContainer):
    """
    Dependency injection container for managing dependencies related to transactions.

    Inherits from containers.DeclarativeContainer.
    """

    correlation_id = providers.Dependency(instance_of=UUID)
    logger = providers.Dependency(instance_of=Logger)
    db_client = providers.Dependency(instance_of=pymongo.database.Database)
    app = providers.Dependency(instance_of=Application)

    project_repository = providers.Singleton(
        ProjectRepository, db_client=db_client, collection_name="projects"
    )
    transaction_repository = providers.Singleton(
        TransactionRepository, db_client=db_client, collection_name="transactions"
    )
    raw_transaction_repository = providers.Singleton(
        RawTransactionRepository,
        db_client=db_client,
        collection_name="raw_transactions",
    )
    settings_repository = providers.Singleton(
        SettingsRepository, db_client=db_client, collection_name="settings"
    )
    user_repository = providers.Singleton(
        UserRepository, db_client=db_client, collection_name="users"
    )
    user_credential_repository = providers.Singleton(
        UserCredentialRepository,
        db_client=db_client,
        collection_name="user_credentials",
    )
    organization_repository = providers.Singleton(
        OrganizationRepository, db_client=db_client, collection_name="organizations"
    )
