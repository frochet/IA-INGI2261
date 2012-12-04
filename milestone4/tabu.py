'''
Created on 1 dec. 2012

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
        self.length = 0 #init
        self.limit = 0 #init
        self.step = 0 #init
        self.tabuList = []
        self.stepList = []
        
    def successor(self, state):
        yield (None, State(self.initial.swap_tabu(self.tabuList,self.stepList,self.step,self.length,self.limit),self.matrice))
    def value(self,state):
        """Compute the path value"""
        return state.compute_path(state.vertices)

def tabu_search(problem, length, limit):
    problem.length = length
    problem.limit = limit
    current = LSNode(problem,problem.initial,0)
    best = current
    for step in range(limit) :
        problem.step = step
        list = current.expand()
        for current in list :
            if current.value() > best.value() :
                best = current
    return best

if __name__ == "__main__":
    parser = Parser(sys.argv[1])
    length = int(sys.argv[2])
    limit = int(sys.argv[3])
    matrice = parser.parse_line()
    N = matrice[0][0]
    initial = Greedy(N,matrice[1:], 1)
    salesman = TravelingSalesman(initial,matrice[1:])
    print(-salesman.value(salesman.initial))
    
    start = time()
    result = tabu_search(salesman,length,limit)
    stop = time()
    interval = stop-start
    print("Temps ecoule : ", format(interval)," seconde(s)")
    print(result.state.vertices)
    print("Cout : ",format(-result.problem.value(result.state)))
    print("step : ",format(result.step))
    
    