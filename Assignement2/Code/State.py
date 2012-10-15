'''
Created on 11 oct. 2012

@author: Florentin
'''
from logging import raiseExceptions
import WrongDirectionException
from Case import *
from Box import Box
from Direction import Direction
from Board import Board
from Char import Char

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
        self.representation = self.make_representation()
    
    def __hash__(self):
        return self.representation
    
    def __eq__(self,other):
        return self.representation == other.representation
    
    def make_representation(self):
        result = ""
        result += str(self.char.y)
        result += str(self.char.x)
        for box in self.boxes:
            result += str(box.y)
            result += str(box.y)
        return int(result)
        
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
                self.char.move_char(Direction.UP), \
                self.copy_currentDeadStates())
            else:
                #There is a box in the way
                if not self.is_a_wall(y-2, x) \
                and not self.is_a_dead_state(y-2, x) \
                and not self.is_a_box(y-2, x):
                    newCurrentDeadStates = self.copy_currentDeadStates()
                    
                    #allows to go to a PDS if already on one
                    if self.is_currentDeadState(y-2, x):
                        if not self.is_currentDeadState(y-1, x) or \
                        self.is_a_box(y-3, x):
                            return False
                    else:
                        if self.creates_dead_state(y-2, x):
                            self.extend_currentDeadStates \
                            (newCurrentDeadStates, y-2, x)
                    
                    return State(self.board, \
                    self.move_box(y-1, x, Direction.UP), \
                    self.char.move_char(Direction.UP), \
                    newCurrentDeadStates)
                else:
                    return False
        else:
            return False
            
    def move_down(self):
        x = self.char.x
        y = self.char.y
        if not self.is_a_wall(y+1, x):
            #There is no wall in the desired direction
            if not self.is_a_box(y+1, x):
                #The is no box in the desired direction
                return State(self.board, self.clone_boxes(self.boxes), \
                self.char.move_char(Direction.DOWN), \
                self.copy_currentDeadStates())
            else:
                #There is a box in the way
                if not self.is_a_wall(y+2, x) \
                and not self.is_a_dead_state(y+2, x) \
                and not self.is_a_box(y+2, x):
                    newCurrentDeadStates = self.copy_currentDeadStates()
                    
                    #allows to go to a PDS if already on one
                    if self.is_currentDeadState(y+2, x) or \
                    self.is_a_box(y+3, x):
                        if not self.is_currentDeadState(y+1, x):
                            return False
                    else:
                        if self.creates_dead_state(y+2, x):
                            self.extend_currentDeadStates \
                            (newCurrentDeadStates, y+2, x)
                    
                    return State(self.board, \
                    self.move_box(y+1, x, Direction.DOWN), \
                    self.char.move_char(Direction.DOWN), \
                    newCurrentDeadStates)
                else:
                    return False
        else:
            return False
    
    def move_left(self):
        x = self.char.x
        y = self.char.y
        if not self.is_a_wall(y, x-1):
            #There is no wall in the desired direction
            if not self.is_a_box(y, x-1):
                #The is no box in the desired direction
                return State(self.board, self.clone_boxes(self.boxes), \
                self.char.move_char(Direction.LEFT), \
                self.copy_currentDeadStates())
            else:
                #There is a box in the way
                if not self.is_a_wall(y, x-2) \
                and not self.is_a_dead_state(y, x-2) \
                and not self.is_a_box(y, x-2):
                    newCurrentDeadStates = self.copy_currentDeadStates()
                    
                    #allows to go to a PDS if already on one
                    if self.is_currentDeadState(y, x-2) or \
                    self.is_a_box(y, x-3):
                        if not self.is_currentDeadState(y, x-1):
                            return False
                    else:
                        if self.creates_dead_state(y, x-2):
                            self.extend_currentDeadStates \
                            (newCurrentDeadStates, y, x-2)
                    
                    return State(self.board, \
                    self.move_box(y, x-1, Direction.LEFT), \
                    self.char.move_char(Direction.LEFT), \
                    newCurrentDeadStates)
                else:
                    return False
        else:
            return False
    
    def move_right(self):
        x = self.char.x
        y = self.char.y
        if not self.is_a_wall(y, x+1):
            #There is no wall in the desired direction
            if not self.is_a_box(y, x+1):
                #The is no box in the desired direction
                return State(self.board, self.clone_boxes(self.boxes), \
                self.char.move_char(Direction.RIGHT), \
                self.copy_currentDeadStates())
            else:
                #There is a box in the way
                if not self.is_a_wall(y, x+2) \
                and not self.is_a_dead_state(y, x+2) \
                and not self.is_a_box(y, x+2):
                    newCurrentDeadStates = self.copy_currentDeadStates()
                    
                    #allows to go to a PDS if already on one
                    if self.is_currentDeadState(y, x+2) or \
                    self.is_a_box(y, x+3):
                        if not self.is_currentDeadState(y, x+1):
                            return False
                    else:
                        if self.creates_dead_state(y, x+2):
                            self.extend_currentDeadStates \
                            (newCurrentDeadStates, y, x+2)
                    
                    return State(self.board, \
                    self.move_box(y, x+1, Direction.RIGHT), \
                    self.char.move_char(Direction.RIGHT), \
                    newCurrentDeadStates)
                else:
                    return False
        else:
            return False
    
    def is_a_wall(self, y, x):
        return self.board.board[y][x] == Case.WALL
    
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
        if self.board.board[y][x] == Case.STATIC_DEAD_STATE:
            return True
        else:
