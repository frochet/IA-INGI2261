'''
Created on Dec 4, 2012

@author: inekar
'''
result = [[1,2,3],
          [1,2,3],
          [1,2,3]
        ]
mean = []
for i in range(len(result[0])):
    item = 0
    for j in range(3):
        item += result[j][i]
    mean += [item]
    
print(mean)