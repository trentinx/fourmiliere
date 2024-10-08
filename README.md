# Une vie de fourmi

## Problématique
### &Eacute;noncé
Une fourmilière est représentée sous forme d'un graphe dont les noeuds sont des salles.
Les individus sont regroupés dans le vestibule et doivent atteindre le dortoir en passant par
des salles intermédiaires pouvant acceuillir chacune un nombre variable de fourmis.

### Exemple
La fourmilière fournie dans le fichier fourmiliere_zero.txt peut se représenter comme suit:

![Graph](pics/fourmiliere_zero/graph.png)


## Solutions

### Intuition
Nous avons considéré les fourmis comme un nombre et non comme des individus. Ainsi, on déplace un nombre d'individus d'un coup d'une salle à une autre.

Chaque fois que des individus avancent dans une salle suivante, ils laissent autant de place pour des individus de la salle précédente. Comme les fourmis avancent toutes ensemble à la même vitesse, on implémente un algorithme qui commence par la cellule finale (le dortoir) et remonte par tous les chemins possibles jusqu'à la salle de départ (le vestibule), afin de déplacer les fourmis les plus avancées en premier, pour libérer de la place pour celles qui les suivent.

### &Eacute;tapes
- Lecture et parsing des fichiers fournis décrivant les fourmilières.
- Modélisation de la fourmilière sous forme de graphe.
- Implémentation d'une fonction récursive qui remonte tous les noeuds précédents d'un noeud donné.
- Déplacement des fourmis selons les règles indiquées.
- Représentation graphique de la fourmilère et des étapes.
- Ajout du calcul la distance de chaque salle à au dortoir (règle le problème de crash lorsqu'un circuit élémentaire est présent) 

### Implémentation
Les salles sont représentés par des instances d'une classe Room. La fourmilière est également modélisée sous la forme d'une classe qui liste l'enseble de ses salles sous forme de dictionnaire.   

Nous avons implémenté une fonction récursive qui permet de remonter dans toutes les salles immédiatement précédentes d'une salle donnée (puis les salles précédentes de ses salles précédentes, etc.) et d'en déplacer les fourmis qui peuvent l'être.

La fonction est appliquée à l'ensemble des salles de la fourmilière, et le programme boucle tant que toutes les fourmis ne sont pas dans le dortoir.

### Exemple 
Le fichier fourmiliere_zero.txt donne une fourmilière simple avec deux salles intermédiaires en parallèle ne pouvant accueillir qu'une fourmi à la fois. La population est composée de deux fourmis.

Les étapes de déplacement sont les suivantes:

![step 0](pics/fourmiliere_zero/initiale.png)
![step 1](pics/fourmiliere_zero/1.png)
![step 2](pics/fourmiliere_zero/2.png)


## Conclusion
La solution mise en place a permis de résoudre les problèmes qui ont été fournis.

Perspectives :
- Minimiser le nombre d'étapes.
- ~~Gérer les problèmes de circuits élémentaires / cycles.~~
- Implémenter une classe représentant les fourmis individuellement (les attributs de classe permettant de passer des informations sur les chemins déjà parcourus à l'ensemble des individus).

# Usage
En ligne de commande.
```bash
python main.py python main.py <filename>
```
$$filename$$ est le nom du fichier (qui doit être placé dans data/fourmilieres)