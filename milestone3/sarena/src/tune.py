#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import shutil
from subprocess import *
import time

class Tune:

    cur_var = 0

    def load_vars():
        """load vars from file"""
        tuned_vars = {}

        load_file = open("tuned_vars.txt","r+")
        vars_string = load_file.read().split("\n")

        player = int(vars_string.pop(0))

        current_var = Tune.cur_var
        for var in vars_string:
            if not var or var[0] == '#': # comment
                continue
            key_value = var.split("=")
            
            if current_var == 0:
                tuned_vars[key_value[0]] = float(key_value[1+player])
            else:
                tuned_vars[key_value[0]] = float(key_value[1])
            current_var-=1
        load_file.close()
        return tuned_vars

    def update_vars(winner, cur_var):
        """update vars in function of the winner

        winner = 0 if yellow, 1 if red
        """
        if winner != 0 and winner != 1:
            return

        load_file = open("tuned_vars.txt","r")
        update_file = open("tuned_vars.txt.tmp","w")
        for line in load_file:
            if line == "1\n" or line == "0\n": # player
                update_file.write(line)
                continue
            elif line == "\n" or line[0] == "#": # comment
                update_file.write(line)
                continue
            elif cur_var != 0: # not the good var
                cur_var -= 1
                update_file.write(line)
                continue
            else:
                var = line.split("=")
                var[1] = float(var[1])
                var[2] = float(var[2])
                if winner == 0:
                    var[1] = var[1] + (var[2]-var[1])/4
                else:
                    var[2] = var[2] - (var[2]-var[1])/4
                output_var = str(var[0])+"="+str(var[1])+"="+str(var[2])+"\n"
                update_file.write(output_var)
        load_file.close()
        update_file.close()
        shutil.copyfile("tuned_vars.txt.tmp", "tuned_vars.txt")


    def set_next_player(p = -1):
        """set the next player p to load vars

        p :
        -1 the next
        1 force the player red
        0 force the player yellow"""
        with open("tuned_vars.txt","r+") as update_file:
            player = int(update_file.read()[0])
            update_file.seek(0,0)
            if player == -1:
                update_file.write(str((player+1)%2))
            else:
                update_file.write(str((player+1)%2))

    def play_and_response(adress1, adress2):
        """play a game

        return : "yellow" or "red" or "draw"
        """
        out = check_output(["python3","game.py","--no-gui","-t 1200" ,"http://localhost:8000","http://localhost:8100"], universal_newlines=True)
        if "Red" in out:
            return "red"
        if "Yellow" in out:
            return "yellow"
        if "Draw" in out:
            return "draw"

    def tune_game():
        nb_vars = len(Tune.load_vars())
        while True:
            yellow_win = 0
            red_win = 0
            for i in list(range(0,5)):
                time.sleep(5) # wait for OS liberate port
                Tune.set_next_player(0)
                yellow_player = Popen(["python3","super_player.py","-p",str(8000)])
                time.sleep(5) # wait for OS liberate port
                Tune.set_next_player(1)
                red_player = Popen(["python3","super_player.py","-p",str(8100)])
                time.sleep(5) # wait for OS liberate port
                win = Tune.play_and_response("http://localhost:"+str(8000),"http://localhost:"+str(8100))
                print("\n\n\n"+win+"\n\n\n")
                yellow_player.send_signal(CTRL_C_EVENT)
                red_player.send_signal(CTRL_C_EVENT)
                yellow_player.send_signal(CTRL_C_EVENT)
                red_player.send_signal(CTRL_C_EVENT)
                if win == "yellow":
                    yellow_win += 1
                if win == "red":
                    red_win += 1
                # stop super 1 and 2
            if yellow_win > red_win:
                Tune.update_vars(0, Tune.cur_var)
            if red_win > yellow_win:
                Tune.update_vars(1, Tune.cur_var)
            Tune.cur_var = (Tune.cur_var + 1)%nb_vars




if __name__ == "__main__":
    Tune.tune_game()
