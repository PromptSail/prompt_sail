from dotenv import load_dotenv
import os
import openai


load_dotenv()


print("Using key", os.environ["OPENAI_API_KEY"])

openai.api_key = os.environ["OPENAI_API_KEY"]
openai.proxy = "http://127.0.0.1:8000"
# openai.api_base = "http://127.0.0.1:8000"

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
        messages=[{"role": "user", "content": "Generate poem made of 2 sentences."}],
        stream=True,
    )
    for chunk in response_stream:
        try:
            print(chunk.choices[0].delta.content, end="")
        except AttributeError:
            print()
