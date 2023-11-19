def test_create_project(client):
    response = client.post("/api/project", json={"id": 1234, "name": "test"})

    assert response.status_code == 200
    assert response.json() == {"id": 1234, "name": "test"}
