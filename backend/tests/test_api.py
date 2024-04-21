test_obj = {
    "name": "Autotest",
    "slug": "autotest1",
    "description": "Project 1 description",
    "ai_providers": [
        {
            "deployment_name": "openai",
            "slug": "openai",
            "api_base": "https://api.openai.com/v1",
            "description": "New test project",
            "provider_name": "provider1",
        }
    ],
    "tags": ["tag1", "tag2"],
    "org_id": "organization",
    "owner": "owner",
}


def test_create_project_returns_201(client, application):
    # arrange
    ...

    # act
    response = client.post("/api/projects", json=test_obj)

    # assert
    assert response.status_code == 201
    assert_obj = test_obj.copy()
    assert_obj["id"] = response.json()["id"]
    assert_obj["total_transactions"] = response.json()["total_transactions"]
    assert_obj["total_cost"] = response.json()["total_cost"]
    assert_obj["created_at"] = response.json()["created_at"]
    assert response.json() == assert_obj


def test_create_project_with_existing_slug_returns_400(client, application):
    # arrange
    with application.transaction_context() as ctx:
        from projects.models import Project

        repo = ctx["project_repository"]
        repo.add(Project(**test_obj))

    # act
    response = client.post("/api/projects", json=test_obj)

    # assert
    assert response.status_code == 400
    assert response.json() == {"message": f'Slug already exists: {test_obj["slug"]}'}


def test_when_no_projects_returns_200_and_empy_list(client, application):
    # arrange
    ...

    # act
    result = client.get("/api/projects")

    # assert
    assert result.status_code == 200
    assert result.json() == []


def test_get_project_happy_path(client, application):
    # arrange
    with application.transaction_context() as ctx:
        from projects.models import Project

        repo = ctx["project_repository"]
        repo.add(Project(id="project1", **test_obj))
        project_id = repo.find_one({"slug": test_obj["slug"]}).id

    # act
    response = client.get(f"/api/projects/{project_id}")

    # assert
    assert response.status_code == 200
    assert response.json() == dict(
        id="project1",
        total_transactions=0,
        total_cost=0,
        created_at=response.json()["created_at"],
        **test_obj,
    )


def test_update_project(client, application):
    # arrange
    with application.transaction_context() as ctx:
        from projects.models import Project

        repo = ctx["project_repository"]
        project_id = "project1"
        repo.add(Project(id=project_id, **test_obj))

    # act
    response = client.put(f"/api/projects/{project_id}", json={"name": "Autotest2"})

    # assert
    assert response.status_code == 200
    assert response.json() == test_obj | dict(
        id=project_id,
        total_transactions=0,
        total_cost=0,
        name="Autotest2",
        created_at=response.json()["created_at"],
    )


def test_delete_project(client, application):
    # arrange
    with application.transaction_context() as ctx:
        from projects.models import Project

        repo = ctx["project_repository"]
        project_id = "project-test"
        repo.add(Project(id=project_id, **test_obj))

    # act
    response = client.delete(f"/api/projects/{project_id}")

    # assert
    assert response.status_code == 204


def test_delete_not_existing_project_returns_204(client, application):
    # arrange
    ...

    # act
    response = client.delete(f"/api/projects/non-existing")

    # assert
    assert response.status_code == 204


def test_get_projects(client, application):
    # arrange
    with application.transaction_context() as ctx:
        from projects.models import Project

        repo = ctx["project_repository"]
        project_id = "project-test"
        repo.add(Project(id=project_id, **test_obj))

    # act
    result = client.get("/api/projects")

    # assert
    assert result.status_code == 200
    assert result.json() == [
        dict(
            id=project_id,
            total_transactions=0,
            total_cost=0,
            created_at=result.json()[0]["created_at"],
            **test_obj,
        )
    ]
