import numpy as np
from collections import deque
from random import randint

class Unit:
    def __init__(self, unit_id, player_id, initial_loc):
        self.id = unit_id
        self.player_id = player_id
        self.var_data = {}
        self.loc = initial_loc
        self.hp = 3

class Board:
    def __init__(self):
        self.board_size = [10, 10]
        self.board = np.zeros((self.board_size[0], self.board_size[0]))

        self.can_act = False
        self.queue = deque()
        self.units = {}
        self.num_total_units_spawned = 0
        self.spawn_unit(0, [5,5])
        self.spawn_unit(1, [2,2])

        self.turn_number = 0

    def current_unit(self):
        return self.units[self.queue[0]]

    def start_turn(self):
        self.can_act = True
        self.turn_number += 1

    def end_turn(self):
        self.can_act = False
        self.queue.appendleft(self.queue.pop())

    def is_free(self, loc):
        if self.board[loc[0], loc[1]] == 0:
            return True
        return False

    def spawn_unit(self, player_id, loc):
        if not self.is_free(loc):
            raise Exception("Cannot spawn unit in location " + str(loc) + " since it is occupied")

        self.num_total_units_spawned += 1
        unit_id = self.num_total_units_spawned
        self.units[unit_id] = Unit(unit_id, player_id, loc)
        self.board[loc[0], loc[1]] = unit_id
        self.queue.append(unit_id)

    def get_adjacent_loc(self, loc):
        return [(loc[0] + randint(-1, 1) + self.board_size[0]) % self.board_size[0],
                (loc[1] + randint(-1, 1) + self.board_size[1]) % self.board_size[1]]

    def move_unit(self, unit_id, new_loc):
        if not self.is_free(new_loc):
            raise Exception("Tried to move unit " + str(unit_id) + "to occupied location " + str(new_loc))
        old_loc = self.units[unit_id].loc
        self.units[unit_id].loc = new_loc
        self.board[old_loc[0], old_loc[1]] = 0
        self.board[new_loc[0], new_loc[1]] = unit_id

    def update_board(self):
        self.board = np.zeros((self.board_size[0], self.board_size[0]))
        for unit in self.units:
            loc = self.units[unit].loc
            id = self.units[unit].id
            if not self.is_free(loc):
                raise Exception("Error, location " + str(loc) + "contains two units: id " + str(id) +
                                " and id " + str(self.board[loc[0], loc[1]]))
            self.board[loc[0], loc[1]] = id

    def num_free_tiles_around_unit(self, unit_id):
        loc = self.units[unit_id].loc
        n = 0
        for x_adj in [-1, 0, 1]:
            for y_adj in [-1, 0, 1]:
                locx = (loc[0] + x_adj + self.board_size[0]) % self.board_size[0]
                locy= (loc[1] + y_adj + self.board_size[1]) % self.board_size[1]
                if self.is_free([locx, locy]):
                    n += 1
        return n
