---
title: "Quick-Start Guide"
permalink: /docs/how-to-setup-llm-proxy-project/
excerpt: "How to quickly install and setup Prompt Sail project."
last_modified_at: 2023-12-22T18:48:05+01:00
redirect_from:
  - /theme-setup/
toc: true
---



## How to incorporate Prompt Sail into your LLM workflow

Prompt Sail works as a docker container that sits between your LLM API and your application. It captures and logs all prompts and responses. 
There are two options to run the Prompt Sail docker container:

Pull and run the Docker image from Docker Hub. 

**Notice:** Currently, the docker image is not available on Docker Hub. Command below will not work yet.
{: .notice--warning}

```bash
docker run prompt-sail
``` 

Recommmened way is to build the Docker image from the source code.
{: .notice--success}

To build the Docker images from the source code, run the following command. It will build the images for proxy and UI.

```bash
docker-compose up --build
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
