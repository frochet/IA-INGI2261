'''
Created on 8 nov. 2012

@author: Debroux Léonard - Rochet Florentin
'''
from sarena import *
import minimax
from time import *
from random import randint
import operator

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
        self.symetricDic = dict()
        self.count_played = 0 # In order to know how many time we have played.
        self._init_pattern()
        self.previousboard = 0
        self.previousSearchedBoard = None
        #self.previousDepth = 0
        #self.currentDepth = 4
        self.time_left = 0
        self.timer = 0
        self.step = 0
        self.timeout = False
        self.actualdepth = 4
    
        
    def successors(self, state):
        
        """
        Successor handle symetric depth but does not
        order the tree. When we tried this, the successor take too long time
        """
        board, player = state        
        for action in board.get_actions():
            tmpBoard = board.clone()
            tmpBoard.play_action(action)
            if tmpBoard not in self.symetricDic :
                self.symetricDic[str(tmpBoard)] = True
                yield (action,(tmpBoard, -player))


    def cutoff(self, state, depth):
        board, player = state

        if board.is_finished():
#            print("finished")
            return True
#        print (self.time_left - (time()-self.timer))
        if self.time_left - (time()-self.timer) <= 15 :
#            print("expired")
#            print (time()-self.timer)
            self.timeout = True
            return depth >= 1
#        elif self.time_left - (time()-self.timer) < 15 : and order the tree
#            return depth >= 2
#        elif self.time_left - (time()-self.timer) < 10 :
#            return True
        # Must cut if we played a suicide move to reach this state.
        # Must cut with iterative depth
        if not self.previousSearchedBoard == None :
            action_played = self._action_played(board,self.previousSearchedBoard)
            if action_played : # sometimes bad things happen and action_playes is false
                move = Action(action_played[1][0],action_played[1][1])
                if move.is_a_pattern(self.suicideDic) and depth % 2 == 0:
                    return True # if a node-max is a suicide, cut it, we do not play the move
                elif move.is_a_pattern(self.mustDoDic) and depth % 2 == 1 :
                    return True # if a node-min is a suicide for the opponent, cut it, he will not play that move
        
        #######################
        maxtime = (self.time_left - 14) / ((1 + (37/(self.step+1))**1.8)/2)
        if (time()-self.timer) >= maxtime:
#            print(maxtime)
            self.timeout = True
            return True
        else:
            return depth == self.actualdepth
        #######################     
        return depth >= 1
        
    def evaluate(self, state):
        board, player = state
        
        self.previousSearchedBoard = None
        if self.step >= 25 :
            return board.get_score()
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
                        if tower[1][0] == Color.YELLOW :
                            score += 4 # 1 for 1 coin win
                        elif tower[1][0] == Color.RED :
                            score -= 4
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
        
        self.time_left = time_left
        self.timer = time()
        self.step = step
        print(self.time_left)
        #print(self.actualdepth)

        if step % 2 == 0:
            player = -1
        else:
            player = 1
        board = Board(percepts)
        state = (board, player)
        
        #print(step)
        
        self.previousSearchedBoard = None
        # MustDo before !
        mustDo = []
        for i in range(board.rows) :
            for j in range(board.columns):
                actions = board.get_tower_actions(i,j)
                for action in actions :
                    t_1 = [board.m[action[0]][action[1]][0]]
                    t_2 = [board.m[action[2]][action[3]][0]]
                    t_1.extend(board.get_tower(board.m[action[0]][action[1]]))
                    t_2.extend(board.get_tower(board.m[action[2]][action[3]]))
                    move = Action(t_1,t_2)
                    if move.is_a_pattern(self.mustDoDic):
                        mustDo.append([action,move.weight])
        if len(mustDo) > 0:
            action_to_play = 0
            weight = 0
            for elem in mustDo :
                if elem[1] > weight :
                    weight = elem[1]
                    action_to_play = elem[0]
            #print(mustDo)
            if action_to_play == 0 :
                print("INVALIDE PLAY in PLAY")
                print(mustDo)
                self.previousboard = board.clone().play_action(mustDo[0][0])
                return mustDo[0][0]
            else:
                self.previousboard = board.clone().play_action(action_to_play)
                return action_to_play                
        else :
