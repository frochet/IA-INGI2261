'''
Created on Sep 28, 2012

@author: inekar
'''

import IO

class State:
    
    def __init__(self, state):
        self.state = state
        
    def move(self, x, y, direction):
        if(self.is_possible(x, y, direction)):
            pass
    
    def is_possible(self, x, y, direction):
        pass