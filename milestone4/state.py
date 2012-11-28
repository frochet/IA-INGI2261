'''
Created on 27 nov. 2012

@author: Florentin
'''
import math

class State(object):
    '''
    classdocs
    '''


    def __init__(self, vertices, cost_matrix):
        '''
        Constructor
        '''
        self.vertices = vertices
        self.cost_matrix = cost_matrix
        
    def swap_all(self):
        """
            yield all the possible swap_all
        """
        def lswap(L,i1,i2):
            L[i1], L[i2] = L[i2], L[i1]
            return L
        i = 0
        while i < len(self.vertices)-1 :
            j = i+1
            while j < len(self.vertices) :
                lswap(self.vertices,i,j)
                yield(self.vertices)
                j+=1
            i+=1   
    
    def swap_best(self, dic):
        pass 
    
    def compute_path(self):
        i = 0
        sum = 0
        while i < len(self.vertices) -1 :
            if self.vertices[i] > self.vertices[i+1] :
                sum += self.matrix_cost[i][i+1]
            else:
                sum += self.matrix_cost[i+1][i]
        return sum
        
        
if __name__ == "__main__" :
    
    state = State([1,2,3,4])
    for elem in state.swap_all():
        print(elem)            