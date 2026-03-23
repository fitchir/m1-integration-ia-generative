# Script 12 - Client Python qui interroge le serveur FastAPI local
# Room 04 - Connecter une API
# Prérequis : le serveur 11_mini_api_fastapi.py doit tourner sur le port 8000

import requests

BASE_URL = "http://127.0.0.1:8000"


def verifier():
    try:
        r = requests.get(f"{BASE_URL}/")
        if r.status_code == 200:
            print("=== Serveur OK ===")
            print(r.json()["message"])
            print()
            return True
    except:
        print("Serveur inaccessible")
    return False


def afficher_historique():
    r = requests.get(f"{BASE_URL}/historique")
    if r.status_code == 200:
        data = r.json()["historique"]
        print("\n=== HISTORIQUE ===")
        if not data:
            print("(vide)")
        for msg in data:
            print(f"{msg['role']} : {msg['content']}")
        print()


def reset():
    requests.post(f"{BASE_URL}/reset")
    print("Historique vidé\n")


def poser(question):
    r = requests.post(
        f"{BASE_URL}/question",
        json={"question": question}
    )

    if r.status_code == 200:
        print("\n=== Réponse ===")
        print(r.json()["reponse"])
        afficher_historique()
    else:
        print("Erreur :", r.text)


if __name__ == "__main__":
    if verifier():
        print("Tape 'historique', 'reset' ou 'quitter'\n")

        while True:
            q = input("Question : ")

            if q == "quitter":
                break
            elif q == "historique":
                afficher_historique()
            elif q == "reset":
                reset()
            else:
                poser(q)