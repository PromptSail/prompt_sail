---
title: "Quick Start Guide"
permalink: /docs/quick-start-guide/
excerpt: "How to incorporate Prompt Sail into your LLM workflo"
last_modified_at: 2023-12-28T15:18:35+01:00
redirect_from:
  - /theme-setup/
toc: true

---




## Run the Prompt Sail Docker images on your local machine

Prompt Sail is build as a set of docker containers. One for backend (promptsail-backend) and one for frontend (promptsail-ui).

- **promptsail-backend** is a proxy that sits between your LLM framework of choice (LangChain, OpenAI python lib etc) and LLM provider API. It captures and logs all prompts and responses. 
- **promptsail-ui** is a user interface that allows you to view, search and analyze prompts and responses.


There are two options to run the Prompt Sail docker containers: build the images from the source code or pull the images from Docker Hub.

### Build the Docker images from the source code


Recommmened way is to build the Docker image from the source code via `docker-compose`.
{: .notice--success}


Clone the repository from GitHub.

```bash
git clone https://github.com/PromptSail/prompt_sail.git
cd prompt_sail
``` 

Build the Docker images. It will build the images for backend and UI and pull mongodb and mongo-express images from Docker Hub.

```bash
docker-compose up --build
```


### Pull and run the Docker images from Docker Hub


**Notice:** Currently, the docker image is not available on Docker Hub. Command below will not work yet.
{: .notice--warning}

```bash
docker run prompt-sail
``` 

### Check that the Docker containers are running


The UI should be running at [http://localhost:80/](http://localhost:80/) with default username and password `admin`:`password`. Default organization name will be `Default`. You can edit it in database using mongo-express.

The backend should be running at [http://localhost:8000/](http://localhost:8000/)

The mongo-express should be running at [http://localhost:8081/](http://localhost:8081/) with default username and password `admin`:`pass`

The mongo should be running at [http://localhost:27017/](http://localhost:27017/) with default username and password `root`:`password`

All of the above are set in the [docker-compose.yml](https://github.com/PromptSail/prompt_sail/blob/main/docker-compose.yml) file and can be changed there.


## Make your first API call

Folder [examples](https://github.com/PromptSail/prompt_sail/tree/docs/examples) and [LLM Integration](/docs/llm-integrations/) section of the documentation contain more examples of how to make API calls to different LLM providers via Prompt Sail.

### OpenAI Chat model example

Based on [How to store transactions from OpenAI via OpenAI Python SDK](https://github.com/PromptSail/prompt_sail/blob/examples/examples/openai_sdk_openai.ipynb) notebook.


Create .evn file with your OpenAI API key and organization ID.

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