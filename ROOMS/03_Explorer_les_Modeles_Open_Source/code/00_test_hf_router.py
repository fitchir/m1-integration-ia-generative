import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN,
)

completion = client.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct:cerebras",
    messages=[
        {
            "role": "user",
            "content": "Explique en 3 phrases simples ce qu'est une base de données relationnelle."
        }
    ],
    max_tokens=200,
)

print("=== Réponse ===")
print(completion.choices[0].message.content)