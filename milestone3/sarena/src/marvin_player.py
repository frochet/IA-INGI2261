'''
Created on 8 nov. 2012

@author: Florentin
'''
from sarena import *
import minimax
import time

class Marvin_player(Player,minimax.Game):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.pattern = dict()
        self.count_played = 0 # In order to know how many time we have played.
        # remplir les dict de pattern TODO
        
    def successors(self, state):
        board, player = state
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
        state = (Board(percepts), player)
        return minimax.search(state, self)
