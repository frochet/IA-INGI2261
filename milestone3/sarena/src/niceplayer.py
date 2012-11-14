#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sarena import *
import minimax


YELLOW = 1
RED = -1
GRIS = 2
NON_ARROW = 3
ARROW = 4


        

class AlphaBetaPlayer(Player, minimax.Game):

    """Sarena Player.
    
    A state is a tuple (b, p) where p is the player to make a move and b
    the board.
    
    """

    #--------------------------------------------------------------
    #Monitoring
    def __init__(self):
        self.count=0
        self.lscount=[]

    
    def getcount(self):
        return self.count
    
    def getlscount(self):
        return self.lscount
    #--------------------------------------------------------------

        
    def successors(self, state):
        
        board, player = state       
        for action in board.get_actions():
            yield (action,(Board(board.get_percepts()).play_action(action),-player))

    
    def cutoff(self, state, depth):
        return depth == 1


    def nbChips(self,playNumber,tower):
        """ Return the number of chips of the player 'playNumber" for the tower located at (i,j)"""
        count = 0
        if (tower[1][0] == playNumber or tower[1][1] == playNumber):
            count = count + 1
        if (tower[2][0] == playNumber or tower[2][1] == playNumber):
            count = count + 1       
        if (tower[3][0] == playNumber or tower[3][1] == playNumber):
            count = count + 1   
        if (tower[4][0] == playNumber or tower[4][1] == playNumber):
            count = count + 1   
        return count    

        
    def isSafeForArrow(self,lenTower,board,i,j):
        """ Decide if a place is safe for a tower of lenTower and located in a Arrow place"""


        if(i != 0 and j != 0 and i != board.rows - 1 and j != board.columns -1):
           tower1 = board.m[i-1][j]
           tower2 = board.m[i][j-1]
           tower3 = board.m[i+1][j]
           tower4 = board.m[i][j+1]

        if (i == 0):
            tower1 = []
            tower3 = board.m[i+1][j]
            if (j == 0): # Coin haut gauche
                tower2 = []
                tower4 = board.m[i][j+1]
            elif (j == board.columns-1): # Coin haut droit
                tower2 = board.m[i][j-1]
                tower4 = []
            else:
                tower2 = board.m[i][j-1]
                tower4 = board.m[i][j+1]

        elif (i == board.rows - 1):
            tower1 = board.m[i-1][j]
            tower3 = []  
            if (j == 0): 
                tower2 = []
                tower4 = board.m[i][j+1]
            elif (j == board.columns-1): 
                tower2 = board.m[i][j-1]
                tower4 = []
            else:
                tower2 = board.m[i][j-1]
                tower4 = board.m[i][j+1]


        if (j == 0): 
            tower2 = []
            tower4 = board.m[i][j+1]
            if (i == 0): 
                tower1 = []
                tower3 = board.m[i+1][j]
            elif (i == board.rows-1): 
                tower1 = board.m[i-1][j]
                tower3 = []
            else:
                tower1 = board.m[i-1][j]
                tower3 = board.m[i+1][j]

        elif (j == board.columns - 1):
            tower2 = board.m[i][j-1]
            tower4 = []
            if (i == 0): 
                tower1 = []
                tower3 = board.m[i+1][j]
            elif (i == board.rows-1): 
                tower1 = board.m[i-1][j] 
                tower3 = []      
            else:
                tower1 = board.m[i-1][j]
                tower3 = board.m[i+1][j] 
                
        verif = 4-lenTower          
        for k in range(verif):
            if(tower4 != []):
                if(tower4[1+k][0] != 0):
                    return False
            if(tower2 != []):
                if(tower2[1+k][0] != 0):
                   return False
            if(tower3 != []):
                if(tower3[1+k][0] != 0):
                    return False
            if(tower1 != []):
                if(tower1[1+k][0] != 0):
                    return False
        return True


    def isSafeForNonArrow(self,lenTower,board,i,j):

        if(i != 0 and j != 0 and i != board.rows - 1 and j != board.columns -1):
           tower1 = board.m[i-1][j]
           tower2 = board.m[i][j-1]
           tower3 = board.m[i+1][j]
           tower4 = board.m[i][j+1]

        if (i == 0):
            tower1 = []
            tower3 = board.m[i+1][j]
            if (j == 0): # Coin haut gauche
                tower2 = []
                tower4 = board.m[i][j+1]
            elif (j == board.columns-1): # Coin haut droit
                tower2 = board.m[i][j-1]
                tower4 = []
            else:
                tower2 = board.m[i][j-1]
                tower4 = board.m[i][j+1]

        elif (i == board.rows - 1):
            tower1 = board.m[i-1][j]
            tower3 = []  
            if (j == 0): 
                tower2 = []
                tower4 = board.m[i][j+1]
            elif (j == board.columns-1): 
                tower2 = board.m[i][j-1]
                tower4 = []
            else:
                tower2 = board.m[i][j-1]
                tower4 = board.m[i][j+1]


        if (j == 0): 
            tower2 = []
            tower4 = board.m[i][j+1]
            if (i == 0): 
                tower1 = []
                tower3 = board.m[i+1][j]
            elif (i == board.rows-1): 
                tower1 = board.m[i-1][j]
                tower3 = []
            else:
                tower1 = board.m[i-1][j]
                tower3 = board.m[i+1][j]

        elif (j == board.columns - 1):
            tower2 = board.m[i][j-1]
            tower4 = []
            if (i == 0): 
                tower1 = []
                tower3 = board.m[i+1][j]
            elif (i == board.rows-1): 
                tower1 = board.m[i-1][j] 
                tower3 = []      
            else:
                tower1 = board.m[i-1][j]
                tower3 = board.m[i+1][j] 
                
        verif = 4-lenTower         
        for k in range(verif):
            if(tower4 != []):
                if(tower4[1+k][0] != 0 or tower4[1][0] == 0):
                    return False
            if(tower2 != []):
                if(tower2[1+k][0] != 0 or tower2[1][0] == 0):
                   return False
            if(tower3 != []):
                if(tower3[1+k][0] != 0 or tower3[1][0] == 0):
                    return False
            if(tower1 != []):
                if(tower1[1+k][0] != 0 or tower1[1][0] == 0):
                    return False
        return True

    def isFreePlace(self,board,i,j):
        """ Decide if the place (i j) is free"""
        tower = board.m[i][j]
        if(tower[1][0] == 0):
            return True
        return False


    def sizeTower(self,tower):
        size = 0
        for i in tower[1:]:
            if i[0] != 0:
                size = size + 1
            else:
                break;
        return size

    def isAdvColor(self,advColor,lenTower,board,i,j):
        """ Return true if there is an adv color on the top on a tower stackable next the place i,j"""
        if(i != 0 and j != 0 and i != board.rows - 1 and j != board.columns -1):
            tower1 = board.m[i-1][j]
            tower2 = board.m[i][j-1]
            tower3 = board.m[i+1][j]
            tower4 = board.m[i][j+1]

        if (i == 0):
            tower1 = []
            tower3 = board.m[i+1][j]
            if (j == 0): # Coin haut gauche
                tower2 = []
                tower4 = board.m[i][j+1]
            elif (j == board.columns-1): # Coin haut droit
                tower2 = board.m[i][j-1]
                tower4 = []
            else:
                tower2 = board.m[i][j-1]
                tower4 = board.m[i][j+1]

        elif (i == board.rows - 1):
            tower1 = board.m[i-1][j]
            tower3 = []  
            if (j == 0): 
                tower2 = []
                tower4 = board.m[i][j+1]
            elif (j == board.columns-1): 
                tower2 = board.m[i][j-1]
                tower4 = []
            else:
                tower2 = board.m[i][j-1]
                tower4 = board.m[i][j+1]


        if (j == 0): 
            tower2 = []
            tower4 = board.m[i][j+1]
            if (i == 0): 
                tower1 = []
                tower3 = board.m[i+1][j]
            elif (i == board.rows-1): 
                tower1 = board.m[i-1][j]
                tower3 = []
            else:
                tower1 = board.m[i-1][j]
                tower3 = board.m[i+1][j]

        elif (j == board.columns - 1):
            tower2 = board.m[i][j-1]
            tower4 = []
            if (i == 0): 
                tower1 = []
                tower3 = board.m[i+1][j]
            elif (i == board.rows-1): 
                tower1 = board.m[i-1][j] 
                tower3 = []      
            else:
                tower1 = board.m[i-1][j]
                tower3 = board.m[i+1][j] 
                              
        for k in range(lenTower):
            if(tower4 != []):
                if(tower4[1+k][1] == advColor):
                    return True
            if(tower2 != []):
                if(tower2[1+k][1] == advColor):
                   return True
            if(tower3 != []):
                if(tower3[1+k][1] == advColor):
                    return True
            if(tower1 != []):
                if(tower1[1+k][1] == advColor):
                    return True
        return False

    def nbFreePlace2(self,board,i,j):
        """ Return the number of free Place next to the place (i,j)"""
        count = 0
        if(i != 0 and j != 0 and i != board.rows - 1 and j != board.columns -1):
            if(self.isFreePlace(board,i,j+1)):
                count += count
            if(self.isFreePlace(board,i,j-1)):
                count += count
            if(self.isFreePlace(board,i+1,j)):
                count += count
            if(self.isFreePlace(board,i-1,j)):
               count += count
        return count
    

    def evaluate(self, state):
        board, player = state 
        result = 0 
        for i in range(board.rows):
            for j in range(board.columns):  
                tower = board.m[i][j]
                print(tower)
                nbChipsPlayer1 = self.nbChips(1,tower)  
                nbChipsPlayer2 = self.nbChips(-1,tower)  
                nbFreePlace = self.nbFreePlace2(board,i,j) # Nb de places libres à côté de l'emplacement (i,j)    
