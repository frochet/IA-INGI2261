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
        self._init_pattern()
        #self.miniboard = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        self.previousboard = 0
        self.previousSearchedBoard = None
        self.previousDepth = 0
    
    def successors(self, state,depth):
        board, player = state
        self.previousSearchedBoard = board.clone()
        self.previousDepth = depth
        for action in board.get_actions():
            yield (action,(board.clone().play_action(action), -player)) 

    def cutoff(self, state, depth):
        board, player = state
        # TODO
        
        # Must cut if we played a suicide move to reach this state.
        # Must cut with iterative depth
        if abs(self.previousDepth-depth) > 1 : self.previousSearchedBoard = None # for the moment
        
        if not self.previousSearchedBoard == None :
            action_played = board.action_played(self.previousSearchedBoard)
            move = Action(action_played[1][0],action_played[1][1])
            if move.is_a_pattern(self.suicideDic) and depth % 2 == 0:
                return True # if a node-max is a suicide, cut it, we do not play the move
            elif move.is_a_pattern(self.mustDoDic) and depth % 2 == 1 :
                return True # if a node-min is a suicide for the opponent, cut it, he will not play that move

        return depth == 5

    def evaluate(self, state):
        board, player = state
        #regarder les points en cours sur le board (jeton isoles + tour a retourner + pattern must_do, suicide) + la difference entre le nombre de jeton
        # down de nos tours avec ceux de l'ennemi.
        #return board.get_score()
        #print("test")
        score = 0
        yellowCoins = 0
        redCoins = 0
        for i,j,tower in board.get_towers() :
            towerHeight = board.get_height(tower) # in number of coins
            if towerHeight > 0 :
                isIsolated = True
                for action in board.get_tower_actions(i,j):
                    # Verify if a pattern exist and compute points.
                    isIsolated = False
                    k,l,m,n = action
                    t_init = list()
                    t_target = list()
                    t_init+=board.m[k][l]
                    t_target+=board.m[m][n]
                    move = Action(t_init,t_target)
                    if player == 1 : # si c'est a nous de jouer ?
                        if move.is_a_pattern(self.mustDoDic) :
                            score+=move.weight
                    else:
                        if move.is_a_pattern(self.suicideDic):
                            score+=move.weight    
                #compute points on the current towers    
                if tower[0] == 3 :
                    # look for a isolated tower :
                    isIsolated = False
                    newScore = self._see_if_isolate(i,j,board,score,tower)
                    if newScore != score : 
                        isIsolated = True
                        score = newScore
                     
                    if not isIsolated:
                        if tower[1][0] == Color.YELLOW :
                            yellowCoins += 1
                        elif tower[1][0] == Color.RED :
                            redCoins += 1
                elif tower[0] == 4 :
                    if isIsolated :
                        if tower[towerHeight][1] == Color.YELLOW :
                            score += towerHeight
                        elif tower[towerHeight][1] == Color.RED :
                            score -= towerHeight
                    else :
                        if tower[4][1] == Color.YELLOW :
                            score += 4 # 1 for 1 coin win
                        elif tower[4][1] == Color.RED :
                            score -= 4
                        if tower[towerHeight][1] == Color.YELLOW :
                            yellowCoins+=1
                        elif tower[towerHeight][1] == Color.RED :
                            redCoins +=1
        score += (yellowCoins-redCoins)
        return score
            
            
            
                

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
        
