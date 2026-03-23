# Challenge - Room 02

## Objectif

Construire un générateur de quiz en JSON exploitable directement par un programme Python.

## Défi

Concevez un prompt qui demande au modèle de générer un quiz de 5 questions à choix multiples sur un sujet donné par l'utilisateur. Le quiz doit être retourné en JSON strictement valide, avec la structure suivante :

```json
{
  "sujet": "...",
  "questions": [
    {
      "numero": 1,
      "question": "...",
      "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
      "bonne_reponse": "A"
    }
  ]
}
```

## Consignes

1. Écrivez le prompt dans un fichier `challenge_room02_prompt.txt`.
2. Créez un script Python `challenge_room02.py` qui :
   - Demande un sujet à l'utilisateur en ligne de commande
   - Envoie le prompt au LLM avec ce sujet
   - Parse le JSON retourné
   - Affiche chaque question et ses options de façon lisible
   - Révèle la bonne réponse après chaque question
3. Testez avec au moins 2 sujets différents.

## Contraintes

- La sortie JSON doit être parsée avec `json.loads()` sans erreur.
- Si le JSON est invalide, le script doit afficher un message d'erreur clair et redemander.
- Le script doit fonctionner en boucle jusqu'à obtenir un JSON valide (maximum 3 tentatives).