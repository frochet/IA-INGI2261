'''
Created on 11 oct. 2012

@author: Florentin
'''
from logging import raiseExceptions
import WrongDirectionException

class State:
    '''
    classdocs
    '''


    def __init__(self, boxes, char):
        '''
        Constructor
        '''
        self.boxes = boxes
        self.char = char
        #self.currentDeadStates = currentDeadStates
        pass
    
    def move(self, direction):
        if direction == "UP":
            return self.move_up()
        elif direction == "DOWN":
            return self.move_down()
        elif direction == "LEFT":
            return self.move_left()
        elif direction == "RIGHT":
            return self.move_right()
        else:
            raise WrongDirectionException(self.char.x,self.char.y,"In the class state, method move")
        
    def move_up(self):
        if not self.is_a_wall(char.x, char.y):
            pass
        else:
            return False
            
    
    def move_down(self):
        pass
    
    def move_left(self):
        pass
    
    def move_right(self):
        pass
    
    def is_a_wall(self, x, y):
        pass
    
    def is_a_box(self, x, y):
        pass
    
    def is_a_dead_state(self, x, y):
        pass
        