<p align="center">
  <p align="center">
    <a href="https://promptsail.com/?utm_source=github&utm_medium=logo" target="_blank">
      <img src="https://bucket.mlcdn.com/a/1777/1777896/images/c2ba3a2cf624d3343a98cbb35f1d02dd373d8000.png" alt="Prompt Sail" width="390" height="91">
    </a>
  </p>
  <p align="center">
    Open Source LLM prompt management and monitoring.
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

## Run Prompt Sail locally

To try out Start Prompt on your own machine, we recommend using docker-compose. Docker images are available from ...

### Linux machine

1. Since Prompt Sail relies on subdomains, first you should update your `/ect/hosts` file with the following lines:

```bash
127.0.1.1	project1.promptsail.local
127.0.1.1	project2.promptsail.local
127.0.1.1	promptsail.local
```
2. Clone the repository and navigate to the main directory:

3. Build and run the docker image:


```bash
docker-docker-compose up --build
```

### Create a project

Navigate to http://promptsail.local, feel free to browse projects. 
Creating a new project via UI is not yet implemented, stay tuned for new commits.

### Modify your code to use Prompt Sail proxy

To use Prompt Sail with `openai` Python library, you need to set `OPENAI_API_BASE` environment variable, or
modify `openai.api_base` parameter to point to your Prompt Sail project.
```python
import openai        
openai.api_base = "http://[your-project-id].promptsail.local:8000"
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
    openai_api_base="http://[your-project-id].promptsail.local:8000",
)
llm("Explaining the meaning of life in one sentence.")
```

### Analyzing the prompts and responses

After running your LLM code, navigate back to your project page and see the prompt and response recorded.

## Testing

To run tests, simpy run `pytest` in the `src` directory of the project.

## Building docker image

```bash
docker build -t prompt_sail .
```