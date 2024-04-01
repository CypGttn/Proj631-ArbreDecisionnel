"""PROJ631 - Arbre décisionnel
Auteur : GUITTON Cyprien IDU3 - G2
"""
#########################################################################################################################
#                                     MODULES NÉCESSAIRES AU PROGRAMME                                                  #
#########################################################################################################################

from math import log
import copy
import numpy as np 

#########################################################################################################################
#                             CREATION DE LA LISTE CONTENANT LE DICTIONNAIRE                                            #
#########################################################################################################################

#Creation d'un dictionnaire à partir d'un nom de fichier
def creation_dictionnaire(nom_fichier:str):
    """Retourne le dictionnaire associé au fichier csv passé en paramètre
    param : nom_fichier : str nom du fichier avec extension csv
    return : liste avec les données 
    """
    #On initialise le liste avec les données
    cas_de_figures = []
    lien_fichier = str(nom_fichier) + ".csv"
    #On apprend les différents attributs existants dans le csv
    with open(lien_fichier,"r") as f: 
        ids = f.readlines()[0]
        liste_id = ids.split(sep=',')[:-1]
        liste_id.append(ids.split(sep=',')[-1][:-1])
        
    
    #On créé le liste contenant les dictionnaires avec chaque combinaison
    with open(lien_fichier,"r") as f:
        liste_figure = []
        #A chaque itération, la liste apprend un dictionnaire contenant une combinaison
        for element in f.readlines()[1:]:
            mot = element.split(sep = ',')
            dico_global = {}
            figure = {}
            for i in range(len(liste_id)):
                if i == len(liste_id)-1: 
                    #On enlève le "\n" présent sur chaque dernier élément
                    figure[liste_id[i]]=mot[i][:-1]
                else : 
                    figure[liste_id[i]]=mot[i]
            
        
            liste_figure.append(figure)
    #ON construit le dictionnaire 
    dico_global["donnees"] = liste_figure
    #On créé l'attribut liste_attr contenant tous les attributs 
    dico_global["liste_attr"]= liste_id
    inter = {}
    liste_valeurs_attr = []

    for attr in dico_global["liste_attr"]: 
        for element in dico_global["donnees"]:
             
            if element[attr] not in liste_valeurs_attr:
                liste_valeurs_attr.append(element[attr])
        
            inter[attr]= liste_valeurs_attr
        liste_valeurs_attr = []
    dico_global["liste_valeurs_possibles"] = inter
    dico_global["liste_attr"]= liste_id[:-1]
    #La liste apprend le dictionnaire
    cas_de_figures.append(dico_global)
    return cas_de_figures
   
#########################################################################################################################
#                                        FORMULES DE CALCULS                                                            #
#########################################################################################################################

#Calcul de p et n 
def calcul_p(liste_dico):
    """Retourne le calcul de p pour un dictionnaire passé en paramètre
    param : liste_dico : liste contenant le dictionnaire de données
    return : int (le nombre de play P dans l'exemple de "golf.csv") 
    """
    p = 0 
    for i in range(len(liste_dico[0]["donnees"])):
        classe  = list(liste_dico[0]["liste_valeurs_possibles"].keys())[-1]
        if liste_dico[0]["donnees"][i][classe] == liste_dico[0]["liste_valeurs_possibles"][classe][0] :
            p+=1           
    return p

def calcul_n(liste_dico):
    """Retourne le calcul de n pour un dictionnaire passé en paramètre
    param : liste_dico : liste contenant le dictionnaire de données
    return : int (le nombre de play N dans l'exemple de "golf.csv") 
    """  
    n = 0 
    for i in range(len(liste_dico[0]["donnees"])):
        classe  = list(liste_dico[0]["liste_valeurs_possibles"].keys())[-1]
        if liste_dico[0]["donnees"][i][classe] == liste_dico[0]["liste_valeurs_possibles"][classe][1] :
            n+=1
    
    return n 

def calcul_I(p,n):
    """Retourne la valeur de I
    param : p : int 
            n : int
    return : float
    """
    if (p+n) == 0 :
        p_sur_pn = 0
        n_sur_pn = 0
    else : 
        p_sur_pn = p/(p+n)
        n_sur_pn = n/(p+n)
    #On prend en compte l'exception de la division par 0 
    if n_sur_pn == 0 or p_sur_pn == 0 : 
        return 0 
    return -p_sur_pn*log(p_sur_pn,2)-n_sur_pn*log(n_sur_pn,2)

