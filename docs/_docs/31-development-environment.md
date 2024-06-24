---
title: "Development environment"
permalink: /docs/development-environment/
excerpt: "How to setup development environment for Prompt Sail."
last_modified_at: 2024-05-30T14:43:00+01:00
redirect_from:
    - /theme-setup/
toc: true
toc_sticky: true
---

If you want to start contributing to Prompt Sail you need to clone our repository first.

```bash
mkdir prompt_sail
cd prompt_sail
git clone https://github.com/PromptSail/prompt_sail.git
```

### Backend

In this section we will focus on the backend, so you need to make sure you have it installed:

-   [Python version 3.10+](https://www.python.org/downloads/release/python-3100/)
-   [Poetry version 1.7.1+](https://python-poetry.org/)
-   [make](https://gnuwin32.sourceforge.net/packages/make.htm)

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
SSO_AUTH: "False"
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

In this section we will focus on the frontend, so you need to make sure you have it installed:

-   [Node.js v20](https://nodejs.org/en/download)
-   [Node Pack Manager](https://www.npmjs.com/package/npm)

When you have the above dependencies, you can proceed to install node modules using node pack manager. To do this, use the following commands:

```bash
cd ui
npm ci
```

Project can be run in two modes: **development** and **production**. Development mode is used for local development and testing purposes. Production mode is used when project is deployed on a server.

Create an `.env.{mode}` file where `{mode}` is `production` or `development`. The `.env.production` file should already be created in the `/ui` folder. The next steps show how to create the `.env.development` file, but they also work for the `.env.production` file.

```bash
<!-- Linux/macOS -->
touch .env.development
nano .env.development
```

```
<!-- Windows: create and edit via notepad -->
notepad .env.development
```

Paste and adjust for yourself the following variables in the `.env` file:

```python
PORT = 80
BACKEND_URL = "http://promptsail-backend:8000"
PROXY_URL_HOST = "http://localhost:8000"

// Optional: check https://promptsail.com/docs/sso-configuration/
SSO_GOOGLE_CLIENT_ID = "*****.apps.googleusercontent.com"
SSO_AZURE_CLIENT_ID = "6fe*******aaa"
SSO_AZURE_TENANT = "4a1******aaa"
SSO_AZURE_SCOPES = "user.read"
SSO_AZURE_AUTHORITY = "https://login.microsoftonline.com/4a1*****aaa"
```

After install dependencies and set environment variables, you can run the project.

**Remember that you need a working instance of the backend for the frontend to work properly.**

-   #### Run in development mode
    You can run the app in development mode using `start` script from `package.json` via node package manager:
    ```
    npm start
    ```
-   #### Run in production mode

    Build the app using `build` script from `package.json:

    ```
    npm run build
    ```

    After build is done, you can run the app using `preview` script from `package.json` which will start a local server with the built files:

    ```
    npm run preview
    ```

Head to link which is displayed in console after running one of the modes above and start contributing!

### Database

We use MoongoDB as a database. Its schema is described in the section [Database Schema](/docs/database-schema/).

### Github Actions

How we use Github Actions to automate the testing and deployment process.
