test_obj = {
        "name": "Autotest",
        "slug": "autotest1",
        "description": "Project 1 description",
        "ai_providers": [
            {
                "api_base": "https://api.openai.com/v1",
                "provider_name": "provider1",
                "ai_model_name": "model1"
            }
        ],
        "tags": [
            "tag1", 
            "tag2"
        ],
        "org_id": "organization"
    }


def test_create_project_returns_201(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["project_repository"]
        repo.remove_all()
    
    # act
    response = client.post("/api/projects", json=test_obj)

    # assert
    assert response.status_code == 201
    assert_obj = test_obj.copy()
    assert_obj["id"] = response.json()["id"]
    assert response.json() == assert_obj


def test_create_project_with_existing_slug_returns_400(client, application):
    # arrange
    with application.transaction_context() as ctx:
        from projects.models import Project
        repo = ctx["project_repository"]
        repo.remove_all()
        repo.add(Project(**test_obj))
    
    # act
    response2 = client.post("/api/projects", json=test_obj)
    
    # assert
    assert response2.status_code == 400
    print(response2.json())
    assert response2.json() == {'message': f'Slug already exists: {test_obj["slug"]}'}
    
   
def test_when_no_projects_returns_200_and_empy_list(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["project_repository"]
        repo.remove_all()

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
        repo.remove_all()
        repo.add(Project(**test_obj))
        project_id = repo.find_one({"slug": test_obj["slug"]}).id
    
    # act
    response = client.get(f"/api/projects/{project_id}")

    # assert
    assert response.status_code == 200
    
    json_response = response.json()
    if "transactions" in json_response:
        json_response.pop("transactions")
    json_response.pop("id")
    assert json_response == test_obj
    

def test_update_project(client, application):
    # arrange
    with application.transaction_context() as ctx:
        from projects.models import Project
        repo = ctx["project_repository"]
        repo.remove_all()
        repo.add(Project(**test_obj))
        project_id = repo.find_one({"slug": test_obj["slug"]}).id
        
    # act
    response = client.put(f"/api/projects/{project_id}", json={"name": "Autotest2"})
    
    # assert
    assert response.status_code == 200
    update_object = test_obj.copy()
    update_object["name"] = "Autotest2"
    update_object["id"] = project_id
    assert response.json() == update_object


def test_delete_project(client, application):
    # arrange
    with application.transaction_context() as ctx:
        from projects.models import Project
        repo = ctx["project_repository"]
        repo.remove_all()
        repo.add(Project(**test_obj))
        project_id = repo.find_one({"slug": test_obj["slug"]}).id
        
    # act
    response = client.delete(f"/api/projects/{project_id}")

    # assert
    assert response.status_code == 204


def test_delete_not_exisitng_project_returns_204(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["project_repository"]
        repo.remove_all()
        
    # act
    response = client.delete(f"/api/projects/123")

    # assert
    assert response.status_code == 204


def test_get_projects(client, application):
    # arrange
    with application.transaction_context() as ctx:
        from projects.models import Project
        repo = ctx["project_repository"]
        repo.remove_all()
        repo.add(Project(**test_obj))
        project_id = repo.find_one({"slug": test_obj["slug"]}).id

    # act
    result = client.get("/api/projects")

    # assert
    assert result.status_code == 200
    test = test_obj.copy()
    test["id"] = project_id
    assert result.json() == [test]
