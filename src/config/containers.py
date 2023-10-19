import inspect
import json
import logging
import uuid
from logging import Logger
from typing import Optional
from uuid import UUID

import pymongo
from dependency_injector import containers, providers
from dependency_injector.containers import Container
from dependency_injector.providers import Dependency, Factory, Provider, Singleton
from dependency_injector.wiring import Provide, inject  # noqa

from projects.repositories import ProjectRepository
from seedwork.application import Application, DependencyProvider, TransactionContext
from transactions.repositories import TransactionRepository

logger = logging.getLogger("ps")
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


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


class IocProvider(DependencyProvider):
    def __init__(self, container):
        self.container = container

    def register_dependency(self, identifier, dependency_instance):
        setattr(self.container, identifier, providers.Object(dependency_instance))

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


def create_application(**kwargs):
    application = Application(
        "PromptSail",
        0.1,
        **kwargs,
    )
    # application.include_module(...)
    # application.include_module(...)

    @application.on_enter_transaction_context
    def on_enter_transaction_context(ctx: TransactionContext):
        correlation_id = uuid.uuid4()
        logger = ctx.app.dependency_provider["logger"]
        transaction_container = TransactionContainer(
            correlation_id=correlation_id, logger=logger
        )
        tlc = ctx.app.dependency_provider["container"]
        transaction_container.tlc.override(tlc)
        ctx.dependency_provider = IocProvider(transaction_container)
        logger.debug(f"transaction started")

    @application.on_exit_transaction_context
    def on_exit_transaction_context(ctx: TransactionContext, exc_type, exc_val, exc_tb):
        ctx["logger"].debug(f"transaction ended ")

    @application.transaction_middleware
    def null_middleware(ctx: TransactionContext, call_next):
        result = call_next()
        return result

    return application


class TopLevelContainer(containers.DeclarativeContainer):
    __self__ = providers.Self()
    config = providers.Configuration()
    logger = providers.Object(logger)
    db_client = providers.Singleton(
        lambda config: pymongo.MongoClient(config["MONGO_URL"]).get_database(
            "prompt_sail"
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
    tlc = providers.Container(
        TopLevelContainer,
    )
    project_repository = providers.Singleton(
        ProjectRepository, db_client=tlc.db_client, collection_name="projects"
    )
    transaction_repository = providers.Singleton(
        TransactionRepository, db_client=tlc.db_client, collection_name="transactions"
    )
