# Script 05 - Assistant pédagogique interactif
# Room 02 - Construire avec des prompts

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from utils import creer_client, MODELE

client = creer_client()


def expliquer_sujet(sujet):
    """
    Envoie un sujet au LLM avec un rôle de professeur bienveillant
    et retourne une explication adaptée à un débutant.
    """
    prompt_explication = (
        "Tu es un professeur bienveillant qui s'adresse à un débutant complet.\n"
        f"Explique en français le sujet suivant : \"{sujet}\".\n"
        "Respecte exactement ce format :\n"
        "Paragraphe 1 : une définition courte et claire.\n"
        "Paragraphe 2 : une analogie du quotidien pour aider à comprendre.\n"
        "Paragraphe 3 : un exemple concret d'utilisation dans la pratique.\n"
        "Utilise des phrases simples, évite le jargon, et ne dépasse pas 150 mots au total."
    )

    reponse = client.chat.completions.create(
        model=MODELE,
        messages=[{"role": "user", "content": prompt_explication}],
        temperature=0.3,
        max_tokens=300
    )
    return reponse.choices[0].message.content


def proposer_exercice(sujet):
    """
    Propose un exercice pratique sur le sujet donné.
    """
    prompt_exercice = (
        "Tu es un professeur bienveillant qui crée un exercice pour un débutant.\n"
        f"Sujet de l'exercice : \"{sujet}\".\n"
        "Propose UN SEUL exercice pratique en français, en respectant ce format :\n"
        "- Une consigne générale en 2 à 3 phrases.\n"
        "- Puis une liste de 3 questions ou tâches numérotées (1., 2., 3.).\n"
        "L'exercice doit être faisable par un débutant et ne doit pas contenir la solution."
    )

    reponse = client.chat.completions.create(
        model=MODELE,
        messages=[{"role": "user", "content": prompt_exercice}],
        temperature=0.5,
        max_tokens=200
    )
    return reponse.choices[0].message.content


# --- Programme principal ---
print("=== Assistant pédagogique ===")
print("Entrez un sujet pour obtenir une explication et un exercice.")
print("Tapez 'quitter' pour arrêter.")
print()

while True:
    sujet = input("Sujet à apprendre : ").strip()

    if sujet.lower() == "quitter":
        print("Au revoir !")
        break

    if not sujet:
        print("Veuillez entrer un sujet.")
        continue

    print("\n--- Explication ---")
    explication = expliquer_sujet(sujet)
    print(explication)

    print("\n--- Exercice ---")
    exercice = proposer_exercice(sujet)
    print(exercice)

    print("\n" + "-" * 50 + "\n")