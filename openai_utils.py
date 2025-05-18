import openai
import os

open.api_key = os.getenv("OPEN_API_KEY")

# Create a client instance (for SDK >= 1.0)
client = openai.OpenAI()

def get_openai_response(messages, model="gpt-3.5-turbo"):
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content

def generate_response(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    return get_openai_response(messages, model=model)