from math import log
import copy

#########################################################################################################################
#                             CREATION DE LA LISTE CONTENANT LE DICTIONNAIRE                                            #
#########################################################################################################################
#Liste des valeurs des attributs d'un attribut donné
def outcome(dictionnaire, attribut):
    """Pour un attribut donné, donne toutes ses valeurs possibles
    param : dictionnaire : liste contenant les données
            atribut : str
    return : list
    
    """
    liste_valeurs_attr = []

    for element in dictionnaire[0]["donnees"]: 
        if element[attribut] not in liste_valeurs_attr:
            liste_valeurs_attr.append(element[attribut])
    return liste_valeurs_attr

#Creation d'une liste vide
cas_de_figures = []

#On apprend les différents attributs existants dans le csv
with open("golf.csv","r") as f:
    ids = f.readlines()[0]
    liste_id = ids.split(sep=',')[:-1]
    
#On créé le liste contenant les dictionnaires avec chaque combinaison
with open("golf.csv","r") as f:
    liste_figure = []
    #A chaque itération, la liste apprend un dictionnaire contenant une combinaison
    for element in f.readlines()[1:]: 
        mot = element.split(sep = ',')
        dico_global = {}
        figure = {}
        figure[liste_id[0]]=mot[0]
        figure[liste_id[1]]=mot[1]
        figure[liste_id[2]]=mot[2]
        figure[liste_id[3]]=mot[3]
        figure["play"]=mot[4][:-1]
        
        liste_figure.append(figure)
        
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
    cas_de_figures.append(dico_global)
   
   
#########################################################################################################################
#                                        FORMULES DE CALCULS                                                            #
#########################################################################################################################

#Calcul de p et n 
def calcul_p(liste_dico):
    """Retourne le calcul de p pour un dictionnaire passé en paramètre
    param : liste_dico : liste contenant le dictionnaire de données
    return : int (le nombre de play P) 
    """
    p = 0 
    for i in range(len(liste_dico[0]["donnees"])):
        if liste_dico[0]["donnees"][i]["play"] == "yes" :
            p+=1           
    return p

def calcul_n(liste_dico):
    """Retourne le calcul de n pour un dictionnaire passé en paramètre
    param : liste_dico : liste contenant le dictionnaire de données
    return : int (le nombre de play N) 
    """  
    n = 0 
    for i in range(len(liste_dico[0]["donnees"])):
        if liste_dico[0]["donnees"][i]["play"] == "no" :
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
    if n_sur_pn == 0 or p_sur_pn == 0 : 
        return 0 
    return -p_sur_pn*log(p_sur_pn,2)-n_sur_pn*log(n_sur_pn,2)

def calcul_E(attribut):
    """Calcule la valeur de E pour une attribut rentré en paramètre
    param : attribut : str
    return : float
    """
    somme = 0
    liste = []
    for element in cas_de_figures[0]["donnees"]:
        if element[attribut] not in liste: 
            liste.append(element[attribut])
    #print(liste)
    dictionnaire_y_n={}
    for element in liste:    
        dictionnaire_y_n[element+"_yes"]=0
        dictionnaire_y_n[element+"_no"]=0
    #Création d'une liste avec les play pour chaque cas de figures
    for i in range(len(cas_de_figures[0]["donnees"])):
        
        yes_no = cas_de_figures[0]["donnees"][i]["play"]
        var = cas_de_figures[0]["donnees"][i][attribut]
        if yes_no == "yes": 
            dictionnaire_y_n[var+"_"+yes_no]+=1
                
        if yes_no == "no": 
            dictionnaire_y_n[var+"_"+yes_no]+=1
                
    for categorie in liste: 
        p_i = dictionnaire_y_n[categorie+"_yes"]
  
        n_i = dictionnaire_y_n[categorie+"_no"]
        somme += ((p_i+n_i)/(calcul_p(cas_de_figures)+calcul_n(cas_de_figures)))*calcul_I(p_i,n_i)
    
    return somme

def calcul_gain(A,p,n):
    """Calcul de le gain pour un attribut passé en paramètre
    param : A : str
            p : int
            n : int
    return float
    """
    return calcul_I(p,n)-calcul_E(A)

#########################################################################################################################
#                                        CHOIX PREMIER NOEUD                                                            #
#########################################################################################################################

#Creation de noeud

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
    
    #liste_id.append(list(dictionnaire[0]["donnees"][1].keys())[:-1])
      
    choix = liste_id[0]
    p = calcul_p(dictionnaire)
    n = calcul_n(dictionnaire)
    val_choix = calcul_gain(choix,p,n)
    for element in liste_id[1:-1]:
        if calcul_gain(element,p,n) > val_choix:
            choix = element 
            val_choix = calcul_gain(element,p,n)
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
    for i in range(len(dico)):
        if dico[i][attribut] == valeur_attribut: 
            liste_parti.append(dico[i])
    liste_ids = dictionnaire[0]["liste_attr"]

    liste_ids.remove(attribut)
    
                 
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
    
    #Condition d'arret 3: Tous les attributs ont été utilisés sur la branche en cours de développement, auquel cas une
    #feuille est retournée avec la classe majoritaire parmi les exemples associés au noeud courant.
    if len(dictionnaire[0]["liste_attr"]) == 1: # il ne reste que la classe
        val1 = list(dictionnaire[0]["liste_valeurs_possibles"].values())[-1][0]
        val2 = list(dictionnaire[0]["liste_valeurs_possibles"].values())[-1][1]
        liste = dictionnaire[0]["donnees"]
        
        if occurence_val(val1,liste) > occurence_val(val2,liste):
            return Node(resultat=val1)
        elif occurence_val(val1,liste) < occurence_val(val2,liste):
            return Node(resultat=val2)
        else:
            return Node()
    
    best_attribut = best_attr(dictionnaire)
    print(f"Le meilleur attribut est : {best_attribut}")
    
    liste_val_best_attr = []

    for element in dictionnaire[0]["donnees"]: 
        if element[best_attribut] not in liste_val_best_attr:
            liste_val_best_attr.append(element[best_attribut])
    
    sous_arbre = {}
    for valeur in liste_val_best_attr: 
        copy_dico = copy.deepcopy(dictionnaire)  
        
        sous_arbre[valeur]  = creation_arbre(partitionne(best_attribut,valeur, copy_dico))
    
    return Node(value=best_attribut, children = sous_arbre)
           
#print(partitionne("outlook", "sunny", cas_de_figures))
print(creation_arbre(cas_de_figures))