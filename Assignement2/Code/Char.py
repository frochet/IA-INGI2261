'''
Created on Oct 13, 2012

@author: inekar
'''
from Direction import Direction

class Char:
    '''
    classdocs
    '''


    def __init__(self, y, x):
        '''
        Constructor
        '''
        self.y = y
        self.x = x
    
    def move_char(self, direction):
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
        