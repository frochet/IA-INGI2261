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
        x = self.char.x
        y = self.char.y
        if not self.is_a_wall(y-1, x):
            #There is no wall in the desired direction
            if not self.is_a_box(y-1, x):
                #The is no box in the desired direction
                return State(self.board, self.clone_boxes(self.boxes), \
                self.char.move_char(Direction.UP))
            else:
                #There is a box in the way
                if not self.is_a_wall(y-2, x) \
                and not self.is_a_dead_state(y-2, x):
                    if self.creates_dead_state(y-2, x):
                        pass
                
                    return State(self.board, \
                    self.move_box(y-1, x, Direction.UP), \
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
    
    def is_a_wall(self, y, x):
        return self.board[y][x] == Case.WALL
    
    def is_a_box(self, y, x):
        '''
        check if return statment is correct and working
        '''
        for box in self.boxes:
            if y == box.y and x == box.x:
                return True
        return False
    
    def is_a_dead_state(self, y, x):
        '''returns true if (y, x) is a static dead state or if it is a 
        current dead state
        '''
        if self.board[y][x] == Case.STATIC_DEAD_STATE:
            return True
        else:
            for deadState in self.currentDeadStates:
                if y == deadState[0] and x == deadState[1]:
                    return True
            return False
        
    def find_current_dead_states(self):
        '''Creates a list of coordinates of the actual dead states for this 
        particular state. Like so [[y1, x1], [y2, x2], ...]
        '''
        pass
    
    def clone_boxes(self, boxes):
        newboxes = []
        for box in boxes:
            newboxes.append(Box(box.y, box.x))
        return newboxes
    
    def move_box(self, y, x, direction):
        newboxes = []
        for box in self.boxes:
            if y == box.y and x == box.x:
                if direction == Direction.UP:
                    newboxes.append(Box(y-1, x))
                elif direction == Direction.DOWN:
                    newboxes.append(Box(y+1, x))
                elif direction == Direction.LEFT:
                    newboxes.append(Box(y, x-1))
                elif direction == Direction.RIGHT:
                    newboxes.append(Box(y, x+1))
                else:
                    pass
            else: newboxes.append(box)
        return self.clone_boxes(newboxes)
    
    def creates_dead_state(self, y, x):
        return self.board[y][x]
                    
                    
                    
                    
                    
                    
                    
                    
    
