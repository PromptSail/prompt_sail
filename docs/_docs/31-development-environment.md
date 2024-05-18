---
title: "Development environment"
permalink: /docs/development-environment/
excerpt: "How to setup development environment for Prompt Sail."
last_modified_at: 2024-05-18T09:48:35+01:00
redirect_from:
  - /theme-setup/
toc: true
toc_sticky: true
---

## Development environment




### Backend

If you want to start contributing to Prompt Sail you need to clone our repository first.

```bash
mkdir prompt_sail
cd prompt_sail
git clone https://github.com/PromptSail/prompt_sail.git
```

In this section we will focus on the backend, so you need to make sure you have it installed:
- [Python version 3.10+](https://www.python.org/downloads/release/python-3100/) 
- [Poetry version 1.7.1+](https://python-poetry.org/)
- [make](https://gnuwin32.sourceforge.net/packages/make.htm)

When you have the above dependencies, you can proceed to install packages using poetry. To do this, use the following commands:
```bash
cd backend
poetry install
poetry shell
```

Now set the environment variables. Go to the backend folder and create an `.env` file and then fill in the variables as in the example below:
```bash
touch .env
nano .env
```

And pase and edit the following variables in the `.env` file:
```python
DEBUG=True
OPENAI_API_KEY="sk-your-api-key"
MONGO_URL="mongodb://root:password@localhost:27017"
BASE_URL="http://promptsail.local:8000"
ORGANIZATION_NAME="your-organization-name"
ADMIN_PASSWORD="your-admin-password"
```


Remember that you need a working instance of the mongoDB database for the backend to work properly. You can run it for example from the docker position. To do this, use the following command:
```bash
docker run -d -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=password --name mongodb mongo:latest
```


Once you've done that then return to the project's main folder and use the make command used to run the project locally:
```bash
cd ..
make run-dev
```




### Frontend

todo: how to run project locally, libraries, node version, ant desing config etc.




### Database

We use MoongoDB as a database. Its schema is described in the section [Database Schema](/docs/database-schema/).


### Github Actions

How we use Github Actions to automate the testing and deployment process.