#            maxtime = (self.time_left - 9) / ((1 + (37/(self.step+1))**1.75)/2)
#            print("maxtime", maxtime)
#            print("timeleft", self.time_left)
#            print("step", self.step)
            if step < 10:
                counteraction = False
                if self.previousboard:
                    differenttowers = self.get_diff_towers(board)
                    #self.timeout = False
                    counteraction = self.get_counter_action(board.get_percepts(), board, differenttowers, player)
                    #self.check_timeout()
                self.timeout = False
                subboardaction = self.get_sub_board_action(board, player)
                self.check_timeout()
                if counteraction:
                    if counteraction[1] and subboardaction[1]:
                        if counteraction[0] > subboardaction[0]:
                            action = counteraction[1]
                        else:
                            action = subboardaction[1]
                    elif counteraction[1]:
                        action = counteraction[1]
                    elif subboardaction[1]:
                        action = subboardaction[1]
                    else:
                        self.symetricDic = dict()
                        self.timeout = False
                        action = minimax.search(state, self)
                        self.check_timeout()
                elif subboardaction[1]:
                    action = subboardaction[1]
                else:
                    self.symetricDic = dict()
                    self.timeout = False
                    action = minimax.search(state, self)
                    self.check_timeout()
                self.previousboard = board.clone().play_action(action)
            else:
                self.symetricDic = dict()
                self.timeout = False
                action = minimax.search(state, self)
                self.check_timeout()
            return action 


    def check_timeout(self):
        if self.timeout:
            self.actualdepth -= 1
            #print("minus")
        else:
            self.actualdepth += 1
            #print("plus")
        return True
    
    
    def get_diff_towers(self, board):
        differenttowers = [False,False]
        i = 0
        while not differenttowers[1] and i <= board.rows - 1:
            j = 0
        #for i in range(board.rows):
            while not differenttowers[1] and j <= board.columns - 1:
            #for j in range(board.columns):
                if board.get_height(board.m[i][j]) != self.previousboard.get_height(self.previousboard.m[i][j]):
                    if not differenttowers[0]:
                        differenttowers[0] = [i, j]
                    else:
                        differenttowers[1] = [i, j]
                j += 1
            i += 1  
        return differenttowers

    
    def get_sub_board_action(self, board, player):
        '''Returnsa tuple val, action with the action on the main board \
        and the value alpha beta found for the associated leaf
        '''
        miniboardvalues = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        best = [0,0,0]
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
                        while coin > 1 and board.m[i][j][coin][1] == 0:
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
        self.symetricStateDic = dict()
        self.time_left = (time()-self.timer)
        self.timer = time()
        subboardaction = search((subboard, player), board, i, j, self)
        if subboardaction[1]:
            boardaction = (subboardaction[0], (subboardaction[1][0] + i, \
            subboardaction[1][1] + j, \
            subboardaction[1][2] + i, \
            subboardaction[1][3] + j))
            if board.is_action_valid(boardaction[1]):
                return boardaction
            else:
                return (0, None)
        else:
            return(0, None)
        
    
    def get_counter_action(self, bigboardpercept, board, differenttowers, player):
        x = 0
        y = 0
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
                    y = differenttowers[0][1] - 1
                else:
                    counterpercept = [[bigboardpercept[i][j] \
                    for j in range(differenttowers[0][1]-1, differenttowers[1][1]+2)] \
                    for i in range(differenttowers[0][0]-1, differenttowers[0][0]+2)]
                    y = differenttowers[0][1] - 1
                x = differenttowers[0][0] - 1
                #y = differenttowers[0][1] - 1
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
                elif differenttowers[1][1] == board.columns - 1:
                    #Towers on the right side
                    counterpercept = [[bigboardpercept[i][j] \
                    for j in range(board.columns-2, board.columns)] \
                    for i in range(differenttowers[0][0]-1, differenttowers[1][0]+2)]
                    y = differenttowers[0][1] - 1
                else:
                    counterpercept = [[bigboardpercept[i][j] \
                    for j in range(differenttowers[0][1]-1, differenttowers[0][1]+2)] \
                    for i in range(differenttowers[0][0]-1, differenttowers[1][0]+2)]
                    y = differenttowers[0][1] - 1
                x = differenttowers[0][0] - 1
            
        counterboard = Board(counterpercept)
        self.symetricDic = dict() # reinit le dic
        counteraction = search((counterboard, player), board, x, y, self)
        if counteraction[1]:
            action = (counteraction[0], (counteraction[1][0] + x, \
            counteraction[1][1] + y, \
            counteraction[1][2] + x, \
            counteraction[1][3] + y))
            if board.is_action_valid(action[1]):
                return action
            else:
                print("unvalid action_played in counter")
                print(action)
                return False
            return action
        else:
            return(0, None)
                        
    def _action_played(self,currentBoard,previousBoard):
        """
            return action + towers involved in the move of previousBoard.
            (action,[tower_init, tower_targeted])
        """
        towers = [0,0]
        action = ()
        for i in range(currentBoard.rows) :
            for j in range(currentBoard.columns):
                if currentBoard.get_height(currentBoard.m[i][j]) != previousBoard.get_height(previousBoard.m[i][j]) :
                    t_1 = [previousBoard.m[i][j][0]]
                    t_1.extend(previousBoard.get_tower(previousBoard.m[i][j]))
                    if currentBoard.get_height(currentBoard.m[i][j]) > previousBoard.get_height(previousBoard.m[i][j]) :
                        towers[1] = t_1
                        action += i,j    
                    else :
                        towers[0] = t_1
                        if len(action) != 0:
                            tmp = action
                            action = (i, j)
                            action += tmp
                        else :
                            action += i,j
        if previousBoard.is_action_valid(action):
            return (action,towers)
        else:
            print("unvalid action_played in _action_played")
            print(action)
            return False
        
        
    def _see_if_isolate(self,i,j,board,score,tower):
        def compute(score,tower):
            if tower[1][0] == Color.YELLOW :
                score += board.get_height(tower)
            elif tower[1][0] == Color.RED :
                score -= board.get_height(tower)
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
        # BUG => WEIGHT == -3 !
        self.mustDoDic[Action([4,[-2,Color.RED],[0,0],[0,0],[0,0]],[3,[2,-2],[-2,-2],[-2,-2],[0,0]])] = True
        #self.mustDoDic[Action([4,[-2,-2],[-2,Color.RED],[0,0],[0,0]],[3,[2,-2],[-2,-2],[0,0],[0,0]])] = True
        #self.mustDoDic[Action([4,[-2,-2],[-2,-2],[-2,Color.RED],[0,0]],[3,[2,-2],[0,0],[0,0],[0,0]])] = True
        
        self.mustDoDic[Action([3,[Color.RED,-2],[-2,-2],[-2,-2],[0,0]],[4, [-2,-2],[0,0],[0,0],[0,0]])] = True
        self.mustDoDic[Action([3,[Color.RED,-2],[-2,-2],[0,0],[0,0]],[4, [-2,-2],[-2,-2],[0,0],[0,0]])] = True
        self.mustDoDic[Action([3,[Color.RED,-2],[0,0],[0,0],[0,0]],[4, [-2,-2],[-2,-2],[-2,-2],[0,0]])] = True
        
        self.mustDoDic[Action([4,[-2,-2],[0,0],[0,0],[0,0]],[3, [-2,-2],[-2,-2],[-2,Color.RED],[0,0]])] = True
        self.mustDoDic[Action([4,[-2,-2],[-2,-2],[0,0],[0,0]],[3, [-2,-2],[-2,Color.RED],[0,0],[0,0]])] = True
        self.mustDoDic[Action([4,[-2,-2],[-2,-2],[-2,-2],[0,0]],[3 ,[-2,Color.RED],[0,0],[0,0],[0,0]])] = True
        # broke one of our tower.
        self.suicideDic[Action([4,[-2,Color.YELLOW],[0,0],[0,0],[0,0]],[3,[2,-2],[-2,-2],[-2,-2],[0,0]])] = True
        #self.suicideDic[Action([4,[-2,-2],[-2,Color.YELLOW],[0,0],[0,0]],[3,[2,-2],[-2,-2],[0,0],[0,0]])] = True
        #self.suicideDic[Action([4,[-2,-2],[-2,-2],[-2,Color.YELLOW],[0,0]],[3,[2,-2],[0,0],[0,0],[0,0]])] = True
