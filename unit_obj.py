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
        self.hp = 3
        self.spawn_timer = 0
        self.can_act = True
        self.defending = False

    def set_spawn(self, interval):
        self.spawn_timer += interval
        self.can_act = False

    def on_new_turn(self):
        self.defending = False
        self.decrement_spawn_timer_and_spawn_if_ready()

    def decrement_spawn_timer_and_spawn_if_ready(self):
        if self.spawn_timer > 0:
            self.spawn_timer -= 1
            if self.spawn_timer == 0:
                self.board.spawn_in_adjacent_location(self.player_id, self.loc)
                print(self.board.num_allies_around_unit(self))
                self.can_act = True

    def decrement_hp(self, dmg):
        self.hp -= dmg
        print("Unit " + str(self.id) + " took " + str(dmg) + " damage")
        if self.hp <= 0:
            self.kill()

    def kill(self):
        self.board.despawn_unit(self)
        print("Unit " + str(self.id) + " destroyed")

    def defend(self):
        self.defending = True

    def damage(self, dmg):
        if self.defending is True:
            self.defending = False
            return
        self.decrement_hp(dmg)