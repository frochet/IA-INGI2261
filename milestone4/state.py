'''
Created on 27 nov. 2012

@author: Florentin
'''

class State(object):
    '''
    classdocs
    '''


    def __init__(self, vertices):
        '''
        Constructor
        '''
        self.vertices = vertices
        self.nbr_of_swap = 0
        
    def swap(self):
        """
            do a swap, return a new vertices. 
            return False if all the swap have been done
        """
        pass
    
    def compute_path(self):
        pass
        
        