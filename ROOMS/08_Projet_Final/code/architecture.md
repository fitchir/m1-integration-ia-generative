# Architecture du projet final - Assistant de recherche documentaire

## Cas d’usage choisi
Assistant de recherche documentaire capable d’indexer un document texte, de rechercher les passages les plus pertinents et de répondre aux questions en citant la source.

## Entrées du système
- Un fichier texte à indexer
- Une question posée par l’utilisateur en ligne de commande

## Composants principaux
1. **Chargement du document**
   - Lecture du fichier texte
2. **Découpage**
   - Le texte est découpé en segments de taille fixe avec chevauchement
3. **Embeddings**
   - Chaque segment est vectorisé avec `all-MiniLM-L6-v2`
4. **Base vectorielle**
   - Les embeddings sont stockés dans ChromaDB
5. **Recherche**
   - La question de l’utilisateur est vectorisée
   - Les passages les plus proches sont récupérés
6. **Génération**
   - Un prompt RAG est construit avec les passages retrouvés
   - Le LLM répond en se basant uniquement sur ces passages

## Sorties
- Une réponse textuelle
- Les passages sources utilisés
- Une gestion des questions hors sujet

## Risques identifiés
- **Hallucination** : le modèle peut inventer si le contexte est insuffisant
- **Question hors sujet** : risque de répondre hors document
- **Données sensibles** : si un document réel contient des données personnelles
- **Biais** : formulation ou interprétation biaisée du document

## Mesures de mitigation
- Prompt strict : répondre uniquement à partir des passages
- Réponse de refus si l’information n’est pas présente
- Affichage des sources utilisées
- Recommandation d’anonymisation des documents sensibles

## Schéma du flux
Utilisateur
  |
  | question
  v
script principal
  |
  | embedding de la question
  v
ChromaDB
  |
  | passages pertinents
  v
construction du prompt RAG
  |
  | contexte + question
  v
API Groq / modèle Llama
  |
  | réponse contextualisée
  v
réponse + sources affichées