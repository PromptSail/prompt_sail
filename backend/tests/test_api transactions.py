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


# ------------------------------
# Create transactions tests
# ------------------------------

def test_create_transaction_with_valid_data_returns_201_and_calculated_costs(client, application, test_project):
    """Test successful transaction creation with cost calculation"""
    # arrange
    data = CreateTransactionWithRawDataSchema(
        **{
            **test_transaction,
            # Convert ISO strings back to datetime objects for the schema
            "request_time": datetime.fromisoformat(test_transaction["request_time"]),
            "response_time": datetime.fromisoformat(test_transaction["response_time"]),
        }
    )

    # Convert to JSON-serializable format for the request
    json_data = data.model_dump(mode='json')

    # act
    response = client.post("/api/transactions", headers=header, json=json_data)

    # assert
    assert response.status_code == 201
    transaction = response.json()
    assert transaction["project_id"] == data.project_id
    assert transaction["provider"] == data.provider
    assert transaction["model"] == data.model
    assert transaction["input_tokens"] == data.input_tokens
    assert transaction["output_tokens"] == data.output_tokens
    assert transaction["status_code"] == data.status_code
    assert transaction["total_cost"] is not None  # Cost should be calculated
    assert transaction["input_cost"] is not None
    assert transaction["output_cost"] is not None
    
    # Verify cost calculation
    assert transaction["input_cost"] > 0
    assert transaction["output_cost"] > 0
    assert transaction["total_cost"] == transaction["input_cost"] + transaction["output_cost"]
  
def test_create_transaction_with_failed_response_returns_201_and_error_details(client, application, test_project):
    """Test transaction creation with failed API response"""
    # arrange
    data = test_transaction.copy()
    data["status_code"] = 400
    data["error_message"] = "Bad request"
    data["response_json"] = {"error": {"message": "Bad request"}}

    # act
    response = client.post("/api/transactions", headers=header, json=data)

    # assert
    assert response.status_code == 201
    transaction = response.json()
    assert transaction["status_code"] == 400
    assert transaction["error_message"] == "Bad request"
    assert transaction["input_cost"] is None
    assert transaction["output_cost"] is None
    assert transaction["total_cost"] is None
 
def test_create_transaction_with_image_generation_model_returns_201_and_proper_costs(client, application, test_project):
    """Test transaction creation for image generation"""
    # arrange
    data = test_transaction.copy()
    data["model"] = "standard/1024x1024/dall-e-3"
    data["type"] = "image_generation"
    data["request_json"]["n"] = 1  # Number of images

    # act
    response = client.post("/api/transactions", headers=header, json=data)

    pytest.skip("todo: add cost calculation")
    # assert
    assert response.status_code == 201
    transaction = response.json()
    assert transaction["type"] == "image_generation"
    
    # todo: add cost calculation
    #assert transaction["total_cost"] == pytest.approx(0.040, rel=1e-4)
    assert transaction["input_cost"] == 0  # Image generation has no input cost

def test_create_transaction_with_missing_required_fields_returns_422(client, application):
    """Test transaction creation with missing required fields"""
    # arrange
    invalid_data = {
        "project_id": "project-test",
        # Missing required fields
    }

    # act
    response = client.post("/api/transactions", headers=header, json=invalid_data)

    # assert
    assert response.status_code == 422  # Validation error

def test_create_transaction_with_unknown_model_returns_201_and_null_costs(client, application, test_project):
    """Test transaction creation with unknown model"""
    # arrange
    data = test_transaction.copy()
    data["model"] = "unknown-model"

    # act
    response = client.post("/api/transactions", headers=header, json=data)

    # assert
    assert response.status_code == 201
    transaction = response.json()
    assert transaction["model"] == "unknown-model"
    assert transaction["input_cost"] is None
    assert transaction["output_cost"] is None
    assert transaction["total_cost"] is None   
    
# --------------------------------
# Transaction cost calculation
# --------------------------------

