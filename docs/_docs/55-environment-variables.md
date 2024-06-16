---
title: "Environment Variables Configuration"
permalink: /docs/env-variables
excerpt: "Environment Variables Configuration"
last_modified_at: 2024-06-12T15:00:00+01:00
redirect_from:
    - /theme-setup/
toc: true
toc_sticky: true
---

## App/Backend

Here is a list of supported environment variables that you should/can provide in shell by `backend/.env` file or inside `docker-compose.yml`.
Those variables are used by `backend/src/config/__init__.py` to build configuration class. Configuration is defined once, when the application is built.

### General

#### `MONGO_URL`

-   Default: `mongodb://localhost:27017`
-   Description: Connection URL to your mongo database.

#### `BASE_URL`

-   Default: `http://localhost:8000`
-   Description: The base url of your application.

#### `ORGANIZATION_NAME`

-   Default: `None` - it needs to be provided
-   Description: The name of your organization displayed on the frontend.

#### `ADMIN_PASSWORD`

-   Default: `None` - it needs to be provided
-   Description: Password of a user with root privileges.

### SSO Authorization

#### `SSO_AUTH`

-   Default: `False`
-   Description: When false authentication is disabled. The default is false. If true, additionally enter `GOOGLE_CLIENT_ID` or `GOOGLE_CLIENT_ID`.

#### `GOOGLE_CLIENT_ID`

-   Default: `None`
-   Description: Customer ID needed to authorize login using Google broker. Possible to obtain at the stage of creating a verification point on the intermediary side.

#### `AZURE_CLIENT_ID`

-   Default: `None`
-   Description: Customer ID needed to authorize login using Azure broker. Possible to obtain at the stage of creating a verification point on the intermediary side.

### Test cases

#### `DEBUG`

-   Default: `True` - it should be set as false for deployment
-   Description: Option for debugging and development purpose. Allows to display errors as the content of the response from the server.

## Frontend

Here is a list of supported environment variables that you should provide in the `ui/.env` file or inside `docker-compose.yml`. These variables are used to configure the application.

### General

#### `PORT`

-   Default: `80`
-   Description: The port on which the application will run.

#### `PROMPT_SAIL_ENV_PLACEHOLDER_BACKEND_URL`

-   Default: `http://promptsail-backend:8000`
-   Description: The backend URL of the application.

#### `PROMPT_SAIL_ENV_PLACEHOLDER_PROXY_URL_HOST`

-   Default: `http://localhost:8000`
-   Description: The proxy URL host used by the application.

### SSO Authorization

#### `PROMPT_SAIL_ENV_PLACEHOLDER_SSO_GOOGLE_CLIENT_ID`

-   Default: `None`
-   Description: Client ID required for Google [SSO authentication](/docs/sso-configuration/#sso-google-configuration).

#### `PROMPT_SAIL_ENV_PLACEHOLDER_SSO_AZURE_CLIENT_ID`

-   Default: `None`
-   Description: Client ID required for Azure [SSO authentication](/docs/sso-configuration/#sso-microsoft-azure-configuration).

#### `PROMPT_SAIL_ENV_PLACEHOLDER_SSO_AZURE_TENANT`

-   Default: `None`
-   Description: Azure tenant ID required for Azure [SSO authentication](/docs/sso-configuration/#sso-microsoft-azure-configuration).

#### `PROMPT_SAIL_ENV_PLACEHOLDER_SSO_AZURE_SCOPES`

-   Default: `user.read`
-   Description: Scopes required for Azure [SSO authentication](/docs/sso-configuration/#sso-microsoft-azure-configuration).

#### `PROMPT_SAIL_ENV_PLACEHOLDER_SSO_AZURE_AUTHORITY`

-   Default: `None`
-   Description: The authority URL for Azure [SSO authentication](/docs/sso-configuration/#sso-microsoft-azure-configuration).
