---
title: "LLM integrations"
permalink: /docs/llm-integrations/
excerpt: "Integrations with most common LLM libraries and providers"
last_modified_at: 2024-01-04T18:18:15+01:00
redirect_from:
  - /theme-setup/
toc: true
toc_sticky: true
---




## Supported Providers and Models


| Provider        | Model                        | Type             | Support       |
|-----------------|------------------------------|------------------|---------------|
| OpenAI          | babbage-002                  | completion       | - [x]         |
| OpenAI          | davinci-002                  | completion       | - [x]         |
| OpenAI          | gpt-3.5-turbo-0125           | chat             | - [x]         |
| OpenAI          | gpt-3.5-turbo-0301           | chat             | - [x]         |
| OpenAI          | gpt-3.5-turbo-0613           | chat             | - [x]         |
| OpenAI          | gpt-3.5-turbo-1106           | chat             | - [x]         |
| OpenAI          | gpt-3.5-turbo-16k-0613       | chat             | - [x]         |
| OpenAI          | gpt-3.5-turbo-instruct       | chat             | - [x]         |
| OpenAI          | gpt-3.5-turbo-instruct-0914  | chat             | - [x]         |
| OpenAI          | gpt-4-0613                   | chat             | - [x]         |
| OpenAI          | gpt-4-1106-preview           | chat             | - [x]         |
| OpenAI          | gpt-4-1106-vision-preview    | chat             | - [x]         |
| OpenAI          | gpt-4-turbo-2024-04-09       | chat             | - [x]         |
| OpenAI          | gpt-4-0125-preview           | chat             | - [x]         |
| OpenAI          | gpt-4o-2024-05-13            | chat             | - [x]         |
| OpenAI          | text-embedding-3-small       | embedding        | - [x]         |
| OpenAI          | text-embedding-3-large       | embedding        | - [x]         |
| OpenAI          | text-embedding-ada-002       | embedding        | - [x]         |
| OpenAI          | dall-e-2                     | image generation | - [x]         |
| OpenAI          | dall-e-3                     | image generation | - [x]         |
| Azure OpenAI    | babbage-002                  | completion       | - [x]         |
| Azure OpenAI    | davinci-002                  | completion       | - [x]         |
| Azure OpenAI    | gpt-3.5-turbo-0125           | chat             | - [x]         |
| Azure OpenAI    | gpt-3.5-turbo-0301           | chat             | - [x]         |
| Azure OpenAI    | gpt-3.5-turbo-0613           | chat             | - [x]         |
| Azure OpenAI    | gpt-3.5-turbo-1106           | chat             | - [x]         |
| Azure OpenAI    | gpt-3.5-turbo-16k-0613       | chat             | - [x]         |
| Azure OpenAI    | gpt-3.5-turbo-instruct       | chat             | - [x]         |
| Azure OpenAI    | gpt-3.5-turbo-instruct-0914  | chat             | - [x]         |
| Azure OpenAI    | gpt-4-0613                   | chat             | - [x]         |
| Azure OpenAI    | gpt-4-1106-preview           | chat             | - [x]         |
| Azure OpenAI    | gpt-4-1106-vision-preview    | chat             | - [x]         |
| Azure OpenAI    | gpt-4-turbo-2024-04-09       | chat             | - [x]         |
| Azure OpenAI    | gpt-4-0125-preview           | chat             | - [x]         |
| Azure OpenAI    | gpt-4o-2024-05-13            | chat             | - [x]         |
| Azure OpenAI    | text-embedding-3-small       | embedding        | - [x]         |
| Azure OpenAI    | text-embedding-3-large       | embedding        | - [x]         |
| Azure OpenAI    | text-embedding-ada-002       | embedding        | - [x]         |
| Azure OpenAI    | dall-e-2                     | image generation | in progress   |
| Azure OpenAI    | dall-e-3                     | image generation | in progress   |
| Google Vertex AI| gemini-1.0-pro-001           | chat             | - [x]         |
| Google Vertex AI| gemini-1.0-pro-002           | chat             | - [x]         |
| Google Vertex AI| gemini-1.0-pro-vision-001    | chat             | - [x]         |
| Google Vertex AI| gemini-1.5-flash-001         | chat             | - [x]         |
| Google Vertex AI| gemini-1.5-flash-preview-0514| chat             | - [x]         |
| Google Vertex AI| gemini-1.5-pro-001           | chat             | - [x]         |
| Google Vertex AI| gemini-1.5-pro-preview-0514  | chat             | - [x]         |
| Anthropic       | claude-2.0                   | chat             | - [x]         |
| Anthropic       | claude-2.1                   | chat             | - [x]         |
| Anthropic       | claude-3-haiku               | chat             | - [x]         |
| Anthropic       | claude-3-opus                | chat             | - [x]         |
| Anthropic       | claude-3-sonnet              | chat             | - [x]         |
| Anthropic       | claude-instant-1.2           | chat             | - [x]         |
| Huggingface     |                              |                  | in progress   |
| Groq            |                              |                  | in progress   |
| Ollama          |                              |                  | in progress   |
