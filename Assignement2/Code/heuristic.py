'''
Created on 16 oct. 2012

@author: Florentin
'''
import math

def make_combi(goals,size):
    i = 0;j = 0
    listCombi = []
    while i < math.factorial(size):
        swapper(goals,j,j+1)
        listCombi.extend(goals)
        j+=1
        if j == size-1:
            j=0
        i+=1
    return listCombi
def swapper(list,i,j):
        elem1 = list.pop(i)
        elem2 = list.pop(j-1)
        list.insert(i, elem2)
        list.insert(j,elem1)
        