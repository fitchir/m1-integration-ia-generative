import os
import sys
import uuid
import chromadb
from sentence_transformers import SentenceTransformer

# Pour importer utils.py depuis la racine du projet
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from utils import creer_client, MODELE


def charger_fichier_txt(chemin_fichier):
    if not os.path.exists(chemin_fichier):
        raise FileNotFoundError(f"Fichier introuvable : {chemin_fichier}")

    if not chemin_fichier.lower().endswith(".txt"):
        raise ValueError("Le fichier doit être au format .txt")

    with open(chemin_fichier, "r", encoding="utf-8") as f:
        return f.read()


def decouper_texte(texte, taille_segment=300, chevauchement=50):
    mots = texte.split()
    segments = []
    debut = 0

    while debut < len(mots):
        fin = debut + taille_segment
        segment = " ".join(mots[debut:fin])
        segments.append(segment)

        if fin >= len(mots):
            break

        debut += taille_segment - chevauchement

    return segments


def creer_index(segments):
    print("Chargement du modèle d'embedding...")
    modele_embedding = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    print("Modèle chargé.")

    print("Création des embeddings...")
    embeddings = modele_embedding.encode(segments).tolist()

    client_chroma = chromadb.Client()
    collection = client_chroma.create_collection(name=f"rag_{uuid.uuid4().hex[:8]}")

    ids = [f"seg_{i}" for i in range(len(segments))]
    metadatas = [{"source": f"segment_{i+1}"} for i in range(len(segments))]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=segments,
        metadatas=metadatas
    )

    print(f"Index créé : {len(segments)} segments stockés.")
    return modele_embedding, collection


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
Voici des extraits d'un document texte :
---
{contexte}
---
En te basant UNIQUEMENT sur ces extraits, réponds à la question suivante :
{question}

Donne une réponse claire et cite les sources utilisées entre parenthèses.
"""

    reponse = client_llm.chat.completions.create(
        model=MODELE,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=300
    )

    return reponse.choices[0].message.content


def main():
    if len(sys.argv) != 2:
        print("Usage : python challenge_room05.py mon_fichier.txt")
        return

    chemin_fichier = sys.argv[1]

    try:
        print("Chargement du fichier texte...")
        texte = charger_fichier_txt(chemin_fichier)
        print(f"Fichier chargé : {len(texte)} caractères")

        print("Découpage du texte...")
        segments = decouper_texte(texte)
        print(f"{len(segments)} segments créés")

        modele_embedding, collection = creer_index(segments)
        client_llm = creer_client()

        print("\n=== Système RAG prêt ===")
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
                print(f"\n--- Passage {i} ({p['source']}, distance={p['distance']:.4f}) ---")
                print(p["texte"][:500] + ("..." if len(p["texte"]) > 500 else ""))

            reponse = generer_reponse(question, passages, client_llm)

            print("\n=== Réponse RAG ===")
            print(reponse)
            print("\n" + "=" * 60 + "\n")

    except FileNotFoundError as e:
        print(f"Erreur : {e}")
    except ValueError as e:
        print(f"Erreur : {e}")
    except Exception as e:
        print(f"Une erreur inattendue est survenue : {e}")


if __name__ == "__main__":
    main()