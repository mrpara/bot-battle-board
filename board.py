from typing import List
from typing import Union
from unit import Unit
from random import choice
from feedback import Feedback
from math import ceil
from random import randint


class Board:
    # This class handles the board_matrix object and the units on it and the manipulation thereof.
    # It also handles all unit- and board_matrix-related commands that should not be directly exposed to the user

    board_matrix: List[List[Union[Unit, None]]]  # Type hinting

    def __init__(self, turn_handler, players, board_size, unit_limit_pct):
        # Board initialization
        self.turn_handler = turn_handler
        self.players = players
        self.board_size = board_size
        self.unit_limit = ceil(board_size[0] * board_size[1] * unit_limit_pct)
        self.board_matrix = [[None for _ in range(self.board_size[1])] for _ in range(self.board_size[0])]
        self.num_total_units_spawned = 0

    ####################################################################################################################
    # Board manipulation
    ####################################################################################################################

    def spawn_unit(self, player_id, loc):
        # Add new unit to board
        if not self.is_free(loc):
            raise Exception("Cannot spawn unit in location " + str(loc) + " since it is occupied")

        if self.players[player_id].num_units() >= self.unit_limit:
            Feedback().display_message("Player " + str(player_id) +
                                       " attempted to spawn new unit, but has reached the spawn limit.")
            return

        self.num_total_units_spawned += 1
        unit_id = self.num_total_units_spawned
        new_unit = Unit(self, unit_id, player_id, loc)
        self.board_matrix[loc[0]][loc[1]] = new_unit
        self.turn_handler.add_to_queue(new_unit)
        self.players[player_id].units.add(new_unit)
        Feedback().display_message("New unit " + str(unit_id) + " spawned by player " + str(player_id) +
                                   " in location " + str(loc))

    def despawn_unit(self, unit):
        # Remove unit from board
        loc = unit.loc
        self.board_matrix[loc[0]][loc[1]] = None
        self.turn_handler.remove_from_queue(unit)
        self.players[unit.player_id].units.remove(unit)

    def spawn_in_adjacent_location(self, player_id, loc):
        spawn_loc = self.get_free_adjacent_loc(loc)
        if spawn_loc is None:
            return
        self.spawn_unit(player_id, spawn_loc)

    def move_unit(self, unit, new_loc):
        if not self.is_free(new_loc):
            raise Exception("Tried to move unit " + str(unit.id) + "to occupied location " + str(new_loc))
        old_loc = unit.loc
        unit.loc = new_loc
        self.board_matrix[old_loc[0]][old_loc[1]] = None
        self.board_matrix[new_loc[0]][new_loc[1]] = unit

    ####################################################################################################################
    # Functions for use in user-commands
    ####################################################################################################################

    def num_allies_around_unit(self, unit):
        loc = unit.loc
        player_id = unit.player_id
        return self.count_adjacent_locs_that_satisfy_bool(loc, lambda tloc: self.is_ally(tloc, player_id))

    def num_enemies_around_unit(self, unit):
        return 8 - self.num_free_tiles_around_unit(unit) - self.num_allies_around_unit(unit)

    def num_total_allies(self, player_id):
        return self.players[player_id].num_units() - 1

    def num_total_enemies(self, player_id):
        return sum([self.players[t_id].num_units() for t_id in self.players if t_id != player_id])

    def distance_from_closest_ally(self, unit):
        dist = [self.board_size[0] + self.board_size[1]]
        for ally in self.get_all_allies(unit):
            dist.append(self.distance_between_units(unit, ally))
        return min(dist)

    def distance_from_closest_enemy(self, unit):
        dist = [self.board_size[0] + self.board_size[1]]
        for enemy in self.get_all_enemies(unit):
            dist.append(self.distance_between_units(unit, enemy))
        return min(dist)

    def attack_adjacent_enemy(self, unit, dmg):
        enemy_unit = self.get_adjacent_enemy_unit(unit)
        if enemy_unit is None:
            Feedback().display_message("Unit " + str(unit.id) + " tried to attack, but no enemy units in range")
            return
        Feedback().display_message("Unit " + str(unit.id) + " attacked unit " + str(enemy_unit.id))
        enemy_unit.damage(dmg)

    ####################################################################################################################
    # Helper functions
    ####################################################################################################################

    def get_random_location(self):
        return [randint(0, self.board_size[0] - 1), randint(0, self.board_size[1]) - 1]

    def is_free(self, loc):
        if self.board_matrix[loc[0]][loc[1]] is None:
            return True
        return False

    def is_ally(self, loc, player_id):
        unit_in_loc = self.get_unit_in_loc(loc)
        if unit_in_loc is not None and unit_in_loc.player_id == player_id:
            return True
        return False

    def is_enemy(self, loc, player_id):
        unit_in_loc = self.get_unit_in_loc(loc)
        if unit_in_loc is not None and unit_in_loc.player_id != player_id:
            return True
        return False

    def get_all_adjacent_locs(self, loc):
        adjacent_locs = []
        for x_adj in [-1, 0, 1]:
            for y_adj in [-1, 0, 1]:
                locx = (loc[0] + x_adj + self.board_size[0]) % self.board_size[0]
                locy = (loc[1] + y_adj + self.board_size[1]) % self.board_size[1]
                if x_adj != 0 or y_adj != 0:
                    adjacent_locs.append([locx, locy])
        return adjacent_locs

    def get_free_adjacent_loc(self, loc):
        free_adjacent_locs = self.get_adjacent_locs_that_satisfy_bool(loc, self.is_free)
        if len(free_adjacent_locs) == 0:
            return None
        return choice(free_adjacent_locs)

    def num_free_tiles_around_loc(self, loc):
        return self.count_adjacent_locs_that_satisfy_bool(loc, self.is_free)

    def num_free_tiles_around_unit(self, unit):
        loc = unit.loc
        return self.num_free_tiles_around_loc(loc)

    def get_unit_in_loc(self, loc):
        return self.board_matrix[loc[0]][loc[1]]

    def get_adjacent_enemy_unit(self, unit):
        enemy_locs = self.get_adjacent_locs_that_satisfy_bool(unit.loc,
                                                              lambda tloc: self.is_enemy(tloc, unit.player_id))
        if len(enemy_locs) == 0:
            return None
        return self.get_unit_in_loc(choice(enemy_locs))

    def count_adjacent_locs_that_satisfy_bool(self, loc, f_bool):
        # Get a location and a boolean function, and count the number of adjacent locations that satisfy the function
        adjacent_locs = self.get_all_adjacent_locs(loc)
        n = 0
        for adjacent_loc in adjacent_locs:
            if f_bool(adjacent_loc):
                n += 1
        return n

    def get_adjacent_locs_that_satisfy_bool(self, loc, f_bool):
        # Get a location and a boolean function, and return all adjacent locations that satisfy the function
        adjacent_locs = self.get_all_adjacent_locs(loc)
        instances = []
        for adjacent_loc in adjacent_locs:
            if f_bool(adjacent_loc):
                instances.append(adjacent_loc)
        return instances

    def get_all_enemies(self, unit):
        return [t_unit
                for player_id in self.players if player_id != unit.player_id
                for t_unit in self.players[player_id].units]

    def get_all_allies(self, unit):
        return [t_unit
                for t_unit in self.players[unit.player_id].units
                if t_unit != unit]

    def distance_between_units(self, unit1, unit2):
        # Return the distance between two units. Here, distance is defined as the minimal number of steps needed to
        # reach one unit from the other, taking into account that units can move one tile in any direction (including
        # diagonally) and that the board_matrix wraps around (so it may be shorter to go from the other side).
        loc1 = unit1.loc
        loc2 = unit2.loc
        xdist_abs = abs(loc1[0] - loc2[0])
        xdist = min(xdist_abs, self.board_size[0] - xdist_abs)
        ydist_abs = abs(loc1[1] - loc2[1])
        ydist = min(ydist_abs, self.board_size[1] - ydist_abs)
        return max(xdist, ydist)

    def get_unit_limit(self):
        # Return the unit limit
        return self.unit_limit