# ------------------------------------- TOUR DE HAUTEUR4 ------------------------------------#
                if(self.sizeTower(tower) == 4): # Regarde la hauteur de la tour   
                    print("tour de hauteur 4 en analyse")
                    if(tower[0] == NON_ARROW): # Regarde le type de la case (Fleche ou non) (3 sans fleche, 4 avec fleche)
                        # Coup favorable : Rapporte des points
                        if(tower[1][0] == 1): #Regarde la couleur tout en dessous de la pile
                            result = result + 90 + (2*nbFreePlace + nbChipsPlayer2 - nbChipsPlayer1)
                        # Coup défavorable :  Rapporte des points à l'adversaire
                        elif(tower[1][0] == -1):
                            result = result - (90 + (2*nbFreePlace + nbChipsPlayer1 - nbChipsPlayer2))
                        # Coup favorable : fait perdre des points à l'adversaire
                        elif(tower[-1][1] == -1):
                            result = result + 90 + (2*nbFreePlace + nbChipsPlayer2 - nbChipsPlayer1)
                        # Coup défavorable : Nous fait perdre des points
                        elif(tower[-1][1] == 1):
                            result = result - (90 + (2*nbFreePlace + nbChipsPlayer1 - nbChipsPlayer2))
                        #Coup favorable : Fait perdre des points à l'adversaire
                        elif(tower[-1][1] == 2 and tower[3][1] == -1 and tower[1][0] != -1):
                            result = result + 85 + (nbChipsPlayer2 - nbChipsPlayer1)
                        #Coup défavorable : Nous fait perdre des points
                        elif(tower[-1][1] == 2 and tower[3][1] == 1 and tower[1][0] != 1):
                            result = result - (85 + (nbChipsPlayer1 - nbChipsPlayer2))                                 
                    elif(tower[0] == ARROW):
                        # Coup favorable : Rapporte des points
                        if(tower[-1][1] == 1): # Regarde la couleur tout au dessus de la pile
                            result = result + 100 + (nbChipsPlayer2 - nbChipsPlayer1)
                        # Coup défavorable :  Rapporte des points à l'adversaire
                        elif(tower[-1][1] == -1):
                            result = result - (100 + (nbChipsPlayer1 - nbChipsPlayer2))
                        # Coup favorable : fait perdre des points à l'adversaire
                        elif(tower[-1][1] == 2 and tower[3][1] == -1):
                            result = result + 95 + (nbChipsPlayer2 - nbChipsPlayer1)
                        # Coup défavorable : Nous fait perdre des points
                        elif(tower[-1][1] == 2 and tower[2][1] == 1):
                            result = result - (95 + (nbChipsPlayer1 - nbChipsPlayer2))                    
                            
                            # PREVOIR FORMATION A PARTIR D'UNE TOUR DE 2  OU DE 3