def calcul_E(attribut, dico):
    """Calcule la valeur de E pour une attribut rentré en paramètre
    param : attribut : str
            dico : dictionnaire des donnees
    return : float
    """
    somme = 0
    liste = []
    for element in dico[0]["donnees"]:
        if element[attribut] not in liste: 
            liste.append(element[attribut])
    #print(liste)
    dictionnaire_y_n={}
    for element in liste:    
        dictionnaire_y_n[element+"_yes"]=0
        dictionnaire_y_n[element+"_no"]=0
    #Création d'une liste avec les play pour chaque cas de figures
    for i in range(len(dico[0]["donnees"])):
        classe  = list(dico[0]["liste_valeurs_possibles"].keys())[-1]
        yes_no = dico[0]["donnees"][i][classe]
        var = dico[0]["donnees"][i][attribut]
        if yes_no == "yes": 
            dictionnaire_y_n[var+"_"+yes_no]+=1
                
        if yes_no == "no": 
            dictionnaire_y_n[var+"_"+yes_no]+=1
                
    for categorie in liste: 
        p_i = dictionnaire_y_n[categorie+"_yes"]
  
        n_i = dictionnaire_y_n[categorie+"_no"]
        somme += ((p_i+n_i)/(calcul_p(dico)+calcul_n(dico)))*calcul_I(p_i,n_i)
    
    return somme

def calcul_gain(A,p,n, dico):
    """Calcul de le gain pour un attribut passé en paramètre
    param : A : str
            p : int
            n : int
            dico : dictionnaire contenant les informations
    return float
    """
    return calcul_I(p,n)-calcul_E(A,dico)

#########################################################################################################################
#                                        CHOIX PREMIER NOEUD                                                            #
#########################################################################################################################

#Classe Noeud
class Node: 
    def __init__(self, attribut:str=None, value=None, children=None, resultat=None):
        self.value = value
        self.attribut = attribut
        self.children = children
        self.resultat = resultat
        
    def affichage(self):
        print(self.value)
        
#Set le meilleur choix de noeud de base
def best_attr(dictionnaire):
    """Choisi le meilleur attribut pour démarrer l'arbre
    param : dictionnaire : liste contenant les données 
    return : str
    """
    liste_id = dictionnaire[0]["liste_attr"]
    #On initilise le choix en prenant la première valeur possible dans la liste des attributs disponibles
    choix = liste_id[0]
    p = calcul_p(dictionnaire)
    n = calcul_n(dictionnaire)
    val_choix = calcul_gain(choix,p,n, dictionnaire)
    #On compare le premier choix initialisé aux autres possibilités
    for element in liste_id[1:]:
        if calcul_gain(element,p,n, dictionnaire) > val_choix:
            choix = element 
            val_choix = calcul_gain(element,p,n, dictionnaire)
    if val_choix > 0 : 
        return choix


def partitionne(attribut, valeur_attribut, dictionnaire):
    """ Créer un nouveau dictionnaire en choissisant un attribut et une valeur spécifique de cet attribut
    param : attribut : str
            valeur_attribut : str
            dictionnaire : liste contenant les données
    return : liste : liste contenant les données après séléction
    """
    dico = dictionnaire[0]["donnees"]
    
    liste_parti = []
    #On séléctionne les élements de l'ancien dictionnaire pour lesquels la valeur de l'attribut est la bonne
    for i in range(len(dico)):
        if dico[i][attribut] == valeur_attribut: 
            liste_parti.append(dico[i])
    liste_ids = dictionnaire[0]["liste_attr"]
    liste_ids.remove(attribut)
    #On créé un nouveau dictionnaire en se basant sur le même format que la création du dictionnaire de la fonction "creation_dictionnaire"
    dictionnaire_parti = {}
    dictionnaire_parti["donnees"]=liste_parti
    dictionnaire_parti["liste_attr"]=liste_ids
    inter = {}
    liste_valeurs_attr = []
    for attr in dictionnaire_parti["liste_attr"]: 
        for element in dictionnaire_parti["donnees"]:
            if element[attr] not in liste_valeurs_attr:
                liste_valeurs_attr.append(element[attr])
        
            inter[attr]= liste_valeurs_attr
        liste_valeurs_attr = []
    
    cle = list(dico[0].keys())[-1]
    liste_valeur_cle = []
    for element in dico:
        if element[cle] not in liste_valeur_cle:
            liste_valeur_cle.append(element[cle])
    inter[cle] = liste_valeur_cle
    dictionnaire_parti["liste_valeurs_possibles"] = inter
    
    partition = []
    partition.append(dictionnaire_parti)
    return partition

def occurence_val(val, dico):
    """Retourne le nombre d'occurence d'une valeur dans un dictionnaire donnée
    param : dictionnaire : le dictionnaire des donnees
            val : la valeur que l'on veut compter
    return : int 
    """
    count =  0
    for element in dico:
        if val in list(element.values()):
            count +=1
    return count

