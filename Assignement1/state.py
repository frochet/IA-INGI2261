'''
Created on Sep 28, 2012

@author: inekar
'''

import IO
import WrongDirectionException

class State:
    """
    Pour certaines m��thodes de cette classe, il est n��caissaire d'utiliser
    un syst��me de coordonn��es, ��tant donn�� que le choix pour state est un
    dictionnaire colonne contenant des dictionnaires lignes, la varibale
    x repr��sente la coordonn��e verticale et y la coordonn��e horizontale
    """
    def __init__(self, state):
        self.state = state
        
    def get_state(self):
        return self.state
        
    def move_vertical(self, x, y, direction, i):
        if direction == "north":
            dirmul = -1
            isInBound = x > 1
        elif direction == "south":
            dirmul = 1
            isInBound = x < 3

        if i == 10:
            if isInBound and self.state[x+dirmul][y] == self.state[x+2*dirmul][y]:
                """Test if the piece is a vertical 2bloc piece"""
                diff = 2
            else:
                """Il s'agit d'une piece 1*1"""
                diff = 1
            self.state[x][y], self.state[x+dirmul*diff][y] = \
            self.state[x+dirmul*diff][y], self.state[x][y]
        else:            
            if i == -1:
                mul = -1
            elif i == 1:
                mul = 1
            if isInBound and self.state[x+dirmul][y] == self.state[x+2*dirmul][y] \
            and self.state[x+dirmul][y] == self.state[x+2*dirmul][y+mul]:
                """Case in which it is the square 2*2"""
                diff = 2
            else:
                """Case in which it is an horizontal 2*1"""
                diff = 1
            self.state[x][y], self.state[x+dirmul*diff][y] = \
            self.state[x+dirmul*diff][y], self.state[x][y]
            self.state[x][y+mul], self.state[x+dirmul*diff][y+mul] = \
            self.state[x+dirmul*diff][y+mul], self.state[x][y+mul]
            
            
    def move_horizontal(self, x, y, direction, i):
        if direction == "east":
            dirmul = -1
            isInBound = y > 1
        elif direction == "west":
            dirmul = 1
            isInBound = y < 2

        if i == 10:
            if isInBound and self.state[x][y+dirmul] == self.state[x][y+2*dirmul]:
                """Test if the piece is a vertical 2bloc piece"""
                diff = 2
            else:
                """Il s'agit d'une piece 1*1"""
                diff = 1
            self.state[x][y], self.state[x][y+dirmul*diff] = \
            self.state[x][y+dirmul*diff], self.state[x][y]
        else:            
            if i == -1:
                mul = -1
            elif i == 1:
                mul = 1
            if isInBound and self.state[x][y+dirmul] == self.state[x][y+2*dirmul] \
            and self.state[x][y+dirmul] == self.state[x+mul][y+2*dirmul]:
                """Case in which it is the square 2*2"""
                diff = 2
            else:
                """Case in which it is an horizontal 2*1"""
                diff = 1
            self.state[x][y], self.state[x][y+dirmul*diff] = \
            self.state[x][y+dirmul*diff], self.state[x][y]
            self.state[x+mul][y], self.state[x+mul][y+dirmul*diff] = \
            self.state[x+mul][y+dirmul*diff], self.state[x+mul][y]
            
            

    def move(self, x, y, direction):    
        """Return a new  state which represent the move. if the
        move is impossible, move return false"""    
        i = self.is_possible(x, y, direction)
        if i:
            if direction == "north" or direction == "south":
                self.move_vertical(x, y, direction, i)
            if direction == "east" or direction == "west":
                self.move_horizontal(x, y, direction, i)
            else:
                pass
    
    
    def is_possible(self, x, y, direction):
        """Return False if the move is impossible, then
        -1 means that the >= 2bloc piece is towards the top or left
        +1 means that the >= 2bloc piece is towards the bottom or right
        10 means that it is a piece with width = 1 in the direction
        Remind : x is vertical coordonate, y is horizontal"""
        if direction == "north":
            if x == 0:
                """Il ne peux pas y avoir de piece au dessus d'une case vide 
                qui est en haut de la grille"""
                return False
            else:
                if y != 0 and self.state[x-1][y] == self.state[x-1][y-1]:
                    """Cas ou c'est une piece de deux (ou quatre) 
                    en (x-1,{y-1, y})"""
                    if self.state[x][y-1] == "0":
                        return -1
                    else:
                        return False
                elif y != 3 and self.state[x-1][y] == self.state[x-1][y+1]:
                    """Cas ou c'est une piece de deux (ou quatre) 
                    en (x-1,{y, y+1})"""
                    if self.state[x][y+1] == "0":
                        return +1
                    else:
                        return False
                else:
                    """La piece dans ce cas fait seulement 1 de large
                    (1*1) ou (2*1) vertical"""
                    return 10
         
         
        elif direction == "south":
            if x == 4:
                return False
            else:
                if y != 0 and self.state[x+1][y] == self.state[x+1][y-1]:
                    """Cas ou c'est une piece de deux (ou quatre) 
                    en (x+1,{y-1, y})"""
                    if self.state[x][y-1] == "0":
                        return -1
                    else:
                        return False
                elif y != 3 and self.state[x+1][y] == self.state[x+1][y+1]:
                    """Cas ou c'est une piece de deux (ou quatre) 
                    en (x-1,{y, y+1})"""
                    if self.state[x][y+1] == "0":
                        return +1
                    else:
                        return False
                else:
                    """La piece dans ce cas fait seulement 1 de large
                    (1*1) ou (2*1) vertical"""
                    return 10
                
                        
        elif direction == "east":
            if y == 3:
                return False
            else:
                if x != 0 and self.state[x][y+1] == self.state[x-1][y+1]:
                    """Cas ou c'est une piece de deux (ou quatre) 
                    en ({x-1, x}, y+1)"""
                    if self.state[x-1][y] == "0":
                        return -1
                    else:
                        return False
                elif x != 4 and self.state[x][y+1] == self.state[x+1][y+1]:
                    """Cas ou c'est une piece de deux (ou quatre) 
                    en ({x, x+1}, y+1)"""
                    if self.state[x+1][y] == "0":
                        return +1
                    else:
                        return False
                else:
                    """La piece dans ce cas fait seulement 1 de large
                    (1*1) ou (2*1) vertical"""
                    return 10
                    
            
        elif direction == "west":
            if y == 0:
                return False
            else:
                if x != 0 and self.state[x][y-1] == self.state[x-1][y-1]:
                    """Cas ou c'est une piece de deux (ou quatre) 
                    en ({x-1, x}, y+1)"""
                    if self.state[x-1][y] == "0":
                        return -1
                    else:
                        return False
                elif x != 4 and self.state[x][y-1] == self.state[x+1][y-1]:
                    """Cas ou c'est une piece de deux (ou quatre) 
                    en ({x, x+1}, y+1)"""
                    if self.state[x+1][y] == "0":
                        return 
                    else:
                        return False
                else:
                    """La piece dans ce cas fait seulement 1 de large
                    (1*1) ou (2*1) vertical"""
                    return 10
        
        else:
            """Mauvaise direction entrée."""
            raise WrongDirectionException(x,y,direction)
    
    #
    # GETTERS AND SETTERS
    #
    
    def _get_state(self):
        return self._state
    
    def _set_state(self,state):
        self._state = state
        

    state = property(_get_state,_set_state)
    
