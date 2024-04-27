---
title: "Quick Start Guide"
permalink: /docs/quick-start-guide/
excerpt: "How build docker images and run Prompt Sail on your local machine and make your first API call."
last_modified_at: 2023-12-28T15:18:35+01:00
redirect_from:
  - /theme-setup/
toc: true

---




## Run Prompt Sail on your local machine

Prompt Sail is build as a set of docker containers. One for backend (promptsail-backend) and one for frontend (promptsail-ui).

- **promptsail-backend** is a proxy that sits between your LLM framework of choice (LangChain, OpenAI python lib etc) and LLM provider API. It captures and logs all prompts and responses. 
- **promptsail-ui** is a user interface that allows you to view, search and analyze prompts and responses.


There are two options to run the Prompt Sail docker containers: 
* build the images from the source code or 
* pull the images from Github Container Repository (ghcr.io).



### Build the Docker images from the source code


Building from source will give the latest version of the code with the latest features, however, you could encounter uncatched bugs.  
{: .notice--warning}


Clone the repository from GitHub.

```bash
git clone https://github.com/PromptSail/prompt_sail.git
cd prompt_sail
``` 

Build the Docker images. It will build the images for backend and UI and pull mongodb and mongo-express images from Docker Hub.

```bash
docker-compose -f docker-compose-build.yml up --build
```


### Pull and run the Docker images from GHCR

Pulling the images from GHCR will give you the latest stable version of the code, however, you will not have the latest features.  
{: .notice--warning}


This will pull the images from the [GitHub Container Registry](https://github.com/orgs/PromptSail/packages?repo_name=prompt_sail)

The prepared docker-compose file will pull images with latest tags:

* [prompt_sail-backend](https://github.com/PromptSail/prompt_sail/pkgs/container/promptsail-backend)
* [prompt_sail-ui](https://github.com/PromptSail/prompt_sail/pkgs/container/promptsail-ui)
* [mongo](https://hub.docker.com/_/mongo)
* [mongo-express](https://hub.docker.com/_/mongo-express)

```bash
docker-compose -f docker-compose.yml up
``` 

All the environment variables are set in the [docker-compose.yml](https://github.com/PromptSail/prompt_sail/blob/main/docker-compose.yml)


### Check that the Docker containers are running


The UI should be running at [http://localhost:80/](http://localhost:80/) with default username and password `admin`:`password`. Default organization name will be `Default`. You can edit it in database using mongo-express.

The backend should be running at [http://localhost:8000/](http://localhost:8000/)

The mongo-express should be running at [http://localhost:8081/](http://localhost:8081/) with default username and password `admin`:`pass`

The mongo should be running at [http://localhost:27017/](http://localhost:27017/) with default username and password `root`:`password`

All of the above are set in the [docker-compose.yml](https://github.com/PromptSail/prompt_sail/blob/main/docker-compose.yml) file and can be changed there.

## Create your first project and add at least one AI provider

In the UI, go to your [Organization's dasboard](https://promptsail.github.io/prompt_sail/docs/organization-dashboard/). Using the [Add new project](https://promptsail.github.io/prompt_sail/docs/how-to-setup-llm-proxy-project/) form, create your first project and add at least one AI provider. 

## Make your first API call

### OpenAI Chat model example

Based on [How to store transactions from OpenAI via OpenAI Python SDK](https://github.com/PromptSail/prompt_sail/blob/examples/examples/openai_sdk_openai.ipynb) notebook.


Create .env file with your OpenAI API key and organization ID.

```bash
OPENAI_API_KEY=sk-xxx
OPENAI_ORG_ID=org-xxx
```

Import OpenAI class from `openai` module and create an instance of the class with your OpenAI API key and organization ID.



```python 

from openai import OpenAI
import os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
openai_org_id = os.getenv("OPENAI_ORG_ID")
```

Make an API call to OpenAI via Prompt Sail without tagging. 
What is and where to get **api_base** [see here](https://promptsail.github.io/prompt_sail/docs/storing-transactions/)

```python

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


Make an API call to OpenAI via Prompt Sail adding some tags for the transaction. 
How structure of **api_base** for passing tags looks like, [see here](https://promptsail.github.io/prompt_sail/docs/storing-transactions/)

```python

api_base = "http://localhost:8000/project1/openai/?tags=zero_shot,simple_prompt,dev1,poc&target_path="

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

Folder [examples](https://github.com/PromptSail/prompt_sail/tree/docs/examples) and [LLM Integration](/docs/llm-integrations/) section of the documentation contain more examples of how to make API calls to different LLM providers via Prompt Sail.