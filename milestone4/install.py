'''
Created on Dec 11, 2012

@author: inekar
'''
from packages import *
import sys
from minisat import *


def depends(A, B):
    return (-A, B)
def depends_on_or(A, B):
    ''' B is a list of indexes of or dependencies for A
    '''
    result = (-A, )
    for pckg in B:
        result += (pckg, )
    return result
def conflicts(A, B):
    return (-A, -B)
def provides(A, B):
    '''B is a list of indexes of providers for A
    '''
    result = (-A, )
    for pckg in B:
        result += (pckg, )
    return result

def look_if_is_provided_package(item,variables,clauses,rep):
    indexes = []
    for rootPackage in rep.packages :
        for provided in rootPackage.provides:
            if item == provided :
                get_clauses(rep, [(rootPackage,)],variables,clauses)
                indexes += [variables.index(rootPackage)+1]
                #add_clause(clauses,[provides(variables.index(rootPackage)+1, variables.index(item)+1)])
    if indexes:
        add_clause(clauses, [provides(variables.index(item)+1, indexes)])


def add_clause(clauses, aClause):
    if aClause not in clauses :
        clauses += aClause
    
def get_clauses(rep, toinstall, full_list = [], full_clause = [], init = False):
    clauses = full_clause
    variables = full_list
    for package in toinstall:
        for pckg in package:
            if pckg not in variables :
                variables += [pckg]
                if init:
                    clauses += [(variables.index(pckg)+1, )]
                (var, cl) = get_clauses(rep,pckg.depends, variables,clauses)
                for tuple in pckg.depends :
                    indexes = []
                    for item in tuple:
                        if item not in variables:
                            variables += [item]
                        indexes += [variables.index(item)+1]
                        look_if_is_provided_package(item,variables,clauses,rep)
                    add_clause(clauses, [depends_on_or(variables.index(pckg)+1, indexes)])
                        
                for conflict in pckg.conflicts:
                    if conflict in variables :
                        add_clause(clauses, [conflicts(variables.index(pckg)+1, variables.index(conflict)+1)])
                    else:
                        variables += [conflict]
                        add_clause(clauses,[conflicts(variables.index(pckg)+1, variables.index(conflict)+1)])
               
    return (variables, clauses)

            
    

if __name__ == "__main__":
    rep = Repository(sys.argv[1])
    toinstall = sys.argv[2:]
    tupletoinstall = []
#    variables = []
#    clauses = []
    for pck in toinstall:
#        variables += [pck]
#        clauses += [(variables.index(pck)+1,)]
        tupletoinstall += [(rep[pck],)]
    (n, clauses) = get_clauses(rep, tupletoinstall, init = True)
    
#    for item in n :
#        print(item)
    print(clauses)
    print(len(n))
    
    computation = minisat(len(n),clauses)
    print(computation)
    for indice in computation :
        print(n[indice-1])