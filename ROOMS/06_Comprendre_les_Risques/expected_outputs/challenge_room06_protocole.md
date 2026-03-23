# Protocole d'audit des réponses d'un LLM

## Étape 1 : Vérification factuelle
Description :
Vérifier que toutes les informations produites par le modèle sont correctes en les comparant à des sources fiables.
Outils :
Wikipédia, sites officiels, bases de données.
Exemple :
Comparer une statistique donnée avec les données INSEE.

---

## Étape 2 : Détection de biais
Description :
Analyser les réponses pour identifier des stéréotypes ou des biais culturels.
Outils :
Tests de prompts (neutre vs orienté).
Exemple :
Comparer la description d’un métier selon le genre.

---

## Étape 3 : Protection des données
Description :
Vérifier qu’aucune donnée personnelle n’est exposée ou envoyée à l’API.
Outils :
Anonymisation, filtrage des entrées.
Exemple :
Supprimer les noms et emails avant envoi.

---

## Étape 4 : Validation humaine finale
Description :
Un humain valide la réponse avant publication.
Outils :
Relecture manuelle.
Exemple :
Validation par un expert métier avant diffusion.

---

## Conclusion
Ce protocole permet de réduire les risques liés aux hallucinations, biais et fuites de données lors de l'utilisation d'un LLM en contexte professionnel.