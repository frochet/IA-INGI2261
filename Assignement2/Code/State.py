'''
Created on 11 oct. 2012

@author: Florentin
'''
from logging import raiseExceptions
import WrongDirectionException
from Case import *
from Box import Box
from Direction import Direction

class State:
    '''
    classdocs
    '''


    def __init__(self, board, boxes, char, currentDeadStates):
        '''
        Constructor
        boxes in a list of boxes
        '''
        self.board = board
        self.boxes = boxes
        self.char = char
        self.currentDeadStates = currentDeadStates
        pass
    
    def move(self, direction):
        if direction == Direction.UP:
            return self.move_up()
        elif direction == Direction.DOWN:
            return self.move_down()
        elif direction == Direction.LEFT:
            return self.move_left()
        elif direction == Direction.RIGHT:
            return self.move_right()
        else:
            raise WrongDirectionException(self.char.x,self.char.y,"In the class state, method move")
        
    def move_up(self):
        if not self.is_a_wall(self.char.x, self.char.y-1):
            #There is no wall in the desired direction
            if not self.is_a_box(self.char.x, self.char.y-1):
                #The is no box in the desired direction
                return State(self.board, self.clone_boxes(self.boxes), \
                self.char.move_char(Direction.UP))
            else:
                #There is a box in the way
                if not self.is_a_wall(self.char.x, self.char.y-2) \
                and not self.is_a_dead_state(self.char.x, self.char.y-2):
                    return State(self.board, \
                    self.move_box(self.char.x, self.char.y-1, Direction.UP), \
                    self.char.move_char(Direction.UP))
                else:
                    return False
        else:
            return False
            
    def move_down(self):
        if not self.is_a_wall(self.char.x, self.char.y+1):
            #There is no wall in the desired direction
            if not self.is_a_box(self.char.x, self.char.y+1):
                #The is no box in the desired direction
                return State(self.board, self.clone_boxes(self.boxes), \
                self.char.move_char(Direction.DOWN))
            else:
                #There is a box in the way
                if not self.is_a_wall(self.char.x, self.char.y+2) \
                and not self.is_a_dead_state(self.char.x, self.char.y+2):
                    return State(self.board, \
                    self.move_box(self.char.x, self.char.y+1, Direction.DOWN), \
                    self.char.move_char(Direction.DOWN))
                else:
                    return False
        else:
            return False
    
    def move_left(self):
        if not self.is_a_wall(self.char.x-1, self.char.y):
            #There is no wall in the desired direction
            if not self.is_a_box(self.char.x-1, self.char.y):
                #The is no box in the desired direction
                return State(self.board, self.clone_boxes(self.boxes), \
                self.char.move_char(Direction.LEFT))
            else:
                #There is a box in the way
                if not self.is_a_wall(self.char.x-2, self.char.y) \
                and not self.is_a_dead_state(self.char.x-2, self.char.y):
                    return State(self.board, \
                    self.move_box(self.char.x-1, self.char.y, Direction.LEFT), \
                    self.char.move_char(Direction.LEFT))
                else:
                    return False
        else:
            return False
    
    def move_right(self):
        if not self.is_a_wall(self.char.x+1, self.char.y):
            #There is no wall in the desired direction
            if not self.is_a_box(self.char.x+1, self.char.y):
                #The is no box in the desired direction
                return State(self.board, self.clone_boxes(self.boxes), \
                self.char.move_char(Direction.RIGHT))
            else:
                #There is a box in the way
                if not self.is_a_wall(self.char.x+2, self.char.y) \
                and not self.is_a_dead_state(self.char.x+2, self.char.y):
                    return State(self.board, \
                    self.move_box(self.char.x+1, self.char.y, Direction.RIGHT), \
                    self.char.move_char(Direction.RIGHT))
                else:
                    return False
        else:
            return False
    
    def is_a_wall(self, x, y):
        return self.board[x][y] == Case.WALL
    
    def is_a_box(self, x, y):
        '''
        check if return statment is correct and working
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
                if direction == Direction.UP:
                    newboxes.append(Box(x, y-1))
                elif direction == Direction.DOWN:
                    newboxes.append(Box(x, y+1))
                elif direction == Direction.LEFT:
                    newboxes.append(Box(x-1, y))
                elif direction == Direction.RIGHT:
                    newboxes.append(Box(x+1, y))
                else:
                    pass
            else: newboxes.append(box)
        return self.clone_boxes(newboxes)
                    
                    
                    
                    
                    
                    
                    
                    
    