def test_transaction_costs_with_embedding_model_returns_201_and_correct_costs(client, application, test_project):
    """Test if transaction costs are calculated accurately for embedding model"""
    # arrange
    data = test_transaction.copy()
    data.update({
        "model": "text-embedding-3-large",
        "type": "embedding",
        "input_tokens": 256,  # Known input tokens
        "output_tokens": 0,   # Embedding models don't have output tokens
        # Clear any existing cost values to test calculation
        "input_cost": None,
        "output_cost": None,
        "total_cost": None
    })

    # act
    response = client.post("/api/transactions", headers=header, json=data)

    # assert
    assert response.status_code == 201
    transaction = response.json()
    
    # text-embedding-3-large pricing: $0.00013/1K tokens (input only)
    expected_input_cost = 0 # No input cost for embeddings
    expected_output_cost = 0  # No output cost for embeddings
    expected_total_cost = (data["input_tokens"] / 1000) * 0.00013  # $0.00003328  # Total cost equals input cost
    
    # Check if calculated costs match expected values (using approximate comparison due to floating point)
    assert transaction["input_cost"] == pytest.approx(expected_input_cost, rel=1e-4)
    assert transaction["output_cost"] == pytest.approx(expected_output_cost, rel=1e-4)
    assert transaction["total_cost"] == pytest.approx(expected_total_cost, rel=1e-4)
    
    # Additional embedding-specific assertions
    assert transaction["type"] == "embedding"
    assert transaction["output_tokens"] == 0
    
def test_transaction_costs_with_embedding_model_with_none_output_tokens_returns_201_and_correct_costs(client, application, test_project):
    """Test if transaction costs are calculated accurately for embedding model with None output tokens"""
    # arrange
    data = test_transaction.copy()
    data.update({
        "model": "text-embedding-3-large",
        "type": "embedding",
        "input_tokens": 256,  # Known input tokens
        "output_tokens": None,   # Embedding models don't have output tokens
        # Clear any existing cost values to test calculation
        "input_cost": None,
        "output_cost": None,
        "total_cost": None
    })
    
    pytest.skip("todo: needs adding the output_tokens none verification")

    # act
    response = client.post("/api/transactions", headers=header, json=data)

    # assert
    assert response.status_code == 201
    transaction = response.json()
    
    # Additional embedding-specific assertions
    assert transaction["type"] == "embedding"
    assert transaction["output_tokens"] is None
    
    # text-embedding-3-large pricing: $0.00013/1K tokens (input only)
    expected_input_cost = 0 # No input cost for embeddings
    expected_output_cost = 0  # No output cost for embeddings
    expected_total_cost = (data["input_tokens"] / 1000) * 0.00013  # $0.00003328  # Total cost equals input cost
    
    # Check if calculated costs match expected values (using approximate comparison due to floating point)
    assert transaction["input_cost"] is None
    assert transaction["output_cost"] is None
    assert transaction["total_cost"] == pytest.approx(expected_total_cost, rel=1e-4)
    
def test_transaction_costs_with_embedding_model_with_set_output_tokens_returns_201_and_correct_costs(client, application, test_project):
    """Test if transaction costs are calculated accurately for embedding model with set output tokens"""
    # arrange
    data = test_transaction.copy()
    data.update({
        "model": "text-embedding-3-large",
        "type": "embedding",
        "input_tokens": 256,  # Known input tokens
        "output_tokens": 100,   # Embedding models should have output tokens, this should not be taken into account for cost calculation
        # Clear any existing cost values to test calculation
        "input_cost": None,
        "output_cost": None,
        "total_cost": None
    })
    
    pytest.skip("todo: needs adding the output_tokens none verification")

    # act
    response = client.post("/api/transactions", headers=header, json=data)

    # assert
    assert response.status_code == 201
    transaction = response.json()
    
    # Additional embedding-specific assertions
    assert transaction["type"] == "embedding"
    assert transaction["output_tokens"] is None
    
    # text-embedding-3-large pricing: $0.00013/1K tokens (input only)
    expected_input_cost = 0 # No input cost for embeddings
    expected_output_cost = 0  # No output cost for embeddings
    expected_total_cost = (data["input_tokens"] / 1000) * 0.00013  # $0.00003328  # Total cost equals input cost
    
    # Check if calculated costs match expected values (using approximate comparison due to floating point)
    assert transaction["input_cost"] is None
    assert transaction["output_cost"] is None
    assert transaction["total_cost"] == pytest.approx(expected_total_cost, rel=1e-4)

    
