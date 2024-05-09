---
title: "Login Page"
permalink: /docs/login-page/
excerpt: "The Login Page allows users to authenticate and access their accounts within the application"
last_modified_at: 2024-05-08T14:06:00+01:00
redirect_from:
    - /theme-setup/
toc: true
---

The Login Page allows users to authenticate and access their accounts within the application. This documentation provides an overview of the login process and details the functionality available on the Login Page.
This page is available at `localhost:80`. You will be redirected to the `/signin` subpage if the application does not find or recognise the **access token** in the browser's storage. To create an **access token** you must select one of the SSO login options available on the current webpage and log in correctly

## Single Sign-On (SSO)

Single Sign-On (SSO) allows users to access multiple applications or services with a single set of login credentials. This means that users can log in once and gain access to all applications that are part of the SSO ecosystem without the need to log in separately to each application.

**You need to configure SSO parameters for at least one SSO Provider in `docker-compose` file to log in**

```
args:
    # Google
    SSO_GOOGLE_CLIENT_ID: '******.apps.googleusercontent.com'

    # Microsoft Azure
    SSO_AZURE_CLIENT_ID: '6fe*******'
    SSO_AZURE_TENANT: '4a1******'
    SSO_AZURE_SCOPES: 'user.read'
    SSO_AZURE_AUTHORITY: 'https://login.microsoftonline.com/4a1*****'
```

In the next steps I'll show you how it's done

-   ### SSO Google Configuration

    To make it work you need to replace `SSO_GOOGLE_CLIENT_ID` for yours **Client ID** and of course you need Google account. For more info about this process, visit the [Google Documentation](https://support.google.com/cloud/answer/6158849?hl=en&authuser=1&ref_topic=3473162&sjid=17476898588436060043-EU)

    1.  Go to [console.cloud.google.com](https://console.cloud.google.com/) (log in to your account where you will be performing the SSO configuration)
    2.  In the top left corner look for **Select a project** (this can also be the name of the current project), press it, then press on **NEW PROJECT** button. A form should open. Fill it as you want then press **CREATE** button

    ![Create a new project](../assets/images/google-SSO-1.png)
    <div style="text-align:center">
    <img src="../assets/images/google-SSO-2.png" alt='Fill the fields and press CREATE'/>
    </div>

    3.  Once created, easily press **SELECT PROJECT** in Notifications or select it via **Select a project**
    4.  You then need to go to **OAuth consenst screen**. You can easily type it in search bar and select it or look for it in the Quick access section

    ![Go to OAuth consenst screen](../assets/images/google-SSO-3.png)

    5.  When you are there select User Type and press **CREATE**

    <div style="text-align:center">
    <img src="../assets/images/google-SSO-4.png" alt='Select User Type'/>
    </div>

    6.  Next to do is fill the fields about your App information. Fill it as you want and press **SAVE AND CONTINUE**. The most important are **App name**, **User support email** and **Developer contact information**

    <div style="text-align:center">
    <img src="../assets/images/google-SSO-5.png" alt='Enter App Info'/>
    </div>

    7.  In next sections Scopes and Test users form is no need to fill anything. For promptasil app is unnecessary. Fill it as you want or scroll down and press **SAVE AND CONTINUE**.

    <div style="text-align:center">
    <img src="../assets/images/google-SSO-6.png" alt='OAuth Summary'/>
    </div>

    Once you have gone through the whole form press **BACK TO DASHBOARD**. If you have not added any Test users, you need change **Publishing status** to **In production** by pressing **PUBLISH APP** in the **OAuth consenst screen** dashboard. The **Testing** status allows only users listed in Test users list to log in.

    <div style="text-align:center">
    <img src="../assets/images/google-SSO-7.png" alt='Publishing status'/>
    </div>

    Now go to **Credentials** tab.

    1.  Press **CREATE CRENDETIALS** and choose **OAuth client ID**. The next form will open.

    <div style="text-align:center">
    <img src="../assets/images/google-SSO-8.png" alt='Create Credentials'/>
    </div>

    2.  In **Application Type** select **Web application** and you can enter any name you like.
    3.  Authorised JavaScript origins is **the most important configuration** in the whole proccess. It gives login access for provided URIs. Press **ADD URI** and type valid url where promptsail app will run. You could enter **internal or external URL**. Enter only hostname, without subpages. The default configuration is `http://localhost`. Remember to specify the port if it's other than 80, for example `http://localhost:5173`
    4.  Press **CREATE** button. No need to fill more information for now

    <div style="text-align:center">
    <img src="../assets/images/google-SSO-9.png" alt='Create OAuth client ID'/>
    </div>

    The form will then close and a modal window will appear where you can find the **Client ID** (the same information can be found by selecting Credentials and pressing on the name of one of the **OAuth 2.0 Client IDs**).

    <div style="text-align:center">
    <img src="../assets/images/google-SSO-10.png" alt='OAuth client created'/>
    </div>

    Copy and paste it in value of `SSO_GOOGLE_CLIENT_ID` in `docker-compose` file

    <div style="text-align:center">
    <img src="../assets/images/google-SSO-11.png" alt='Copy to docker-compose'/>
    </div>
