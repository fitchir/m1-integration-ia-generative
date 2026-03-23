import os
import uuid
import chromadb
from sentence_transformers import SentenceTransformer


def charger_document(chemin_fichier):
    if not os.path.exists(chemin_fichier):
        raise FileNotFoundError(f"Fichier introuvable : {chemin_fichier}")

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


def creer_index(chemin_fichier):
    print("Chargement du document...")
    texte = charger_document(chemin_fichier)

    print("Découpage du document...")
    segments = decouper_texte(texte)
    print(f"{len(segments)} segments créés.")

    print("Chargement du modèle d'embedding...")
    modele_embedding = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    print("Modèle chargé.")

    print("Création des embeddings...")
    embeddings = modele_embedding.encode(segments).tolist()

    client_chroma = chromadb.Client()
    collection = client_chroma.create_collection(name=f"projet_final_{uuid.uuid4().hex[:8]}")

    ids = [f"seg_{i}" for i in range(len(segments))]
    metadatas = [{"source": f"segment_{i+1}"} for i in range(len(segments))]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=segments,
        metadatas=metadatas
    )

    print("Index créé avec succès.")
    return modele_embedding, collection