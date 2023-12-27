---
title: "Quick-Start Guide"
permalink: /docs/quick-start-guide/
excerpt: "How to quickly install and setup Prompt Sail."
last_modified_at: 2023-12-22T18:48:05+01:00
redirect_from:
  - /theme-setup/
toc: true
---


## What is Prompt Sail?

Prompt Sail is a transparent and user-friendly tool designed to capture and log all interactions with LLM APIs such as OpenAI, Cohere, and others. 

For **developers**, it offers a way to analyze and optimize API prompts. 

**Project managers** can gain insights into project and experiment costs. 

**Business owners** can ensure compliance with regulations and maintain governance over prompts and responses.

## Key Features of Prompt Sail

1. **Transparent Logging**: Prompt Sail captures and logs all interactions with General AI APIs, providing a comprehensive record of prompts and responses.

2. **Optimization and Analysis**: With the ability to analyze and optimize API prompts, developers can fine-tune their applications for better performance and results.

3. **Cost Insights**: Project managers can track and analyze the costs associated with each project and experiment, enabling better budget management.

4. **Compliance and Governance**: Business owners can ensure that their use of AI APIs is compliant with relevant regulations, and maintain control over the prompts and responses used.

5. **Easy Integration**: Prompt Sail is designed to be easily integrated into your existing workflow. Simply change the `base_url` when creating your AI API object to start using Prompt Sail.

6. **Searchable Database**: All prompts and responses are stored in a searchable database, making it easy to find and analyze specific interactions.

7. **User-Friendly Interface**: Prompt Sail features a simple, intuitive UI that makes it easy to search and analyze prompts and responses.

## Incorporating Prompt Sail into Your Workflow

**Installation**

There are two options for installing Prompt Sail:


Execute the Docker image from Docker Hub. (todo: add docker hub link)

```bash
docker run prompt-sail
``` 


Build the Docker image from the source code.

```bash
docker-docker-compose up --build
```


**Configuration**

The setup is straightforward. You need to modify the `base_url` when creating your AI API object. You can also include additional parameters in the URL, such as `project_slug`, `experiment_id`, and `tags`.

Here's a template for the `base_url`:

```
http://localhost:8000/<project_slug>/chat/completions?experiment_id=welcome_message_gen&tags=zero_shot,simple_prompt,dev1,poc
```



**Usage**

Once the setup is complete, you can begin using Prompt Sail. It will automatically capture and log all prompts and responses. You can then view and analyze this data through the intuitive user interface. UI is available at [http://localhost:80/](http://localhost:80/)

Prompt Sail is designed to integrate smoothly into your workflow, offering valuable insights without causing any disruption to your development process.
