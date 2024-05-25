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


## Azure Deployment 

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
      BASE_URL: "http://localhost:8000"
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
    - add https port mapping `443:443`
- in `promptsail-ui`:
    - set `PROMPT_SAIL_ENV_PLACEHOLDER_PROXY_URL_HOST` as `https://` + (2.2.) `name of the instance` + `.azurewebsites.net/api`
    - set `PROMPT_SAIL_ENV_PLACEHOLDER_SSO_AZURE_CLIENT_ID` as your Client ID [(here you can find how to setup auth)](docs/sso-configuration/),
    - set `PROMPT_SAIL_ENV_PLACEHOLDER_SSO_AZURE_TENANT` as your Tenant (as above),
    - set `PROMPT_SAIL_ENV_PLACEHOLDER_SSO_AZURE_AUTHORITY` as your authority (as above)
- image version specification (in both backend and ui) changed from environment variable notation to `lastest`,

4. Now you can press the `Review + create` button then `Create`
![Photo 4]({{ site.url }}{{ site.baseurl }}assets/images/azure-deploy-4.png)