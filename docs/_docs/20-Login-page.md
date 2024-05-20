---
title: "Login Page"
permalink: /docs/login-page/
excerpt: "The Login Page allows users to authenticate and access their accounts within the application"
last_modified_at: 2024-05-20T10:11:00+01:00
redirect_from:
    - /theme-setup/
toc: true
---

The Login Page allows users to authenticate and access their accounts within the application. This documentation provides an overview of the login process and details the functionality available on the Login Page.
This page is available at `localhost:80`. You will be redirected to the `/signin` subpage if the application does not find or recognise the **access token** in the browser's storage.
Login page may operate in one of two mode, which you can set in `docker-compose`:

-   `SSO_AUTH: "False"` - this mode is set by default, no need to login anywhere just press **Click to continue**
-   `SSO_AUTH: "True"` - this mode requires you to select one of the available SSO login options and log in correctly. For more information, see [SSO Configuration](/docs/sso-configuration/)
