from utils import MockResponse


def test_transaction_openai_ok(client, application, monkeypatch):
    # arrange
    def mock_post(*args, **kwargs):
        return MockResponse(
            200,
            {
                "id": "chatcmpl-9OF7xvrxwC860PkaQUGuNv7DX2EXC",
                "object": "chat.completion",
                "created": 1715565049,
                "model": "gpt-3.5-turbo-0125",
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": "Yes, I am sure. The concept of the soul is a complex and abstract idea that falls outside the realm of scientific inquiry. While science can study physical and biological aspects of life, consciousness, spirituality, and the existence of the soul are topics that are typically discussed in philosophy, religion, and other non-scientific disciplines. As a biology teacher, my focus is on teaching scientifically-supported information about the physical aspects of life and living organisms.",
                        },
                        "logprobs": None,
                        "finish_reason": "stop",
                    }
                ],
                "usage": {
                    "prompt_tokens": 305,
                    "completion_tokens": 89,
                    "total_tokens": 394,
                },
                "system_fingerprint": None,
            },
        )

    monkeypatch.setattr(client, "post", mock_post)

    # act
    resp = client.post(
        "/project1/openai/chat/completions",
        {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a teacher and help kids learn biology.",
                },
                {"role": "user", "content": "Name the elements of human body."},
            ],
        },
    )

    # assert
    assert resp.status_code == 200
    assert resp.json()["object"] == "chat.completion"
    assert resp.json()["model"] == "gpt-3.5-turbo-0125"
    assert len(resp.json()["choices"]) == 1
    assert resp.json()["usage"]["prompt_tokens"] == 305
    assert resp.json()["usage"]["completion_tokens"] == 89


def test_transaction_openai_unauthorized(client, application, monkeypatch):
    # arrange
    def mock_post(*args, **kwargs):
        return MockResponse(
            401,
            {
                "error": {
                    "message": "You didn't provide an API key. You need to provide your API key in an Authorization header using Bearer auth (i.e. Authorization: Bearer YOUR_KEY), or as the password field (with blank username) if you're accessing the API from your browser and are prompted for a username and password. You can obtain an API key from https://platform.openai.com/account/api-keys.",
                    "type": "invalid_request_error",
                    "param": None,
                    "code": None,
                }
            },
        )

    monkeypatch.setattr(client, "post", mock_post)

    # act
    resp = client.post(
        "/project1/openai/chat/completions",
        {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a teacher and help kids learn biology.",
                },
                {"role": "user", "content": "Name the elements of human body."},
            ],
        },
    )

    # assert
    assert resp.status_code == 401
    assert resp.json()["error"]["type"] == "invalid_request_error"
    assert (
        resp.json()["error"]["message"]
        == "You didn't provide an API key. You need to provide your API key in an Authorization header using Bearer auth (i.e. Authorization: Bearer YOUR_KEY), or as the password field (with blank username) if you're accessing the API from your browser and are prompted for a username and password. You can obtain an API key from https://platform.openai.com/account/api-keys."
    )


