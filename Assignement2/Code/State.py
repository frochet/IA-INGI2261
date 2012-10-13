'''
Created on 11 oct. 2012

@author: Florentin
'''
from logging import raiseExceptions
import WrongDirectionException
from Case import *
from Box import Box

class State:
    '''
    classdocs
    '''


    def __init__(self, board, boxes, char):
        '''
        Constructor
        boxes in a list of boxes
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
            raise WrongDirectionException(self.char.x,self.char.y,"In the class state, method move")
        
    def move_up(self):
        ''' /!\ aux dead states
        '''
        if not self.is_a_wall(self.char.x, self.char.y-1):
            '''There is no wall in the desired direction'''
            if not self.is_a_box(self.char.x, self.char.y-1):
                '''The is no box in the desired direction'''
                return State(self.board, self.clone_boxes(self.boxes), \
                self.char.move_char("UP"))
            else:
                '''There is a box in the way'''
                if not self.is_a_wall(self.char.x, self.char.y-2) \
                and not self.is_a_dead_state(self.char, self.char.y-2):
                    return State(self.board, \
                    self.move_box(self.char.x, self.char.y-1, "UP"), \
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
        return self.board[x][y] == Case.WALL
    
    def is_a_box(self, x, y):
        '''check if return statment is correct and working
        '''
        for box in self.boxes:
            if x == box.x and y == box.y:
                return True
        return False
    
    def is_a_dead_state(self, x, y):
        '''returns true if (x, y) is a static dead state or if it is a 
        current dead state
        '''
        if self.board[x][y] == Case.STATIC_DEAD_STATE:
            return True
        else:
            for deadState in self.currentDeadStates:
                if x == deadState[0] and y == deadState[1]:
                    return True
            return False
        
    def find_current_dead_states(self):
        '''Creates a list of coordinates of the actual dead states for this 
        particular state. Like so [[x1, y1], [x2, y2], ...]
        '''
        pass
    
    def clone_boxes(self, boxes):
        newboxes = []
        for box in boxes:
            newboxes.append(Box(box.x, box.y))
        return newboxes
    
    def move_box(self, x, y, direction):
        newboxes = []
        for box in self.boxes:
            if x == box.x and y == box.y:
                if direction == "UP":
                    newboxes.append(Box(x, y-1))
                elif direction == "DOWN":
                    newboxes.append(Box(x, y+1))
                elif direction == "LEFT":
                    newboxes.append(Box(x-1, y))
                elif direction == "RIGHT":
                    newboxes.append(Box(x+1, y))
                else:
                    pass
            else: newboxes.append(box)
        return self.clone_boxes(newboxes)
                    
                    
                    
                    
                    
                    
                    
                    
    
