import os
import sys
import json

# Pour importer utils.py depuis la racine du projet
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))

from utils import creer_client, MODELE

client = creer_client()


def charger_articles(chemin_fichier):
    with open(chemin_fichier, "r", encoding="utf-8") as f:
        contenu = f.read()

    # Découpage simple sur lignes vides
    blocs = [bloc.strip() for bloc in contenu.split("\n\n") if bloc.strip()]
    return blocs


def construire_prompt(texte):
    return f"""
Tu es un assistant d'analyse de texte.

Analyse le texte suivant et retourne UNIQUEMENT un objet JSON valide, sans texte avant ni après.

Structure attendue :
{{
  "sentiment": "positif | negatif | neutre",
  "mots_cles": ["mot1", "mot2", "mot3", "mot4", "mot5"],
  "resume": "Résumé en 2 phrases."
}}

Contraintes :
- "sentiment" doit être exactement : positif, negatif ou neutre
- "mots_cles" doit contenir exactement 5 éléments
- "resume" doit contenir 2 phrases maximum
- Réponds uniquement en JSON valide

Texte à analyser :
\"\"\"
{texte}
\"\"\"
"""


def analyser_un_texte(texte):
    prompt = construire_prompt(texte)

    reponse = client.chat.completions.create(
        model=MODELE,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=300
    )

    contenu = reponse.choices[0].message.content

    # Vérification JSON
    data = json.loads(contenu)

    # Vérification minimale de structure
    assert "sentiment" in data
    assert "mots_cles" in data
    assert "resume" in data
    assert isinstance(data["mots_cles"], list)
    assert len(data["mots_cles"]) == 5

    return data


if __name__ == "__main__":
    chemin_articles = "C:/Users/itchi/Int-gration-d-IA-g-n-rative-M1-LDFS/datasets/articles_presse.txt"

    print("=== Chargement des articles ===")
    articles = charger_articles(chemin_articles)
    print(f"{len(articles)} blocs trouvés\n")

    resultats = []

    for i, article in enumerate(articles[:3], start=1):
        print(f"--- Analyse article {i} ---")
        try:
            analyse = analyser_un_texte(article)
            resultats.append({
                "article": i,
                "analyse": analyse
            })
            print(json.dumps(analyse, ensure_ascii=False, indent=2))
            print()
        except json.JSONDecodeError as e:
            print(f"Erreur JSON sur l'article {i} : {e}\n")
        except Exception as e:
            print(f"Erreur sur l'article {i} : {e}\n")

    # Sauvegarde résultats
    sortie = "C:/Users/itchi/Int-gration-d-IA-g-n-rative-M1-LDFS/ROOMS/07_Projets_Guides/expected_outputs/resultats_analyse.json"
    with open(sortie, "w", encoding="utf-8") as f:
        json.dump(resultats, f, ensure_ascii=False, indent=2)

    print("=== Sauvegarde terminée ===")
    print(f"Résultats enregistrés dans : {sortie}")