def test_transaction_azure_ok(client, application, monkeypatch):
    # arrange
    def mock_post(*args, **kwargs):
        return MockResponse(
            200,
            {
                "choices": [
                    {
                        "content_filter_results": {
                            "hate": {"filtered": False, "severity": "safe"},
                            "self_harm": {"filtered": False, "severity": "safe"},
                            "sexual": {"filtered": False, "severity": "safe"},
                            "violence": {"filtered": False, "severity": "safe"},
                        },
                        "finish_reason": "stop",
                        "index": 0,
                        "message": {
                            "content": "1. Identify and pursue your passions and interests.\n2. Set and work towards achievable goals.\n3. Prioritize your physical and mental health by eating well, staying active, and seeking support when you need it.\n4. Cultivate strong, meaningful relationships with family and friends.\n5. Practice gratitude and mindfulness to appreciate the present moment.\n6. Continue learning and growing through education, experiences, and new perspectives.\n7. Find purpose and fulfillment in your work or hobbies.\n8. Contribute to your community through acts of kindness and service.\n9. Manage stress and prioritize self-care to maintain balance in your life.\n10. Keep an open mind and be adaptable to change.",
                            "role": "assistant",
                        },
                    }
                ],
                "created": 1715565752,
                "id": "chatcmpl-9OFJIogUNTVPZdDYf2zv9sr42Hr7Q",
                "model": "gpt-35-turbo",
                "object": "chat.completion",
                "prompt_filter_results": [
                    {
                        "prompt_index": 0,
                        "content_filter_results": {
                            "hate": {"filtered": False, "severity": "safe"},
                            "self_harm": {"filtered": False, "severity": "safe"},
                            "sexual": {"filtered": False, "severity": "safe"},
                            "violence": {"filtered": False, "severity": "safe"},
                        },
                    }
                ],
                "system_fingerprint": "fp_2f57f81c11",
                "usage": {
                    "completion_tokens": 136,
                    "prompt_tokens": 15,
                    "total_tokens": 151,
                },
            },
        )

    monkeypatch.setattr(client, "post", mock_post)

    # act
    resp = client.post(
        "/project1/azure/openai/deployments/gpt-35-turbo-test/chat/completions",
        {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "What to do to live good life."}],
        },
    )

    # assert
    assert resp.status_code == 200
    assert len(resp.json()["choices"]) == 1
    assert resp.json()["choices"][0]["finish_reason"] == "stop"
    assert resp.json()["choices"][0]["message"]["role"] == "assistant"
    assert resp.json()["object"] == "chat.completion"
    assert resp.json()["model"] == "gpt-35-turbo"
    assert resp.json()["usage"]["prompt_tokens"] == 15
    assert resp.json()["usage"]["completion_tokens"] == 136


def test_transaction_azure_unauthorized(client, application, monkeypatch):
    # arrange
    def mock_post(*args, **kwargs):
        return MockResponse(
            401,
            {
                "statusCode": 401,
                "message": "Unauthorized. Access token is missing, invalid, audience is incorrect (https://cognitiveservices.azure.com), or have expired.",
            },
        )

    monkeypatch.setattr(client, "post", mock_post)

    # act
    resp = client.post(
        "/project1/azure/openai/deployments/gpt-35-turbo-test/chat/completions",
        {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "What to do to live good life."}],
        },
    )

    # assert
    assert resp.status_code == 401
    assert (
        resp.json()["message"]
        == "Unauthorized. Access token is missing, invalid, audience is incorrect (https://cognitiveservices.azure.com), or have expired."
    )


def test_transaction_anthropic_ok(client, application, monkeypatch):
    # arrange
    def mock_post(*args, **kwargs):
        return MockResponse(
            200,
            {
                "id": "msg_01W9Hw1AUuPmms7mV373ZmKC",
                "type": "message",
                "role": "assistant",
                "model": "claude-3-opus-20240229",
                "stop_sequence": None,
                "usage": {"input_tokens": 10, "output_tokens": 12},
                "content": [
                    {"type": "text", "text": "Hello! How can I assist you today?"}
                ],
                "stop_reason": "end_turn",
            },
        )

    monkeypatch.setattr(client, "post", mock_post)

    # act
    resp = client.post(
        "/project1/anthropic/v1/messages",
        {
            "model": "claude-3-opus-20240229",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": "Hello, world"}],
        },
    )

    # assert
    assert resp.status_code == 200
    assert resp.json()["type"] == "message"
    assert resp.json()["role"] == "assistant"
    assert resp.json()["model"] == "claude-3-opus-20240229"
    assert resp.json()["usage"]["input_tokens"] == 10
    assert resp.json()["usage"]["output_tokens"] == 12
    assert len(resp.json()["content"]) == 1
    assert resp.json()["content"][0]["type"] == "text"
    assert resp.json()["content"][0]["text"] == "Hello! How can I assist you today?"
    assert resp.json()["stop_reason"] == "end_turn"


def test_transaction_anthropic_unauthorized(client, application, monkeypatch):
    # arrange
    def mock_post(*args, **kwargs):
        return MockResponse(
            401,
            {
                "type": "error",
                "error": {
                    "type": "authentication_error",
                    "message": "x-api-key header is required",
                },
            },
        )

    monkeypatch.setattr(client, "post", mock_post)

    # act
    resp = client.post(
        "/project1/anthropic/v1/messages",
        {
            "model": "claude-3-opus-20240229",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": "Hello, world"}],
        },
    )

    # assert
    assert resp.status_code == 401
    assert resp.json()["type"] == "error"
    assert resp.json()["error"]["type"] == "authentication_error"
    assert resp.json()["error"]["message"] == "x-api-key header is required"
