#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

from sarena import *
import minimax
import time


class AlphaBetaPlayer(Player, minimax.Game):

    """Sarena Player.

    A state is a tuple (b, p) where p is the player to make a move and b
    the board.

    """
    count = 0
    depthCount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    start = time.time()
    
    def successors(self, state):
        board, player = state 
        for action in board.get_actions():
            yield (action,(board.clone().play_action(action), -player))

    def cutoff(self, state, depth):
        self.depthCount[depth] += 1
        self.count += 1
        if self.count % 1000000 == 0:
            print("% noeud totaux", self.count)
            print("% par depth", self.depthCount)
            print("% secondes", time.time()-self.start)
        board, player = state
        return board.is_finished()

    def evaluate(self, state):
        board, player = state
        score = board.get_score()
        if player == 1 :
            if score > 0 :
                return 1
            elif score < 0:
                return -1
            else: return 0
        else:
            if score > 0 :
                return -1
            elif score < 0 :
                return 1
            else: return 0

    def play(self, percepts, step, time_left):
        if step % 2 == 0:
            player = -1
        else:
            player = 1
        state = (Board(percepts), player)
        m = minimax.search(state, self, False)

        print("nombre de noeuds explorés : ", self.count)
        print("nombre de noeuds explorés par depth : ", self.depthCount)
        self.count = 0
        depthCount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        print("temps elapsed : ", format(time.time()-self.start))
        return m


if __name__ == "__main__":
    player_main(AlphaBetaPlayer())
