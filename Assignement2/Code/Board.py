'''"
Created on 11 oct. 2012

@author: Debroux Léonard, Rochet Florentin
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
        self.positionGoal = []
        i = 0
        j = 0
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
                    self.positionGoal.append([i,j])
                j+=1
            j=0
            i+=1
            self.board.append(boardLine)
        self.detect_dead_state()
        self.detect_possible_dead_state()
    
    
    def detect_possible_dead_state(self):
        """
            In our board, we might have some possible dead state which 
            are configuration like :
            #######
            #  .  #
            on the goal line, there are pure dead state on the corners and
            possible dead state on the cases on the line. That means that if
            a box is push on that line, all the others case are transformed to 
            dead state.
        """
        def detect_bound_on_raw(y, goalX):
            left = False
            right = False
            i = goalX    
            while (self.board[y-1][i] == Case.WALL or self.board[y+1][i] == Case.WALL) and not right :
                if self.board[y][i+1] == Case.WALL :
                    right = True
                i+=1                
            if not right :
                return False
            r = i-1
            i = goalX
            while (self.board[y-1][i] == Case.WALL or self.board[y+1][i] == Case.WALL) and not left :
                if self.board[y][i-1] == Case.WALL :
                    left = True
                i-=1
            if not left :
                return False
            l = i+1
            return [l,r]
        def detect_bound_on_col(goalY,x):
            up = False
            down = False
            i = goalY
            while(self.board[i][x+1] == Case.WALL or self.board[i][x-1] == Case.WALL) and not up :
                if self.board[i-1][x] == Case.WALL :
                    up = True
                i-=1
            if not up :
                return False
            u = i+1
            i = goalY
            while(self.board[i][x+1] == Case.WALL or self.board[i][x-1] == Case.WALL) and not down :
                if self.board[i+1][x] == Case.WALL :
                    down = True
                i+=1
            if not down :
                return False
            d = i-1
            return [u,d]
        
        
        x = 2
        y = 2
        while y < len(self.board)-2 :
            while x < len(self.board[y])-2 :
                if self.board[y][x] == Case.GOAL :
                    coord = detect_bound_on_raw(y,x)
                    if coord :
                        # on va placer des HPDS entre les elements r,l compris.
                        i = coord[0]
                        while i < coord[1] :
                            if self.board[y][i] == Case.NORMAL :
                                self.board[y][i] = Case.HPDS
                            i+=1
                    coord = detect_bound_on_col(y,x)
                    if coord :
                        i = coord[0]
                        while i < coord[1] :
                            if self.board[i][x] == Case.NORMAL :
                                self.board[i][x] = Case.VPDS
                            i+=1
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
                                right = False
                                left  = False
                                i = x
                                while self.board[y+1][i+1] != Case.WALL :
                                    if self.board[y+1][i+1] == Case.GOAL : right = True
                                    i+=1
                                i=x
                                while self.board[y+1][i-1] != Case.WALL :
                                    if self.board[y+1][i-1] == Case.GOAL : left = True
                                    i-=1
                                if right or left :
                                    self.board[y+1][x] = Case.HPDS
                                else : self.board[y+1][x] = Case.STATIC_DEAD_STATE
                            else :
                                self.board[y+1][x] = Case.STATIC_DEAD_STATE 
                    # On cases at the edges
                    elif y == len(self.board)-1 and ( x >0 and x < len(self.board[y])-1):
                        if self.board[y-1][x] == Case.NORMAL:
                            hasAGoal = False
                            if Case.GOAL in self.board[y-1] :
                                hasAGoal = True
                            if hasAGoal :
                                # si on trouve un mur dans les deux direction, sans goal alors c'est un
                                # static dead state
                                right = False
                                left  = False
                                i = x
                                while self.board[y-1][i+1] != Case.WALL :
                                    if self.board[y-1][i+1] == Case.GOAL : right = True
                                    i+=1
                                i=x
                                while self.board[y-1][i-1] != Case.WALL :
                                    if self.board[y-1][i-1] == Case.GOAL : left = True
                                    i-=1
                                if right or left :
                                    self.board[y-1][x] = Case.HPDS
                                else : self.board[y-1][x] = Case.STATIC_DEAD_STATE
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
                                up = False
                                down  = False
                                i = y
                                while self.board[i+1][x+1] != Case.WALL :
                                    if self.board[i+1][x+1] == Case.GOAL : down = True
                                    i+=1
                                i=y
                                while self.board[i-1][x+1] != Case.WALL :
                                    if self.board[i-1][x+1] == Case.GOAL : up = True
                                    i-=1
                                if down or up :
                                    self.board[y][x+1] = Case.HPDS
                                else : self.board[y][x+1] = Case.STATIC_DEAD_STATE
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
                                up = False
                                down  = False
                                i = y
                                while self.board[i+1][x-1] != Case.WALL :
                                    if self.board[i+1][x-1] == Case.GOAL : down = True
                                    i+=1
                                i = y
                                while self.board[i-1][x-1] != Case.WALL :
                                    if self.board[i-1][x-1] == Case.GOAL : up = True
                                    i-=1
                                if down or up :
                                    self.board[y][x-1] = Case.HPDS
                                else : self.board[y][x-1] = Case.STATIC_DEAD_STATE
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
        
     
    def print_board(self,char,boxes):
        y = 0
        x = 0
        for line in self.board :
            for elem in line :
                special = False
                for box in boxes :
                    if box.x == x and box.y == y:
                        sys.stdout.write("$")
                        special = True
                if char.x == x and char.y == y :
                    sys.stdout.write("@")
                    special = True
                if not special :
                    if elem == Case.GOAL : sys.stdout.write(" ")
                    elif elem == Case.WALL : sys.stdout.write("#")
                    else: sys.stdout.write(" ")
                x+=1
            sys.stdout.write("\n")
            x=0
            y+=1
    def print_board_repr(self):
        """print the board with our case representation (see module Case)"""
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
                    