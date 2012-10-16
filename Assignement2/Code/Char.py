'''
Created on Oct 13, 2012

@author: Debroux Léonard, Rochet Florentin
'''
from Direction import Direction

class Char:
    '''
    Represent an avatar
    '''


    def __init__(self, y, x):
        '''
        Constructor
        '''
        self.y = y
        self.x = x
    
    def move_char(self, direction):
        '''Returns a new instance of char 
        which has done a move of 1 in the given direction
        '''
        newY = self.y
        newX = self.x
        if direction == Direction.UP:
            newY -= 1
        elif direction == Direction.DOWN:
            newY += 1
        elif direction == Direction.LEFT:
            newX -= 1
        elif direction == Direction.RIGHT:
            newX += 1
        return Char(newY, newX)
        