# ------------------------------------- TOUR DE HAUTEUR 3------------------------------------#
                elif(self.sizeTower(tower) == 3):
                    print("tour de hauteur 3 en analyse")
                    if(tower[0] == NON_ARROW): 
                        # Coup favorable : Rapporte des points
                        if(tower[1][0] == 1 and self.isSafeForNonArrow(3,board,i,j)):
                            result = result + 70 + (2*nbFreePlace + nbChipsPlayer2 - nbChipsPlayer1)
                        # Coup défavorable :  Rapporte des points à l'adversaire
                        elif(tower[1][0] == -1 and self.isSafeForNonArrow(3,board,i,j)):
                            result = result - (70 + (2*nbFreePlace + nbChipsPlayer1 - nbChipsPlayer2))
                        #Coup favorable : Fait perdre des points à l'adversaire
                        elif(tower[3][1] == 2 and tower[2][1] == -1 and tower[1][0] != -1 and not self.isAdvColor(-1,3,board,i,j)):
                            result = result + 65 + (nbChipsPlayer2 - nbChipsPlayer1)
                        #Coup défavorable : Nous fait perdre des points
                        elif(tower[3][1] == 2 and tower[2][1] == 1 and tower[1][0] != 1 and not self.isAdvColor(1,3,board,i,j)):
                            result = result - (65 + (nbChipsPlayer1 - nbChipsPlayer2))           
                    elif(tower[0] == ARROW):
                        if(tower[3][1] == 1 and self.isSafeForArrow(3,board,i,j)):
                        # Coup favorable : Rapporte des points
                            result = result + 80 + (nbChipsPlayer2 - nbChipsPlayer1)
                        elif(tower[3][1] == -1 and self.isSafeForArrow(3,board,i,j)):
                        # Coup défavorable :  Rapporte des points à l'adversaire
                            result = result - (80 + (nbChipsPlayer1 - nbChipsPlayer2))
                        # Coup favorable : fait perdre des points à l'adversaire
                        if(tower[3][1] == 2 and tower[2][1] == -1 and not self.isAdvColor(-1,3,board,i,j)):
                            result = result + 75 + (nbChipsPlayer2 - nbChipsPlayer1)
                        # Coup défavorable : Nous fait perdre des points
                        elif(tower[3][1] == 2 and tower[2][1] == 1 and not self.isAdvColor(1,3,board,i,j)):
                            result = result - (75 + (nbChipsPlayer1 - nbChipsPlayer2))
