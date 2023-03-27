import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

location = '51.7687058,-2.8412781'
prompt = "Imagine you are standing at coordinates {location}, facing north. What can you see?"

response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=prompt,
    max_tokens=50,
    n=1
)

print(response["choices"][0]["text"])