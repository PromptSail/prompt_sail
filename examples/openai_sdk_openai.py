# %%
from openai import OpenAI
import os
from dotenv import load_dotenv, dotenv_values
from pprint import pprint

config = dotenv_values(".env")

openai_key = config["OPENAI_API_KEY"]
openai_org_id = config["OPENAI_ORG_ID"]
print(
    f"OpenAI api key={openai_key[0:3]}...{openai_key[-3:]}"
)


# %%
ps_api_base = "http://localhost:8000/project1/openai"

#ps_api_base = "http://promptsail.local:8000/project1/?model=model1&tags=tag1,tag2&experiment=exp1&target_path="

#ps_api_base = "https://api.openai.com/v1/model1/"

ps_client = OpenAI(
    base_url=ps_api_base, 
    api_key=openai_key, max_retries=0)


response = ps_client.chat.completions.create(
    model="gpt-3.5-turbo",
    timeout=1000, 
    extra_headers={ "accept-encoding": "deflate"},
    messages=[
        {
            "role": "system",
            "content": "Yoda assistant you are, skilled in explaining complex life and phisopical matters.",
        },
        {
            "role": "user",
            "content": "What number 42 means",
        },
    ],
)

pprint(response.choices[0].message.content)
# %%
