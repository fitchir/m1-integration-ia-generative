import os
import sys

# Pour importer utils.py depuis la racine du projet
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))

from utils import creer_client, MODELE

client = creer_client()

SYSTEM_PROMPT = (
    "Tu es un assistant pédagogique bienveillant. "
    "Tu aides un étudiant débutant à comprendre clairement les notions. "
    "Tu réponds en français, de manière simple, structurée et concise."
)

# Historique complet
historique = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

MAX_MESSAGES_HORS_SYSTEM = 10  # au-delà, on résume les anciens messages


def resumer_conversation(messages_a_resumer):
    """
    Résume une partie de la conversation en un seul message.
    """
    texte = "\n".join(
        [f"{m['role']} : {m['content']}" for m in messages_a_resumer]
    )

    prompt = f"""
Tu es un assistant chargé de résumer une conversation.
Résume les échanges suivants en 3 phrases maximum, en conservant les informations importantes pour la suite de la discussion.

Conversation :
{texte}
"""

    reponse = client.chat.completions.create(
        model=MODELE,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=150
    )

    return reponse.choices[0].message.content


def ajouter_au_contexte(role, contenu):
    """
    Ajoute un message à l'historique.
    Si l'historique devient trop long, résume les anciens échanges
    au lieu de simplement les supprimer.
    """
    global historique

    historique.append({"role": role, "content": contenu})

    # On garde toujours le message système à part
    system_message = historique[0]
    autres_messages = historique[1:]

    # Si l'historique dépasse la limite, on résume les 5 premiers messages
    if len(autres_messages) > MAX_MESSAGES_HORS_SYSTEM:
        anciens = autres_messages[:5]
        reste = autres_messages[5:]

        resume = resumer_conversation(anciens)

        message_resume = {
            "role": "system",
            "content": "Résumé de la conversation précédente : " + resume
        }

        historique = [system_message, message_resume] + reste
    else:
        historique = [system_message] + autres_messages


def envoyer_message():
    """
    Envoie l'historique complet au LLM et retourne la réponse.
    """
    reponse = client.chat.completions.create(
        model=MODELE,
        messages=historique,
        temperature=0.3,
        max_tokens=300
    )
    return reponse.choices[0].message.content


def approx_tokens():
    """
    Estimation grossière du coût en tokens.
    """
    texte_total = " ".join(msg["content"] for msg in historique)
    nb_mots = len(texte_total.split())
    return int(nb_mots / 0.75)


def afficher_historique():
    print("\n=== Historique courant ===")
    for msg in historique:
        print(f"[{msg['role']}] {msg['content']}")
    print()


if __name__ == "__main__":
    print("=== Assistant mémoire avec résumé automatique ===")
    print("Posez vos questions.")
    print("Tapez 'historique' pour voir le contexte.")
    print("Tapez 'tokens' pour voir une estimation du coût.")
    print("Tapez 'quitter' pour arrêter.\n")

    while True:
        question = input("Vous : ").strip()

        if question.lower() == "quitter":
            print("Au revoir !")
            break

        if question.lower() == "historique":
            afficher_historique()
            continue

        if question.lower() == "tokens":
            print(f"Estimation approximative : {approx_tokens()} tokens\n")
            continue

        if not question:
            print("Veuillez entrer une question.\n")
            continue

        ajouter_au_contexte("user", question)
        reponse = envoyer_message()
        ajouter_au_contexte("assistant", reponse)

        print(f"\nAssistant : {reponse}\n")