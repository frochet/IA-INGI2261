'''
Created on Nov 13, 2012

@author: inekar
'''
from sarena import Board, random_board
from random_player import RandomPlayer
from game import play_game


def merge(l1, l2):
    result = []
    for i in range(len(l1) - 1):
        result += [l1[i]]
        result += [l2[i]]
    result += [l1[i+1]]
    if len(l2) == len(l1):
        result += [l2[i+1]]
    return result


sumlist=[]


for i in range(100):

    board = Board(percepts = random_board())
    
    p0 = RandomPlayer()
    p1 = RandomPlayer()
    
    play_game((p0, p1), board)
    
    #print(p0.listoflen)
    #print(p1.listoflen)
    
    mergelist = merge(p0.listoflen, p1.listoflen)
    
    #print(mergelist)
    for j in range(len(mergelist)):
        if j < len(sumlist):
            sumlist[j] += mergelist[j]
        else:
            sumlist += [mergelist[j]]
            
    #print (sumlist)

for i in range(len(sumlist)):
    sumlist[i] = sumlist[i]/100
    
print(sumlist)