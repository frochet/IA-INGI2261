'''
Created on 28 nov. 2012

@author: Florentin
'''
from search import *
from state import *
from parserCity import *
from GreedySearch import *
from time import time
from salesman import *

def max_value(problem):
    current = LSNode(problem,salesman.initial,0)
    best = current
    listofval = []
    for step in range(100) :
        #########
        listofval += [-current.value()]
        #########
        for elem in current.expand() :
            if elem.value() > best.value() :
                best = elem
                current = elem
    print(listofval)
    return best

if __name__ == "__main__":
    
    parser = Parser(sys.argv[1])
    matrice = parser.parse_line()
    N = matrice[0][0]
    initial = Greedy(N,matrice[1:], 1)   
    salesman = TravellingSalesman(initial,matrice[1:])
    #print(initial)
    start = time()
    #print(-salesman.value(salesman.initial))
    best = max_value(salesman)

    stop = time()
    #print("temps ecoule :",format(stop-start), " seconde(s)")
    #print(-best.problem.value(best.state))
    #print(best.state.vertices)
    #print("step when best solution reached : ",format(best.step))
#    print(format(stop-start))
#    print(format(-best.problem.value(best.state)))
#    print(format(best.step))
    
    print(-best.value()) 