class Color :
    YELLOW = 1
    RED = -1


class Action(object):
    '''
    classdocs
    '''
    


    def __init__(self,tower_init,tower_target,**kwords):
        '''    
             tower_init : initial tower from the move goes to the tower target
             tower_target : tower targeted by a move.
             color : Color of the player executing the next action
             **kwords is used to extend an Action to a must complex pattern.
             
             See board representation to pass the correct format for towers.
        '''
        while [0,0] in tower_init  :
            tower_init.remove([0,0])
            
        while [0,0] in tower_target:
            tower_target.remove([0,0])
            
        self.t_init = tower_init
        self.t_target = tower_target
        self.size_t_init = len(self.t_init)
        self.size_t_target = len(self.t_target)
        self.kwords = kwords
        self.weight = self._compute_weight()
        self.t_target.extend(self.t_init) 
        self.t_target.append(self.weight)
        #print(self.t_target)
        self.representation = self._make_representation()
        #print(self.weight)
        #print(str(self.representation)+" tour final :"+str(self.t_target))
        if 'sub_board' in kwords :
            pass # analyse a pattern
        # define the representation TODO
    
    def __eq__(self,other):
        return self.representation == other.representation
    
    def __hash__(self):
        return self.representation
    
    def _make_representation(self):
        return hash(str(self.t_target))
    def _weight(self):
        if self.size_t_init == 2 and self.size_t_target == 2 : # one coin each towers
            self.weight = 1
        elif self.size_t_init == 3 and self.size_t_target == 3 : # two coins on each towers
            self.weight = 3
        elif self.size_t_init == 2 and self.size_t_target == 3 :
            self.weight = 2
        elif self.size_t_init == 3 and self.size_t_target == 2 :
            self.weight = 2 
        elif self.size_t_init == 4 and self.size_t_target == 2 :
            self.weight = 3
        elif self.size_t_init == 2 and self.size_t_target == 4 :
            self.weight = 3        
    def _detect_sandwich(self):
            if self.size_t_init > 1 and self.size_t_target > 1:
                if (self.t_init[1][0] == Color.RED and self.t_target[self.size_t_target-1][1] == Color.RED) \
                    or (self.t_init[1][0] == Color.YELLOW and self.t_target[self.size_t_target-1][1] == Color.YELLOW):
                    i = 1
                    while i < self.size_t_init :
                        if i == 1:
                            self.t_init[i][1] = -2
                        else :
                            self.t_init[i][0] = -2
                            self.t_init[i][1] = -2
                        i+=1
                    i = 1
                    while i < self.size_t_target :
                        if i == self.size_t_target-1 :
                            self.t_target[i][0] = -2
                        else :
                            self.t_target[i][0] = -2
                            self.t_target[i][1] = -2
                        i+=1 
                    self._weight()
                    if self.t_init[1][0] == Color.YELLOW :
                        self.weight = -self.weight
                    self.t_target.pop(0)
                    self.t_init.pop(0)
                    return True
                else :
                    return False
            else :
                return False
            
    
    def _detect_color_up(self):
        if self.size_t_init + self.size_t_target == 6 and self.size_t_target >1 :
            if self.t_init[self.size_t_init-1][1] == Color.YELLOW or self.t_init[self.size_t_init-1][1] == Color.RED :
                
                i = 1
                while i < self.size_t_init :
                    if i == self.size_t_init-1:
                        self.t_init[i][0] = -2
                    else :
                        self.t_init[i][0] = -2
                        self.t_init[i][1] = -2
                    i+=1
                i = 1
                while i < self.size_t_target :
                    self.t_target[i][0] = -2
                    self.t_target[i][1] = -2
                    i+=1 
                    
                self._weight()
                
                if self.t_init[self.size_t_init-1][1] == Color.RED and self.t_target[0] == 4 :
                    self.weight = -self.weight
                elif self.t_init[self.size_t_init-1][1] == Color.YELLOW and self.t_target[0] == 3 and \
                    self.t_target[1][0] != Color.YELLOW :
                    self.t_target[1][0] = 2
                    #choisir pattern
                    self.weight = -self.weight
                elif self.t_init[self.size_t_init-1][1] == Color.RED and self.t_target[0] == 3 and \
                    self.t_target[1][0] == Color.RED :
                    self.weight = -self.weight
                    self.t_target[1][0] = 2
                self.t_init.pop(0)
                return True
            elif self.t_target[self.size_t_target-1][1] == Color.RED and self.t_target[1][0] != Color.RED and self.t_target[0] == 3 :
                i = 1
                while i < self.size_t_init :
                    self.t_init[i][0] = -2
                    self.t_init[i][1] = -2
                    i+=1
                i = 1
                while i < self.size_t_target :
                    if i == self.size_t_target-1 :
                        self.t_target[i][0] = -2
                    else :
                        self.t_target[i][0] = -2
                        self.t_target[i][1] = -2
                    i+=1 
                self._weight()
                self.t_init.pop(0)
                return True
            return False
                 
        return False
    def _detect_color_bot(self):
        if self.size_t_init + self.size_t_target == 6 and self.size_t_target > 1 :
            if (self.t_target[1][0] == Color.YELLOW or self.t_target[1][0] == Color.RED) and self.t_target[0] == 3 :
                i = 1
                while i < self.size_t_init :
                        self.t_init[i][0] = -2
                        self.t_init[i][1] = -2
                        i+=1 
                i = 1
                while i < self.size_t_target :
                    if i == 1 :
                        self.t_target[i][1] = -2
                    else :
                        self.t_target[i][0] = -2
                        self.t_target[i][1] = -2
                    i+=1
                self._weight()
                
                if self.t_target[1][0] == Color.RED :
                    self.weight = -self.weight
                self.t_init.pop(0)
                return True
            elif (self.t_init[1][0] == Color.RED  and self.t_target[0] == 4) :
                
                i = 1
                while i < self.size_t_init :
                    if i == 1 :
                        self.t_init[i][1] = -2
                    else:
                        self.t_init[i][0] = -2
                        self.t_init[i][1] = -2    
                    i+=1 
                i = 1
                while i < self.size_t_target :
                    self.t_target[i][0] = -2
                    self.t_target[i][1] = -2
                    i+=1
                self._weight()
                self.t_init.pop(0)
                return True
        return False
        
    def _compute_weight(self):
        self.weight = 0
           
        if 'sub_borad' in self.kwords :
            pass
        #basic action
        else :
            #detect sandwich

            if self._detect_sandwich() :
                return self.weight
            if self._detect_color_up() :
                return self.weight
            if self._detect_color_bot() :
                return self.weight
            else: return 0
                    
    def is_a_pattern(self,dico):
        return self in dico


