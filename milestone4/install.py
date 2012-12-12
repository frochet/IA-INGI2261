'''
Created on Dec 11, 2012

@author: inekar
'''
from packages import *
import sys
from minisat import *

def depends(A, B):
    return (-A, B)
def conflicts(A, B):
    return (-A, -B)
def provides(A, B):
    return (-A, B)

def look_if_is_provided_package(item,variables,clauses,rep):
    for rootPackage in rep.packages :
        for provided in rootPackage.provides:
            if item == provided :
                get_clauses(rep, [(rootPackage,)],variables,clauses)
                clauses += [provides(variables.index(rootPackage)+1, variables.index(item)+1)]

def get_clauses(rep,toinstall, full_list = [], full_clause = []):
    clauses = full_clause
    variables = full_list
    for package in toinstall:
        for pckg in package:
            if pckg not in variables :
                variables += [pckg]
                (var, cl) = get_clauses(rep,pckg.depends, variables,clauses)
                for tuple in pckg.depends :
                    for item in tuple :
                        clauses += [depends(variables.index(pckg)+1, variables.index(item)+1)]                
                        # +  look if item is a provided package
                        look_if_is_provided_package(item,variables,clauses,rep)
                        ##() = get_clauses(rep,packageToAddToInstallation,variables)
                        #toinstall+=[(packageToAddToInstallation,)]
                        #clauses += [provides(variables.index(item)+1,variables.index(packageToAddToInstallation)+1)]
                for conflict in pckg.conflicts:
                    if conflict in variables :
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
    (n, clauses) = get_clauses(rep,tupletoinstall)
    
    print((n,clauses))
