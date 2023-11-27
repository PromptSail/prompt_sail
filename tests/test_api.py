def test_create_project(client):
    test_obj = {
        "name": "Autotest",
        "slug": "autotest1",
        "description": "Project 1 description",
        "ai_providers": [
            {
                "api_base": "https://api.openai.com/v1",
                "provider_name": "provider1",
                "model_name": "model1"
            }
        ],
        "tags": [
            "tag1", 
            "tag2"
        ],
        "org_id": "organization"
    }
    response = client.post("/api/project", json=test_obj)

    assert response.status_code == 200
    assert response.json() == test_obj

    response2 = client.post("/api/project", json=test_obj)
    assert response2.status_code == 400
    assert response2.json() == {"error": "Project already exists"}


def test_get_project(client):
    proj_id = client.get("/api/projects").json()[0]["id"]
    response = client.get(f"/api/project/{proj_id}")

    assert response.status_code == 200
    
    response = response.json()
    if response["transactions"]:
        response.pop("transactions")
    
    assert response == {
        "id": proj_id,
        "name": "Project 1",
        "slug": "project1",
        "description": "Project 1 description",
        "ai_providers": [
            {
                "api_base": "https://api.openai.com/v1",
                "provider_name": "OpenAI",
                "model_name": "gpt-3.5-turbo"
            }
        ], 
        "tags": [
            "tag1",
            "tag2",
        ],
        "org_id": "organization"
    }


def test_update_project(client):
    projects = client.get("/api/projects").json()
    proj_ids = {proj['slug']: proj["id"] for proj in projects}
    
    response = client.put("/api/project/autotest", json={
        "id": proj_ids["autotest1"],
        "name": "Autotest",
        "slug": "autotest-1u",
        "description": "Project 1 description for updated autotest.",
        "ai_providers": [
            {
                "api_base": "https://api.openai.com/v1",
                "provider_name": "provider1",
                "model_name": "model1"
            }
        ],
        "tags": [
            "tag1", 
            "tag2"
        ],
        "org_id": "org1"
    })

    assert response.status_code == 200
    assert response.json() == {"success": "Project updated successfully"}


def test_delete_project(client):
    proj_id = client.get("/api/projects").json()[2]["id"]
    response = client.delete(f"/api/project/{proj_id}")

    assert response.status_code == 200
    assert response.json() == {"success": "Project deleted successfully"}

    response2 = client.delete("/api/project/autotest")

    assert response2.status_code == 404
    assert response2.json() == {"error": "Project not found"}


def test_get_projects(client):
    response = client.get("/api/projects")
    
    print(response.json())
    proj1_id, proj2_id = response.json()[0]["id"], response.json()[1]["id"]
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": proj1_id,
            "name": "Project 1",
            "slug": "project1",
            "description": "Project 1 description",
            "ai_providers": [
                {
                    "api_base": "https://api.openai.com/v1",
                    "provider_name": "OpenAI",
                    "model_name": "gpt-3.5-turbo"
                }
            ], 
            "tags": [
                "tag1",
                "tag2",
            ],
            "org_id": "organization"
        },
        {
            "id": proj2_id,
            "name": "Project 2",
            "slug": "project2",
            "description": "Project 2 description",
            "ai_providers": [
                {
                    "api_base": "https://api.openai.com/v1",
                    "provider_name": "OpenAI",
                    "model_name": "gpt-3.5-turbo"
                }
            ], 
            "tags": [
                "tag1",
                "tag2",
                "tag3",
            ],
            "org_id": "organization"
        }
    ]
