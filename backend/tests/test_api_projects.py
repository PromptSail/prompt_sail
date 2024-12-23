from datetime import datetime, timezone, timedelta
from transactions.schemas import CreateTransactionWithRawDataSchema
from projects.schemas import GetProjectSchema
import pytest


header = {
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImN0eSI6IkpXVCJ9.eyJpc3MiOiJ0ZXN0IiwiYXpwIjoiNDA3NDA4NzE4MTkyLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiNDA3NDA4NzE4MTkyLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTEyMTAyODc3OTUzNDg0MzUyNDI3IiwiZW1haWwiOiJ0ZXN0QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiYm54OW9WT1o4U3FJOTcyczBHYjd4dyIsIm5hbWUiOiJUZXN0IFVzZXIiLCJwaWN0dXJlIjoiIiwiZ2l2ZW5fbmFtZSI6IlRlc3QiLCJmYW1pbHlfbmFtZSI6IlVzZXIiLCJpYXQiOjE3MTM3MzQ0NjEsImV4cCI6OTk5OTk5OTk5OX0.eZYMQzcSRzkAq4Me8C6SNU3wduS7EIu_o5XGAbsDmU05GtyipQEb5iNJ1QiLg-11RbZFL3dvi8xKd3mpuw8b-5l6u8hwSpZg6wNPLY0zPX-EOwxeHLtev_2X5pUf1_IWAnso9K_knsK8CcmJoVsCyNNjlw3hrkChacJHGNzg0TTT1rh3oe6KCpbLvYlV6tUPfm5k3AMFZIT7Jntr38CZvs6gac6L_DhItJc3TNNUUHie2zgA29_r9YFlaEr_nGoSmBhIi-i0i0h34TL4JAb4qJkVM2YI2eTTv2HjEGtkx4mE5JvNQ0VxzHSJcCNOHh1gCiFD5c6rhvvxVeEqMkGGbCZKHX_vCgnIp0iE_OWyICjVTFPitQJ00fXLhyHyPb7q5J605tuK2iTHp2NCRJEXIAl9e0F_qASBBAfyL0C4FCBtvbnEMwtpoV1VWinkKgkI7JVH0AsyTugjXyAjxxsJxBTJT9qwZLxVBoaxgqNTOFfxvwstyq1VfCl3iBbpt71D"
}

