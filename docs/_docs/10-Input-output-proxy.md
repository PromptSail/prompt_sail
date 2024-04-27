---
title: "How PromptSail stores transactions"
permalink: /docs/storing-transactions/
excerpt: "How all inputs and outputs are stored by PromptSail"
last_modified_at: 2024-01-04T18:48:05+01:00
redirect_from:
  - /theme-setup/
toc: true

---


## Input/output proxy

Prompt Sail stores transactions by acting as a proxy for libraries and capturing the request and response data. 

All the magic happens when you replace **api_base**(or similar parameter) which originaly points to your LLM provider endpoint by ours **proxy_url**. Thanks to this substitution we can bypass your request and grab response transparently. 


Before you start using Prompt Sail as a proxy, you need to configure the `project` and add `ai-providers` via UI, those information  eventaully will be used to create your unique **proxy_url**.

In one project you can have multiple AI deployments, each with its own **proxy_url**.



### The **proxy_url** structure is as follows:

```
http://localhost:8000/project_slug/deployment_name/
```

where: 
* **project_slug** is a slugified project name, configured in the UI while creating a project
* **deployment_name** is a slugified AI deployment name, configured in the project settings with the target AI provider api url eg. https://api.openai.com/v1/, you can configure multiple AI deployments for a single project

Through the **proxy_url**, it is also possible to tag transactions. 

### The **proxy_url** structure for passing the tags is as follows:

```
http://localhost:8000/project_slug/deployment_name/?tags=tag1,tag2,tag3&target_path=
```

where:
* **tags** is a comma-separated list of tags. This is optional and can be used to tag a transaction eg. with a specific user_id, 
department_name, prompting_technique etc. Tags can help you filter and analyze transactions in the UI.
* **target_path** is required in proxy url when tags are added to it and is used for capturing the target path of particular requests. If you send requests by Python libraries, target_path should be empty (like this: target_path=). In such cases, it will be filled by external Python packages (eg. Langchain, OpenAI).  


Proxy on your behalf makes a call to the configured AI API and log the request and response data in the database.

Transaction object is created with the following fields:

* `id`: The ID of the transaction.
* `project_id`: The ID of the project that the transaction belongs to.
* `request`: A dictionary that contains the original request data, including the method, URL, host, headers, extensions, and content.
* `response`: A dictionary that contains the response data, including the status code, headers, next request, error status, success status, content, elapsed time, and encoding.
* `tags`: A list that contains tags for transaction.
* `model`: Name of model used to generate this transaction. It can be empty when the transaction did not go through due to an error.
* `type`: Type of the model,such as chat, text, embedding, code.
* `os`: The operating system from which the transaction was executed. May be empty because it is only present in some libraries.
* `token_usage`: Total tokens used for this transaction.
* `library`: The library from which the transaction was executed.
* `status_code`: Transaction status code.
* `message`: Content of the response (When the transaction was successfully completed).
* `prompt`: Content of the request.
* `error_message`: Content of the request (When the transaction was not completed successfully).
* `request_time`: Date and time of the start of the transaction.
* `response_time`: Date and time of receipt of the response (and recording of the transaction in the system).