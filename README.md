

<p align="center">
  <p align="center">
    <a href="https://promptsail.com/?utm_source=github&utm_medium=logo" target="_blank">
      <img src="docs/assets/images/Logo-teal_black.png" alt="Prompt Sail" width="390" height="91">
    </a>
  </p>
  <p align="center">
    LLM’s proxy for prompt and response governance, monitoring, and analysis. 📊🔍
  </p>
</p>

> ⚠️ **Prompt Sail is currently in Development**: Expect breaking changes and bugs! Feedback and contributions are welcome. Please see the [Contributing Guide](CONTRIBUTING.md) for more information.

<p align="center">
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
  <img alt="GitHub License" src="https://img.shields.io/github/license/promptsail/prompt_sail">
<img alt="GitHub Actions Workflow Status" src="https://img.shields.io/github/actions/workflow/status/promptsail/prompt_sail/docker-publish.yml?label=Build%20and%20Publish%20Docker">
<img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/m/promptsail/prompt_sail"/>
  <img alt="Github Last Commit" src="https://img.shields.io/github/last-commit/promptsail/prompt_sail"/>
<img alt="Github Contributors" src="https://img.shields.io/github/contributors/promptsail/prompt_sail"/>
  <img alt="GitHub closed issues" src="https://img.shields.io/github/issues-closed/promptsail/prompt_sail"/>

</p>


## What is Prompt Sail? 

Prompt Sail is a proxy for Large Language Models (LLMs) API's such as OpenAI GPT models, Azure OpenAI, Anthropic Clude etc. that allows you to record prompts and responses, analyze costs, generation speed, compare and track trends and changes across various models and projects over time.

To learn more about Prompt Sail’s features and capabilities, see 

* [Documentation](https://promptsail.github.io/prompt_sail/) 📖
* [Examples](https://github.com/PromptSail/prompt_sail/tree/main/examples) 💻
    * [OpenAI SDK -> OpenAI API](/examples/openai_sdk_openai.ipynb)
    * [Langchain SDK -> OpenAI API](/examples/langchain_openai.ipynb)
    * [OpenAI SDK -> Azure OpenAI](/examples/openai_sdk_azure_openai.ipynb)
    * [Langchain SDK -> Azure OpenAI](/examples/langchain_azure_openai.ipynb)
    * [Langchain SDK -> Azure OpenAI Ada embeddings](/examples/langchain_azure_oai_embeddings.ipynb)

<!-- * [API Reference](https://promptsail.github.io/prompt_sail/api/). -->

## Getting started 🚀

The simplest way to try Prompt Sail is to create a project on https://try.promptsail.com and integrate it with 
your code.

If you prefer to install and manage Prompt Sail yourself, you can build or download a docker image and run it locally.

## Run Prompt Sail locally via Docker Compose 🐳

To try out Start Prompt on your own machine, we recommend using docker-compose. Docker images are available from ...

### Requirements 📋

* installed docker and docker-compose on your machine [Windows](https://docs.docker.com/docker-for-windows/install/) | [Mac](https://docs.docker.com/docker-for-mac/install/) | [Linux](https://docs.docker.com/engine/install/ubuntu/)
* git clone repository and navigate to main directory
```bash
git clone https://github.com/PromptSail/prompt_sail.git
cd prompt_sail
```



### Build docker images 🏗️

Build and run the docker image:

```bash
docker-docker-compose up --build
```


### Create a project 📝

Navigate to http://localhost:80 and add you AI provider of choice. 


### Modify your code to use Prompt Sail proxy 👨‍💻

To use Prompt Sail with `openai` Python library, you need to set `OPENAI_API_BASE` environment variable, or
modify `openai.api_base` parameter to point to your Prompt Sail project.

```python
from openai import OpenAI
import os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
openai_org_id = os.getenv("OPENAI_ORG_ID")

api_base = "http://localhost:8000/project1/openai/"

ps_client = OpenAI(
    base_url=api_base,
    api_key=openai_key,
)

response = ps_client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair.",
        },
        {
            "role": "user",
            "content": "Compose a poem that explains the concept of recursion in programming.",
        },
    ],
)

pprint(response.choices[0].message)
```

Using Prompt Sail with `langchain` is similar:
```python
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.schema import HumanMessage, SystemMessage

haiku_prompt = [
    SystemMessage(
        content="You are a poetic assistant, skilled in explaining complex programming concepts with creative flair.",
    ),
    HumanMessage(
        content="Compose a haiku that explains the concept of recursion in programming.",
    ),
]
chat = ChatOpenAI(
    temperature=0.9,
    openai_api_key=openai_key,
    openai_organization=openai_org_id,
    model="gpt-3.5-turbo-1106",
)

chat(haiku_prompt)
```

## Contact 📞

- Bugs & requests: file a GitHub ticket 🐞
- For business inquiries: email contact@promptsail.com. 📧
- Our website: [https://promptsail.com](https://promptsail.com) 🌐


## License 📜

Prompt Sail is free and open source, under the [MIT license](LICENSE).

