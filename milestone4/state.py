'''
Created on 27 nov. 2012

@author: Florentin
'''
import math
import random

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
    
    def swap(self,i1,i2):
        self.vertices[i1], self.vertices[i2] = self.vertices[i2], self.vertices[i1]
        return self.vertices

    def compute_path(self,L):
        i = 0
        sumation = 0
        while i < len(L) -1 :
            if L[i] > L[i+1]:
                sumation += self.cost_matrix[L[i]][L[i+1]]
            else:
                sumation += self.cost_matrix[L[i+1]][L[i]]
            i+=1
        return -sumation
