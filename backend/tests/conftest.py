import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def test_config():
    from config import config

    return config


@pytest.fixture
def fastapi_instance(test_config):
    from app.app import app

    return app


@pytest.fixture
def client(fastapi_instance):
    return TestClient(fastapi_instance)


@pytest.fixture
def application(fastapi_instance):
    app = fastapi_instance.container.application()
    for collection in app["db_client"].list_collection_names():
        app["db_client"][collection].drop()

    # with app.transaction_context() as ctx:
    #     ctx["project_repository"].remove_all()
    #     ctx["transaction_repository"].remove_all()

    return app
