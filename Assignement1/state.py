'''
Created on Sep 28, 2012

@author: inekar
'''

import IO

class State:
    """
    Pour certaines méthodes de cette classe, il est nécaissaire d'utiliser
    un système de coordonnées, étant donné que le choix pour state est un
    dictionnaire colonne contenant des dictionnaires lignes, la varibale
    x représente la coordonnée verticale et y la coordonnée horizontale
    """
    def __init__(self, state):
        self.state = state
        
    def move(self, x, y, direction):
        if(self.is_possible(x, y, direction)):
            pass
    
    def is_possible(self, x, y, direction):
        if direction == "north":
            if x == 0:
                """
                Il ne peux pas y avoir de piece au dessus d'une case vide 
                qui est en haut de la grille
                """
                return False
            else:
                if y != 0 and self.state[x-1][y] == self.state[x-1][y-1]:
                    """
                    Cas où c'est une piece de deux (ou quatre) 
                    en (x-1,{y-1, y})
                    """
                    if self.state[x][y-1] == "0":
                        return True
                    else:
                        return False
                elif y != 4 and self.state[x-1][y] == self.state[x-1][y+1]:
                    """
                    Cas où c'est une piece de deux (ou quatre) 
                    en (x-1,{y, y+1})
                    """
                    if self.state[x][y+1] == "0":
                        return True
                    else:
                        return False
                else:
                    """
                    La piece dans ce cas fait seulement 1 de large
                    (1*1) ou (2*1) vertical
                    """
                    return True
                
        elif direction == "east":
            if y == 4:
                return False
            else:
                pass
                    
        elif direction == "south":
            if x == 4:
                return False
            else:
                pass
            
        elif direction == "west":
            if y == 0:
                return False
            else:
                pass
        
        else:
            pass
        pass