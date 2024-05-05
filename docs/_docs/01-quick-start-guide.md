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

- **promptsail-backend** is a proxy that sits between your LLM framework of choice (LangChain, OpenAI python lib etc) and LLM provider API. You change `api_base` to point to Prompt Sail `proxy_url` and then it will captures and logs all your prompts and responses. 
- **promptsail-ui** is a user interface that allows you to view, search and analyze all transactions (prompts and responses).


There are two options to run the Prompt Sail docker containers: 
* [build the images from the source code](#build-the-docker-images-from-the-source-code) or 
* [pull the images from Github Container Repository (ghcr.io)](#pull-and-run-the-docker-images-from-ghcr).



### Build the Docker images from the source code


Building from source will give you the latest version of the code with the newest features. However, please note that there might be uncaught bugs that could affect the stability of the application.
{: .notice--warning}


Clone the repository from GitHub.

```bash
git clone https://github.com/PromptSail/prompt_sail.git
cd prompt_sail
``` 

To build the Docker images, execute the following command. This will build the images for the backend and UI, and pull the MongoDB and Mongo Express images from Docker Hub.
All environment variables are set for you, but you can change them. 
```bash
docker-compose -f docker-compose-build.yml up --build
```


### Pull and run the Docker images from GHCR

Pulling the images from GHCR will give you the latest stable version of the code, however, you will not have the latest features.  
{: .notice--warning}



The prepared docker-compose file will pull Prompt Sail (backend,ui) images from [GitHub Container Registry](https://github.com/orgs/PromptSail/packages?repo_name=prompt_sail) with `latest` tags, also it will pull the latest mongo and mongo-express images from Docker Hub:

* [prompt_sail-backend ](https://github.com/PromptSail/prompt_sail/pkgs/container/promptsail-backend)(ghcr.io package)
* [prompt_sail-ui](https://github.com/PromptSail/prompt_sail/pkgs/container/promptsail-ui)(ghcr.io package)
* [mongo](https://hub.docker.com/_/mongo)
* [mongo-express](https://hub.docker.com/_/mongo-express)

```bash
docker-compose -f docker-compose.yml up
``` 

If you want to run the dev version of the images, you can pull the `dev-release` tag insted of `latest`. More on image tagging strategy and deployments you will find at [Deployment Cookbook - Local Deployment](/docs/deploy-promptsail-local/#Pull-and-run-the-Docker-images-from-GHCR) section.


All the environment variables are set to default and non-production deployment in the [docker-compose.yml](https://github.com/PromptSail/prompt_sail/blob/main/docker-compose.yml) it is recommended to change them to your own values. 



### Check that the Docker containers are running



🖥️ **User Interface (UI)**

The UI should be up and running at [http://localhost:80/](http://localhost:80/). 
- Default login credentials: `admin`:`password`
- Default organization name: `Default`
- 🛠️ You can edit the organization name in the database using mongo-express.


🔧 **Backend Service (API)**

The backend services should be operational at [http://localhost:8000/](http://localhost:8000/). 
- Swagger UI can be accessed at [http://localhost:8000/docs/](http://localhost:8000/docs/).




🗄️ **MongoDB**

The MongoDB database should be running at [http://localhost:27017/](http://localhost:27017/). 
- Default login credentials: `root`:`password`
- Default database name: `prompt_sail`
- Default folder for storing data will be located in the root directory of the project in the `data/mongo` folder.


📊 **Mongo-Express**

Mongo-Express acts as a web-based MongoDB admin interface. It should be accessible at [http://localhost:8081/](http://localhost:8081/). 
- Default login credentials: `admin`:`pass`
- It is not necessary to use Mongo-Express to run Prompt Sail, but it can be helpful for debugging and monitoring the database.


**All the settings** can be changed in the appropriate `dokcer-compose` files: 

* for pulled images in [docker-compose.yml](https://github.com/PromptSail/prompt_sail/blob/main/docker-compose.yml) 
* for build images in [docker-compose-build.yml](https://github.com/PromptSail/prompt_sail/blob/main/docker-compose-build.yml)



## Create your first project and add at least one AI provider

In the UI, go to your [Organization's dasboard](/docs/organization-dashboard/). Using the [Add new project](/docs/how-to-setup-llm-proxy-project/) form, create your first project and add at least one AI provider. 


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

## More examples

You can find more examples as jupyter notebooks in the repository folder [prompt_sail/examples](https://github.com/PromptSail/prompt_sail/tree/docs/examples). 

All tested integraion are documented in [LLM Integration](/docs/llm-integrations/) section.