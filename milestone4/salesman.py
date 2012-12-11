'''
Created on 11 dec. 2012

@author: Florentin
'''
from search import *
from state import *
from parserCity import *
from GreedySearch import *
from time import time


class TravellingSalesman(object):
    '''
    classdocs
    '''

    def __init__(self, initial,matrice, goal=None):
        self.initial= State(initial,matrice)
        self.matrice = matrice  
    def successor(self, state):
        i = 0
        next_state = State(state.vertices[:],self.matrice)   
        while i < len(self.initial.vertices)-1:
            j=i+1
            while j < len(self.initial.vertices):
                next_state.swap(i, j)
                next_state = State(next_state.vertices[:],self.matrice)
                yield (None, next_state)
                next_state = State(state.vertices[:],self.matrice)
                j+=1
            i+=1
    def value(self,state):
        """Compute the path value"""
        return state.compute_path(state.vertices)


def best_in_tab(tab, val,swap):
        valToRemember = None
        swapToRemember = None
        i = 0
        for elem in tab :
            i+=1
            if val < elem[1] :
                elemToRemember = elem[1]
                swapToRemember = elem[0]
                tab[tab.index(elem)][1] = val
                tab[tab.index(elem)][0] = swap
                break
        if valToRemember != None:
            return best_in_tab(tab[i:],elemToRemember,swapToRemember)