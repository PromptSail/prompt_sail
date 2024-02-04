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

Prompt Sail stores transactions by acting as a proxy for libraries and capturing the request and response data. This is done in the **store_transaction** function in the **src\transactions\use_cases.py** file.

All the magic happens thanks to properly prepared **base_url** with points to the  prompt sail backend as a proxy

The url structure is as follows:

```
http://<prompt_sail_backend_url>/project_slug/ai_deployment/?tags=tag1,tag2,tag3
```

where: 
* **project_slug** is a slugified project name, configured in the UI while creating a project
* **ai_deployment** is a slugified AI deployment name, configured in the project settings with the target AI provider api url eg. https://api.openai.com/v1/, you can configure multiple AI deployments for a single project
* **tags** is a comma-separated list of tags. This is optional and can be used to tag a transaction eg. with a specific experiment name, department, prompting technique etc. Tags can help you filter and analyze transactions in the UI.


Proxy on your behalf make a call to the configured AI API and log the request and response data in the database.

Transaction object is created with the following fields:

* `id`: The ID of the transaction.
* `project_id`: The ID of the project that the transaction belongs to.
* `request`: A dictionary that contains the original request data, including the method, URL, host, headers, extensions, and content.
* `response`: A dictionary that contains the response data, including the status code, headers, next request, error status, success status, content, elapsed time, and encoding.
* `query_params`: A dictionary that contains additional query parameters like tags.
