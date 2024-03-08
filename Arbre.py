from math import log
class AB_Liste:
    def __init__(self, root, children=[]):
        self.root = root
        
    def affichage(self):
        print(self.root)


class Node: 
    def __init__(self, value, condition):
        self.value = value
        self.condition = condition

node1=Node("outlook", ["sunny", "overcast", "rain"])   
node2=Node("temperature", ["cool", "mild", "hot"])
node3=Node("humidity", ["high", "normal"])
node4=Node("windy", ["true", "false"])

arbre=AB_Liste(node1)
print(arbre.affichage)

def calcul_I(p,n):
    return (-p/(p+n))*log(2)*(p/(p+n))-((n/p+n)*log(2)*(n/(p+n)))

def calcul_E(A, p, n):
    somme = 0
    for i in range(1,len(A)+1) :
        somme += (()/(p+n))*calcul_I(p,n)

def calcul_gain(A,p,n):
    return calcul_I(p,n)-calcul_E(A)