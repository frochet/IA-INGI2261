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
        best = self.compute_path(self.vertices)
        swap = self.vertices
        while i < len(self.vertices)-1 :
            j = i+1
            while j < len(self.vertices):
                self.swap(i, j)
                path = self.compute_path(self.vertices)
                if path > best :
                    best = path
                    swap = self.vertices[:]
                j+=1
            i+=1
        self.vertices = swap[:]
        return swap
    
    def best_in_tab(self,tab, val,swap):
            valToRemember = None
            swapToRemember = None
            i = 0
            for elem in tab :
                i+=1
                if val < elem[1] :
                    elemToRemember = elem[1]
                    swapToRemember = elem[0][:]
                    tab[tab.index(elem)][1] = val
                    tab[tab.index(elem)][0] = swap
                    break
            if valToRemember != None:
                return self.best_in_tab(tab[i:],elemToRemember,swapToRemember)
            
    def swap_random_from_bests(self):
                          
        tab = [[[],float('inf')],[[],float('inf')],[[],float('inf')],[[],float('inf')],[[],float('inf')]]
        i = 0
        
        while i < len(self.vertices)-1:
            j = i+1
            while j < len(self.vertices):
                L = self.lswap(self.vertices[:], i, j)
                path = self.compute_path(L)
                self.best_in_tab(tab,-path,L)
                j+=1
            i+=1
        elem = random.choice(tab)
        self.vertices = elem[0]
        return elem[0]
    
    def swap_tabu(self, tabuList,stepList,step,length,limit):
        tab = [[[],float('inf')],[[],float('inf')],[[],float('inf')],[[],float('inf')],[[],float('inf')]]
        i = 0
        while i < len(self.vertices)-1:
            j = i+1
            while j < len(self.vertices):
                L = self.lswap(self.vertices[:], i, j)
                if L in tabuList :
                    elem = stepList[tabuList.index(L)] # recover the step when the tabu has been encoded
                    if step - elem >= length : # L no more longer tabu
                        path = self.compute_path(L)
                        self.best_in_tab(tab, -path, L)
                else:
                    path = self.compute_path(L)
                    self.best_in_tab(tab, -path, L)
                j+=1
            i+=1
        elem = random.choice(tab)
        tabuList.append(elem[0])
        stepList.append(step)
        self.vertices = elem[0]
        return elem[0]
                        
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
