import os

import openai
from dotenv import load_dotenv

load_dotenv()


print("Using key", os.environ["OPENAI_API_KEY"])

openai.api_key = os.environ["OPENAI_API_KEY"]
# openai.proxy = "http://127.0.0.1:8000"
openai.api_base = "http://project1.promptsail.local:8000"


def capture_and_print_urls(request, context):
    url = request.url
    print(f"Request URL: {url}")


# with requests_mock.Mocker() as mocker:
# Add the custom request callback to capture and print URLs
# mocker.register_uri('POST', requests_mock.ANY, text=capture_and_print_urls)


if True:
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Generate poem made of 2 sentences."}],
    )
    print(completion.choices[0].message.content)
else:
    # stream version
    response_stream = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Generate poem made of 1 sentence."}],
        stream=True,
    )
    for chunk in response_stream:
        try:
            print(chunk.choices[0].delta.content, end="")
        except AttributeError:
            print()
