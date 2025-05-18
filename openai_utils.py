import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")  # Set in your environment

def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You're a helpful agent for Barbeque Nation."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content'].strip()