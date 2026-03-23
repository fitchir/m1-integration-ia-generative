# Script Challenge Room 02 - Générateur de quiz en JSON
# Room 02 - Construire avec des prompts

import json
import sys
import os

# Ajouter la racine du projet au path pour importer utils.py
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from utils import creer_client, MODELE

client = creer_client()

# Chemin du fichier de prompt
PROMPT_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "expected_outputs",
    "challenge_room02_prompt.txt"
)


def charger_prompt_modele():
    """Charge le prompt de base depuis le fichier texte."""
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        return f.read()


def generer_quiz_json(sujet, max_tentatives=3):
    """
    Envoie le prompt au LLM avec le sujet donné.
    Réessaie jusqu'à max_tentatives fois tant que le JSON est invalide.
    Retourne le dictionnaire Python si succès, None sinon.
    """
    prompt_modele = charger_prompt_modele()

    for tentative in range(1, max_tentatives + 1):
        print(f"\n=== Tentative {tentative}/{max_tentatives} ===")

        # On insère le sujet dans le prompt modèle
        prompt_complet = prompt_modele.format(sujet=sujet)

        reponse = client.chat.completions.create(
            model=MODELE,
            messages=[{"role": "user", "content": prompt_complet}],
            temperature=0.3,
            max_tokens=800
        )

        texte = reponse.choices[0].message.content

        print("\n--- Réponse brute du modèle ---")
        print(texte)
        print()

        # Tentative de parsing JSON
        try:
            quiz = json.loads(texte)
            print("✅ JSON valide reçu.")
            return quiz
        except json.JSONDecodeError as e:
            print("❌ JSON invalide reçu.")
            print(f"Détail de l'erreur : {e}")
            if tentative < max_tentatives:
                print("On réessaie avec une nouvelle requête...")
            else:
                print("Nombre maximum de tentatives atteint. Abandon.")
    return None


def afficher_quiz(quiz):
    """Affiche le quiz de manière lisible dans le terminal."""
    print("\n=== Quiz généré ===")
    print(f"Sujet : {quiz.get('sujet', 'Inconnu')}")
    print()

    questions = quiz.get("questions", [])
    for q in questions:
        numero = q.get("numero", "?")
        question = q.get("question", "")
        options = q.get("options", [])
        bonne = q.get("bonne_reponse", "?")

        print(f"Question {numero} : {question}")
        print("Options :")
        for opt in options:
            print(f"  - {opt}")
        print(f"=> Bonne réponse : {bonne}")
        print("-" * 40)


def main():
    print("=== Challenge Room 02 – Générateur de quiz en JSON ===")
    print("Tapez 'quitter' pour sortir.")
    print()

    while True:
        sujet = input("Sujet du quiz : ").strip()

        if sujet.lower() == "quitter":
            print("Au revoir !")
            break

        if not sujet:
            print("Veuillez entrer un sujet valide.\n")
            continue

        quiz = generer_quiz_json(sujet, max_tentatives=3)

        if quiz is None:
            print("Impossible d'obtenir un JSON valide après plusieurs tentatives.\n")
        else:
            afficher_quiz(quiz)
            print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()