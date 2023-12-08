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

### Requirements

* installed docker and docker-compose on your machine [Windows](https://docs.docker.com/docker-for-windows/install/) | [Mac](https://docs.docker.com/docker-for-mac/install/) | [Linux](https://docs.docker.com/engine/install/ubuntu/)
* git clone repository and navigate to main directory
```bash
git clone https://github.com/PromptSail/prompt_sail.git
cd prompt_sail
```



### Linux machine

1. Since Prompt Sail relies on subdomains, first you should update your `/ect/hosts` file with the following lines:

```bash
127.0.1.1	project1.promptsail.local
127.0.1.1	project2.promptsail.local
127.0.1.1	promptsail.local
```

3. Build and run the docker image:

```bash
docker-docker-compose up --build
```

If you want to run the code locally:

Create `.env` file in the root project directory with the following content:

```
OPENAI_API_KEY="[your-openai-api-key]"
MONGO_URL="mongodb://root:password@localhost:27017"
BASE_URL="http://promptsail.local:8000"
```

Make sure you have Poetry installed, then:
```bash
poetry install
poetry shell
```

Make sure you have `make` installed, then:

```bash
make run # to start docker-compose
```

```bash
cd src
python main.py # to run the code
```

### Windows 11 machine

1. Since Prompt Sail relies on subdomains, first you should update your system  `host` 
```
notepad C:\Windows\System32\Drivers\etc\hosts
```
file with the following lines:


```bash
127.0.1.1	project1.promptsail.local
127.0.1.1	project2.promptsail.local
127.0.1.1	promptsail.local
```


2. Build and run the docker image:

```bash
docker-compose up --build
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

To run tests, simpy run `make test`.

## Building the docker image

```bash
make build
```