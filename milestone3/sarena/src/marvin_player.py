'''
Created on 8 nov. 2012

@author: Florentin
'''
from sarena import *
import minimax
import time
from pattern import *

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
        # remplir les dict de pattern TODO
    
    def successors(self, state):
        board, player = state
        #temporaly
        for action in board.get_actions():
            yield (action,(board.clone().play_action(action), -player)) 
        # TODO

    def cutoff(self, state, depth):
        board, player = state
        # TODO
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
                print(str(tower))
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
                print("end of compute fo current")
        score += (yellowCoins-redCoins)
        return score
            
            
            
                

    def play(self, percepts, step, time_left):
        if step % 2 == 0:
            player = -1
        else:
            player = 1
            
        # TODO
        state = (Board(percepts), player)
        return minimax.search(state, self)  
    
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