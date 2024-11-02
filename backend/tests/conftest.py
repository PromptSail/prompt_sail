import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timezone
from projects.models import Project, AIProvider
from test_utils import read_transactions_from_csv


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


@pytest.fixture
def test_project(application):
    """Create a default test project for API tests."""
    with application.transaction_context() as ctx:
        project = Project(
            id="project-test",
            name="Autotest",
            slug="autotest1",
            description="Project 1 description",
            ai_providers=[
                AIProvider(
                    deployment_name="openai",
                    slug="openai",
                    api_base="https://api.openai.com/v1",
                    description="New test project",
                    provider_name="provider1",
                )
            ],
            tags=["test", "api-test"],
            org_id="test-organization",
            owner="test@example.com"
        )
        
        repo = ctx["project_repository"]
        repo.add(project)
        
        yield project
        
        # Use delete instead of delete_cascade
        repo.delete(project.id)


@pytest.fixture
def test_project_id(test_project):
    """Helper fixture to get just the project ID"""
    return test_project.id


@pytest.fixture
def test_transactions_count(application):
    """Fixture to load and store test transactions"""
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv("test_transactions.csv")
        for transaction in transactions:
            repo.add(transaction)
        yield transactions
        repo.remove_all()


@pytest.fixture(autouse=True)
def clean_database(application):
    """Automatically clean database before each test"""
    for collection in application["db_client"].list_collection_names():
        application["db_client"][collection].drop()
    yield
