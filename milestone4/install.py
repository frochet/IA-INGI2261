'''
Created on Dec 11, 2012

@author: inekar
'''
from packages import *
import sys

def depends(A, B):
    return (-A, B)
def conflicts(A, B):
    return (-A, -B)
def provides(A, B):
    return (-A, B)


def get_clauses(toinstall, full_list = []):
    clauses = []
    variables = []
    for package in toinstall:
        for pckg in package:
            if pckg not in variables + full_list :
                variables += [pckg]
                (var, cl) = get_clauses(pckg.depends, variables)
                for item in var:
                    if item not in variables + full_list:
                        variables += [item]
                        clauses += [depends(variables.index(pckg)+1, variables.index(item)+1)]
                for conflict in pckg.conflicts:
                    if conflict in variables + full_list :
                        clauses += [conflicts(variables.index(pckg)+1, variables.index(conflict)+1)]
                    else:
                        variables += [conflict]
                        clauses += [conflicts(variables.index(pckg)+1, variables.index(conflict)+1)]
    return (variables, clauses)

            
    

if __name__ == "__main__":
    rep = Repository(sys.argv[1])
    toinstall = sys.argv[2:]
    tupletoinstall = []
    for pck in toinstall:
        tupletoinstall += [(rep[pck],)]
    (n, clauses) = get_clauses(tupletoinstall)
    print((n,clauses))
