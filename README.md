#Proj631 - Arbre décisionnel

Auteur : GUITTON Cyprien
Langage de programmation : Python

Le but de ce programme est à partir d'un fichier csv contenant différents attributs avec différentes valeurs et une décision à son extrémité de créer l'arbre décision de fichier.
Pour cela, à partir du nom du fichier, on créé une liste contenant un dictionnaire avec trois clés : 
1. "donnees" dont la valeur est une liste contenant toutes les combinaisons et la décision associées
2. "liste_valeurs_possibles" qui pour chaque attribut donne ses différentes valeurs possibles
3. "liste_attr" qui donne la liste des attributs pas encore utilisés lors de la création de l'arbre.

Pour créer l'arbre, on appelle la fonction "creation_arbre" prenant en paramètre une liste contenant un dictionnaire avec toutes les informatiosn expliquées précédemment. 
Pour choisir la racine de l'arbre, on utilise la fonction "best_attr" qui permet de calcul le gain pour chaque attribut et choisir l'attribut avec le gain le plus grand.
A partir de cette racine, on créé l'arbre de manière récursive en utilisant la classe "Node" et la fonction "creation_arbre" pour chauqe sous branche.

A partir de cet arbre et en le comparant avec le dictionnaire créé précédemment, nous allons pour créer la matrice de confusion qui permet de savoir si l'arbre a été crée correctement. 
Cela permet aussi de voir si les décisions données dans l'arbre sont les bonnes.

-------------------------------------------------------------------------------------------------------------------
UTILISATION
-------------------------------------------------------------------------------------------------------------------
Pour utiliser ce programme, vous pouvez télécharger le git et ouvrir le fichier "arbre_v2".
Avant de lancer le programme, vérifiez que les modules "math", "copy" et "numpy" sont importés dans votre executeur python.
Vous pourrez lancer le programme, le fichier par défaut est "golf.csv" mais vous pouvez changer le nom du fichier à la ligne 357.

Une fois lancé, le programme affichera dans un premier temps le dictionnaire créé, puis affichera le meilleur attribut pour la racine de l'arbre.
Ensuite l'arbre puis la matrice de confusion seront crées. Enfin le programme affichera la matrice de confusion.
