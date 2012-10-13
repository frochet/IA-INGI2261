'''
Created on Oct 13, 2012

@author: inekar
'''

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
        if direction == "UP":
            newX -= 1
        elif direction == "DOWN":
            newX += 1
        elif direction == "LEFT":
            newY -= 1
        elif direction == "RIGHT":
            newY += 1
        return Char(newX, newY)
        