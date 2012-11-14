#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

from sarena import *
import minimax
import time
import operator


class AlphaBetaPlayer(Player, minimax.Game):

    """Sarena Player.

    A state is a tuple (b, p) where p is the player to make a move and b
    the board.

    """
#    count = 0
#    depthCount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    def __init__(self):
        '''
        Constructor
        '''
        self.mustDoDic = dict()
        self.suicideDic = dict()
        self.symetricDic = dict()
        self.count_played = 0 # In order to know how many time we have played.
        self._init_pattern()
        #self.miniboard = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        self.previousboard = 0
        self.previousSearchedBoard = None
        self.previousDepth = 0
        self.currentDepth = 5
        self.time_left = 0
        self.timer = 0
        self.step = 0
        self.timeout = False
        
    
    def successors(self, state):
        
        """
        Successor handle symetric depth and order the tree
        """
        board, player = state        
        actions_ordered = []
        for action in board.get_actions():
            tmpBoard = board.clone()
            tmpBoard.play_action(action)
            if tmpBoard not in self.symetricDic :
                self.symetricDic[str(tmpBoard)] = True
                yield (action,(tmpBoard, -player))
#                actions_ordered.append(OrderedBoard(self.evaluate((tmpBoard,player)),action))
#        if player == 1:
#            actions_ordered.sort(key=operator.attrgetter('eval'),reverse=True)
#        else : 
#            actions_ordered.sort(key=operator.attrgetter('eval'))
#        for orderedBoard in actions_ordered:
#            self.previousSearchedBoard = board.clone()
#            yield (orderedBoard.action,(board.clone().play_action(orderedBoard.action), -player)) 

    
    def cutoff(self, state, depth):
        if depth == 4:
            return True
#        self.depthCount[depth] += 1
#        self.count += 1
#        if self.count % 1000000 == 0:
#            print("% noeud totaux", self.count)
#            print("% par depth", self.depthCount)
#            print("% secondes", time.time()-self.start)
        board, player = state
        return board.is_finished()

    def evaluate(self, state):
        board, player = state
        return board.get_score()
    
    def play(self, percepts, step, time_left):
        if step % 2 == 0:
            player = -1
        else:
            player = 1
        start = time.time()
        state = (Board(percepts), player)
        m = minimax.search(state, self)

#        print("nombre de noeuds explorés : ", self.count)
#        print("nombre de noeuds explorés par depth : ", self.depthCount)
#        self.count = 0
#        depthCount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        print("temps elapsed : ", format(time.time()-start))
        return m

    
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
       
        # broke one of our tower.
        self.suicideDic[Action([4,[-2,Color.YELLOW],[0,0],[0,0],[0,0]],[3,[2,-2],[-2,-2],[-2,-2],[0,0]])] = True
        #self.suicideDic[Action([4,[-2,-2],[-2,Color.YELLOW],[0,0],[0,0]],[3,[2,-2],[-2,-2],[0,0],[0,0]])] = True
        #self.suicideDic[Action([4,[-2,-2],[-2,-2],[-2,Color.YELLOW],[0,0]],[3,[2,-2],[0,0],[0,0],[0,0]])] = True



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

class Color :
    YELLOW = 1
    RED = -1

class OrderedBoard(object):
    
    def __init__(self,eval,action):
        self.eval = eval
        self.action = action
    
    def __eq__(self,other):
        return self.eval == other.eval
    def __cmp__(self,other):
        if self.eval > other.eval:
            return 1
        elif self.eval < other.eval:
            return -1
        else: return 0


if __name__ == "__main__":
    player_main(AlphaBetaPlayer())
