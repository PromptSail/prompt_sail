---
title: "Run Prompt Sail on your local machine via docker"
permalink: /docs/deploy-promptsail-local/
excerpt: "How run Prompt Sail on your local machine via docker."
last_modified_at: 2024-05-05T11:18:35+01:00
redirect_from:
  - /theme-setup/
toc: true

---




## Run Prompt Sail on your local machine

Prompt Sail is build as a set of docker containers:

- **promptsail-backend** is a proxy that sits between your LLM framework of choice (LangChain, OpenAI python lib etc) and LLM provider API. You change `api_base` to point to Prompt Sail `proxy_url` and then it will captures and logs all your prompts and responses. 
- **promptsail-ui** is a user interface that allows you to view, search and analyze all transactions (prompts and responses)
- **mongo** is a database that stores all the transactions
- **mongo-express** is a web-based MongoDB admin interface that allows you to view and edit the database. Not necessary for running Prompt Sail, but can be helpful for debugging and monitoring the database.

We have prepared a set of docker-compose files that will run all the services for you. Do not hesitate to change the settings in the `docker-compose` files to your own values.


There are a few options to run the Prompt Sail docker containers: 
* [build the images from the source code](#build-the-docker-images-from-the-source-code) - good for developement and testing
* [pull the images from Github Container Repository (ghcr.io)](#pull-and-run-the-docker-images-from-ghcr) - good for production with some changes in the environment variables.



### Build the Docker images from the source code


Building from source will give you the latest version of the code with the newest features. However, please note that there might be uncaught bugs that could affect the stability of the application.
{: .notice--warning}


Clone the repository from GitHub.

```bash
git clone https://github.com/PromptSail/prompt_sail.git
cd prompt_sail
``` 

To build the Docker images use prepared `docker-compose-build.yml` file. 

The command below will build the images for the backend and UI, and pull the MongoDB and Mongo Express images from Docker Hub.

All environment variables are set for you, but you can change them. 
```bash
docker-compose -f docker-compose-build.yml up --build
```


### Pull and run the Docker images from GHCR

Pulling the images from GHCR will give you the latest stable version of the code, however, you will not have the latest features.  
{: .notice--warning}
change to reflect changes that this documentation describe deployment on google cloud platfrom gcp


The prepared `docker-compose.yml` file will pull Prompt Sail (backend,ui) images from [GitHub Container Registry](https://github.com/orgs/PromptSail/packages?repo_name=prompt_sail) with `latest` tag, also it will pull the latest mongo and mongo-express images from Docker Hub:

* [prompt_sail-backend ](https://github.com/PromptSail/prompt_sail/pkgs/container/promptsail-backend)(ghcr.io package)
* [prompt_sail-ui](https://github.com/PromptSail/prompt_sail/pkgs/container/promptsail-ui)(ghcr.io package)
* [mongo](https://hub.docker.com/_/mongo)
* [mongo-express](https://hub.docker.com/_/mongo-express)

```bash
docker-compose -f docker-compose.yml up
``` 

### Images tags

There are three main image tags used for tagging the images in the GitHub Container Registry:

* `latest` - the latest stable version of the code, build after each version release
* `relese-candidate` - the latest release candidate version of the code, build after each push or merge pull request to the main branch, trade-off between the latest features and stability
* `dev-release` - the latest dev version of the code, build after each push to the dev branch, the most recent version of the code

You can set the environment variable `PROMPTSAIL_TAG` to one of the above tags to pull the appropriate version of the images. If you do not set the `PROMPTSAIL_TAG` environment variable, the `latest` tag will be used by default.


To automate setting the `PROMPTSAIL_TAG` environment variable, you can use a `.env` file. Docker Compose automatically looks for this file in the directory where you run the `docker-compose` command and uses the environment variables defined in it.


Example `.env` file:
```
PROMPTSAIL_TAG=latest
```

### Service configuration

All the environment variables are set to default and non-production deployment in the [docker-compose.yml](https://github.com/PromptSail/prompt_sail/blob/main/docker-compose.yml) it is recommended to change them to your own values. 



🗄️ **MongoDB settings**


The MongoDB database should be running at [http://localhost:27017/](http://localhost:27017/). 
- Default login credentials: `root`:`password`
- Default database name: `prompt_sail`
- Default folder for storing data will be located in the root directory of the project in the `data/mongo` folder.

For production deployment, it is recommended to change:
* `MONGO_INITDB_ROOT_USERNAME` and `MONGO_INITDB_ROOT_PASSWORD` environment variables to your own values
* `volumes` to store the data in a different location


```
  mongodb:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - ./data/mongo:/data/db
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: password
    healthcheck:
      test: echo 'db.runCommand("ping").ok' | mongosh localhost:27017/test --quiet
      interval: 10s
      timeout: 10s
      retries: 5
      start_period: 40s
```


🔧 **promptsail-backend**


Backend Service (API) by default should be operational at [http://localhost:8000/](http://localhost:8000/). 
- Swagger UI can be accessed at [http://localhost:8000/docs/](http://localhost:8000/docs/).


```
  promptsail-backend:
    image: ghcr.io/promptsail/promptsail-backend:${PROMPTSAIL_TAG:-latest}
    container_name: promptsail-backend
    ports:
      - "8000:8000"
    environment:
      BASE_URL: "http://localhost:8000"
      STATIC_DIRECTORY: "/static"
      MONGO_URL: "mongodb://root:password@mongodb:27017"
      ORGANIZATION_NAME: "Default"
      ADMIN_PASSWORD: "password"
```

Be shure to check the `BASE_URL` and `MONGO_URL` environment variables. The `BASE_URL` should be set and is needed by UI, and the `MONGO_URL` should point to the MongoDB service, by default uses `root`:`password` credentials.



🖥️ **User Interface (UI)**

The UI should be up and running at [http://localhost:80/](http://localhost:80/). 
- Default login credentials: `admin`:`password`
- Default organization name: `Default`
- 🛠️ You can edit the organization name in the database using mongo-express.


```
  promptsail-ui:
    image: ghcr.io/promptsail/promptsail-ui:${PROMPTSAIL_TAG:-latest}
    container_name: promptsail-ui
    ports:
      - "80:80"
    environment:
      BACKEND_URL: "http://promptsail-backend:8000"
      PROXY_URL_HOST: "http://localhost:8000"
    depends_on:
        mongodb:
            condition: service_started
        promptsail-backend:
            condition: service_started
```

* `BACKEND_URL` should point to the backend service the url should be available from UI docker container.
* `PROXY_URL_HOST` is used to properly set the proxy url for creating the links to ai providers, this should point to public url of the backend service host. 



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


### Troubleshooting

Community FAQ and troubleshooting. If you have any issues and been able to solve them, please share your solution with the community. 
{: .notice--info}