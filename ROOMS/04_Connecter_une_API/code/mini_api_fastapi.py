# mini_api_fastapi.py - Mini serveur FastAPI qui interroge un LLM
# Room 04 - Connecter une API
# Lancer avec : python -m uvicorn code.mini_api_fastapi:app --reload --port 8000

from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from utils import creer_client, MODELE

app = FastAPI()
client = creer_client()

# Historique en mémoire
historique = []

MAX_MESSAGES = 20  # 10 échanges (user + assistant)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {"message": "Le serveur fonctionne correctement."}


@app.post("/question")
def poser_question(data: QuestionRequest):
    global historique

    # Ajouter la question utilisateur
    historique.append({"role": "user", "content": data.question})

    # Limiter historique
    historique = historique[-MAX_MESSAGES:]

    # Appel au modèle avec historique
    reponse = client.chat.completions.create(
        model=MODELE,
        messages=historique,
        temperature=0.3,
        max_tokens=300
    )

    texte = reponse.choices[0].message.content

    # Ajouter réponse
    historique.append({"role": "assistant", "content": texte})
    historique = historique[-MAX_MESSAGES:]

    return {"reponse": texte}


@app.get("/historique")
def get_historique():
    return {"historique": historique}


@app.post("/reset")
def reset():
    global historique
    historique = []
    return {"message": "Historique vidé"}