'''"
Created on 11 oct. 2012

@author: Florentin
'''
from IO import IO
from Case import *
import sys

class Board:
    
    '''
        Represent the static game board, with wall, goal and normal cases.
    '''


    def __init__(self, filename):
        """
            This constructor take the filename where the initial board representation is
            writting. It will make a representation in a matrix, containing Cases.
        """
        self.Io = IO(filename)
        self.Io.init_reader()
        self.board = []
        self.nbrGoal = 0
        self.nbrBox = 0
        for line in self.Io.file :
            boardLine = []
            for char in line :
                if char == "#" :
                    boardLine.append(Case.WALL)
                elif char == " " :
                    boardLine.append(Case.NORMAL)
                elif char == ".":
                    boardLine.append(Case.GOAL)
                    self.nbrGoal += 1
            self.board.append(boardLine)
        self.detect_dead_state()
        self.detect_possible_dead_state()
    
    def detect_possible_dead_state(self):
        """
            Those states occurs when we have a goal along a wall like that :
            p#
            g#
            p#
            p#
            p#
             all case marked with p are possible dead state, that means that if the goal
             g is filled with a box, all the p become dead state.
            The code is clearly illisible but the logic is simple, each time
            we find a goal, we look for wall side by side to it. if the goal
            is along some wall, some case will be marked as HPDS for row and
            VPDS for column. That means that those case are potentially dead
            state, if the number of boxes on those cases is more than the number
            of goal on those cases.
        """
        x = 2
        y = 2
        while y < len(self.board)-2 :
            while x < len(self.board[y])-2 :
                if self.board[y][x] == Case.GOAL :
                    # HANDLE HPDS ! #
                    left = True
                    right = True
                    i = x
                    while i < len(self.board[y])-2 and right:
                        if self.board[y-1][i] != Case.WALL : 
                            right = False
                        else:
                            i+=1
                    if x - i < 0 :
                        j = x
                        while j < i :
                            if self.board[y][j+1] != Case.WALL and self.board[y][j] == Case.NORMAL :
                                self.board[y][j] = Case.HPDS
                            j+=1
                    right = True
                    i = x
                    while i < len(self.board[y])-2 and right:
                        if self.board[y+1][i] != Case.WALL : 
                            right = False
                        else:
                            i+=1
                    if x - i < 0 :
                        j = x
                        while j < i :
                            if self.board[y][j+1] != Case.WALL and self.board[y][j] == Case.NORMAL :
                                self.board[y][j] = Case.HPDS
                            j+=1
                    i = x
                    while i > 2 and left :
                        if self.board[y-1][i] != Case.WALL :
                            left = False
                        else :
                            i-=1
                    if x - i > 0:
                        j = x
                        while j > i:
                            if self.board[y][j-1] != Case.WALL and self.board[y][j] == Case.NORMAL :
                                self.board[y][j] = Case.HPDS
                            j-=1
                    left = True
                    i = x
                    while i > 2 and left :
                        if self.board[y+1][i] != Case.WALL :
                            left = False
                        else :
                            i-=1
                    if x - i > 0:
                        j = x
                        while j > i:
                            if self.board[y][j-1] != Case.WALL and self.board[y][j] == Case.NORMAL :
                                self.board[y][j] = Case.HPDS
                            j-=1
                    # HANDLE VPDS
                    up = True
                    down = True
                    i = y
                    while i < len(self.board)-2 and down :
                        if self.board[i][x-1] != Case.WALL :
                            down = False
                        i+=1
                    if y - i < 0 :
                        j = x
                        while j < i :
                            if self.board[j+1][x] != Case.WALL and self.board[j][x] == Case.NORMAL:
                                self.board[j][x] = Case.VPDS
                            j+=1
                    i = y
                    while i > 2 and up:
                        if self.board[i][x-1]!= Case.WALL:
                            up = False
                        i-=1
                    if y - i > 0:
                        j = y
                        while j > i :
                            if self.board[j-1][x] != Case.WALL and self.board[j][x] == Case.NORMAL:
                                self.board[j][x] = Case.VPDS
                            j-=1
                    up = True
                    down = True
                    i = y
                    while i < len(self.board)-2 and down :
                        if self.board[i][x+1] != Case.WALL :
                            down = False
                        i+=1
                    if y - i < 0 :
                        j = x
                        while j < i :
                            if self.board[j+1][x] != Case.WALL and self.board[j][x] == Case.NORMAL:
                                self.board[j][x] = Case.VPDS
                            j+=1
                    i = y
                    while i > 2 and up:
                        if self.board[i][x+1]!= Case.WALL:
                            up = False
                        i-=1
                    if y - i > 0:
                        j = y
                        while j > i :
                            if self.board[j-1][x] != Case.WALL and self.board[j][x] == Case.NORMAL:
                                self.board[j][x] = Case.VPDS
                            j-=1
                x+=1
            x=0
            y+=1
        
    def detect_dead_state(self):
        x = 0
        y = 0
        while y < len(self.board) :
            while x < len(self.board[y]):
                if self.board[y][x] == Case.WALL :
                    if (y > 0 and y < (len(self.board)-1)) and (x > 0 and x < len(self.board[y])-1):
                        # On a case not at the edges
                        if self.board[y-1][x] == Case.WALL and self.board[y][x+1]== Case.WALL :
                            # this kind of configuration : #x
                            #                              ##
                            # x for dead_state
                            if self.board[y-1][x+1] == Case.NORMAL :
                                self.board[y-1][x+1] = Case.STATIC_DEAD_STATE
                        if self.board[y+1][x] == Case.WALL and self.board[y][x+1]== Case.WALL :
                            # this kind of configuration : ##
                            #                              #x
                            # x for dead_state
                            if self.board[y+1][x+1] == Case.NORMAL :
                                self.board[y+1][x+1] = Case.STATIC_DEAD_STATE
                        if self.board[y+1][x] == Case.WALL and self.board[y][x-1]== Case.WALL :
                            # this kind of configuration : ##
                            #                              x#
                            # x for dead_state
                            if self.board[y+1][x-1] == Case.NORMAL :
                                self.board[y+1][x-1] = Case.STATIC_DEAD_STATE
                        if self.board[y-1][x] == Case.WALL and self.board[y][x-1]== Case.WALL :
                            # this kind of configuration : x#
                            #                              ##
                            # x for dead_state
                            if self.board[y-1][x-1] == Case.NORMAL:
                                self.board[y-1][x-1] = Case.STATIC_DEAD_STATE
                    # On cases at the edges !
                    elif y == 0 and ( x>0 and x < len(self.board[y])-1):
                        if self.board[y+1][x] == Case.NORMAL:
                            hasAGoal = False
                            for elem in self.board[y+1] :
                                if elem == Case.GOAL : hasAGoal = True
                            if  hasAGoal :
                                if self.board[y+1][x+1] == Case.WALL or self.board[y+1][x-1] == Case.WALL :
                                    self.board[y+1][x] = Case.STATIC_DEAD_STATE
                                else :
                                    self.board[y+1][x] = Case.HPDS
                            else :
                                self.board[y+1][x] = Case.STATIC_DEAD_STATE 
                    # On cases at the edges
                    elif y == len(self.board)-1 and ( x >0 and x < len(self.board[y])-1):
                        if self.board[y-1][x] == Case.NORMAL:
                            hasAGoal = False
                            for elem in self.board[y-1] :
                                if elem == Case.GOAL : hasAGoal = True
                            if hasAGoal :
                                if self.board[y-1][x+1] == Case.WALL or self.board[y-1][x-1] == Case.WALL:
                                    self.board[y-1][x] = Case.STATIC_DEAD_STATE
                                else :
                                    self.board[y-1][x] = Case.HPDS
                            else :
                                self.board[y-1][x] = Case.STATIC_DEAD_STATE
                    # on cases at the edges
                    elif (y>0 and y < len(self.board)-1) and x == 0 :
                        if self.board[y][x+1] == Case.NORMAL:
                            hasAGoal = False
                            i = 0
                            while i < len(self.board) :
                                if self.board[i][x+1] == Case.GOAL : hasAGoal = True
                                i+=1
                            if hasAGoal :
                                if self.board[y-1][x+1] == Case.WALL or self.board[y+1][x+1] == Case.WALL:
                                    self.board[y][x+1] = Case.STATIC_DEAD_STATE
                                else:
                                    self.board[y][x+1] = Case.VPDS
                            else :
                                self.board[y][x+1] = Case.STATIC_DEAD_STATE
                    elif (y>0 and y < len(self.board)-1) and x == len(self.board[0])-1 :
                        if self.board[y][x-1] == Case.NORMAL:
                            hasAGoal = False
                            i = 0
                            while i < len(self.board) :
                                if self.board[i][x-1] == Case.GOAL : hasAGoal = True
                                i+=1
                            if hasAGoal :
                                if self.board[y-1][x-1] == Case.WALL or self.board[y+1][x-1] == Case.WALL:
                                    self.board[y][x-1] = Case.STATIC_DEAD_STATE
                                else:
                                    self.board[y][x-1] = Case.VPDS
                            else :
                                self.board[y][x-1] = Case.STATIC_DEAD_STATE
                    elif x == 0 and y == 0 :
                        if self.board[y][x+1] == Case.WALL and self.board[y+1][x]==Case.WALL :
                            if self.board[y+1][x+1] == Case.NORMAL :
                                self.board[y+1][x+1] = Case.STATIC_DEAD_STATE
                    elif x == 0 and y == len(self.board)-1 :
                        if self.board[y][x+1] == Case.WALL and self.board[y-1][x]==Case.WALL :
                            if self.board[y-1][x+1] == Case.NORMAL :
                                self.board[y-1][x+1] = Case.STATIC_DEAD_STATE
                    elif x == len(self.board[0])-1 and y == 0 :
                        if self.board[y+1][x] == Case.WALL and self.board[y][x-1]==Case.WALL :
                            if self.board[y+1][x-1] == Case.NORMAL :
                                self.board[y+1][x-1] = Case.STATIC_DEAD_STATE
                    elif x == len(self.board[0])-1 and y == len(self.board)-1 :
                        if self.board[y-1][x] == Case.WALL and self.board[y][x-1]==Case.WALL :
                            if self.board[y-1][x-1] == Case.NORMAL :
                                self.board[y-1][x-1] = Case.STATIC_DEAD_STATE
                x+=1   
            x=0
            y+=1
        
                
    def print_board(self):
        for line in self.board :
            for char in line :
                sys.stdout.write(str(char))
            print("\n")
    
    def getUp(self,x,y):
        assert y > 0 and y < len(self.board)
        assert x >= 0 and x < len(self.board[y])
        return self.board[y-1][x]
        
    def getRight(self,x,y):
        assert y >= 0 and y < len(self.board)
        assert x < len(self.board[y]-1) and x >= 0
        return self.board[y][x+1]
 
    def getLeft(self,x,y):
        assert y >= 0 and y < len(self.board)
        assert x > 0 and x < len(self.board[y]-1)
        return self.board[y][x-1]
    
    def getDown(self,x,y):
        assert y >= 0 and y < len(self.board-1)
        assert x >= 0 and x < len(self.board[y])
        return self.board[y-1][x]


# TEST 
    
if __name__ == "__main__" :
    plateau = Board("../benchs/sokoInst10.goal")
    plateau.print_board()
                    