# Tableau comparatif des modèles - Room 03

## Réponses obtenues

### Mistral-7B-Instruct
```
[Une base de données relationnelle organise les informations sous forme de tables : chaque table regroupe des lignes (enregistrements) et des colonnes (attributs).
Les tables sont reliées entre elles par des clés (primaires et étrangères) qui permettent de faire des liens logiques, comme des relations entre clients et leurs commandes.
Grâce à ce modèle, on peut interroger, ajouter, modifier ou supprimer des données de façon structurée et cohérente à l’aide du langage SQL.]
```

### Llama 2 7B Chat
```
[Une base de données relationnelle est un système informatique qui stocke et organise des données sous forme de tables, où chaque table est composée de colonnes (attributs) et de lignes (enregistrements).
Chaque colonne représente un attribut spécifique des données, et chaque ligne représente un enregistrement unique.
Les relations entre les tables sont établies par des clés primaires et étrangères, permettant de lier les données entre elles.]
```

### Flan-T5-large
```
[Le modèle n’a pas respecté la consigne. Il a affiché son raisonnement intermédiaire au lieu de produire directement une réponse simple en 3 phrases.]
```

## Grille de comparaison


| Critère | Mistral-7B-Instruct | Llama 2 7B Chat | Flan-T5-large |
|---------|---------------------|-----------------|---------------|
| Qualité (correcte, pertinente ?) | Très bonne | Bonne | Faible |
| Longueur (nombre de phrases) | 3 phrases | 3 phrases | Non respecté |
| Cohérence (logique du début à la fin ?) | Très cohérente | Cohérente | Peu cohérente |
| Rapidité (estimation en secondes) | Rapide (~2-3s) | Rapide (~2-3s) | Rapide (~2-3s) |

## Analyse critique (5 lignes minimum)

[Le modèle Mistral-7B-Instruct a produit la meilleure réponse, car elle est claire, structurée et respecte parfaitement la consigne des 3 phrases simples. La réponse est également pédagogique et facile à comprendre pour un débutant.  
Le modèle Llama 2 fournit aussi une réponse correcte et pertinente, mais légèrement plus technique et moins fluide dans l’explication.  
Le modèle Flan-T5-large est le moins adapté dans ce test, car il ne respecte pas la consigne et affiche son raisonnement au lieu de donner directement une réponse exploitable.  
On constate donc que la qualité dépend non seulement de la taille du modèle, mais aussi de son entraînement à suivre des instructions.  
Pour construire un assistant pédagogique, le modèle Mistral serait le meilleur choix, car il produit des réponses claires, fiables et adaptées au niveau débutant.]