inf = float("inf")

def search(state, bigboard, i, j, game, prune=True):
    """Perform a MiniMax/AlphaBeta search and return the best action.

    Arguments:
    state -- initial state
    game -- a concrete instance of class Game
    prune -- whether to use AlphaBeta pruning

    """
    def get_leaf_state(state, bigboard, i, j):
        bigclone = bigboard.clone()
        miniboard, player = state
        width = len(miniboard.m)
        hight = len(miniboard.m[0])
        for x in range(width):
            for y in range(hight):
                bigclone.m[x+i][y+j] = miniboard.m[x][y]
        return (bigclone, player)
        
        
    def max_value(state, bigboard, i, j, alpha, beta, depth):
        if game.cutoff(state, depth):
            bigstate = get_leaf_state(state, bigboard, i, j)
            return game.evaluate(bigstate), None
        val = -inf
        action = None
        for a, s in game.successors(state):
            v, _ = min_value(s, bigboard, i, j, alpha, beta, depth + 1)
            if v > val:
                val = v
                action = a
                if prune:
                    if v >= beta:
                        return v, a
                    alpha = max(alpha, v)
        return val, action

    def min_value(state, bigboard, i, j, alpha, beta, depth):
        if game.cutoff(state, depth):
            bigstate = get_leaf_state(state, bigboard, i, j)
            return game.evaluate(bigstate), None
        val = inf
        action = None
        for a, s in game.successors(state):
            v, _ = max_value(s, bigboard, i, j, alpha, beta, depth + 1)
            if v < val:
                val = v
                action = a
                if prune:
                    if v <= alpha:
                        return v, a
                    beta = min(beta, v)
        return val, action

    val, action = max_value(state, bigboard, i, j, -inf, inf, 0)
    return val, action

class OrderedBoard(object):
    
    def __init__(self,eval,action):
        self.eval = eval
        self.action = action
    
#    def __eq__(self,other):
#        return self.eval == other.eval
#    def __cmp__(self,other):
#        if self.eval > other.eval:
#            return 1
#        elif self.eval < other.eval:
#            return -1
#        else: return 0
        
if __name__ == "__main__" :
    player_main(Marvin_player())
