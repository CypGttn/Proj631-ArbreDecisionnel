# -*- coding: utf-8 -*-
"""
RTree module to build and manage rooted tree
"""

class Node :
    """
    A node is defind by a value and a list of child
    """
    def __init__(self, value,children):
        """
        """
        self.value = value
        self.children = children
        
    def get_values(self):
        """Return the value of the node
        """
        return self.value
    
    def get_children(self):
        """Return children of the node
        """
        return self.children
    
    def is_leaf(self):
        """Return true if the node is a leaf
        """
        return self.get_children() == []
    
    def get_descending(self, liste):
        """
        create a list with all the descendants
        """
        children_list = self.get_children()
        liste = liste + children_list
        
        for elt in children_list:
            elt.get_descending(liste)
            
        print(liste)
            
    

        
        
        
        
    
class Rtree(Node):
    """
    A rooted tree is represented by
    A set of vertices
    A set of edges
    """
    def __init__(self, root = None):
        self.root = root
    
    def get_root(self):
        """
        Return the root of rooted tree
        root : Rtree → Node
        """
        return self.root 

    def sub_tree(self):
        """
        Return a list of all subtrees of the root
        """
        #Get all the children of the tree
        root_children  = self.get_root().get_children()
        sub= []
        for k in root_children :
            sub.append(Rtree(k))
        return sub
    
    def display_depth(self):
        """
        Return the label by a display by depth
        """
        if self.get_root().is_leaf() :
            print(self.get_root().get_values())
        else :
            print(self.get_root().get_values())
            subtree_list = self.sub_tree()
            for i in subtree_list :
                i.display_depth()
                
    def display_width1(self):
        """
        Return the label by a display by depth
        """
        
        if not self.get_root().is_leaf() :
            
            child_list = self.get_root().get_children()
            for f in child_list:
                print(f.get_values())
            
            subtree_list = self.sub_tree()
            for i in subtree_list :
                i.display_width1()
                
    def display_width(self):
        """
        Display the tree by width
        """
        print(self.get_root().get_values())
        self.display_width1()
        
    def get_father(self, bebe):
        """
        Return the father of a node in parameter
        """
        if not self.get_root().is_leaf():
            children_list= self.get_root().get_children()
            if bebe in children_list:
                print(self.get_root().get_values())
            else:
                subtree = self.sub_tree()
                for sub in subtree:
                    sub.get_father(bebe)
    