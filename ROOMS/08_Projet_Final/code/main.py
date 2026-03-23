import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from utils import creer_client, MODELE
from build_index import creer_index


def rechercher_passages(question, modele_embedding, collection, top_k=3):
    question_embedding = modele_embedding.encode([question]).tolist()[0]

    resultats = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k
    )

    documents = resultats["documents"][0]
    metadatas = resultats["metadatas"][0]
    distances = resultats["distances"][0]

    passages = []
    for doc, meta, dist in zip(documents, metadatas, distances):
        passages.append({
            "texte": doc,
            "source": meta["source"],
            "distance": dist
        })

    return passages


def generer_reponse(question, passages, client_llm):
    contexte = "\n\n".join(
        [f"[{p['source']}]\n{p['texte']}" for p in passages]
    )

    prompt = f"""
Voici des extraits d'un document :
---
{contexte}
---
Réponds UNIQUEMENT à partir de ces extraits.
Si l'information n'est pas dans le document, réponds exactement :
"Cette information ne figure pas dans le document fourni."

Question : {question}

Donne une réponse claire et cite les sources utilisées entre parenthèses.
"""

    reponse = client_llm.chat.completions.create(
        model=MODELE,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=300
    )

    return reponse.choices[0].message.content


if __name__ == "__main__":
    chemin_document = "C:/Users/itchi/Int-gration-d-IA-g-n-rative-M1-LDFS/datasets/texte_entreprise.txt"

    client_llm = creer_client()
    modele_embedding, collection = creer_index(chemin_document)

    print("\n=== Assistant de recherche documentaire prêt ===")
    print("Posez vos questions sur le document.")
    print("Tapez 'quitter' pour arrêter.\n")

    while True:
        question = input("Question : ").strip()

        if question.lower() == "quitter":
            print("Au revoir !")
            break

        if not question:
            print("Veuillez entrer une question.\n")
            continue

        passages = rechercher_passages(question, modele_embedding, collection, top_k=3)

        print("\n=== Passages sources ===")
        for i, p in enumerate(passages, start=1):
            print(f"\n--- Passage {i} ({p['source']}) ---")
            print(p["texte"][:500] + ("..." if len(p["texte"]) > 500 else ""))

        reponse = generer_reponse(question, passages, client_llm)

        print("\n=== Réponse ===")
        print(reponse)
        print("\n" + "=" * 60 + "\n")