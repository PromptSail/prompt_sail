from src.projects.schemas import CreateProjectSchema


def test_create_project(client):
    response = client.post("/api/project", json={
        "id": "autotest",
        "name": "Test auto",
        "slug": "test-auto",
        "api_base": "https://api.openai.com/v1",
        "org_id": "org1"
    })
    assert response.status_code == 200
    assert response.json() == {
        "id": "autotest",
        "name": "Test auto",
        "slug": "test-auto",
        "api_base": "https://api.openai.com/v1",
        "org_id": "org1"
    }

    response2 = client.post("/api/project", json={
        "id": "autotest",
        "name": "Test auto",
        "slug": "test-auto",
        "api_base": "https://api.openai.com/v1",
        "org_id": "org1"
    })
    assert response2.status_code == 400
    assert response2.json() == {"error": "Project already exists"}


def test_get_project(client):
    response = client.get("/api/project/autotest")

    assert response.status_code == 200
    assert response.json() == {
        "id": "autotest",
        "name": "Test auto",
        "api_base": "https://api.openai.com/v1",
        "slug": "test-auto",
        "org_id": "org1",
        "transactions": []
    }


def test_update_project(client):
    response = client.put("/api/project/autotest", json={
        "id": "autotest",
        "name": "Test auto",
        "api_base": "https://api.openai.com/v1",
        "slug": "test-auto",
        "org_id": "org3"
    })

    assert response.status_code == 200
    assert response.json() == {"success": "Project updated successfully"}


def test_delete_project(client):
    response = client.delete("/api/project/autotest")

    assert response.status_code == 200
    assert response.json() == {"success": "Project deleted successfully"}

    response2 = client.delete("/api/project/autotest")

    assert response2.status_code == 404
    assert response2.json() == {"error": "Project not found"}


def test_get_projects(client):
    response = client.get("/api/projects")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": "project1",
            "name": "Project 1",
            "api_base": "https://api.openai.com/v1",
            "slug": "",
            "org_id": ""
        },
        {
            "id": "project2",
            "name": "Project 2",
            "api_base": "https://api.openai.com/v1",
            "slug": "",
            "org_id": ""
        },
    ]
    