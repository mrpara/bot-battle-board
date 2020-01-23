from unit_obj import Unit
from collections import deque
from random import choice


class Board:
    def __init__(self, turn_handler):
        self.turn_handler = turn_handler
        self.board_size = [10, 10]
        self.board = [[None for _ in range(self.board_size[0])] for _ in range(self.board_size[1])]
        self.units = {}
        self.num_total_units_spawned = 0
        self.spawn_unit(1, [5, 5])
        self.spawn_unit(2, [2, 2])

    def is_free(self, loc):
        if self.board[loc[0]][loc[1]] is None:
            return True
        return False

    def spawn_unit(self, player_id, loc):
        if not self.is_free(loc):
            raise Exception("Cannot spawn unit in location " + str(loc) + " since it is occupied")

        self.num_total_units_spawned += 1
        unit_id = self.num_total_units_spawned
        new_unit = Unit(self, unit_id, player_id, loc)
        self.board[loc[0]][loc[1]] = new_unit
        self.turn_handler.add_to_queue(new_unit)
        self.units[unit_id] = new_unit
        print("New unit " + str(unit_id) + " spawned by player " + str(player_id) + " in location " + str(loc))

    def despawn_unit(self, unit):
        loc = unit.loc
        self.board[loc[0]][loc[1]] = None
        self.turn_handler.remove_from_queue(unit)
        del self.units[unit.id]

    def spawn_in_adjacent_location(self, player_id, loc):
        spawn_loc = self.get_free_adjacent_loc(loc)
        if spawn_loc is None:
            return
        self.spawn_unit(player_id, spawn_loc)

    def get_free_adjacent_loc(self, loc):
        free_adjacent_locs = self.get_locs_with_true_value_around_loc(loc, self.is_free)
        if len(free_adjacent_locs) == 0:
            return None
        return choice(free_adjacent_locs)

    def get_all_adjacent_locs(self, loc):
        adjacent_locs = []
        for x_adj in [-1, 0, 1]:
            for y_adj in [-1, 0, 1]:
                locx = (loc[0] + x_adj + self.board_size[0]) % self.board_size[0]
                locy = (loc[1] + y_adj + self.board_size[1]) % self.board_size[1]
                if x_adj != 0 or y_adj != 0:
                    adjacent_locs.append([locx, locy])
        return adjacent_locs

    def move_unit(self, unit, new_loc):
        if not self.is_free(new_loc):
            raise Exception("Tried to move unit " + str(unit.id) + "to occupied location " + str(new_loc))
        old_loc = unit.loc
        unit.loc = new_loc
        self.board[old_loc[0]][old_loc[1]] = None
        self.board[new_loc[0]][new_loc[1]] = unit

    def num_free_tiles_around_loc(self, loc):
        return self.count_true_values_around_loc(loc, self.is_free)

    def num_free_tiles_around_unit(self, unit):
        loc = unit.loc
        return self.num_free_tiles_around_loc(loc)

    def get_unit_in_loc(self, loc):
        return self.board[loc[0]][loc[1]]

    def get_adjacent_enemy_unit(self, unit):
        enemy_locs = self.get_locs_with_true_value_around_loc(unit.loc,
                                                              lambda tloc: self.is_ally(tloc, unit.player_id))
        if len(enemy_locs) == 0:
            return None
        return self.get_unit_in_loc(choice(enemy_locs))

    def attack_adjacent_enemy(self, unit):
        enemy_unit = self.get_adjacent_enemy_unit(unit)
        if enemy_unit is None:
            print("Unit " + str(unit.id) + " tried to attack, but no enemy units in range")
            return
        print("Unit " + str(unit.id) + " attacked unit " + str(enemy_unit.id))
        enemy_unit.decrement_hp()

    def num_enemies_around_unit(self, unit):
        return 8 - self.num_free_tiles_around_unit(unit) - self.num_allies_around_unit(unit)

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

    def num_allies_around_unit(self, unit):
        loc = unit.loc
        player_id = unit.player_id
        return self.count_true_values_around_loc(loc, lambda tloc: self.is_ally(tloc, player_id))

    def count_true_values_around_loc(self, loc, f_bool):
        adjacent_locs = self.get_all_adjacent_locs(loc)
        n = 0
        for adjacent_loc in adjacent_locs:
            if f_bool(adjacent_loc) is True:
                n += 1
        return n

    def get_locs_with_true_value_around_loc(self, loc, f_bool):
        adjacent_locs = self.get_all_adjacent_locs(loc)
        instances = []
        for adjacent_loc in adjacent_locs:
            if f_bool(adjacent_loc) is True:
                instances.append(adjacent_loc)
        return instances

    def print_board(self):
        output_mtx = []
        for row in self.board:
            output_mtx.append(['X' if elem is None else elem.id for elem in row])
        s = [[str(e) for e in row] for row in output_mtx]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        print('\n'.join(table))

    def num_total_allies(self, player_id):
        num_allies = 0
        for unit_id in self.units:
            if self.units[unit_id].player_id == player_id:
                num_allies += 1
        return num_allies - 1

    def num_total_enemies(self, player_id):
        return len(self.units) - self.num_total_allies(player_id) - 1

    def get_all_enemies(self, unit):
        return [self.units[t_unit] for t_unit in self.units if self.units[t_unit].player_id != unit.player_id]

    def get_all_allies(self, unit):
        return [self.units[t_unit] for t_unit in self.units if (self.units[t_unit].player_id == unit.player_id
                                                                and self.units[t_unit] != unit)]

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

    def distance_between_units(self, unit1, unit2):
        loc1 = unit1.loc
        loc2 = unit2.loc
        xdist_abs = abs(loc1[0] - loc2[0])
        xdist = min(xdist_abs, self.board_size[0] - xdist_abs)
        ydist_abs = abs(loc1[1] - loc2[1])
        ydist = min(ydist_abs, self.board_size[1] - ydist_abs)
        return max(xdist, ydist)
