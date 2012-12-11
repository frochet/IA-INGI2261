'''

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
    
    print(-salesman.value(salesman.initial))
    
    start = time()
    result = simulated_annealing(salesman)
    stop = time()
    interval = stop-start
    print("Temps ecoule : ", format(interval)," seconde(s)")
    print(result.state.vertices)
    print("Cout : ",format(-result.problem.value(result.state)))
    print("step : ",format(result.step))