---
title: "Repository structure"
permalink: /docs/repository-structure/
excerpt: "How to contribute to Prompt Sail"
last_modified_at: 2023-12-22T18:48:35+01:00
redirect_from:
  - /theme-setup/
toc: true
---

## How the project structure is organized



TODO: Please add a screenshot of the GitHub repository structure to provide a visual representation of the project organization.{: .notice--warning}








## backend folder

A directory containing files related to the application backend.

Files: 

- Dockerfile - 
- pyproject.toml 
- pytest.ini
- provider_price_list.json


### - src

This directory contains the most important files for the operation of the application. Here we can find the `config` configuration, `app` startup files and the rest of `projects`, `transactions` and `settings` which are the objects present in the database along with the necessary tools for their operation such as `repositories` and `use_cases`. The repositories of all objects are built on top of a single, common and generic one stored in the `seedwork` directory. There is also a `utils.py` file containing general-purpose functions.
   
- **app**: In `app` we store the initialization of containers and applications, and make sure that if there are no projects, two primary ones will be created. In `dependencies` we store the functions used to retrieve dependencies from the request. In `exception_handlers` we store exception handling modules. In `logging` we initialize the application logger. In `middleware` we store middleware that, for example, detects a subdomain. In `web_api` are all the endpoints used to communicate the visual layer with the backend. In `web_home` is the endpoint that captures all the unattended traffic within the application. Well, and the most important part of the application: `reverse_proxy`. This is where we intercept user requests, process them, send them to an external AI provider, and store the received response in the system and send it back to the user.
      
- **config**: In `__init__` the basic application configuration is initialized, and `containers` contains all the application container logic.
      
- **projects/transactions/settings**: These are objects stored in the database, and the structure of the files in these folders is uniform. `models` contains the models of these objects, and `schemas` the schemas used in endpoints. `repositories` contains the repository of a given object. `use_cases` is a set of functions that use the repository, used in endpoints to retrieve, for example, a list of objects or add a new object.
      
### - tests 
Here you can find tests of the application. This is a very important part. Without running tests, the production image of the application will not be built.


### perf_tests

This directory contains performance tests for the application with use of locust.io
   
## docs
A directory containing the github pages jackyll files from which the application documentation is automaticallly built.
More information on how to contribute to the documentation can be found is section [How the documentation is organized](/docs/how-to-write-documentation/)

## examples folder 
Jupyter notebooks examples for various AI providers.

## UI
A directory containing the files from which the visual layer of the application is built.
