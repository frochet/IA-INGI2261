'''
Created on Sep 28, 2012

@author: inekar
'''

import IO

class State:
    """
    Pour certaines m��thodes de cette classe, il est n��caissaire d'utiliser
    un syst��me de coordonn��es, ��tant donn�� que le choix pour state est un
    dictionnaire colonne contenant des dictionnaires lignes, la varibale
    x repr��sente la coordonn��e verticale et y la coordonn��e horizontale
    """
    def __init__(self, state):
        self.state = state
        
    def move(self, x, y, direction):
        i = self.is_possible(x, y, direction)
        if i:
            if direction == "north":
                if i == 10:
                    pass
                elif i == -1:
                    pass
                elif i == 1:
                    pass
            
            if direction == "east":
                if i == 10:
                    pass
                elif i == -1:
                    pass
                elif i == 1:
                    pass
                
            if direction == "south":
                if i == 10:
                    pass
                elif i == -1:
                    pass
                elif i == 1:
                    pass
                
            if direction == "west":
                if i == 10:
                    pass
                elif i == -1:
                    pass
                elif i == 1:
                    pass
            
            else:
                pass
    
    
    
    def is_possible(self, x, y, direction):
        """
        Return False if the move is impossible, then
        -1 means that the >= 2bloc piece is towards the top or left
        +1 means that the >= 2bloc piece is towards the bottom or right
        10 means that it is a 1*1 piece
        """
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
                    Cas ou c'est une piece de deux (ou quatre) 
                    en (x-1,{y-1, y})
                    """
                    if self.state[x][y-1] == "0":
                        return -1
                    else:
                        return False
                elif y != 4 and self.state[x-1][y] == self.state[x-1][y+1]:
                    """
                    Cas ou c'est une piece de deux (ou quatre) 
                    en (x-1,{y, y+1})
                    """
                    if self.state[x][y+1] == "0":
                        return +1
                    else:
                        return False
                else:
                    """
                    La piece dans ce cas fait seulement 1 de large
                    (1*1) ou (2*1) vertical
                    """
                    return 10
                
        elif direction == "east":
            if y == 4:
                return False
            else:
                if x != 0 and self.state[x][y+1] == self.state[x-1][y+1]:
                    """
                    Cas ou c'est une piece de deux (ou quatre) 
                    en ({x-1, x}, y+1)
                    """
                    if self.state[x-1][y] == "0":
                        return -1
                    else:
                        return False
                elif x != 4 and self.state[x][y+1] == self.state[x+1][y+1]:
                    """
                    Cas ou c'est une piece de deux (ou quatre) 
                    en ({x, x+1}, y+1)
                    """
                    if self.state[x+1][y] == "0":
                        return +1
                    else:
                        return False
                else:
                    """
                    La piece dans ce cas fait seulement 1 de large
                    (1*1) ou (2*1) vertical
                    """
                    return 10
                    
        elif direction == "south":
            if x == 4:
                return False
            else:
                if y != 0 and self.state[x+1][y] == self.state[x+1][y-1]:
                    """
                    Cas ou c'est une piece de deux (ou quatre) 
                    en (x+1,{y-1, y})
                    """
                    if self.state[x][y-1] == "0":
                        return -1
                    else:
                        return False
                elif y != 4 and self.state[x+1][y] == self.state[x+1][y+1]:
                    """
                    Cas ou c'est une piece de deux (ou quatre) 
                    en (x-1,{y, y+1})
                    """
                    if self.state[x][y+1] == "0":
                        return +1
                    else:
                        return False
                else:
                    """
                    La piece dans ce cas fait seulement 1 de large
                    (1*1) ou (2*1) vertical
                    """
                    return 10
            
        elif direction == "west":
            if y == 0:
                return False
            else:
                if x != 0 and self.state[x][y-1] == self.state[x-1][y-1]:
                    """
                    Cas ou c'est une piece de deux (ou quatre) 
                    en ({x-1, x}, y+1)
                    """
                    if self.state[x-1][y] == "0":
                        return -1
                    else:
                        return False
                elif x != 4 and self.state[x][y-1] == self.state[x+1][y-1]:
                    """
                    Cas ou c'est une piece de deux (ou quatre) 
                    en ({x, x+1}, y+1)
                    """
                    if self.state[x+1][y] == "0":
                        return 
                    else:
                        return False
                else:
                    """
                    La piece dans ce cas fait seulement 1 de large
                    (1*1) ou (2*1) vertical
                    """
                    return 10
        
        else:
            """
            Mauvaise direction entrée.
            """
            pass