def test_transaction_costs_with_chat_model_returns_201_and_correct_costs(client, application, test_project):
    """Test if transaction costs are calculated accurately based on token counts"""
    # arrange
    data = test_transaction.copy()
    data.update({
        "model": "gpt-3.5-turbo-0125",  # Specific model with known pricing
        "input_tokens": 100,  # Known input tokens
        "output_tokens": 50,   # Known output tokens
        # Clear any existing cost values to test calculation
        "input_cost": None,
        "output_cost": None,
        "total_cost": None
    })

    # act
    response = client.post("/api/transactions", headers=header, json=data)

    # assert
    assert response.status_code == 201
    transaction = response.json()
    
    # GPT-3.5-turbo-0125 pricing: $0.0005/1K input tokens, $0.0015/1K output tokens
    expected_input_cost = (data["input_tokens"] / 1000) * 0.0005   # $0.00005
    expected_output_cost = (data["output_tokens"] / 1000) * 0.0015    # $0.000075
    expected_total_cost = expected_input_cost + expected_output_cost  # $0.000125
    
    # Check if calculated costs match expected values (using approximate comparison due to floating point)
    assert transaction["input_cost"] == pytest.approx(expected_input_cost, rel=1e-4)
    assert transaction["output_cost"] == pytest.approx(expected_output_cost, rel=1e-4)
    assert transaction["total_cost"] == pytest.approx(expected_total_cost, rel=1e-4)
    
    # Verify the relationship between costs
    assert transaction["total_cost"] == transaction["input_cost"] + transaction["output_cost"]

  

def test_transaction_costs_with_precalculated_values_returns_201_and_same_costs(client, application, test_project):
    """Test transaction creation with pre-calculated costs"""
    # arrange
    data = test_transaction.copy()
    data["input_cost"] = 0.001
    data["output_cost"] = 0.002
    data["total_cost"] = 0.003

    # act
    response = client.post("/api/transactions", headers=header, json=data)

    # assert
    assert response.status_code == 201
    transaction = response.json()
    assert transaction["input_cost"] == data["input_cost"]
    assert transaction["output_cost"] == data["output_cost"]
    assert transaction["total_cost"] == data["total_cost"]

def test_transaction_costs_with_unknown_model_returns_201_and_null_costs(client, application, test_project):
    """Test if transaction costs are handled properly for unknown/unsupported models"""
    # arrange
    data = test_transaction.copy()
    data.update({
        "model": "gpt-5-future-model",  # Non-existent model
        "type": "chat",
        "input_tokens": 100,
        "output_tokens": 50,
        # Clear any existing cost values to test calculation
        "input_cost": None,
        "output_cost": None,
        "total_cost": None
    })

    # act
    response = client.post("/api/transactions", headers=header, json=data)

    # assert
    assert response.status_code == 201
    transaction = response.json()
    
    # For unknown models, all costs should be None
    assert transaction["input_cost"] is None
    assert transaction["output_cost"] is None
    assert transaction["total_cost"] is None
    
    # Other transaction data should still be recorded correctly
    assert transaction["model"] == "gpt-5-future-model"
    assert transaction["input_tokens"] == 100
    assert transaction["output_tokens"] == 50
    assert transaction["type"] == "chat"

