<p align="center">
  <p align="center">
    <a href="https://promptsail.com/?utm_source=github&utm_medium=logo" target="_blank">
      <img src="https://bucket.mlcdn.com/a/1777/1777896/images/c2ba3a2cf624d3343a98cbb35f1d02dd373d8000.png" alt="Prompt Sail" width="390" height="91">
    </a>
  </p>
  <p align="center">
    Open Source LLM prompt performance monitoring for quality and efficiency validation.
  </p>
</p>

## What is Prompt Sail?

Prompt Sail is a proxy for Large Language Models (LLMs) such as GPT-3, ChatGPT, DialoGPT, etc. 
that allows you to record prompts and responses, analyze the output, compare the outcome over time, 
track trends and changes across various models and their versions.

To learn more about Prompt Sail’s features and capabilities, see our [product page](https://promptsail.com/).

## Getting started

The simplest way to try Prompt Sail is to create a project on https://try.promptsail.com and integrate it with 
your code.

If you prefer to install and manage Prompt Sail yourself, you can download a docker image and run it locally.

## Run Start Prompt locally

To try out Start Prompt on your own machine, we recommend using docker-compose. Docker images are available from ...


### Start Prompt Sail

```bash
git clone ...
docker-docker-compose up -d
```

### Create a project

Navigate to http://localhost:8000 and create a project. 

TODO: modify `hosts` file to point to `localhost`

### Modify your code to use Prompt Sail

To use Prompt Sail with `openai` Python library, you need to set `OPENAI_API_BASE` environment variable, or
modify `openai.api_base` parameter to point to your Prompt Sail project.
```python
import openai        
openai.api_base = "[your project api base]"
openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Explaining the meaning of life in one sentence."}],
)
```

Using Prompt Sail with `langchain` is similar:
```python
from langchain.llms import OpenAI
llm = OpenAI(
    model_name="text-davinci-003",
    openai_api_base="[your project api base]",
)
llm("Explaining the meaning of life in one sentence.")
```

### Analyzing the prompts and responses

After running your LLM code, navigate back to your project page and see the prompt and response recorded.

## Building docker image

```bash
docker build -t prompt_sail .
```