# Add this with other test data at the top of the file
test_transaction = {
    "project_id": "project-test",  # This will match our test project ID
    "request_json": {
        "method": "POST",
        "url": "https://api.openai.com/v1/chat/completions?tags=dev,test&target_path=/chat/completions",
        "host": "api.openai.com",
        "headers": {
            "host": "api.openai.com",
            "connection": "close",
            "content-length": "304",
            "accept": "application/json",
            "user-agent": "OpenAI/Python 1.35.7",
            "accept-encoding": "gzip, deflate",
            "authorization": "Bearer sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "max-forwards": "10",
            "x-stainless-lang": "python",
            "x-stainless-package-version": "1.35.7",
            "x-stainless-os": "Windows",
            "x-stainless-arch": "other:amd64",
            "x-stainless-runtime": "CPython",
            "x-stainless-runtime-version": "3.10.11",
            "x-stainless-async": "false",
            "x-arr-log-id": "4e939686-fa43-4b14-b1c8-1316b943d77c",
            "client-ip": "79.184.224.10:64769",
            "x-client-ip": "79.184.224.10",
            "disguised-host": "try-promptsail.azurewebsites.net",
            "x-site-deployment-id": "try-promptsail",
            "was-default-hostname": "try-promptsail.azurewebsites.net",
            "x-forwarded-proto": "https",
            "x-appservice-proto": "https",
            "x-arr-ssl": "2048|256|CN=Microsoft Azure RSA TLS Issuing CA 03, O=Microsoft Corporation, C=US|CN=*.azurewebsites.net, O=Microsoft Corporation, L=Redmond, S=WA, C=US",
            "x-forwarded-tlsversion": "1.3",
            "x-forwarded-for": "79.184.224.10:64769",
            "x-original-url": "/api/models-playground/openai/?tags=dev_2,test&target_path=/chat/completions",
            "x-waws-unencoded-url": "/api/models-playground/openai/?tags=dev_2,test&target_path=/chat/completions",
            "x-client-port": "64769",
            "content-type": "application/json",
        },
        "extensions": {
            "timeout": {"connect": 50, "read": 100, "write": 100, "pool": 100}
        },
        "content": {
            "messages": [
                {
                    "role": "system",
                    "content": "You are an experienced marketer, who helps companies to create their marketing strategy.",
                },
                {
                    "role": "user",
                    "content": "Hello",
                },
            ],
            "model": "gpt-3.5-turbo-0125",
            "temperature": 0.5,
        },
    },
    "response_json": {
        "status_code": 200,
        "headers": {
            "date": "Thu, 24 Oct 2024 20:37:47 GMT",
            "content-type": "application/json",
            "transfer-encoding": "chunked",
            "connection": "close",
            "access-control-expose-headers": "X-Request-ID",
            "openai-organization": "ermlab-software",
            "openai-processing-ms": "5752",
            "openai-version": "2020-10-01",
            "x-ratelimit-limit-requests": "10000",
            "x-ratelimit-limit-tokens": "200000",
            "x-ratelimit-remaining-requests": "9999",
            "x-ratelimit-remaining-tokens": "199938",
            "x-ratelimit-reset-requests": "8.64s",
            "x-ratelimit-reset-tokens": "18ms",
            "x-request-id": "req_34c80008a9bdf45008eaf3a0b1b1eb8a",
            "strict-transport-security": "max-age=31536000; includeSubDomains; preload",
            "cf-cache-status": "DYNAMIC",
            "set-cookie": "__cf_bm=63oSPzfIgrh2XHvHIhPy._mzS8FaUBoY_aoLtBOYkKs-1729802267-1.0.1.1-Lpkpb1G3CkL1avTcO_HamD3uTj5A54g0RpJcaIalmf7dJPAlldf_tN9qOSRy6fegziJAqGgPNiPw7C4joCQrEg; path=/; expires=Thu, 24-Oct-24 21:07:47 GMT; domain=.api.openai.com; HttpOnly; Secure; SameSite=None, _cfuvid=gF0UbGQ5.6CmFcpYCz.9AFVWz2DAZtiUnFJ8ppSe2Dw-1729802267379-0.0.1.1-604800000; path=/; domain=.api.openai.com; HttpOnly; Secure; SameSite=None",
            "x-content-type-options": "nosniff",
            "server": "cloudflare",
            "cf-ray": "8d7cc4247ee30ead-AMS",
            "content-encoding": "gzip",
            "alt-svc": 'h3=":443"; ma=86400',
        },
        "is_error": "false",
        "is_success": "true",
        "content": {
            "id": "chatcmpl-ALysP7bzYZUx3U2TgcTFSTiooLBt4",
            "object": "chat.completion",
            "created": 1729802261,
            "model": "gpt-3.5-turbo-0125",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": "Hi there!",
                    },
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": 40,
                "completion_tokens": 25,
                "total_tokens": 65,
                "prompt_tokens_details": {"cached_tokens": 0},
                "completion_tokens_details": {"reasoning_tokens": 0},
            },
            "system_fingerprint": None,
        },
        "elapsed": 6.253704,
        "encoding": "utf-8",
    },
    "tags": ["test-tag"],
    "provider": "OpenAI",
    "model": "gpt-3.5-turbo-0125",
    "type": "chat",
    "os": None,
    "input_tokens": 10,
    "output_tokens": 20,
    "library": "python-openai",
    "status_code": 200,
    "messages": [
        {
            "role": "system",
            "content": "You are an experienced marketer, who helps companies to create their marketing strategy.",
        },
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"},
    ],
    "last_message": "Hi there!",
    "prompt": "Hello",
    "error_message": None,
    "generation_speed": None,
    # Convert datetime strings to ISO format
    "request_time": datetime.now(tz=timezone.utc).isoformat(),
    "input_cost": None,
    "output_cost": None,
    "total_cost": None,
    "response_time": datetime.now(tz=timezone.utc).isoformat(),
}



