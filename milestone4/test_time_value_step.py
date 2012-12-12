'''
Created on Dec 4, 2012

@author: inekar
'''


file = open("test_result_tabu", mode='r')
state = 0
time = 0
value = 0
step = 0

#file.readline()

for line in file:
    #print(line)
    #if line is not "Break":
    #print(state)
    if state < (3*5):
        if state%3 == 0:
            time += float(line)
        elif state%3 == 1:
            value += float(line)
        elif state%3 == 2:
            step += float(line)
        state += 1
    else:
        amount = float(state) / 3
        time = time / amount
        value = value / amount
        step = step / amount
        
        print(time," ", value," ", step)
        #print(value)
        #print(step)
        print(" ")
        
        state = 0
        time = 0
        value = 0
        step = 0
#    else:
#        amount = state / 4
#        time = time / amount
#        value = value / amount
#        step = step / amount
#        
#        print(time)
#        print(value)
#        print(step)
#        print(" ")
#        
#        state = 0
#        time = 0
#        value = 0
#        step = 0
        

#result = [[1,2,3],
#          [1,2,3],
#          [1,2,3]
#        ]
#mean = []
#for i in range(len(result[0])):
#    item = 0
#    for j in range(3):
#        item += result[j][i]
#    mean += [item]
    
#print(time)
#print(value)
#print(step)