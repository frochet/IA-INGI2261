'''
Created on 1 dec. 2012

@author: Florentin
'''

from search import *
from state import *
from parserCity import *
from GreedySearch import *
from time import time
from salesman import *
   
def tabu_search(problem, length, limit):
    current = LSNode(problem,problem.initial,0)
    best = current
    tabuList = [[],[]]
    listofval = []
    for step in range(limit):
        listofval += [-current.value()]
        tab = [[best,float('inf')],[best,float('inf')],[best,float('inf')],[best,float('inf')],[best,float('inf')]]
        problem.step = step
        for current in current.expand() :
            if current in tabuList[0] :
                tabuPos = tabuList[0].index(current)
                if step - tabuList[1][tabuPos] > length :
                    best_in_tab(tab,-current.value(),current)
                    tabuList[0].remove(current)
                    tabuList[1].remove(tabuPos)
            else :
                best_in_tab(tab,-current.value(),current)
        elem = random.choice(tab)
        current = elem[0]
        tabuList[0].append(current)
        tabuList[1].append(step)
        if current.value() > best.value() :
            best = current
    return [best,listofval]


if __name__ == "__main__":
    parser = Parser(sys.argv[1])
    length = int(sys.argv[2])
    limit = int(sys.argv[3])
    matrice = parser.parse_line()
    N = matrice[0][0]
    initial = Greedy(N,matrice[1:], 1)
    salesman = TravellingSalesman(initial,matrice[1:])
    #print(-salesman.value(salesman.initial))
    
    start = time()
    tabu_result = tabu_search(salesman,length,limit)
    result = tabu_result[0]
    listofval = tabu_result[1]
    stop = time()
    interval = stop-start
#    print(listofval)
    print("Temps ecoule : ", format(interval)," seconde(s)")
    print(result.state.vertices)
    print("Cout : ",format(-result.problem.value(result.state)))
    print("step : ",format(result.step))
#    print(format(interval))
#    print(format(-result.problem.value(result.state)))
#    print(format(result.step))
    
    