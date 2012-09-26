'''
Created on 24 sept. 2012

@author: Florentin
'''
from search import *

class Test:
    '''
    classdocs
    '''


    def __init__(self) :
        '''
        Constructor
        '''
        self.name = "boup"
        
    def toString(self) :
        print(self.name+" est son nom")



if __name__ == "__main__":
    test = Test()
    test.toString()

