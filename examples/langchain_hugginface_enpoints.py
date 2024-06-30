#%%
import os
from dotenv import load_dotenv, dotenv_values
from rich import print


config = dotenv_values(".env")


hf_key = config["HUGGINGFACEHUB_API_TOKEN"]

api_base_url = "https://kc55dk3asuq5aovy.us-east-1.aws.endpoints.huggingface.cloud"

print(
    f"HF api key={hf_key[0:3]}...{hf_key[-5:]}"
)
print(
    f"HF api endpoint={api_base_url[0:17]}..."
)
#%%

from langchain_huggingface import HuggingFaceEndpoint

llm = HuggingFaceEndpoint(
                endpoint_url=api_base_url,
                max_new_tokens=512,
                top_k=10,
                top_p=0.95,
                typical_p=0.95,
                temperature=0.01,
                repetition_penalty=1.03,
                huggingfacehub_api_token=hf_key,
                model="NousResearch/Hermes-2-Theta-Llama-3-8B"
            )

print(llm.invoke("Who is Adam Mickiewicz?"))
# %%

ps_proxy = "https://ps-proxy.azurewebsites.net/models-playground/hf_hermes"

llm = HuggingFaceEndpoint(
                endpoint_url=ps_proxy,
                max_new_tokens=512,
                top_k=10,
                top_p=0.95,
                typical_p=0.95,
                temperature=0.01,
                repetition_penalty=1.03,
                huggingfacehub_api_token=hf_key
            )

print(llm.invoke("Who is Adam Mickiewicz?"))
# %%
