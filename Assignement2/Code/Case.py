'''
Created on 11 oct. 2012

@author: Florentin
'''

class Case:
    '''
        Enumeration that represent a case on the board.
    '''
    GOAL = 0
    NORMAL = 1
    WALL = 2
    STATIC_DEAD_STATE = 3
    VPDS = 4 #Vertical Possible Dead State
    HPDS = 5 #Horizontal Possible Dead State