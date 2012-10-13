'''
Created on 11 oct. 2012

@author: Florentin
'''
from logging import raiseExceptions

class State:
    '''
    classdocs
    '''


    def __init__(self, board, boxes, char):
        '''
        Constructor
        '''
        self.board = board
        self.boxes = boxes
        self.char = char
        self.currentDeadStates = self.find_current_dead_states()
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
            pass
        
    def move_up(self):
        if not self.is_a_wall(self.char.x, self.char.y - 1):
            '''There is no wall in the desired direction'''
            if not self.is_a_box(self.char.x, self.char.y - 1):
                '''The is no box in the desired direction'''
                return State(self.board, self.clone_boxes(), \
                self.char.move_char("UP"))
            else:
                '''There is a box in the way'''
                if not self.is_a_wall(self.char.x, self.char.y - 2):
                    return State(self.board, self.move_box("UP"), \
                    self.char.move_char("UP"))
                else:
                    return False
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
        
    def find_current_dead_states(self):
        pass
    
    def clone_boxes(self):
        pass