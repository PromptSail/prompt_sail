---
title: "Introduction"
permalink: /docs/introduction/
excerpt: "Intorduction, key features and philosophy of Prompt Sail"
last_modified_at: 2023-12-28T14:48:05+01:00
redirect_from:
  - /theme-setup/
toc: true

---


## What is Prompt Sail?


Is a self-hosted application that captures and logs all interactions with LLM APIs such as OpenAI, Anthropic, Google Gemini and others. It is a proxy between your framework of choice (LangChain, OpenAI etc) and LLM provider API. 

For **developers**, it offers a way to analyze and optimize API prompts. 

For **Project managers** can gain insights into project and experiment costs. 

For **Business owners** can ensure compliance with regulations and maintain governance over prompts and responses.


## How does it work?

Prompt Sail is build as a set of docker containers. One for backend (promptsail-backend) and one for frontend (promptsail-ui).

- **promptsail-backend** is a proxy that sits between your LLM framework of choice (LangChain, OpenAI python lib etc) and LLM provider API. You change `api_base` to point to Prompt Sail `proxy_url` and then it will captures and logs all your prompts and responses. 
- **promptsail-ui** is a user interface that allows you to view, search and analyze all transactions (prompts and responses).


There are two options to run the Prompt Sail docker containers: 
* [build the images from the source code](/docs/quick-start-guide/#build-the-docker-images-from-the-source-code) or 
* [pull the images from Github Container Repository (ghcr.io)](/docs/quick-start-guide/#pull-and-run-the-docker-images-from-ghcr).


In the next page you will:

* learn how to run Prompt Sail on your local machine
* make your first API call to OpenAI



