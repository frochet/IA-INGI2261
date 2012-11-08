'''
Created on 8 nov. 2012

@author: Florentin
'''
class Color :
    Color.YELLOW = 1
    Color.RED = -1


class Action(object):
    '''
    classdocs
    '''
    


    def __init__(self,tower_init,tower_target,color,**kwords):
        '''    
             tower_init : initial tower from the move goes to the tower target
             tower_target : tower targeted by a move.
             color : Color of the player executing the next action
             **kwords is used to extend an Action to a must complex pattern.
             
             See board representation to pass the correct format for towers.
        '''
        self.t_init = tower_init
        self.t_target = tower_target
        self.size_t_init = len(self.t_init)
        self.size_t_target = len(self.t_target)
        self.color = color
        if self.color == Color.YELLOW :
            self.enemy_color = Color.RED
        else : self.enemy_color = Color.YELLOW
        self.kwords = kwords
        self.t_init.pop(0)
        self.final_tower = self.t_target.append(self.t_init) 
        self.weight = self._compute_weight()
        self.representation = hash(self.final_tower.append(self.weight))
        if 'sub_board' in kwords :
            pass # analyse a pattern
        # define the representation TODO
    
    def __eq__(self,other):
        return self.representation == other.representation
    
    def __hash__(self):
        return self.representation
    
    def _detect_sandwich(self):
            if self.t_init[self.size_t_init-2][0] == self.enemy_color and self.t_target[self.size_t_target][1] == self.enemy_color :
                if self.size_t_init == 2 and self.size_t_target == 2 : # one coin each towers
                    self.weight = 1
                    return True
                elif self.size_t_init == 3 and self.size_t_target == 3 : # two coins on each towers
                    self.weight = 3
                    return True
                elif self.size_t_init == 2 and self.size_t_target == 3 :
                    self.weight = 2
                    return True
                elif self.size_t_init == 3 and self.size_t_target == 2 :
                    self.weight = 2 
                    return True
                elif self.size_t_init == 4 and self.size_t_target == 2 :
                    self.weight = 3
                    return True
                elif self.size_t_init == 2 and self.size_t_target == 4 :
                    self.weight = 3
                    return True
            return False
             
    def _compute_weight(self):
        self.weight = 0
           
        if 'sub_borad' in self.kwords :
            pass
        #basic action
        else :
            #detect sandwich
            if self._detect_sandwich() :
                return self.weight
            else :
                pass
                    
    def is_a_pattern(self,dico):
        return dico[self.representation]
        
