import copy
import inspect
import json
import uuid
from logging import Logger
from typing import Optional
from uuid import UUID

import pymongo
from app.logging import logger, logging_context
from dependency_injector import containers, providers
from dependency_injector.containers import Container
from dependency_injector.providers import Dependency, Factory, Provider, Singleton
from dependency_injector.wiring import Provide, inject  # noqa
from lato import Application, DependencyProvider, TransactionContext
from projects.repositories import ProjectRepository
from settings.repositories import SettingsRepository
from transactions.repositories import TransactionRepository

# logger = logging.getLogger("ps")
# logger.setLevel(logging.DEBUG)
#
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.DEBUG)
# formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# console_handler.setFormatter(formatter)
# logger.addHandler(console_handler)


def resolve_provider_by_type(container: Container, cls: type) -> Optional[Provider]:
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
    import uuid

    if isinstance(val, uuid.UUID):
        return str(val)
    raise TypeError()


def dumps(d):
    return json.dumps(d, default=_default)


class ContainerProvider(DependencyProvider):
    def __init__(self, container: Container):
        self.container = container
        self.counter = 0

    def has_dependency(self, identifier: str | type) -> bool:
        if isinstance(identifier, type) and resolve_provider_by_type(
            self.container, identifier
        ):
            return True
        if type(identifier) is str:
            return identifier in self.container.providers

    def register_dependency(self, identifier, dependency_instance):
        pr = providers.Object(dependency_instance)
        try:
            setattr(self.container, identifier, pr)
        except TypeError:
            setattr(self.container, f"{str(identifier)}-{self.counter}", pr)
            self.counter += 1

    def get_dependency(self, identifier):
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
        dp = ContainerProvider(copy.copy(self.container))
        dp.update(*args, **kwargs)
        return dp


def create_application(container, **kwargs):
    application = Application(
        name="PromptSail",
        dependency_provider=ContainerProvider(container),
        **kwargs,
    )
    # application.include_module(...)
    # application.include_module(...)

    @application.on_create_transaction_context
    def on_create_transaction_context():
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
        logging_context.correlation_id = ctx["correlation_id"]
        logger.debug(f"transaction started")

    @application.on_exit_transaction_context
    def on_exit_transaction_context(ctx: TransactionContext, exception):
        logger.debug(f"transaction ended ")
        logging_context.correlation_id = None

    # @application.transaction_middleware
    # def null_middleware(ctx: TransactionContext, call_next):
    #     result = call_next()
    #     return result

    return application


class TopLevelContainer(containers.DeclarativeContainer):
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


class TransactionContainer(containers.DeclarativeContainer):
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
    settings_repository = providers.Singleton(
        SettingsRepository, db_client=db_client, collection_name="settings"
    )