def test_transaction_costs_with_two_image_generation_returns_201_and_correct_costs(client, application, test_project):
    """Test if transaction costs are calculated accurately for DALL-E 3 1024x1792 image generation"""
    # arrange
    data = test_transaction.copy()
    data.update({
        "model": "standard/1024x1792/dall-e-3",  # DALL-E 3 with specific size
        "type": "image_generation",
        "input_tokens": 0,    # Image generation doesn't use tokens
        "output_tokens": 0,   # Image generation doesn't use tokens
        "request_json": {
            "n": 2,  # Number of images requested
            "size": "1024x1792",  # Image size
            "quality": "standard",  # Image quality
            "model": "dall-e-3"
        },
        # Clear any existing cost values to test calculation
        "input_cost": None,
        "output_cost": None,
        "total_cost": None
    })
    
    pytest.skip("todo: add cost calculation for image generation models")

    # act
    response = client.post("/api/transactions", headers=header, json=data)

    # assert
    assert response.status_code == 201
    transaction = response.json()
    
    # DALL-E 3 1024x1792 pricing: $0.080 per image (standard quality)
    cost_per_image = 0.080
    expected_total_cost = cost_per_image * data["request_json"]["n"]  # $0.160 for 2 images
    
    
    
    # Additional image generation specific assertions
    assert transaction["type"] == "image_generation"
    assert transaction["model"] == "standard/1024x1792/dall-e-3"
    assert transaction["input_tokens"] == 0
    assert transaction["output_tokens"] == 0
    
    # Check if calculated costs match expected values
    assert transaction["input_cost"] == 0  # Image generation has no input cost
    assert transaction["output_cost"] == 0  # Image generation has no output cost
    assert transaction["total_cost"] == pytest.approx(expected_total_cost, rel=1e-4)
    


# --------------------------------
# Transation generation speed tests
# --------------------------------

def test_transaction_generation_speed_with_chat_model_returns_201_and_calculated_speed(client, application, test_project):
    """Test generation speed calculation for chat model with output tokens"""
    # arrange
    data = test_transaction.copy()
    
    request_time = datetime.fromisoformat("2024-11-03T12:00:00")
    response_time = request_time + timedelta(seconds=2.5)
    
    data.update({
        "model": "gpt-3.5-turbo-0125",
        "type": "chat",
        "input_tokens": 100,
        "output_tokens": 50,
        "generation_speed": None,  # Clear generation speed to test calculation
        "request_time": request_time.isoformat(),
        "response_time": response_time.isoformat()  
    })
    


    # act
    response = client.post("/api/transactions", headers=header, json=data)

    # assert
    assert response.status_code == 201
    transaction = response.json()
    
    # Generation speed should be output_tokens / time_elapsed
    assert transaction["generation_speed"] is not None
    assert transaction["generation_speed"] > 0
    
    expected_speed = (data["output_tokens"] / (datetime.fromisoformat(data["response_time"]) - datetime.fromisoformat(data["request_time"])).total_seconds())
    

    assert expected_speed == pytest.approx(transaction["generation_speed"], rel=0.01)

def test_transaction_generation_speed_with_image_model_returns_201_and_null_speed(client, application, test_project):
    """Test generation speed calculation for image generation model (zero output tokens)"""
    # arrange
    data = test_transaction.copy()
    data.update({
        "model": "standard/1024x1024/dall-e-3",
        "type": "image_generation",
        "input_tokens": 0,
        "output_tokens": 0,  # Image generation has no output tokens
        "generation_speed": None,
        "request_time": (datetime.now(tz=timezone.utc) - timedelta(seconds=3.2)).isoformat(),
        "response_time": datetime.now(tz=timezone.utc).isoformat()
    })

    # act
    response = client.post("/api/transactions", headers=header, json=data)

    # assert
    assert response.status_code == 201
    transaction = response.json()
    
    # Generation speed should be None for zero output tokens
    assert transaction["generation_speed"] is None

