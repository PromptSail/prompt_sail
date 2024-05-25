# %%

# https://aws.amazon.com/blogs/aws/amazon-bedrock-is-now-generally-available-build-and-scale-generative-ai-applications-with-foundation-models/?trk=55dc591c-143b-4ecb-898e-fa3dcd67469e&sc_channel=el

import json

import boto3

# bedrock = boto3.client(service_name="bedrock", region_name="us-east-1")

# bedrock.list_foundation_models()
# %%
bedrock_runtime = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")

modelId = "amazon.titan-text-express-v1"
accept = "application/json"
contentType = "application/json"

# "{\"inputText\":\"Hello\\n\\nHello! How can I help you?\",\"textGenerationConfig\":{\"maxTokenCount\":2048,\"stopSequences\":[\"User:\"],\"temperature\":0,\"topP\":0.9}}

body = json.dumps(
    {
        "inputText": "Knock, knock!",
    }
)
# https://bedrock-runtime.us-east-1.amazonaws.com/+/model/{modelId}/invoke
response = bedrock_runtime.invoke_model(
    body=body, modelId=modelId, accept=accept, contentType=contentType
)

response_body = json.loads(response.get("body").read())
# %%
print(response_body)
