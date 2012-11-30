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
    
    def lswap(self,L,i1,i2):
        L[i1], L[i2] = L[i2], L[i1]
        return L
    def swap(self,i1,i2):
        self.vertices[i1], self.vertices[i2] = self.vertices[i2], self.vertices[i1]
        return self.vertices

    def swap_best(self):        
        i = 0
        best = self.compute_path()
        swap = self.vertices
        while i < len(self.vertices)-1 :
            j = i+1
            while j < len(self.vertices):
                self.lswap(self.vertices, i, j)
                path = self.compute_path()
                if path < best :
                    swap = self.vertices[:]
                j+=1
            i+=1
        self.vertices = swap[:]
        return swap
    
    def swap_random_from_bests(self,size):
        tab = []
        i = 0
        while i < size :
            tab.insert(i, self.swap_best())
        return random.choice(tab)
        
    
    def compute_path(self):
        i = 0
        sumation = 0
        while i < len(self.vertices) -1 :
            if self.vertices[i] > self.vertices[i+1]:
                sumation += self.cost_matrix[self.vertices[i]][self.vertices[i+1]]
            else:
                sumation += self.cost_matrix[self.vertices[i+1]][self.vertices[i]]
            i+=1
        return -sumation