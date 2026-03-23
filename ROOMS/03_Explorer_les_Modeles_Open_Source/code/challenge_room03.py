import os
from dotenv import load_dotenv
from openai import OpenAI

# Charger token
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN,
)

# Lire le fichier texte
chemin = os.path.join(
    os.path.dirname(__file__),
    "..", "..", "..",
    "datasets",
    "texte_entreprise.txt"
)

with open(chemin, "r", encoding="utf-8") as f:
    texte = f.read()

# Prompt
prompt = f"Résume ce texte en exactement 5 phrases claires et concises, sans puces, sans titre, sans introduction et sans montrer ton raisonnement :\n\n{texte}"
# Appel modèle (Llama - celui qui marche chez toi)
completion = client.chat.completions.create(
    model="Qwen/Qwen3-4B-Thinking-2507",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=400,
    temperature=0.3,
)

print("=== Résumé (modèle 1) ===")
print(completion.choices[0].message.content)