# --------------------------------
# Projects CRUD tests
# --------------------------------  

def test_create_project_with_valid_data_returns_201(client, application):
    """Test creating a new project with valid data returns 201 and correct project data"""
    # arrange
    new_project_data = {
        "name": "Test Marketing Campaign",
        "slug": "test-marketing-2024",
        "description": "Project for testing AI-driven marketing campaign optimization",
        "ai_providers": [
            {
                "deployment_name": "marketing-gpt",
                "slug": "marketing-gpt",
                "api_base": "https://api.openai.com/v1",
                "description": "GPT model optimized for marketing content",
                "provider_name": "OpenAI Marketing",
            }
        ],
        "tags": ["marketing", "test", "gpt-optimization"],
        "org_id": "test-marketing-org",
        "owner": "test.marketer@example.com",
    }

    # act
    response = client.post("/api/projects", headers=header, json=new_project_data)

    # assert
    assert response.status_code == 201
    
    expected_response = new_project_data.copy()
    expected_response.update({
        "id": response.json()["id"],
        "total_transactions": 0,
        "total_cost": 0,
        "created_at": response.json()["created_at"]
    })
    
    assert response.json() == expected_response

def test_create_project_with_existing_slug_returns_400_and_error(client, application, test_project):
    """Test creating a project with an existing slug returns 400 and error message"""
    # arrange - test_project fixture has already created a project with slug "autotest1"
    # Create a new project data without datetime fields
    new_project_data = {
        "name": test_project.name,
        "slug": test_project.slug,  # Same slug as test_project
        "description": test_project.description,
        "ai_providers": [provider.model_dump() for provider in test_project.ai_providers],
        "tags": test_project.tags,
        "org_id": test_project.org_id,
        "owner": test_project.owner
    }
    
    # act - try to create another project with the same slug
    response = client.post("/api/projects", headers=header, json=new_project_data)

    # assert
    assert response.status_code == 400
    assert response.json() == {"message": f'Slug already exists: {test_project.slug}'}

def test_get_projects_with_empty_database_returns_200_and_empty_list(client, application):
    """Test when no projects exist, returns 200 and empty list"""
    # arrange
    ...

    # act
    result = client.get("/api/projects", headers=header)

    # assert
    assert result.status_code == 200
    assert result.json() == []

def test_get_project_with_valid_id_returns_200_and_project_data(client, application, test_project):
    """Test retrieving a project by ID returns 200 and correct project data"""
    # act
    response = client.get(f"/api/projects/{test_project.id}", headers=header)
    response_data = response.json()

    # assert
    assert response.status_code == 200
    
    # Prepare expected data
    expected_response = {
        "id": test_project.id,
        "name": test_project.name,
        "slug": test_project.slug,
        "description": test_project.description,
        "ai_providers": [provider.model_dump() for provider in test_project.ai_providers],
        "tags": test_project.tags,
        "org_id": test_project.org_id,
        "owner": test_project.owner,
        "total_transactions": 0,
        "total_cost": 0,
        "created_at": test_project.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]  # Match API format
    }

    # Compare datetime strings after formatting
    assert response_data["created_at"].startswith(expected_response["created_at"])
    
    # Remove created_at for the rest of the comparison
    del response_data["created_at"]
    del expected_response["created_at"]
    
    assert response_data == expected_response

