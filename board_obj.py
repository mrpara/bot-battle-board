import numpy as np
from unit_obj import Unit
from collections import deque
from random import randint


class Board:
    def __init__(self, turn_handler):
        self.turn_handler = turn_handler
        self.board_size = [10, 10]
        self.board_matrix = np.zeros((self.board_size[0], self.board_size[0]))
        self.units = {}
        self.num_total_units_spawned = 0
        self.spawn_unit(0, [5, 5])
        self.spawn_unit(1, [2, 2])

    def is_free(self, loc):
        if self.board_matrix[loc[0], loc[1]] == 0:
            return True
        return False

    def spawn_unit(self, player_id, loc):
        if not self.is_free(loc):
            raise Exception("Cannot spawn unit in location " + str(loc) + " since it is occupied")

        self.num_total_units_spawned += 1
        unit_id = self.num_total_units_spawned
        self.units[unit_id] = Unit(self, unit_id, player_id, loc)
        self.board_matrix[loc[0], loc[1]] = unit_id
        self.turn_handler.add_to_queue(self.units[unit_id])
        print("New unit " + str(unit_id) + " spawned by player " + str(player_id) + " in location " + str(loc))

    def despawn_unit(self, unit_id):
        if unit_id not in self.units:
            raise KeyError("Tried to delete nonexistent unit " + str(unit_id))
        loc = self.units[unit_id].loc
        self.board_matrix[loc[0], loc[1]] = 0
        self.turn_handler.remove_from_queue(self.units[unit_id])
        del self.units[unit_id]

    def spawn_in_adjacent_location(self, player_id, loc):
        spawn_loc = self.get_free_adjacent_loc(loc)
        if spawn_loc is None:
            return
        self.spawn_unit(player_id, spawn_loc)

    def get_free_adjacent_loc(self, loc):
        if self.num_free_tiles_around_loc(loc) == 0:
            return None
        free_loc = self.get_adjacent_loc(loc)
        while not self.is_free(free_loc):
            free_loc = self.get_adjacent_loc(free_loc)
        return free_loc

    def get_adjacent_loc(self, loc):
        return [(loc[0] + randint(-1, 1) + self.board_size[0]) % self.board_size[0],
                (loc[1] + randint(-1, 1) + self.board_size[1]) % self.board_size[1]]

    def move_unit(self, unit_id, new_loc):
        if not self.is_free(new_loc):
            raise Exception("Tried to move unit " + str(unit_id) + "to occupied location " + str(new_loc))
        old_loc = self.units[unit_id].loc
        self.units[unit_id].loc = new_loc
        self.board_matrix[old_loc[0], old_loc[1]] = 0
        self.board_matrix[new_loc[0], new_loc[1]] = unit_id

    def update_board(self):
        self.board_matrix = np.zeros((self.board_size[0], self.board_size[0]))
        for unit in self.units:
            unit_loc = self.units[unit].loc
            unit_id = self.units[unit].id
            if not self.is_free(unit_loc):
                raise Exception("Error, location " + str(unit_loc) + "contains two units: id " + str(unit_id) +
                                " and id " + str(self.board_matrix[unit_loc[0], unit_loc[1]]))
            self.board_matrix[unit_loc[0], unit_loc[1]] = unit_id

    def num_free_tiles_around_loc(self, loc):
        return self.count_boolean_function_around_loc(loc, self.is_free)

    def num_free_tiles_around_unit(self, unit_id):
        loc = self.units[unit_id].loc
        return self.num_free_tiles_around_loc(loc)

    def get_unit_in_loc(self, loc):
        unit_id = self.board_matrix[loc[0], loc[1]]
        if unit_id == 0:
            return None
        return self.units[unit_id]

    def num_enemies_around_unit(self, unit_id):
        return 8 - self.num_free_tiles_around_unit(unit_id) - self.num_allies_around_unit(unit_id)

    def is_ally(self, loc, player_id):
        unit_in_loc = self.get_unit_in_loc(loc)
        if unit_in_loc is not None and unit_in_loc.player_id == player_id:
            return True
        return False

    def num_allies_around_unit(self, unit_id):
        loc = self.units[unit_id].loc
        player_id = self.units[unit_id].player_id
        return self.count_boolean_function_around_loc(loc, lambda tloc: self.is_ally(tloc, player_id)) - 1

    def count_boolean_function_around_loc(self, loc, f_bool):
        n = 0
        for x_adj in [-1, 0, 1]:
            for y_adj in [-1, 0, 1]:
                locx = (loc[0] + x_adj + self.board_size[0]) % self.board_size[0]
                locy = (loc[1] + y_adj + self.board_size[1]) % self.board_size[1]
                if f_bool([locx, locy]) is True:
                    n += 1
        return n
