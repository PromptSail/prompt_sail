import os

from dotenv import load_dotenv
from langchain.llms import OpenAI

load_dotenv()


print("Using key", os.environ["OPENAI_API_KEY"])


llm = OpenAI(
    model_name="text-davinci-003",
    openai_api_base="http://project2.promptsail.local:8000",
)
output = llm("Explaining the meaning of life in one sentence")
print(output)
