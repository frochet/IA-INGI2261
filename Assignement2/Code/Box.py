'''
Created on Oct 13, 2012

@author: Debroux Léonard, Rochet Florentin
'''

class Box:
    '''
    classdocs
    '''


    def __init__(self, y, x):
        '''
        Constructor
        '''
        self.y = y
        self.x = x

    
    def __repr__(self):
        return "x : {}, y: {}".format(self.x,self.y)

