'''
Created on 29 nov. 2012

@author: Florentin
'''
from search import *
from state import *
from parserCity import *
from GreedySearch import *
from time import time
from salesman import *

if __name__ == "__main__":
    
    parser = Parser(sys.argv[1])
    matrice = parser.parse_line()
    N = matrice[0][0]
    initial = Greedy(N,matrice[1:], 1)   
    salesman = TravellingSalesman(initial,matrice[1:])
    print(initial)
    print(-salesman.value(salesman.initial))
    start = time()
    current = LSNode(salesman,salesman.initial,0)
    best = current
    listofval = []
    for step in range(100) :
        tab = [[best,float('inf')],[best,float('inf')],[best,float('inf')],[best,float('inf')],[best,float('inf')]]
        #########
        listofval += [-current.value()]
        #########
        for current in current.expand() :
            best_in_tab(tab,-current.value(),current)
        elem = random.choice(tab)
        current = elem[0]
        if current.value() > best.value():
            best = current
    stop = time()
    #print(listofval)
    print("elapsed time :",format(stop-start), " second(s)")
    print(-best.problem.value(best.state))
    print(best.state.vertices)
    print("step when best solution reached : ",format(best.step))
    
    #print(format(stop-start))
    #print(-best.problem.value(best.state))
    #print(format(best.step)) 
    #print(-best.value())
    #print(listofval) 