def test_update_project_with_new_name_returns_200_and_updated_data(client, application, test_project):
    """Test updating project name returns 200 and updated project data"""
    # arrange
    updated_name = "AI Marketing Campaign 2024"
    update_data = {"name": updated_name}

    # act
    response = client.put(
        f"/api/projects/{test_project.id}", 
        headers=header, 
        json=update_data
    )
    response_data = response.json()

    # assert
    assert response.status_code == 200
    
    # Prepare expected response
    expected_response = {
        "id": test_project.id,
        "name": updated_name,  # Updated name
        "slug": test_project.slug,
        "description": test_project.description,
        "ai_providers": [provider.model_dump() for provider in test_project.ai_providers],
        "tags": test_project.tags,
        "org_id": test_project.org_id,
        "owner": test_project.owner,
        "total_transactions": 0,
        "total_cost": 0,
        "created_at": test_project.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
    }

    # Compare datetime strings after formatting
    assert response_data["created_at"].startswith(expected_response["created_at"])
    
    # Remove created_at for the rest of the comparison
    del response_data["created_at"]
    del expected_response["created_at"]
    
    assert response_data == expected_response

def test_update_project_with_multiple_fields_returns_200_and_updated_data(client, application, test_project):
    """Test updating multiple project fields returns 200 and correctly updated project data"""
    # arrange
    update_data = {
        "name": "Enterprise AI Solutions",
        "description": "Advanced AI integration for enterprise clients",
        "tags": ["enterprise", "production", "gpt4"],
        "ai_providers": [
            {
                "deployment_name": "gpt4-prod",
                "slug": "gpt4-prod",
                "api_base": "https://api.openai.com/v1",
                "description": "Production GPT-4 deployment",
                "provider_name": "OpenAI Enterprise"
            },
            {
                "deployment_name": "azure-gpt4",
                "slug": "azure-gpt4",
                "api_base": "https://azure.openai.com/v1",
                "description": "Azure GPT-4 backup deployment",
                "provider_name": "Azure OpenAI"
            }
        ]
    }

    # act
    response = client.put(
        f"/api/projects/{test_project.id}", 
        headers=header, 
        json=update_data
    )
    response_data = response.json()

    # assert
    assert response.status_code == 200
    
    # Prepare expected response
    expected_response = {
        "id": test_project.id,
        "name": update_data["name"],
        "slug": test_project.slug,  # Slug remains unchanged
        "description": update_data["description"],
        "ai_providers": update_data["ai_providers"],
        "tags": update_data["tags"],
        "org_id": test_project.org_id,  # Organization remains unchanged
        "owner": test_project.owner,    # Owner remains unchanged
        "total_transactions": 0,
        "total_cost": 0,
        "created_at": test_project.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
    }

    # Compare datetime strings after formatting
    assert response_data["created_at"].startswith(expected_response["created_at"])
    
    # Remove created_at for the rest of the comparison
    del response_data["created_at"]
    del expected_response["created_at"]
    
    assert response_data == expected_response

def test_delete_project_with_valid_id_returns_204(client, application, test_project):
    """Test deleting a project with valid ID returns 204"""
    # act
    response = client.delete(f"/api/projects/{test_project.id}", headers=header)

    # assert
    assert response.status_code == 204

def test_delete_project_with_nonexistent_id_returns_204(client, application):
    """Test deleting a non-existing project returns 204"""
    # arrange
    ...

    # act
    response = client.delete(f"/api/projects/non-existing", headers=header)

    # assert
    assert response.status_code == 204

def test_get_projects_with_existing_project_returns_200_and_project_list(client, application, test_project):
    """Test retrieving all projects returns 200 and list containing the test project"""
    # act
    response = client.get("/api/projects", headers=header)
    response_data = response.json()

    # assert
    assert response.status_code == 200
    assert len(response_data) == 1  # Should contain only our test project
    
    # Prepare expected project data
    expected_project = {
        "id": test_project.id,
        "name": test_project.name,
        "slug": test_project.slug,
        "description": test_project.description,
        "ai_providers": [provider.model_dump() for provider in test_project.ai_providers],
        "tags": test_project.tags,
        "org_id": test_project.org_id,
        "owner": test_project.owner,
        "total_transactions": 0,
        "total_cost": 0,
        "created_at": test_project.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
    }

    # Compare datetime strings after formatting
    assert response_data[0]["created_at"].startswith(expected_project["created_at"])
    
    # Remove created_at for the rest of the comparison
    del response_data[0]["created_at"]
    del expected_project["created_at"]
    
    assert response_data[0] == expected_project