def creation_arbre(dictionnaire):
    """Créé l'arbre à partir d'un dictionnaire passé en paramètre
    param : dictionnaire : liste contenant les données
    return : node 
    """
    
    #Premier condition d'arret : l'ensemble d'exemples associés au noeud courant 
    if dictionnaire[0]["donnees"] == []: 
        return Node(resultat="null")
    #Deuxieme conditon d'arret: Tous les exemples d’apprentissage associés au noeud courant ont la même valeur de classe,
    #auquel cas une feuille avec cette valeur de classe est retournée.
    if len(list(dictionnaire[0]["liste_valeurs_possibles"].values())[-1]) == 1: #On va chercher la ou les valeurs de classe
        var = list(dictionnaire[0]["liste_valeurs_possibles"].values())[-1][0]
        return Node(resultat = var)
    
    #Troisième condition d'arrêt: Tous les attributs ont été utilisés sur la branche en cours de développement, auquel cas une
    #feuille est retournée avec la classe majoritaire parmi les exemples associés au noeud courant.
    if len(dictionnaire[0]["liste_attr"]) == 1: # il ne reste que la classe (play dans le cas de "golf.csv")
        val1 = list(dictionnaire[0]["liste_valeurs_possibles"].values())[-1][0]
        
        val2 = list(dictionnaire[0]["liste_valeurs_possibles"].values())[-1][1]
        liste = dictionnaire[0]["donnees"]
        
        if occurence_val(val1,liste) > occurence_val(val2,liste):
            return Node(resultat=val1)
        elif occurence_val(val1,liste) < occurence_val(val2,liste):
            return Node(resultat=val2)
        else:
            return Node()
    #On choix le meilleur attribut pour construire l'arbre
    best_attribut = best_attr(dictionnaire)
    print(f"Le meilleur attribut est : {best_attribut}")
    
    liste_val_best_attr = []
    if best_attribut == None : 
        val1 = list(dictionnaire[0]["liste_valeurs_possibles"].values())[-1][0]
        
        val2 = list(dictionnaire[0]["liste_valeurs_possibles"].values())[-1][1]
        liste = dictionnaire[0]["donnees"]
        
        if occurence_val(val1,liste) > occurence_val(val2,liste):
            return Node(resultat=val1)
        elif occurence_val(val1,liste) < occurence_val(val2,liste):
            return Node(resultat=val2)
        else:
            return Node()
        
    else : 
        #Dans le cas où il existe un meilleur attribut, on créé le sous arbre 
        for element in dictionnaire[0]["donnees"]: 
            if element[best_attribut] not in liste_val_best_attr:
                liste_val_best_attr.append(element[best_attribut])
    
        sous_arbre = {}
        for valeur in liste_val_best_attr: 
            copy_dico = copy.deepcopy(dictionnaire)  
        
            sous_arbre[valeur]  = creation_arbre(partitionne(best_attribut,valeur, copy_dico))
            
    
    return Node(value=best_attribut, children = sous_arbre)

#########################################################################################################################
#                                      MATRICE DE CONFUSION                                                             #
#########################################################################################################################

def predire(arbre, dictionnaire, matrice):
    """Construit la matrice de confusion de l'arbre passé en paramètre
    param : arbre : arbre
            dictionnaire : liste contenant le dictionnaire avec toutes les donnees
    return matrice : la matrice de confusion
    """
    #Condition d'arrêt : l'arbre est une feuille
    #Dans cas on incrémente la matrice de confusion
    if arbre.children is None :
        yes = "yes"
        no = "no"
        classe = list(dictionnaire[0]["liste_valeurs_possibles"].keys())[-1]
        #On compare les resultats des branches puis on incrémente la matrice
        if arbre.resultat == yes and dictionnaire[0]["donnees"][0][classe]==yes : 
            matrice[0][0] +=1
            
        elif arbre.resultat == no and dictionnaire[0]["donnees"][0][classe]==no : 
            matrice[1][1] +=1
            
        elif arbre.resultat == no and dictionnaire[0]["donnees"][0][classe]==yes : 
            matrice[1][0] +=1
            
        elif arbre.resultat == yes and dictionnaire[0]["donnees"][0][classe]==yes : 
            matrice[0][1] +=1
               
    #S'il existe des enfants on parcourt l'arbre jusqu'à atteindre une feuille
    if arbre.children is not None: 
        for child in list(arbre.children):
            copie = copy.deepcopy(dictionnaire)
            dico = partitionne(arbre.value, child, copie)
            predire(arbre.children[child], dico, matrice)
        
    return matrice

#########################################################################################################################
#                                                TESTS                                                                  #
#########################################################################################################################

#On initilise la liste avec le dictionnaire à partir du nom du fichier
dico = creation_dictionnaire("golf")
print(f"La liste contenant les données sous la forme d'un dictionnaire est le suivant : {dico} ")

#on affiche le premier element pour créer la racine
print(f"La racine sera l'attribut : {best_attr(dico)}")

#On créé l'arbre à partir du dictionnaire 
arbre = creation_arbre(dico)

#On initialise la matrice de confusion avec des 0
matrice = np.array([[0,0],[0,0]])
#On incrémente la matrice de confusion
matrice_conf = predire(arbre, dico, matrice)
print(f"La matrice de confusion est la suivant : \n {matrice_conf}")

