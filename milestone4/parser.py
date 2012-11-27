'''
Created on 27 nov. 2012

@author: Florentin
'''

from IO import *

class Parser(object):
    '''
    classdocs
    '''


    def __init__(self,filename):
        
        '''
        Constructor
        '''
        self.io = IO(filename);
    
    def parse_line(self,separator):
        
        matrice = []
        self.io.init_reader()
        for line in self.io.file :
            if separator != None :
                matrice += line.split(separator)
        return matrice
        