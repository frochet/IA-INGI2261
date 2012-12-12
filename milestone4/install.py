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
                indexes += variables.index(rootPackage)+1
                #add_clause(clauses,[provides(variables.index(rootPackage)+1, variables.index(item)+1)])
    addclause(clauses, [provides(variables.index(item)+1, indexes)])


def add_clause(clauses, aClause):
    if aClause not in clauses :
        clauses += aClause
    
def get_clauses(rep,toinstall, full_list = [], full_clause = []):
    clauses = full_clause
    variables = full_list
    for package in toinstall:
        for pckg in package:
            if pckg not in variables :
                variables += [pckg]
                (var, cl) = get_clauses(rep,pckg.depends, variables,clauses)
                for tuple in pckg.depends :
                    if(len(tuple) == 1):
                        if tuple[0] not in variables:
                            variables += [tuple[0]]
                        add_clause(clauses, [depends(variables.index(pckg)+1, variables.index(tuple[0])+1)])
                        look_if_is_provided_package(tuple[0],variables,clauses,rep)
                    else:
                        indexes = []
                        for item in tuple:
                            if item not in variables:
                                variables += item
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
    for pck in toinstall:
        tupletoinstall += [(rep[pck],)]
    (n, clauses) = get_clauses(rep,tupletoinstall)
    
#    for item in n :
#        print(item)
    print(clauses)
    print(len(n))
    
#    computation = minisat(len(n),clauses)
#    print(computation)