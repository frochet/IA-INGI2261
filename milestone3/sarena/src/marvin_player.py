'''
Created on 8 nov. 2012

@author: Florentin
'''
from sarena import *
import minimax
import time
from pattern import *
from random import randint

class Marvin_player(Player,minimax.Game):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.mustDoDic = dict()
        self.suicideDic = dict()
        self.count_played = 0 # In order to know how many time we have played.
        # remplir les dict de pattern TODO
        #self.miniboard = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        self.previousboard = 0
    
    def successors(self, state):
        board, player = state
        
        #Rajouter un boolean pour dire si on fait le subboard ou pas
        #Find the subboard 4*4 in which we're going to play
        miniboardvalues = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        best = [0,0,0]
        #Need to check those -3
        for i in range(board.rows - 3):
            for j in range(board.columns - 3):
                for x in range (i, i+4):
                    for y in range (j, j+4):
                        if board.m[i][j][0] == 3:
                            if board.m[x][y][1][0] == -1:
                                miniboardvalues[i][j] +=1
                            elif board.m[x][y][1][0] == 1:
                                miniboardvalues[i][j] +=1
                        coin = 4
                        while board.m[i][j][coin][1] == 0:
                            coin -= 1
                        if board.m[i][j][coin][1] == 1:
                            miniboardvalues[i][j] +=1
                        if board.m[i][j][coin][1] == -1:
                            miniboardvalues[i][j] +=1
                                   
                miniboardvalues[i][j] += randint(0,1)
                if miniboardvalues[i][j] > best[0]:
                    best[0] == miniboardvalues[i][j]
                    best[1] == i
                    best[2] == j
        
        i = best[1]
        j = best[2]
        bigboardpercept = board.get_percepts()
        newpercept = [0,0,0,0]
        for x in range(4):
            newpercept[x] = bigboardpercept[x+i][j:j+4]
        
        subboard = Board(newpercept)
        for action in subboard.get_actions():
            action[0] += i
            action[1] += j
            action[2] += i
            action[3] += j   
            yield (action,(board.clone().play_action(action), -player))
            
        
            


        # TODO

    def cutoff(self, state, depth):
        board, player = state
        # TODO

    def evaluate(self, state):
        board, player = state
        # TODO

    def play(self, percepts, step, time_left):
        if step % 2 == 0:
            player = -1
        else:
            player = 1
            
        # TODO
        board = Board(percepts)
        state = (board, player)
        action = minimax.search(state, self)
        #we must perform two searches on both subboard and return the best move
        if self.previousboard:
            differenttowers = [0,0]
            i = 0
            while differenttowers[1] == 0 and i <= range(board.rows):
                j = 0
            #for i in range(board.rows):
                while differenttowers[1] == 0 and j <= range(board.columns):
                #for j in range(board.columns):
                    if board.m[i][j] == self.previousboard[i][j]:
                        if differenttowers[0] == 0:
                            differenttowers[0] = [i, j]
                        else:
                            differenttowers[1] = [i, j]
                    j += 1
                i += 1        
            #Need to build the subboard around differenttowers
            bigboardpercept = board.get_percepts()
            counterpercept = 0
            if differenttowers[0][0] == differenttowers[1][0]:
                #The different towers are on the same row
                if differenttowers[0][0] == 0:
                    #The different towers are on the upper row
                    if differenttowers[0][1] == 0:
                        #The left tower is on the left side of the board
                        #We can check only difftower[0]because of the way it is fill earlier
                        counterpercept = [[bigboardpercept[i][j] \
                        for j in range(3)] \
                        for i in range(2)]
                    elif differenttowers[1][1]:
                        #Right tower on the right side
                        #Only need to check difftower[1]
                        counterpercept = [[bigboardpercept[i][j] \
                        for j in range(board.columns-3, board.columns)] \
                        for i in range(2)]
                    else:
                        counterpercept = [[bigboardpercept[i][j] \
                        for j in range(differenttowers[0][1]-1, differenttowers[1][1]+2)] \
                        for i in range(2)]
                elif differenttowers[0][0] == board.rows - 1:     
                    #The different towers are on the lower row
                    if differenttowers[0][1] == 0:
                        #The left tower is on the left side of the board
                        #We can check only difftower[0]because of the way it is fill earlier
                        counterpercept = [[bigboardpercept[i][j] \
                        for j in range(3)] for i in range(board.rows-2, board.rows)]
                    elif differenttowers[1][1]:
                        #Right tower on the right side
                        #Only need to check difftower[1]
                        counterpercept = [[bigboardpercept[i][j] \
                        for j in range(board.columns-3, board.columns)] \
                        for i in range(board.rows-2, board.rows)]
                    else:
                        counterpercept = [[bigboardpercept[i][j] \
                        for j in range(differenttowers[0][1]-1, differenttowers[1][1]+2)] \
                        for i in range(board.rows-2, board.rows)]
                    
                else:
                    #on the middle rows
                    if differenttowers[0][1] == 0:
                        #The left tower is on the left side of the board
                        #We can check only difftower[0]because of the way it is fill earlier
                        counterpercept = [[bigboardpercept[i][j] \
                        for j in range(3)] \
                        for i in range(differenttowers[0][0]-1, differenttowers[0][0]+2)]
                    elif differenttowers[1][1]:
                        #Right tower on the right side
                        #Only need to check difftower[1]
                        counterpercept = [[bigboardpercept[i][j] \
                        for j in range(board.columns-3, board.columns)] \
                        for i in range(differenttowers[0][0]-1, differenttowers[0][0]+2)]
                    else:
                        counterpercept = [[bigboardpercept[i][j] \
                        for j in range(differenttowers[0][1]-1, differenttowers[1][1]+2)] \
                        for i in range(differenttowers[0][0]-1, differenttowers[0][0]+2)]
            else:
                #The different towers are on the same column
                pass
            
        
        
        self.previousboard = board.clone.play_action(action)
        return action 
    
    def _init_pattern(self):
        # Pattern Sandwich 
        self.mustDoDic[Action([3,[Color.RED, -2],[0,0],[0,0],[0,0]],[4,[-2,Color.RED],[0,0],[0,0],[0,0]])] = True
        self.mustDoDic[Action([3,[Color.RED, -2],[0,0],[0,0],[0,0]],[4,[-2,-2],[-2,Color.RED,][0,0],[0,0]])] = True
        self.mustDoDic[Action([3,[Color.RED, -2],[0,0],[0,0],[0,0]],[4,[-2,-2],[-2,-2],[-2,Color.RED],[0,0]])] = True
        self.mustDoDic[Action([3,[Color.RED, -2],[-2,-2],[0,0],[0,0]],[4,[-2,Color.RED],[0,0],[0,0],[0,0]])] = True
        self.mustDoDic[Action([3,[Color.RED, -2],[-2,-2],[-2,-2],[0,0]],[4,[-2,Color.RED],[0,0],[0,0],[0,0]])] = True
        self.mustDoDic[Action([3,[Color.RED, -2],[-2,-2],[0,0],[0,0]],[4,[-2,-2],[-2,Color.RED],[0,0],[0,0]])] = True
        
        self.suicideDic[Action([3,[Color.YELLOW, -2],[0,0],[0,0],[0,0]],[4,[-2,Color.YELLOW],[0,0],[0,0],[0,0]])] = True
        self.suicideDic[Action([3,[Color.YELLOW, -2],[0,0],[0,0],[0,0]],[4,[-2,-2],[-2,Color.YELLOW,][0,0],[0,0]])] = True
        self.suicideDic[Action([3,[Color.YELLOW, -2],[0,0],[0,0],[0,0]],[4,[-2,-2],[-2,-2],[-2,Color.YELLOW],[0,0]])] = True
        self.suicideDic[Action([3,[Color.YELLOW, -2],[-2,-2],[0,0],[0,0]],[4,[-2,Color.YELLOW],[0,0],[0,0],[0,0]])] = True
        self.suicideDic[Action([3,[Color.YELLOW, -2],[-2,-2],[-2,-2],[0,0]],[4,[-2,Color.YELLOW],[0,0],[0,0],[0,0]])] = True
        self.suicideDic[Action([3,[Color.YELLOW, -2],[-2,-2],[0,0],[0,0]],[4,[-2,-2],[-2,Color.RED],[0,0],[0,0]])] = True
        # end of pattern sandwich
        # pattern deplacement obligatoire.
        
        #pattern make a 4-stack with a Yellow color on top, on an arrow case
        
        self.mustDoDic[Action([3,[-2,Color.YELLOW],[0,0],[0,0],[0,0]],[4,[-2,-2],[-2,-2],[-2,-2],[0,0]])] = True
        self.mustDoDic[Action([3,[-2,-2],[-2,Color.YELLOW],[0,0],[0,0]],[4,[-2,-2],[-2,-2],[0,0],[0,0]])] = True
        self.mustDoDic[Action([3,[-2,-2],[-2,-2],[-2,Color.YELLOW],[0,0]],[4,[-2,-2],[0,0],[0,0],[0,0]])] = True
        
        self.suicideDic[Action([3,[-2,Color.RED],[0,0],[0,0],[0,0]],[4,[-2,-2],[-2,-2],[-2,-2],[0,0]])] = True
        self.suicideDic[Action([3,[-2,-2],[-2,Color.RED],[0,0],[0,0]],[4,[-2,-2],[-2,-2],[0,0],[0,0]])] = True
        self.suicideDic[Action([3,[-2,-2],[-2,-2],[-2,Color.RED],[0,0]],[4,[-2,-2],[0,0],[0,0],[0,0]])] = True
    
        #pattern make a 4-stack with yellow color on bottom, on a blank case
        self.mustDoDic[Action([4,[-2,-2],[0,0],[0,0],[0,0]],[3,[Color.YELLOW,-2],[-2,-2],[-2,-2],[0,0]])] = True
        self.mustDoDic[Action([4,[-2,-2],[-2,-2],[0,0],[0,0]],[3,[Color.YELLOW,-2],[-2,-2][0,0][0,0]])] = True
        self.mustDoDic[Action([4,[-2,-2],[-2,-2],[-2,-2],[0,0]],[3,[Color.YELLOW,-2],[0,0][0,0][0,0]])] = True
        
        self.suicideDic[Action([4,[-2,-2],[0,0],[0,0],[0,0]],[3,[Color.RED,-2],[-2,-2],[-2,-2],[0,0]])] = True
        self.suicideDic[Action([4,[-2,-2],[-2,-2],[0,0],[0,0]],[3,[Color.RED,-2],[-2,-2][0,0][0,0]])] = True
        self.suicideDic[Action([4,[-2,-2],[-2,-2],[-2,-2],[0,0]],[3,[Color.RED,-2],[0,0][0,0][0,0]])] = True
        
        # broke an enemy tower. will be reversed after.
        self.mustDoDic[Action([4,[-2,Color.RED],[0,0],[0,0],[0,0]],[3,[2,-2],[-2,-2],[-2,-2],[0,0]])] = True
        self.mustDoDic[Action([4,[-2,-2],[-2,Color.RED],[0,0],[0,0]],[3,[2,-2],[-2,-2],[0,0],[0,0]])] = True
        self.mustDoDic[Action([4,[-2,-2],[-2,-2],[-2,Color.RED],[0,0]],[3,[2,-2],[0,0],[0,0],[0,0]])] = True
       
        # broke one of our tower.
        self.suicideDic[Action([4,[-2,Color.YELLOW],[0,0],[0,0],[0,0]],[3,[2,-2],[-2,-2],[-2,-2],[0,0]])] = True
        self.suicideDic[Action([4,[-2,-2],[-2,Color.YELLOW],[0,0],[0,0]],[3,[2,-2],[-2,-2],[0,0],[0,0]])] = True
        self.suicideDic[Action([4,[-2,-2],[-2,-2],[-2,Color.YELLOW],[0,0]],[3,[2,-2],[0,0],[0,0],[0,0]])] = True