# ------------------------------------- TOUR DE HAUTEUR 2------------------------------------#                    
                elif(self.sizeTower(tower) == 2):
                    print("tour de hauteur 2 en analyse")
 

# PROBLEME ISSAFEFORARROW POSSIBLE
                    if(tower[0] == NON_ARROW):
						#Coup favorable : Fait gagner des points.
                        if(tower[1][0] == 1  and self.isSafeForNonArrow(2,board,i,j)):
                            result = result + 50 + (2*nbFreePlace + nbChipsPlayer2 - nbChipsPlayer1)
                        #Coup défavorable : Fait gagner des points à mon adversaire.
                        elif(tower[1][0] == -1 and self.isSafeForNonArrow(2,board,i,j)):
                            result = result - (50 + (2*nbFreePlace + nbChipsPlayer1 - nbChipsPlayer2))
                        #Coup favorable : Fait perdre des points à l'adversaire
                        elif(tower[2][1] == 2 and tower[1][1] == -1 and tower[1][0] != -1 and not self.isAdvColor(-1,2,board,i,j)):
                            result = result + 45 + (nbChipsPlayer2 - nbChipsPlayer1)
                        #Coup défavorable : Nous fait perdre des points
                        elif(tower[2][1] == 2 and tower[1][1] == 1 and tower[1][0] != 1 and not self.isAdvColor(1,2,board,i,j)):
                            result = result - (45 + (nbChipsPlayer1 - nbChipsPlayer2))                     							
                    elif(tower[0] == ARROW):
                        if(tower[2][1] == 1 and self.isSafeForArrow(2,board,i,j)):
                            result = result + 60 + (nbChipsPlayer2 - nbChipsPlayer1)
                        elif(tower[2][1] == -1 and self.isSafeForArrow(2,board,i,j)):
                            result = result - (60 + (nbChipsPlayer1 - nbChipsPlayer2)) 
                        # Coup favorable : fait perdre des points à l'adversaire
                        elif(tower[2][1] == 2 and tower[1][1] == -1 and not self.isAdvColor(-1,2,board,i,j)):
                            result = result + 55 + (nbChipsPlayer2 - nbChipsPlayer1)
                        # Coup défavorable : Nous fait perdre des points
                        elif(tower[2][1] == 2 and tower[1][1] == 1 and not self.isAdvColor(1,2,board,i,j)):
                            result = result - (55 + (nbChipsPlayer1 - nbChipsPlayer2)) 

        
# ------------------------------------- TOUR DE HAUTEUR 1------------------------------------#
                #~ elif(self.sizeTower(tower) == 1):
                    #~ print("tour de hauteur 1 en analyse")
                    #~ if(tower[0] == NON_ARROW and self.isSafeForNonArrow(1,board,i,j)):
                        #~ if(tower[1][0] == 1):
                            #~ result = result + 30 + (2*nbFreePlace + nbChipsPlayer2 - nbChipsPlayer1)
                        #~ elif(tower[1][0] == -1):
                            #~ result = result - (30 + (2*nbFreePlace + nbChipsPlayer1 - nbChipsPlayer2))
                    #~ elif(tower[0] == ARROW and self.isSafeForArrow(1,board,i,j)):
                        #~ if(tower[1][1] == 1):
                            #~ result = result + 40 + (nbChipsPlayer2 - nbChipsPlayer1)
                        #~ elif(tower[1][1] == -1):
                            #~ result = result - (40 + (nbChipsPlayer1 - nbChipsPlayer2))       
# -------------------------------------------------------------------------------------------#
                elif(self.sizeTower(tower) == 0):
                    pass
        return result

 
    
    def play(self, percepts, step, time_left):
        if step % 2 == 0:
            player = -1
        else:
            player = 1
            
        state = (Board(percepts), player)  
        return minimax.search(state, self,True)

if __name__ == "__main__":
    player_main(AlphaBetaPlayer())
