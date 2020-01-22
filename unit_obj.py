import numpy as np
from collections import deque
from random import randint


class Unit:
    def __init__(self, board, unit_id, player_id, initial_loc):
        self.board = board
        self.id = unit_id
        self.player_id = player_id
        self.var_data = {}
        self.loc = initial_loc
        self.hp = 5
        self.spawn_timer = 0
        self.can_act = True

    def set_spawn(self, interval):
        self.spawn_timer += interval
        self.can_act = False

    def on_new_turn(self):
        self.decrement_hp()
        self.decrement_spawn_timer_and_spawn_if_ready()

    def decrement_spawn_timer_and_spawn_if_ready(self):
        if self.spawn_timer > 0:
            self.spawn_timer -= 1
            if self.spawn_timer == 0:
                self.board.spawn_in_adjacent_location(self.player_id, self.loc)
                self.can_act = True

    def decrement_hp(self):
        self.hp -= 1
        if self.hp == 0:
            self.kill()

    def kill(self):
        self.board.despawn_unit(self.id)
        print("Unit " + str(self.id) + " destroyed")