#        subboardaction = self.get_sub_board_action(board, player)
#        
#        if self.previousboard:
#            differenttowers = [0,0]
#            i = 0
#            while differenttowers[1] == 0 and i <= range(board.rows):
#                j = 0
#            #for i in range(board.rows):
#                while differenttowers[1] == 0 and j <= range(board.columns):
#                #for j in range(board.columns):
#                    if board.m[i][j] == self.previousboard[i][j]:
#                        if differenttowers[0] == 0:
#                            differenttowers[0] = [i, j]
#                        else:
#                            differenttowers[1] = [i, j]
#                    j += 1
#                i += 1        
#            counteraction = self.get_counter_action(board.get_percepts(), board, differenttowers, player)          
#            
#        self.previousboard = board.clone().play_action(action)
        return action 
    
    
    def get_sub_board_action(self, board, player):
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
                    best[0] = miniboardvalues[i][j]
                    best[1] = i
                    best[2] = j
        i = best[1]
        j = best[2]
        bigboardpercept = board.get_percepts()
        newpercept = [0,0,0,0]
        for x in range(4):
            newpercept[x] = bigboardpercept[x+i][j:j+4]
        subboard = Board(newpercept)
        subboardaction = minimax.search((subboard, player), self)
        subboardaction[0] += i
        subboardaction[1] += j
        subboardaction[2] += i
        subboardaction[3] += j   
        return (subboardaction,(board.clone().play_action(subboardaction), -player))
    
    
    def get_counter_action(self, bigboardpercept, board, differenttowers, player):
        x, y = 0
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
                elif differenttowers[1][1] == board.columns - 1:
                    #Right tower on the right side
                    #Only need to check difftower[1]
                    counterpercept = [[bigboardpercept[i][j] \
                    for j in range(board.columns-3, board.columns)] \
                    for i in range(2)]
                    y = differenttowers[0][1] - 1
                else:
                    counterpercept = [[bigboardpercept[i][j] \
                    for j in range(differenttowers[0][1]-1, differenttowers[1][1]+2)] \
                    for i in range(2)]
                    y = differenttowers[0][1] - 1
            elif differenttowers[0][0] == board.rows - 1:     
                #The different towers are on the lower row
                x = board.rows - 2
                if differenttowers[0][1] == 0:
                    #The left tower is on the left side of the board
                    #We can check only difftower[0]because of the way it is fill earlier
                    counterpercept = [[bigboardpercept[i][j] \
                    for j in range(3)] \
                    for i in range(board.rows-2, board.rows)]
                elif differenttowers[1][1] == board.columns - 1:
                    #Right tower on the right side
                    #Only need to check difftower[1]
                    counterpercept = [[bigboardpercept[i][j] \
                    for j in range(board.columns-3, board.columns)] \
                    for i in range(board.rows-2, board.rows)]
                    y = differenttowers[0][1] - 1
                else:
                    counterpercept = [[bigboardpercept[i][j] \
                    for j in range(differenttowers[0][1]-1, differenttowers[1][1]+2)] \
                    for i in range(board.rows-2, board.rows)]
                    y = differenttowers[0][1] - 1
            else:
                #on the middle rows
                if differenttowers[0][1] == 0:
                    #The left tower is on the left side of the board
                    #We can check only difftower[0]because of the way it is fill earlier
                    counterpercept = [[bigboardpercept[i][j] \
                    for j in range(3)] \
                    for i in range(differenttowers[0][0]-1, differenttowers[0][0]+2)]
                elif differenttowers[1][1] == board.columns - 1:
                    #Right tower on the right side
                    #Only need to check difftower[1]
                    counterpercept = [[bigboardpercept[i][j] \
                    for j in range(board.columns-3, board.columns)] \
                    for i in range(differenttowers[0][0]-1, differenttowers[0][0]+2)]
                else:
                    counterpercept = [[bigboardpercept[i][j] \
                    for j in range(differenttowers[0][1]-1, differenttowers[1][1]+2)] \
                    for i in range(differenttowers[0][0]-1, differenttowers[0][0]+2)]
                x = differenttowers[0][0] - 1
                y = differenttowers[0][1] - 1
        else:
            #The different towers are on the same column
            if differenttowers[0][0] == 0:
                #The upper tower is on the upper row
                if differenttowers[0][1] == 0:
                    #The towers are on the left side of the board
                    counterpercept = [[bigboardpercept[i][j] \
                    for j in range(2)] \
                    for i in range(3)]
                elif differenttowers[1][1] == board.columns - 1:
                    #Towers on the right side
                    counterpercept = [[bigboardpercept[i][j] \
                    for j in range(board.columns-2, board.columns)] \
                    for i in range(3)]
                    y = differenttowers[0][1] - 1
                else:
                    counterpercept = [[bigboardpercept[i][j] \
                    for j in range(differenttowers[0][1]-1, differenttowers[0][1]+2)] \
                    for i in range(3)]     
                    y = differenttowers[0][1] - 1
            elif differenttowers[1][0] == board.rows - 1:     
                #The lower tower is on the lower row
                x = board.rows - 3
                if differenttowers[0][1] == 0:
                    #The towers are on the left side of the board
                    counterpercept = [[bigboardpercept[i][j] \
                    for j in range(2)] \
                    for i in range(board.rows-3, board.rows)]
                elif differenttowers[0][1] == board.columns - 1:
                    #Right tower on the right side
                    counterpercept = [[bigboardpercept[i][j] \
                    for j in range(board.columns-2, board.columns)] \
                    for i in range(board.rows-3, board.rows)]
                    y = differenttowers[0][1] - 1
                else:
                    counterpercept = [[bigboardpercept[i][j] \
                    for j in range(differenttowers[0][1]-1, differenttowers[1][1]+2)] \
                    for i in range(board.rows-3, board.rows)]
                    y = differenttowers[0][1] - 1
            else:
                #on the middle rows
                if differenttowers[0][1] == 0:
                    #The towers are on the left side of the board
                    counterpercept = [[bigboardpercept[i][j] \
                    for j in range(2)] \
                    for i in range(differenttowers[0][0]-1, differenttowers[1][0]+2)]
                elif differenttowers[1][1]:
                    #Towers on the right side
                    counterpercept = [[bigboardpercept[i][j] \
                    for j in range(board.columns-2, board.columns)] \
                    for i in range(differenttowers[0][0]-1, differenttowers[1][0]+2)]
                else:
                    counterpercept = [[bigboardpercept[i][j] \
                    for j in range(differenttowers[0][1]-1, differenttowers[0][1]+2)] \
                    for i in range(differenttowers[0][0]-1, differenttowers[1][0]+2)]
                x = differenttowers[0][0] - 1
                y = differenttowers[0][1] - 1
            
        counterboard = Board(counterpercept)
        counteraction = minimax.search((counterboard, player), self)
        counteraction[0] += x
        counteraction[1] += y
        counteraction[2] += x
        counteraction[3] += y 
        return (counteraction,(board.clone().play_action(counteraction), -player))
                        
    
    def _see_if_isolate(self,i,j,board,score,tower):
        def compute(score,tower):
            if tower[1][0] == Color.YELLOW :
                score += board.get_hight(tower)
            elif tower[1][0] == Color.RED :
                score -= board.get_hight(tower)
            return score
        i_start = 0
        j_start = 0
        i_end = len(board.m)-1
        j_end = len(board.m[0])-1
        if (i > i_start and i < i_end) and (j > j_start and j < j_end) :
            if board.get_height(board.m[i][j+1])+board.get_height(board.m[i][j-1]) + \
                board.get_height(board.m[i+1][j])+ board.get_height(board.m[i-1][j]) == 0 :
                return compute(score,tower)
        elif i==i_start and j==j_start:
            if board.get_height(board.m[i][j+1]) + board.get_height(board.m[i+1][j]) == 0 :
                return compute(score,tower)
        elif i==i_end and j == j_start:
            if board.get_height(board.m[i][j+1]) + board.get_height(board.m[i-1][j]) == 0 :
                return compute(score,tower)
        elif i==i_start and j == j_end:
            if board.get_height(board.m[i+1][j]) + board.get_height(board.m[i-1][j]) == 0 :
                return compute(score,tower)  
        elif i==i_end and j == j_end:
            if board.get_height(board.m[i-1][j]) + board.get_height(board.m[i][j-1]) == 0 :
                return compute(score,tower) 
        elif i==i_start and (j > j_start and j < j_end) :
            if board.get_height(board.m[i][j+1]) +board.get_height(board.m[i][j-1])+ \
                board.get_height(board.m[i+1][j]) == 0:
                return compute(score,tower)
        elif i==i_end and (j > j_start and j < j_end) :
            if board.get_height(board.m[i][j+1]) +board.get_height(board.m[i][j-1])+ \
                board.get_height(board.m[i-1][j]) == 0:
                return compute(score,tower)
        elif (i > i_start and i < i_end) and j==j_start :
            if board.get_height(board.m[i+1][j]) +board.get_height(board.m[i-1][j])+ \
                board.get_height(board.m[i][j+1]) == 0:
                return compute(score,tower)
        elif (i > i_start and i < i_end) and j==i_end :
            if board.get_height(board.m[i+1][j]) +board.get_height(board.m[i-1][j])+ \
                board.get_height(board.m[i][j-1]) == 0:
                return compute(score,tower)      
        return score
        
    def _init_pattern(self):
        # Pattern Sandwich 
        self.mustDoDic[Action([3,[Color.RED, -2],[0,0],[0,0],[0,0]],[4,[-2,Color.RED],[0,0],[0,0],[0,0]])] = True
        self.mustDoDic[Action([3,[Color.RED, -2],[0,0],[0,0],[0,0]],[4,[-2,-2],[-2,Color.RED],[0,0],[0,0]])] = True
        self.mustDoDic[Action([3,[Color.RED, -2],[0,0],[0,0],[0,0]],[4,[-2,-2],[-2,-2],[-2,Color.RED],[0,0]])] = True
        self.mustDoDic[Action([3,[Color.RED, -2],[-2,-2],[0,0],[0,0]],[4,[-2,Color.RED],[0,0],[0,0],[0,0]])] = True
        self.mustDoDic[Action([3,[Color.RED, -2],[-2,-2],[-2,-2],[0,0]],[4,[-2,Color.RED],[0,0],[0,0],[0,0]])] = True
        self.mustDoDic[Action([3,[Color.RED, -2],[-2,-2],[0,0],[0,0]],[4,[-2,-2],[-2,Color.RED],[0,0],[0,0]])] = True
        
        self.suicideDic[Action([3,[Color.YELLOW, -2],[0,0],[0,0],[0,0]],[4,[-2,Color.YELLOW],[0,0],[0,0],[0,0]])] = True
        self.suicideDic[Action([3,[Color.YELLOW, -2],[0,0],[0,0],[0,0]],[4,[-2,-2],[-2,Color.YELLOW],[0,0],[0,0]])] = True
        self.suicideDic[Action([3,[Color.YELLOW, -2],[0,0],[0,0],[0,0]],[4,[-2,-2],[-2,-2],[-2,Color.YELLOW],[0,0]])] = True
        self.suicideDic[Action([3,[Color.YELLOW, -2],[-2,-2],[0,0],[0,0]],[4,[-2,Color.YELLOW],[0,0],[0,0],[0,0]])] = True
        self.suicideDic[Action([3,[Color.YELLOW, -2],[-2,-2],[-2,-2],[0,0]],[4,[-2,Color.YELLOW],[0,0],[0,0],[0,0]])] = True
        self.suicideDic[Action([3,[Color.YELLOW, -2],[-2,-2],[0,0],[0,0]],[4,[-2,-2],[-2,Color.YELLOW],[0,0],[0,0]])] = True
        # end of pattern sandwich
        
        #pattern make a 4-stack with a Yellow color on top, on an arrow case
        
        self.mustDoDic[Action([3,[-2,Color.YELLOW],[0,0],[0,0],[0,0]],[4,[-2,-2],[-2,-2],[-2,-2],[0,0]])] = True
        #self.mustDoDic[Action([3,[-2,-2],[-2,Color.YELLOW],[0,0],[0,0]],[4,[-2,-2],[-2,-2],[0,0],[0,0]])] = True
        #self.mustDoDic[Action([3,[-2,-2],[-2,-2],[-2,Color.YELLOW],[0,0]],[4,[-2,-2],[0,0],[0,0],[0,0]])] = True
        
        self.suicideDic[Action([3,[-2,Color.RED],[0,0],[0,0],[0,0]],[4,[-2,-2],[-2,-2],[-2,-2],[0,0]])] = True
        #self.suicideDic[Action([3,[-2,-2],[-2,Color.RED],[0,0],[0,0]],[4,[-2,-2],[-2,-2],[0,0],[0,0]])] = True
        #self.suicideDic[Action([3,[-2,-2],[-2,-2],[-2,Color.RED],[0,0]],[4,[-2,-2],[0,0],[0,0],[0,0]])] = True
    
        #pattern make a 4-stack with yellow color on bottom, on a blank case
        self.mustDoDic[Action([4,[-2,-2],[0,0],[0,0],[0,0]],[3,[Color.YELLOW,-2],[-2,-2],[-2,-2],[0,0]])] = True
        #self.mustDoDic[Action([4,[-2,-2],[-2,-2],[0,0],[0,0]],[3,[Color.YELLOW,-2],[-2,-2],[0,0],[0,0]])] = True
        #self.mustDoDic[Action([4,[-2,-2],[-2,-2],[-2,-2],[0,0]],[3,[Color.YELLOW,-2],[0,0],[0,0],[0,0]])] = True
        
        self.suicideDic[Action([4,[-2,-2],[0,0],[0,0],[0,0]],[3,[Color.RED,-2],[-2,-2],[-2,-2],[0,0]])] = True
        #self.suicideDic[Action([4,[-2,-2],[-2,-2],[0,0],[0,0]],[3,[Color.RED,-2],[-2,-2],[0,0],[0,0]])] = True
        #self.suicideDic[Action([4,[-2,-2],[-2,-2],[-2,-2],[0,0]],[3,[Color.RED,-2],[0,0],[0,0],[0,0]])] = True
        
        # broke an enemy tower. will be reversed after.
        self.mustDoDic[Action([4,[-2,Color.RED],[0,0],[0,0],[0,0]],[3,[2,-2],[-2,-2],[-2,-2],[0,0]])] = True
        #self.mustDoDic[Action([4,[-2,-2],[-2,Color.RED],[0,0],[0,0]],[3,[2,-2],[-2,-2],[0,0],[0,0]])] = True
        #self.mustDoDic[Action([4,[-2,-2],[-2,-2],[-2,Color.RED],[0,0]],[3,[2,-2],[0,0],[0,0],[0,0]])] = True
       
        # broke one of our tower.
        self.suicideDic[Action([4,[-2,Color.YELLOW],[0,0],[0,0],[0,0]],[3,[2,-2],[-2,-2],[-2,-2],[0,0]])] = True
        #self.suicideDic[Action([4,[-2,-2],[-2,Color.YELLOW],[0,0],[0,0]],[3,[2,-2],[-2,-2],[0,0],[0,0]])] = True
        #self.suicideDic[Action([4,[-2,-2],[-2,-2],[-2,Color.YELLOW],[0,0]],[3,[2,-2],[0,0],[0,0],[0,0]])] = True


if __name__ == "__main__" :
    player_main(Marvin_player())
