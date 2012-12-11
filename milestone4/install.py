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


def get_clauses(rep, toinstall, full_list = []):
    clauses = []
    variables = []
    for package in toinstall:
        for pckg in package:
            variables += [pckg]
            (var, cl) = get_clauses(rep, pckg.depends, variables)
            for item in var:
                variables += item
                clauses += [depends(pckg, item)]
            for conflict in pckg.conflicts:
                if conflict in full_list + variables:
                    clauses += conflicts(pckg, conflict)
    return (variables, clauses)

            
    

if __name__ == "__main__":
    rep = Repository(sys.argv[1])
    toinstall = sys.argv[2:]
    tupletoinstall = []
    for pck in toinstall:
        tupletoinstall += [(pck)]
    (n, clauses) = get_clauses(rep, toinstall)
