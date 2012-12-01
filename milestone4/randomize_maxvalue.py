'''
Created on 29 nov. 2012

@author: Florentin
'''
from search import *
from state import *
from parserCity import *
from GreedySearch import *
from time import time

class TravelingSalesman(Problem):
   
    def __init__(self, initial,matrice,goal=None):
        self.matrice = matrice
        self.initial = State(initial,self.matrice)
    def successor(self, state):
        yield (None, State(self.initial.swap_random_from_bests(5),self.matrice))
    def value(self,state):
        """Compute the path value"""
        return state.compute_path()

if __name__ == "__main__":
    
    parser = Parser(sys.argv[1])
    matrice = parser.parse_line()
    N = matrice[0][0]
    initial = Greedy(N,matrice[1:], 1)   
    salesman = TravelingSalesman(initial,matrice[1:])
    print(initial)
    print(-salesman.value(salesman.initial))
    start = time()
    current = LSNode(salesman,salesman.initial,0)
    best = current
    for step in range(100) :
        list = current.expand()
        for current in list :
            if current.value() > best.value() :
                best = current
    stop = time()
    print("temps ecoule :",format(stop-start), " seconde(s)")
    print(-best.problem.value(best.state))
    print(best.state.vertices)