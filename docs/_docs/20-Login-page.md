---
title: "Login Page"
permalink: /docs/login-page
excerpt: "The Login Page allows users to authenticate and access their accounts within the application"
last_modified_at: 2024-05-20T10:11:00+01:00
redirect_from:
    - /theme-setup/
toc: true
---


## Overview

The Login Page allows users to authenticate and access their accounts within the application. 


Prompt Sail login page for annomous access is shown below:
![PromptSail Login page - annomous access]({{ site.url }}{{ site.baseurl }}assets/images/promptsail_ui_login_page.png){: .align-center}

Promp Sail login page for SSO authentication enabled is shown below:

![PromptSail Login page - SSO enabled]({{ site.url }}{{ site.baseurl }}assets/images/promptsail_ui_login_page_sso.png){: .align-center}

By default, the application will redirect you to the login page if it does not find or recognize the access token in the browser's storage. The login functionality can operate in one of two modes, which you can set in the `docker-compose` file:

* allow annomous access to the application by setting env variable `SSO_AUTH: "False"` - this mode is set by default, no need to login anywhere just press **Click to continue**
* allow only authenticated users to access the application via SSO, to configure this just follow the steps described in [SSO Configuration](/docs/sso-configuration/)

You can customize the organization name by setting the `ORGANIZATION_NAME` environment variable in the `docker-compose` file. See the [Environment Variables](/docs/env-variables) documentation for more information.
