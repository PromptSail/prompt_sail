---
title: "Environment Variables"
permalink: /docs/env-variables
excerpt: "Environment Variables"
last_modified_at: 2024-05-05T11:48:05+01:00
redirect_from:
  - /theme-setup/
toc: true
toc_sticky: true
---


# Environment Variable Configuration


## App/Backend


Here is a list of supported environment variables that you should/can provide in shell by `backend/.env` file or inside `docker-compose.yml`.
Those variables are used by `backend/src/config/__init__.py` to build configuration class. Configuration is defined once, when the application is built.


### General


#### `MONGO_URL`

- Default: `mongodb://localhost:27017`
- Description: Connection URL to your mongo database.


#### `BASE_URL`

- Default: `http://localhost:8000`
- Description: The base url of your application.

#### `ORGANIZATION_NAME`

- Default: `None` - it needs to be provided
- Description: The name of your organization displayed on the frontend.

#### `ADMIN_PASSWORD`

- Default: `None` - it needs to be provided
- Description: Password of a user with root privileges.


### SSO Authorization


#### `SSO_AUTH`

- Default: `False`
- Description: When false authentication is disabled. The default is false. If true, additionally enter `GOOGLE_CLIENT_ID` or `GOOGLE_CLIENT_ID`.

#### `GOOGLE_CLIENT_ID`

- Default: `None`
- Description: Customer ID needed to authorize login using Google broker. Possible to obtain at the stage of creating a verification point on the intermediary side.

#### `AZURE_CLIENT_ID`

- Default: `None`
- Description: Customer ID needed to authorize login using Azure broker. Possible to obtain at the stage of creating a verification point on the intermediary side.


### Test cases


#### `DEBUG`

- Default: `True` - it should be set as false for deployment
- Description: Option for debugging and development purpose. Allows to display errors as the content of the response from the server.


## Frontend

___Under construction___