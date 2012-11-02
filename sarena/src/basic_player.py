#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

from sarena import *
import minimax


class AlphaBetaPlayer(Player, minimax.Game):

    """Sarena Player.

    A state is a tuple (b, p) where p is the player to make a move and b
    the board.

    """

    def successors(self, state):
        board, player = state 
        for action in board.get_actions():
            yield (action,(board.clone().play_action(action), -player))

    def cutoff(self, state, depth):
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
        return minimax.search(state, self)


if __name__ == "__main__":
    player_main(AlphaBetaPlayer())