#            for deadState in self.currentDeadStates:
#                if y == deadState[0] and x == deadState[1]:
#                    return True
            return False
        
    def is_a_goal(self, y, x):
        return self.board.board[y][x] == Case.GOAL
        
    def is_currentDeadState(self, y, x):
        return [y, x] in self.currentDeadStates
        
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
        return self.board.board[y][x] == Case.HPDS or \
        self.board.board[y][x] == Case.VPDS
    
    def copy_currentDeadStates(self):
        newlist = []
        for state in self.currentDeadStates:
            newlist.append([state[0], state[1]])
        return newlist
    
    def extend_currentDeadStates(self, stateList, y, x):
        iterY = y
        iterX = x
        
        if self.board.board[y][x] == Case.HPDS and \
        self.same_amount(y, x, Direction.HORIZONTAL):
            while self.board.board[iterY][iterX] == Case.HPDS \
            or self.board.board[iterY][iterX] == Case.GOAL:
                stateList.append([iterY, iterX])
                iterX -= 1
            iterX = x+1
            while self.board.board[iterY][iterX] == Case.HPDS \
            or self.board.board[iterY][iterX] == Case.GOAL:
                stateList.append([iterY, iterX])
                iterX += 1
                
        if self.board.board[y][x] == Case.VPDS and \
        self.same_amount(y, x, Direction.VERTICAL):
            while self.board.board[iterY][iterX] == Case.VPDS \
            or self.board.board[iterY][iterX] == Case.GOAL:
                stateList.append([iterY, iterX])
                iterY -= 1
            iterY = y+1
            while self.board.board[iterY][iterX] == Case.VPDS \
            or self.board.board[iterY][iterX] == Case.GOAL:
                stateList.append([iterY, iterX])
                iterY += 1
                
    def same_amount(self, y, x, dir):
        #iterY = y
        #iterX = x
        nbBoxes = 0
        nbGoals = 0
        if dir == Direction.HORIZONTAL:
            while not self.is_a_dead_state(y, x):
                x -= 1
            x += 1
            while not self.is_a_dead_state(y, x):
                if [y, x] in self.boxes:
                    nbBoxes += 1
                if self.is_a_goal(y, x):
                    nbGoals += 1
                x += 1
        if dir == Direction.VERTICAL:
            while not self.is_a_dead_state(y, x):
                y -= 1
            y += 1
            while not self.is_a_dead_state(y, x):
                if [y, x] in self.boxes:
                    nbBoxes += 1
                if self.is_a_goal(y, x):
                    nbGoals += 1
                y += 1
        return nbBoxes >= nbGoals - 1
                
                    
                    
                    
if __name__ == "__main__" :
    plateau = Board("../benchs/sokoInst01.goal")
    plateau.print_board()
    #plateau.board[2][2] = Case.VPDS
    #plateau.board[3][2] = Case.VPDS
    etattest = State(plateau, [Box(2, 3), Box(2, 1)], Char(3, 3), [])
    print (etattest.char.y)
    newetattest = etattest.move(Direction.UP)
    print (newetattest.boxes[0].y)
    print (newetattest.char.y)
    plateau.print_board()
    print (newetattest.currentDeadStates)


                    
                    
                    
    