def test_transaction_generation_speed_with_embedding_model_returns_201_and_zero_speed(client, application, test_project):
    """Test generation speed calculation for embedding model (None output tokens)"""
    # arrange
    data = test_transaction.copy()
    
    # set date to 2024-11-03T12:00:00   
    request_time = datetime.fromisoformat("2024-11-03T12:00:00")
    response_time = request_time + timedelta(seconds=2.5)
    
    data.update({
        "model": "text-embedding-3-large",
        "type": "embedding",
        "input_tokens": 100,
        "output_tokens": None,  # Embedding models don't have output tokens
        "generation_speed": None,
        "request_time": request_time.isoformat(),
        "response_time": response_time.isoformat()
    })
    
    pytest.skip("todo: needs adding the output_tokens none verification")

    # act
    response = client.post("/api/transactions", headers=header, json=data)

    # assert
    assert response.status_code == 201
    transaction = response.json()
    
    # Generation speed should be 0 for None output tokens
    assert transaction["generation_speed"] == 0
    


def test_transaction_generation_speed_with_existing_value_returns_201_and_unchanged_speed(client, application, test_project):
    """Test that existing generation speed is not overwritten"""
    # arrange
    data = test_transaction.copy()
    
    request_time = datetime.fromisoformat("2024-11-03T12:00:00")
    response_time = request_time + timedelta(seconds=2)
    data.update({
        "model": "gpt-3.5-turbo-0125",
        "type": "chat",
        "input_tokens": 100,
        "output_tokens": 50,
        "generation_speed": 15.5,  # Pre-set generation speed
        "request_time": request_time.isoformat(),
        "response_time": response_time.isoformat()
    })

    # act
    response = client.post("/api/transactions", headers=header, json=data)

    # assert
    assert response.status_code == 201
    transaction = response.json()
    
    # Generation speed should remain unchanged
    assert transaction["generation_speed"] == 15.5

def test_transaction_generation_speed_with_fast_response_returns_201_and_calculated_speed(client, application, test_project):
    """Test generation speed calculation with very small time difference"""
    # arrange
    data = test_transaction.copy()
    request_time = datetime.now(tz=timezone.utc) 
    response_time = request_time + timedelta(milliseconds=10)
    data.update({
        "model": "gpt-3.5-turbo-0125",
        "type": "chat",
        "input_tokens": 100,
        "output_tokens": 500,
        "generation_speed": None,
        # Set request_time very close to current time
        "request_time": request_time.isoformat(),
        "response_time": response_time.isoformat()
    })

    # act
    response = client.post("/api/transactions", headers=header, json=data)

    # assert
    assert response.status_code == 201
    transaction = response.json()
    
    # Generation speed should be calculated even with very small time difference
    assert transaction["generation_speed"] > 0
    
    expected_speed = (data["output_tokens"] / (datetime.fromisoformat(data["response_time"]) - datetime.fromisoformat(data["request_time"])).total_seconds())
    

    assert expected_speed == pytest.approx(transaction["generation_speed"], rel=0.01)

    

def test_transaction_generation_speed_with_future_request_time_returns_201_and_null_speed(client, application, test_project):
    """Test generation speed calculation with future request time (edge case)"""
    # arrange
    data = test_transaction.copy()
    request_time = datetime.now(tz=timezone.utc) + timedelta(seconds=20)
    response_time = datetime.now(tz=timezone.utc)
    data.update({
        "model": "gpt-3.5-turbo-0125",
        "type": "chat",
        "input_tokens": 100,
        "output_tokens": 50,
        "generation_speed": None,
        # Set request_time in the future (edge case)
        "request_time": request_time.isoformat(),
        "response_time": response_time.isoformat()
    })

    pytest.skip("todo: needs adding check for future request time")

    # act
    response = client.post("/api/transactions", headers=header, json=data)

    # assert
    assert response.status_code == 201
    transaction = response.json()
    
    # Generation speed should still be calculated
    assert transaction["generation_speed"] is None




