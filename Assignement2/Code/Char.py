'''
Created on Oct 13, 2012

@author: inekar
'''
from Direction import Direction

class Char:
    '''
    classdocs
    '''


    def __init__(self, x, y):
        '''
        Constructor
        '''
        self.x = x
        self.y = y
    
    def move_char(self, direction):
        newX = self.x
        newY = self.y
        if direction == Direction.UP:
            newX -= 1
        elif direction == Direction.DOWN:
            newX += 1
        elif direction == Direction.LEFT:
            newY -= 1
        elif direction == Direction.RIGHT:
            newY += 1
        return Char(newX, newY)
        