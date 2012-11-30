'''
Created on Nov 28, 2012

@author: inekar
'''            
    
        
def Greedy(N, Dist, city):   
    result = []
    NotExplored = []
    city -= 1
    for i in range(N):
        NotExplored += [i]     
    while NotExplored:
        NotExplored.remove(city)
        best = float('inf')
        succ = None
        for nextCity in NotExplored:
            if nextCity > city:
                if Dist[nextCity][city] < best:
                    best = Dist[nextCity][city]
                    succ = nextCity
            else:
                if Dist[city][nextCity] < best:
                    best = Dist[city][nextCity]
                    succ = nextCity
        result += [city+1]
        city = succ
    return result


if __name__ == "__main__":
    
    D = [[0], [30, 0], [7, 22, 0], [18, 9, 16]]
    initial = 3 # to be found with greedy method, leowlo-lo
    N = 4
    result = Greedy(N, D, initial)
    
    
    print(result)
    
        