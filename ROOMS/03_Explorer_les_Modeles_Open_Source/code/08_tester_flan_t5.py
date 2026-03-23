import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN,
)

prompt = "Explique en 3 phrases simples ce qu'est une base de données relationnelle. Réponds directement, sans montrer ton raisonnement."

completion = client.chat.completions.create(
    model="Qwen/Qwen3-4B-Thinking-2507",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=200,
    temperature=0.3,
    reasoning_effort="none",
)

print("=== Interrogation du modèle 3 ===")
print(f"Prompt : {prompt}\n")
print("=== Réponse ===")
print(completion.choices[0].message.content)