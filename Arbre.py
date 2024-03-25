from math import log
   
#########################################################################################################################
#                                        FORMULES DE CALCULS                                                            #
#########################################################################################################################
cas_de_figures = []

with open("golf.csv","r") as f:
    ids = f.readlines()[0]
    liste_id = ids.split(sep=',')[:-1]


    
with open("golf.csv","r") as f:
    for element in f.readlines()[1:]: 
        mot = element.split(sep = ',')
        
        figure = {}
        figure["outlook"]=mot[0]
        figure["temp"]=mot[1]
        figure["humidity"]=mot[2]
        figure["wind"]=mot[3]
        figure["play"]=mot[4][:-1]

        cas_de_figures.append(figure)
        
#Calcul de p et n 
def calcul_p(liste_dico):   
    p = 0 

    for i in range(len(liste_dico)):
        if liste_dico[i]["play"] == "yes" :
            p+=1
            
    return p
            
def calcul_n(liste_dico):   
    n = 0 

    for i in range(len(liste_dico)):
        if liste_dico[i]["play"] == "no" :
            n+=1
    
    return n 
          
p=calcul_p(cas_de_figures) 
n=calcul_n(cas_de_figures)
       
 
#print(cas_de_figures)

def calcul_I(p,n):
    if (p+n) == 0 :
        p_sur_pn = 0
        n_sur_pn = 0
    else : 
        p_sur_pn = p/(p+n)
        n_sur_pn = n/(p+n)
    if n_sur_pn == 0 or p_sur_pn == 0 : 
        return 0 
    return -p_sur_pn*log(p_sur_pn,2)-n_sur_pn*log(n_sur_pn,2)

def calcul_E(condition):
    somme = 0
    liste = []
    for element in cas_de_figures:
        if element[condition] not in liste: 
            liste.append(element[condition])
    #print(liste)
    dictionnaire={}
    for element in liste:    
        dictionnaire[element+"_yes"]=0
        dictionnaire[element+"_no"]=0
    #Création d'une liste avec les play pour chaque cas de figures
    for i in range(len(cas_de_figures)):
        
        yes_no = cas_de_figures[i]["play"]
        var = cas_de_figures[i][condition]
        if yes_no == "yes": 
            dictionnaire[var+"_"+yes_no]+=1
                
        if yes_no == "no": 
            dictionnaire[var+"_"+yes_no]+=1
                
    for categorie in liste: 
        p_i = dictionnaire[categorie+"_yes"]
  
        n_i = dictionnaire[categorie+"_no"]
        somme += ((p_i+n_i)/(p+n))*calcul_I(p_i,n_i)
    
    return somme
      

def calcul_gain(A,p,n):
    return calcul_I(p,n)-calcul_E(A)


#########################################################################################################################
#                                        CHOIX PREMIER NOEUD                                                            #
#########################################################################################################################

#Tests pour vérifier les calculs
print(calcul_I(p,n))
# print(calcul_I(3,2))
print("outlook : "+str(calcul_gain("outlook",p,n)))
print("temperature : " + str(calcul_gain("temp",p,n)))
print("humidity : "+str(calcul_gain("humidity",p,n)))
print("windy : "+str(calcul_gain("wind",p,n)))
print(liste_id)

#Set le meilleur choix de noeud de base
choix = liste_id[0]
val_choix = calcul_gain(choix,p,n)
for element in liste_id[1:]:
    if calcul_gain(element,p,n) > val_choix:
        choix = element 
        val_choix = calcul_gain(element,9,5)
        


#########################################################################################################################
#                                        CREATION ARBRE                                                                 #
#########################################################################################################################

#Construction de l'arbre

class AB_Liste:
    def __init__(self, root):
        self.root = root
        
    def affichage(self):
        print(self.root)


class Node: 
    def __init__(self, value, condition, children=[]):
        self.value = value
        self.condition = condition
        self.children = children
        
    def affichage(self):
        print(self.value)
        

     
liste_attributs = []

for element in cas_de_figures: 
    if element[choix] not in liste_attributs:
        liste_attributs.append(element[choix])

root = Node(choix, liste_attributs)


if choix in liste_id:
    liste_id.remove(choix)
    
def attribut(dictionnaire, condition):
    liste_attributs = []

    for element in dictionnaire: 
        if element[condition] not in liste_attributs:
            liste_attributs.append(element[condition])
    return liste_attributs

print(liste_id)
#Noeud suivant 
def attributs_suivants(dictionnaire, condition): 
    liste_attributs = attribut(dictionnaire, condition)
          
    for eventualite in liste_attributs: 
        liste = []
        for i in range(len(dictionnaire)) :
            
            if dictionnaire[i][condition] == eventualite : 
                liste.append(dictionnaire[i])
                
        liste_gain = []        
        for elt in liste_id: 
            p = calcul_p(liste)
            n = calcul_n(liste)
            gain = calcul_gain(elt,p, n)
            liste_gain.append((elt, gain))
            
        gain_inter = liste_gain[0][1]
        choix_inter = liste_gain[0][0]
        
        for max_gain in liste_gain[1:]: 
            if max_gain[1] > gain_inter :
                gain_inter = max_gain[1]
                choix_inter = max_gain[0]
                
        root = Node(condition, liste_attributs)
                
        if gain_inter > 0 : 
            liste_id.remove(choix_inter)
            root.children.append(Node(eventualite, attribut(dictionnaire, choix_inter)))
        else : 
            root.children.append([])
    return root.children
            
            
              
 
print(attributs_suivants(cas_de_figures, choix))

