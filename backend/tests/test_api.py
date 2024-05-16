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

header = {
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImN0eSI6IkpXVCJ9.eyJpc3MiOiJ0ZXN0IiwiYXpwIjoiNDA3NDA4NzE4MTkyLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiNDA3NDA4NzE4MTkyLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTEyMTAyODc3OTUzNDg0MzUyNDI3IiwiZW1haWwiOiJ0ZXN0QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiYm54OW9WT1o4U3FJOTcyczBHYjd4dyIsIm5hbWUiOiJUZXN0IFVzZXIiLCJwaWN0dXJlIjoiIiwiZ2l2ZW5fbmFtZSI6IlRlc3QiLCJmYW1pbHlfbmFtZSI6IlVzZXIiLCJpYXQiOjE3MTM3MzQ0NjEsImV4cCI6OTk5OTk5OTk5OX0.eZYMQzcSRzkAq4Me8C6SNU3wduS7EIu_o5XGAbsDmU05GtyipQEb5iNJ1QiLg-11RbZFL3dvi8xKd3mpuw8b-5l6u8hwSpZg6wNPLY0zPX-EOwxeHLtev_2X5pUf1_IWAnso9K_knsK8CcmJoVsCyNNjlw3hrkChacJHGNzg0TTT1rh3oe6KCpbLvYlV6tUPfm5k3AMFZIT7Jntr38CZvs6gac6L_DhItJc3TNNUUHie2zgA29_r9YFlaEr_nGoSmBhIi-i0i0h34TL4JAb4qJkVM2YI2eTTv2HjEGtkx4mE5JvNQ0VxzHSJcCNOHh1gCiFD5c6rhvvxVeEqMkGGbCZKHX_vCgnIp0iE_OWyICjVTFPitQJ00fXLhyHyPb7q5J605tuK2iTHp2NCRJEXIAl9e0F_qASBBAfyL0C4FCBtvbnEMwtpoV1VWinkKgkI7JVH0AsyTugjXyAjxxsJxBTJT9qwZLxVBoaxgqNTOFfxvwstyq1VfCl3iBbpt71D"
}


def test_create_project_returns_201(client, application):
    # arrange
    ...

    # act
    response = client.post("/api/projects", headers=header, json=test_obj)

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
    response = client.post("/api/projects", headers=header, json=test_obj)

    # assert
    assert response.status_code == 400
    assert response.json() == {"message": f'Slug already exists: {test_obj["slug"]}'}


def test_when_no_projects_returns_200_and_empy_list(client, application):
    # arrange
    ...

    # act
    result = client.get("/api/projects", headers=header)

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
    response = client.get(f"/api/projects/{project_id}", headers=header)

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
    response = client.put(
        f"/api/projects/{project_id}", headers=header, json={"name": "Autotest2"}
    )

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
    response = client.delete(f"/api/projects/{project_id}", headers=header)

    # assert
    assert response.status_code == 204


def test_delete_not_existing_project_returns_204(client, application):
    # arrange
    ...

    # act
    response = client.delete(f"/api/projects/non-existing", headers=header)

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
    result = client.get("/api/projects", headers=header)

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
