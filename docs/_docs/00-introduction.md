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

Prompt Sail is built as a set of Docker containers: one for the backend (promptsail-backend) and one for the frontend (promptsail-ui).

- **promptsail-backend** acts as a proxy between your chosen LLM framework (such as LangChain or the OpenAI Python library) and the LLM provider API. By changing the `api_base` to point to Prompt Sail's `proxy_url`, it captures and logs all prompts and responses.
- **promptsail-ui** provides a user interface for viewing, searching, and analyzing all transactions (prompts and responses).


There are two options to run the Prompt Sail docker containers: 
* [build the images from the source code](/docs/quick-start-guide/#build-the-docker-images-from-the-source-code) or 
* [pull the images from Github Container Repository (ghcr.io)](/docs/quick-start-guide/#pull-and-run-the-docker-images-from-ghcr).


In the next page you will:

* learn how to run Prompt Sail on your local machine
* make your first API call to OpenAI



