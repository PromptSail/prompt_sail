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
    return fastapi_instance.container.application()
    
    # TODO: make sure that database is cleared before every test
