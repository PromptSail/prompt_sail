---
title: "How to deploy Prompt Sail on Azure"
permalink: /docs/deploy-promptsail-azure
excerpt: "How to deploy Prompt Sail on Azure, AWS, GCP, or your local machine."
last_modified_at: 2024-05-05T11:48:05+01:00
redirect_from:
  - /theme-setup/
toc: true
toc_sticky: true
---


## Azure Deployment with PROXY and UI as different services

### PROXY Setup

1. Go to [Create a resource](https://portal.azure.com/#create/hub) webpage and select `Create` under `Web App` section.
![Photo 1]({{ site.url }}{{ site.baseurl }}assets/images/azure-deploy-1.png)
2. On the first page you need to specify (1) `Resource Group` that you will use to deploy promptsail proxy, (2) `name of the instance` and (3) `publish type`. Then press (4) `Next`.
![Photo 2]({{ site.url }}{{ site.baseurl }}assets/images/azure-deploy-2.png)
3. In the `Container` tab you need to specify `Image Source` as (1) `Docker Hub or other registries` and as a `Options` the (2) `Single Container`. Now you need to provide Registry server URL (3) - `https://ghcr.io/` and Image and tag in this case should be `promptsail/promptsail-backend:lastest` (4).
![Photo 3]({{ site.url }}{{ site.baseurl }}assets/images/azure-deploy-3b.png)
4. Now you can press the `Review + create` button then `Create`.
5. When your proxy web app is created, go to `Overview` page of your app (1), then you need to move to the `Environment Variables` (2) using left navigation bar.
![Photo 4]({{ site.url }}{{ site.baseurl }}assets/images/azure-deploy-5.png)
6. Here you need to add backend (proxy) environment variables. You can do this by hand (1) using `Add` option or pasting pre-created variables using `Advanced edit` (2).
![Photo 5]({{ site.url }}{{ site.baseurl }}assets/images/azure-deploy-6.png)
Example pre-created variables for your proxy:


```json
[
  {
    "name": "AZURE_CLIENT_ID",
    "value": "d3bxyz-xxxx-xxxx-xxxx-d0xyzxyzd9",
    "slotSetting": false
  },
  {
    "name": "BASE_URL",
    "value": "https://<your-proxy-name>.azurewebsites.net",
    "slotSetting": false
  },
  {
    "name": "DOCKER_ENABLE_CI",
    "value": "true",
    "slotSetting": false
  },
  {
    "name": "DOCKER_REGISTRY_SERVER_URL",
    "value": "https://ghcr.io/",
    "slotSetting": false
  },
  {
    "name": "MONGO_URL",
    "value": "mongodb://<some-credentials>",
    "slotSetting": false
  },
  {
    "name": "ORGANIZATION_NAME",
    "value": "Prompt Sail",
    "slotSetting": false
  },
  {
    "name": "SSO_AUTH",
    "value": "True",
    "slotSetting": false
  },
  {
    "name": "WEBSITE_HEALTHCHECK_MAXPINGFAILURES",
    "value": "10",
    "slotSetting": false
  },
  {
    "name": "WEBSITES_ENABLE_APP_SERVICE_STORAGE",
    "value": "false",
    "slotSetting": false
  }
]
```


Remember! You need to edit those variables:
- set `AZURE_CLIENT_ID` as your Client ID [(here you can find how to setup auth)](docs/sso-configuration/)
- set `PROMPT_SAIL_ENV_PLACEHOLDER_PROXY_URL_HOST` as `https://` + (2.2.) `name of the instance` + `.azurewebsites.net`
- set `MONGO_URL` as your MongoDB connection string (you can create instance of MongoDB for example using Azure Cosmos)

Other variables can remain unchanged, although we recommend changing the value of `ORGANIZATION_NAME`.

7. After applying changes redirect to `Overwiew` page and press `Restart` button.
![Photo 6]({{ site.url }}{{ site.baseurl }}assets/images/azure-deploy-7.png)


### UI Setup

1. The first steps look essentially the same as for creating a proxy application. You can repeat the first two steps.
2. In the `Container` tab you need to specify `Image Source` as (1) `Docker Hub or other registries` and as a `Options` the (2) `Single Container`. Now you need to provide Registry server URL (3) - `https://ghcr.io/` and Image and tag in this case should be `promptsail/promptsail-ui:lastest`.
![Photo 1]({{ site.url }}{{ site.baseurl }}assets/images/azure-deploy-3c.png)
3. After creating UI web app go to `Overview` page of your app, then you need to move to the `Environment Variables` using left navigation bar.
4. Here you need to add frontend (UI) environment variables. You can do this by hand using `Add` option or pasting pre-created variables using `Advanced edit`.

Example pre-created variables for your UI:

```json
[
  {
    "name": "DOCKER_ENABLE_CI",
    "value": "true",
    "slotSetting": false
  },
  {
    "name": "DOCKER_REGISTRY_SERVER_URL",
    "value": "https://ghcr.io/",
    "slotSetting": false
  },
  {
    "name": "PORT",
    "value": "80",
    "slotSetting": false
  },
  {
    "name": "PROMPT_SAIL_ENV_PLACEHOLDER_BACKEND_URL",
    "value": "https://<your-proxy-name>.azurewebsites.net",
    "slotSetting": false
  },
  {
    "name": "PROMPT_SAIL_ENV_PLACEHOLDER_PROXY_URL_HOST",
    "value": "https://<your-proxy-name>.azurewebsites.net/api",
    "slotSetting": false
  },
  {
    "name": "PROMPT_SAIL_ENV_PLACEHOLDER_SSO_AZURE_AUTHORITY",
    "value": "https://login.microsoftonline.com/<PROMPT_SAIL_ENV_PLACEHOLDER_SSO_AZURE_TENANT>",
    "slotSetting": false
  },
  {
    "name": "PROMPT_SAIL_ENV_PLACEHOLDER_SSO_AZURE_CLIENT_ID",
    "value": "d3bxyz-xxxx-xxxx-xxxx-d0xyzxyzd9",
    "slotSetting": false
  },
  {
    "name": "PROMPT_SAIL_ENV_PLACEHOLDER_SSO_AZURE_SCOPES",
    "value": "user.read",
    "slotSetting": false
  },
  {
    "name": "PROMPT_SAIL_ENV_PLACEHOLDER_SSO_AZURE_TENANT",
    "value": "xyzxyzxyz-xxx-xxx-xxx-xyzxyzxyz",
    "slotSetting": false
  },
  {
    "name": "WEBSITES_ENABLE_APP_SERVICE_STORAGE",
    "value": "false",
    "slotSetting": false
  }
]
```


Remember! You need to edit those variables:
- set `PROMPT_SAIL_ENV_PLACEHOLDER_BACKEND_URL` as `https://` + (2.2.) `name of proxy instance` + `.azurewebsites.net`
- set `PROMPT_SAIL_ENV_PLACEHOLDER_PROXY_URL_HOST` as `PROMPT_SAIL_ENV_PLACEHOLDER_BACKEND_URL` + `/api`
- set `PROMPT_SAIL_ENV_PLACEHOLDER_SSO_AZURE_CLIENT_ID` as your Client ID [(here you can find how to setup auth)](docs/sso-configuration/),
- set `PROMPT_SAIL_ENV_PLACEHOLDER_SSO_AZURE_TENANT` as your Tenant (as above),
- set `PROMPT_SAIL_ENV_PLACEHOLDER_SSO_AZURE_AUTHORITY` as `https://login.microsoftonline.com/` + `PROMPT_SAIL_ENV_PLACEHOLDER_SSO_AZURE_TENANT`


5. After applying changes redirect to `Overwiew` page and press `Restart` button.

## Azure Deployment as composed service

1. Go to [Create a resource](https://portal.azure.com/#create/hub) webpage and select `Create` under `Web App` section.
![Photo 1]({{ site.url }}{{ site.baseurl }}assets/images/azure-deploy-1.png)
2. On the first page you need to specify (1) `Resource Group` that you will use to deploy promptsail, (2) `name of the instance` and (3) `publish type`. Then press (4) `Next`.
![Photo 2]({{ site.url }}{{ site.baseurl }}assets/images/azure-deploy-2.png)
3. In the `Container` tab you need to specify `Image Source` as (1) `Docker Hub or other registries` and as a `Options` the (2) `Docker Compose (Preview)`. Now you need to add (3) a little bit updated version of docker-compose.yml that you can find on our [Github](https://github.com/PromptSail/prompt_sail/blob/main/docker-compose.yml).
![Photo 3]({{ site.url }}{{ site.baseurl }}assets/images/azure-deploy-3.png)

```yaml
version: "3.8"
services:
  mongodb:
    image: mongo:latest
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: password
    healthcheck:
      test: echo 'db.runCommand("ping").ok' | mongosh localhost:27017/test --quiet
      interval: 10s
      timeout: 10s
      retries: 5
      start_period: 40s
  promptsail-backend:
    image: ghcr.io/promptsail/promptsail-backend:lastest
    container_name: promptsail-backend
    ports:
      - "8000:8000"
    environment:
      BASE_URL: "https://promptsail-test.azurewebsites.net"
      STATIC_DIRECTORY: "/static"
      MONGO_URL: "mongodb://root:password@mongodb:27017"
      ORGANIZATION_NAME: "Promptsail"
      ADMIN_PASSWORD: "password"
      SSO_AUTH: "True"
      AZURE_CLIENT_ID: "d3xxxx25-xxxx-xxxx-xxxx-d080xxxxxcd9"
    depends_on:
      mongodb:
        condition: service_healthy
  promptsail-ui:
    image: ghcr.io/promptsail/promptsail-ui:lastest
    container_name: promptsail-ui
    ports:
      - "80:80"
      - "443:443"
    environment:
      PORT: 80
      PROMPT_SAIL_ENV_PLACEHOLDER_BACKEND_URL: 'http://promptsail-backend:8000/api'
      PROMPT_SAIL_ENV_PLACEHOLDER_PROXY_URL_HOST: 'https://promptsail-test.azurewebsites.net/api'
      PROMPT_SAIL_ENV_PLACEHOLDER_SSO_GOOGLE_CLIENT_ID: 'change_me_compose.apps.googleusercontent.com'
      PROMPT_SAIL_ENV_PLACEHOLDER_SSO_AZURE_CLIENT_ID: 'd3xxxx25-xxxx-xxxx-xxxx-d08xxxxxcd9'
      PROMPT_SAIL_ENV_PLACEHOLDER_SSO_AZURE_TENANT: '4a1bxxxx-xxxx-xxxx-xxxx-bcxxxx86cb29'
      PROMPT_SAIL_ENV_PLACEHOLDER_SSO_AZURE_SCOPES: 'user.read'
      PROMPT_SAIL_ENV_PLACEHOLDER_SSO_AZURE_AUTHORITY: 'https://login.microsoftonline.com/4axxxx18-xxxx-xxxx-xxxx-bcbxxxxxcb29'
    depends_on:
        mongodb:
            condition: service_started
        promptsail-backend:
            condition: service_started

networks:
  internal-network:
    internal: true
  external-network:
```

The main changes in the file are:
- delete `mongoexpress` section (it's only for local access),
- in `mongodb` delete `volumes` section,
- in `promptsail-backend`:
    - set `ORGANIZATION_NAME` as your organization name,
    - set `SSO_AUTH` as True,
    - set `AZURE_CLIENT_ID` as your Client ID [(here you can find how to setup auth)](docs/sso-configuration/)
    - set `BASE_URL` as `https://` + (2.2.) `name of the instance` + `.azurewebsites.net`
    - add https port mapping `443:443`
- in `promptsail-ui`:
    - set `PROMPT_SAIL_ENV_PLACEHOLDER_PROXY_URL_HOST` as `https://` + (2.2.) `name of the instance` + `.azurewebsites.net/api`
    - set `PROMPT_SAIL_ENV_PLACEHOLDER_SSO_AZURE_CLIENT_ID` as your Client ID [(here you can find how to setup auth)](docs/sso-configuration/),
    - set `PROMPT_SAIL_ENV_PLACEHOLDER_SSO_AZURE_TENANT` as your Tenant (as above),
    - set `PROMPT_SAIL_ENV_PLACEHOLDER_SSO_AZURE_AUTHORITY` as your authority (as above)
- image version specification (in both backend and ui) changed from environment variable notation to `lastest`,

4. Now you can press the `Review + create` button then `Create`
![Photo 4]({{ site.url }}{{ site.baseurl }}assets/images/azure-deploy-4.png)

Remember! This option to build the application creates the database anew every time - all entries will be deleted. 
If you want to keep your data you need to remove the `mongodb` section in docker-compose and in the `promptsail-backend` section set `MONGO_URL` as connection string to your database created for example using Azure Cosmos.