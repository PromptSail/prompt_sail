---
title: "Project Setup"
permalink: /docs/how-to-setup-llm-proxy-project/
excerpt: "How to quickly install and setup Prompt Sail project."
last_modified_at: 2024-02-21T12:14:05+01:00
redirect_from:
    - /theme-setup/
toc: true
toc_sticky: true
---

The Project Setup page guides users through the process of creating a new project within our application. This includes defining project details and integrating AI providers. To begin the process of creating a new project, click on "Add new Project" on the [Organization Dashboard](https://promptsail.github.io/prompt_sail/docs/organization-dashboard/) page. You should see a form with two sections:

## Project Details

This section contains key information about the project

1. **Name**: This is the name that will uniquely identify your project within the application.
2. **Slug**: The project slug is a URL-friendly version of the project name. It is used to create a proxy URL for a project. It is filled in automatically or you can enter it yourself.
3. **Description (optional)**: This field enables providing additional information about your project. You can use it to describe the goals, objectives, or any other relevant details that users should know about the project. While optional, providing a description can help users better understand the purpose of your project.

4. **Tags (optional)**: Tags are keywords or labels that you can assign to your project to help categorize and organize it. They can be used to group similar projects together or to indicate specific characteristics or features of your project. While optional, adding tags can make it easier for users to search for and discover your project within the application.

## Provider Details

This section contains information about the AI providers in use. Once you have added at least one AI provider, you will see a list with it and the option to add another one

1. **AI Providers (Select Provider)**: This functionality allows users to choose from a list of available AI providers to integrate into their project. The dropdown list typically contains a variety of AI providers offering different services or functionalities.
2. **Deployment name**: The deployment name is a unique identifier for the deployment of your AI model or service within the project. It is used to create a proxy URL for a project.
3. **Api base URL**: The API base URL is the root URL for the API endpoints provided by your AI service or model. It serves as the starting point for accessing various functionalities and resources offered by the AI provider.
4. **Proxy URL**: The proxy URL serves as an intermediary between the project and the AI provider's API. It is generated automatically based on the deployment name and project slug. After filled in neccsesary information copy this link to used it

After entering the necessary information, click Add AI Provider to add it to the project. **You need to add at least one Ai Provider**

## Complete Project Creation

Once all necessary information is provided, click the "Create" button to finalize project creation. The new project will then be visible in the [Organization Dashboard](https://promptsail.github.io/prompt_sail/docs/organization-dashboard/) and now you can [make your first LLM API call](https://promptsail.github.io/prompt_sail/docs/quick-start-guide/#make-your-first-api-call)