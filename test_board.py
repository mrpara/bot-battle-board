import unittest
import board
import turn_handler
import player


def check_adjacent(loc1, loc2, board_size):
    # Check if two locations are adjacent
    # Calc distance on each axis, account for wraparound
    x_dist = abs(loc1[0] - loc2[0])
    if x_dist == board_size[0] - 1:
        x_dist = 1
    y_dist = abs(loc1[1] - loc2[1])
    if y_dist == board_size[1] - 1:
        y_dist = 1
    # For the locations to be adjacent they must differ by 0 or 1 on each axis, but cannot be 0 on both axes
    x_dist_okay = x_dist == 0 or x_dist == 1
    y_dist_okay = y_dist == 0 or y_dist == 1
    comb_dist_okay = x_dist != 0 or y_dist != 0
    return x_dist_okay and y_dist_okay and comb_dist_okay


class TestBoard(unittest.TestCase):
    # Class for unit testing the board object
    def setUp(self):
        self.turn_handler = turn_handler.TurnHandler()
        self.players = {0: player.Player(0, None), 1: player.Player(1, None), 2: player.Player(2, None)}

    def test_unit_limit(self):
        # Test the unit limit feature. Unit limit must be greater than zero and less than one
        with self.assertRaises(Exception):
            board.Board(self.turn_handler, {}, [20, 20], -1)
        with self.assertRaises(Exception):
            board.Board(self.turn_handler, {}, [20, 20], 0)
        with self.assertRaises(Exception):
            board.Board(self.turn_handler, {}, [20, 20], 1.2)

    def test_spawn(self):
        # Test that spawning a unit adds it to board
        test_board = board.Board(self.turn_handler, self.players, [20, 20], 0.5)
        self.assertIsNone(test_board.board_matrix[0, 0])
        test_board.spawn_unit(self.players[0], [0, 0])
        self.assertIsNotNone(test_board.board_matrix[0, 0])

    def test_spawn_free(self):
        # Test spawning in the same location
        test_board = board.Board(self.turn_handler, self.players, [20, 20], 0.5)
        test_board.spawn_unit(self.players[0], [1, 1])
        with self.assertRaises(Exception):
            test_board.spawn_unit(self.players[0], [1, 1])

    def test_spawn_limit(self):
        # Test that attempting to spawn beyond limit will not spawn new units
        test_board = board.Board(self.turn_handler, self.players, [20, 20], 0.01)  # set limit to 4 units
        self.assertTrue(test_board.spawn_unit(self.players[0], [0, 0]))
        self.assertTrue(test_board.spawn_unit(self.players[0], [0, 1]))
        self.assertTrue(test_board.spawn_unit(self.players[0], [0, 2]))
        self.assertTrue(test_board.spawn_unit(self.players[0], [0, 3]))
        self.assertEqual(self.players[0].num_units(), 4)  # After 4 spawns we should have 4 units
        self.assertFalse(test_board.spawn_unit(self.players[0], [0, 4]))
        self.assertEqual(self.players[0].num_units(), 4)  # After 5 spawns we should still have 4 units

    def test_despawn(self):
        # Spawn a unit, then despawn it and check that it is indeed removed from the board
        test_board = board.Board(self.turn_handler, self.players, [20, 20], 0.01)
        test_board.spawn_unit(self.players[0], [0, 0])
        self.assertIsNotNone(test_board.board_matrix[0, 0])
        unit = list(self.players[0].units)[0]
        test_board.despawn_unit(unit)
        self.assertIsNone(test_board.board_matrix[0, 0])

    def test_spawn_adjacent(self):
        # Spawn a unit, then spawn an adjacent unit and verify that it is adjacent.
        test_board = board.Board(self.turn_handler, self.players, [20, 20], 0.01)
        self.assertTrue(test_board.spawn_unit(self.players[0], [0, 0]))
        unit1 = self.players[0].units.pop()
        self.assertTrue(test_board.spawn_in_adjacent_location(unit1.player, unit1.loc))
        unit2 = self.players[0].units.pop()
        self.assertTrue(check_adjacent(unit1.loc, unit2.loc, [20, 20]))

    def test_spawn_adjacent_limit(self):
        # Spawn a unit, then spawn 9 units around it. The spawn of the 9th unit should fail since there is no room.
        test_board = board.Board(self.turn_handler, self.players, [20, 20], 0.5)
        self.assertTrue(test_board.spawn_unit(self.players[0], [0, 0]))
        unit1 = self.players[0].units.pop()
        for i in range(8):
            self.assertTrue(test_board.spawn_in_adjacent_location(unit1.player, unit1.loc))
        self.assertFalse(test_board.spawn_in_adjacent_location(unit1.player, unit1.loc))

    def test_move(self):
        # Spawn a unit, move it to a new location, verify it is now in that location
        test_board = board.Board(self.turn_handler, self.players, [20, 20], 0.01)
        test_board.spawn_unit(self.players[0], [0, 0])
        unit1 = self.players[0].units.pop()
        test_board.move_unit(unit1, [3, 3])
        self.assertTrue(unit1.loc == [3, 3])
        self.assertTrue(test_board.board_matrix[[3, 3]] == unit1)

    def test_move_to_adjacent_loc(self):
        # Spawn a unit, call move to adjacent loc, verify it is now in an adjacent loc
        test_board = board.Board(self.turn_handler, self.players, [20, 20], 0.01)
        test_board.spawn_unit(self.players[0], [0, 0])
        unit = self.players[0].units.pop()
        old_loc = unit.loc
        test_board.move_to_adjacent_loc(unit)
        new_loc = unit.loc
        self.assertTrue(check_adjacent(old_loc, new_loc, test_board.board_size))

    def test_num_allies_around_unit(self):
        # Spawn a unit, spawn 2 allied units and one enemy unit around it, check number of allies
        test_board = board.Board(self.turn_handler, self.players, [20, 20], 0.01)
        test_board.spawn_unit(self.players[0], [0, 0])
        unit = self.players[0].units.pop()
        test_board.spawn_in_adjacent_location(self.players[0], [0, 0])
        test_board.spawn_in_adjacent_location(self.players[0], [0, 0])
        test_board.spawn_in_adjacent_location(self.players[1], [0, 0])
        self.assertTrue(test_board.num_allies_around_unit(unit) == 2)

    def test_num_total_enemies(self):
        # Spawn a unit, spawn 2 allies and 3 enemies (from 2 different players) around it, check num total enemies
        test_board = board.Board(self.turn_handler, self.players, [20, 20], 0.01)
        test_board.spawn_unit(self.players[0], [0, 0])
        unit = self.players[0].units.pop()
        test_board.spawn_in_adjacent_location(self.players[0], [0, 0])
        test_board.spawn_in_adjacent_location(self.players[0], [0, 0])
        test_board.spawn_in_adjacent_location(self.players[1], [0, 0])
        test_board.spawn_in_adjacent_location(self.players[2], [0, 0])
        test_board.spawn_in_adjacent_location(self.players[2], [0, 0])
        self.assertEqual(test_board.num_total_enemies(unit.player), 3)

    def test_distance_from_closest_ally(self):
        # Spawn a unit and two allies and an enemy, check distance from them
        test_board = board.Board(self.turn_handler, self.players, [20, 20], 0.01)
        test_board.spawn_unit(self.players[0], [0, 0])
        unit1 = self.players[0].units.pop()
        test_board.spawn_unit(self.players[0], [18, 0])
        test_board.spawn_unit(self.players[0], [5, 5])
        test_board.spawn_unit(self.players[1], [1, 0])
        self.assertEqual(test_board.distance_from_closest_ally(unit1), 2)

    def test_distance_from_closest_enemy(self):
        # Spawn a unit and two enemies and an ally, check distance from them
        test_board = board.Board(self.turn_handler, self.players, [20, 20], 0.01)
        test_board.spawn_unit(self.players[0], [0, 0])
        unit1 = self.players[0].units.pop()
        test_board.spawn_unit(self.players[0], [18, 0])
        test_board.spawn_unit(self.players[1], [5, 5])
        test_board.spawn_unit(self.players[1], [7, 0])
        self.assertEqual(test_board.distance_from_closest_enemy(unit1), 5)

    def test_attack_adjacent_enemy(self):
        # First spawn a unit and have it attack, and check that this fails.
        # Then spawn an adjacent enemy and check that it works, and that the unit took damage
        test_board = board.Board(self.turn_handler, self.players, [20, 20], 0.01)
        test_board.spawn_unit(self.players[0], [0, 0])
        unit1 = self.players[0].units.pop()
        self.assertFalse(test_board.attack_adjacent_enemy(unit1, 1))
        test_board.spawn_unit(self.players[1], [1, 0])
        self.assertTrue(test_board.attack_adjacent_enemy(unit1, 1))
        unit2 = self.players[1].units.pop()
        self.assertEqual(unit2.hp, unit1.hp - 1)

    def test_is_free(self):
        # Check that a location is free, then spawn a unit in it and verify that it is no longer free
        test_board = board.Board(self.turn_handler, self.players, [20, 20], 0.01)
        self.assertTrue(test_board.is_free([0, 0]))
        test_board.spawn_unit(self.players[0], [0, 0])
        self.assertFalse(test_board.is_free([0, 0]))

    def test_is_ally(self):
        # Verify that unit is an ally to the player that spawned it and not an ally to another player
        test_board = board.Board(self.turn_handler, self.players, [20, 20], 0.01)
        test_board.spawn_unit(self.players[0], [0, 0])
        self.assertTrue(test_board.is_ally([0, 0], self.players[0]))
        self.assertFalse(test_board.is_ally([0, 0], self.players[1]))

    def test_is_enemy(self):
        # Verify that unit is not an enemy to the player that spawned it an enemy to another player
        test_board = board.Board(self.turn_handler, self.players, [20, 20], 0.01)
        test_board.spawn_unit(self.players[0], [0, 0])
        self.assertFalse(test_board.is_enemy([0, 0], self.players[0]))
        self.assertTrue(test_board.is_enemy([0, 0], self.players[1]))

    def test_get_all_adjacent_locs(self):
        # Supply a location and compare against the results of the get_all_adjacent_locs
        # A location on the edge is chosen to make sure that wrapping works
        # The list of locations must be sorted so that order does not change the result
        test_board = board.Board(self.turn_handler, self.players, [20, 20], 0.01)
        loc = [0, 2]
        adjacent_locs = sorted([[19, 1], [19, 2], [19, 3], [0, 1], [0, 3], [1, 1], [1, 2], [1, 3]])
        self.assertEqual(sorted(test_board.get_all_adjacent_locs(loc)), adjacent_locs)

    def test_num_free_tiles_around_loc(self):
        # Check that 8 locations are free around a given location, then spawn a unit around it and check
        # that the number is reduced
        test_board = board.Board(self.turn_handler, self.players, [20, 20], 0.01)
        self.assertEqual(test_board.num_free_tiles_around_loc([0, 0]), 8)
        test_board.spawn_unit(self.players[0], [1, 0])
        self.assertEqual(test_board.num_free_tiles_around_loc([0, 0]), 7)

    def test_get_unit_in_loc(self):
        # First check that getting a unit from an empty location returns none
        # Then spawn a unit and verify that the correct unit is returned
        test_board = board.Board(self.turn_handler, self.players, [20, 20], 0.01)
        self.assertIsNone(test_board.get_unit_in_loc([0, 0]))
        test_board.spawn_unit(self.players[0], [0, 0])
        unit = self.players[0].units.pop()
        self.assertEqual(unit, test_board.get_unit_in_loc([0, 0]))

    def test_get_adjacent_enemy_unit(self):
        # First check that getting an enemy unit when there isn't one returns none
        # Then spawn a an enemy unit and verify that the correct unit is returned
        test_board = board.Board(self.turn_handler, self.players, [20, 20], 0.01)
        test_board.spawn_unit(self.players[0], [0, 0])
        unit1 = self.players[0].units.pop()
        self.assertIsNone(test_board.get_adjacent_enemy_unit(unit1))
        test_board.spawn_unit(self.players[1], [1, 0])
        unit2 = self.players[1].units.pop()
        self.assertEqual(test_board.get_adjacent_enemy_unit(unit1), unit2)

    def test_get_adjacent_locs(self):
        # Test method that returns all adjacent locs that satisfy some boolean function
        # For this test we'll use the condition (x_loc + y_loc) mod 2 == 0
        test_board = board.Board(self.turn_handler, self.players, [20, 20], 0.01)
        test_loc = [5, 5]
        expected_locs = sorted([[4, 4], [4, 6], [6, 4], [6, 6]])

        def loc_is_even(loc):
            return (loc[0] + loc[1]) % 2 == 0
        res = sorted(test_board.get_adjacent_locs(test_loc, loc_is_even))
        self.assertEqual(expected_locs, res)

    def test_get_all_enemies(self):
        # Spawn some enemies and make sure we get the right answer
        test_board = board.Board(self.turn_handler, self.players, [20, 20], 0.01)
        test_board.spawn_unit(self.players[0], [0, 0])
        unit = self.players[0].units.pop()
        test_board.spawn_unit(self.players[1], [1, 0])
        test_board.spawn_unit(self.players[1], [1, 1])
        test_board.spawn_unit(self.players[2], [0, 1])
        test_board.spawn_unit(self.players[2], [3, 2])
        test_board.spawn_unit(self.players[2], [10, 17])
        self.assertEqual(set(test_board.get_all_enemies(unit)), self.players[1].units | self.players[2].units)

    def test_get_all_allies(self):
        # Spawn a unit, remove it from the play, spawn some ally units and check that they are returned by the method
        test_board = board.Board(self.turn_handler, self.players, [20, 20], 0.01)
        test_board.spawn_unit(self.players[0], [0, 0])
        unit = self.players[0].units.pop()
        test_board.spawn_unit(self.players[0], [1, 0])
        test_board.spawn_unit(self.players[0], [1, 1])
        test_board.spawn_unit(self.players[0], [0, 1])
        test_board.spawn_unit(self.players[0], [3, 2])
        test_board.spawn_unit(self.players[0], [10, 17])
        self.assertEqual(set(test_board.get_all_allies(unit)), self.players[0].units)

    def test_distance_between_units(self):
        # Test some different cases of distances
        test_board = board.Board(self.turn_handler, self.players, [20, 20], 0.01)

        test_board.spawn_unit(self.players[0], [0, 0])
        unit1 = self.players[0].units.pop()
        test_board.spawn_unit(self.players[0], [19, 0])
        unit2 = self.players[0].units.pop()
        self.assertEqual(test_board.distance_between_units(unit1, unit2), 1)

        test_board.spawn_unit(self.players[0], [5, 5])
        unit1 = self.players[0].units.pop()
        test_board.spawn_unit(self.players[0], [10, 10])
        unit2 = self.players[0].units.pop()
        self.assertEqual(test_board.distance_between_units(unit1, unit2), 5)

        test_board.spawn_unit(self.players[0], [1, 2])
        unit1 = self.players[0].units.pop()
        test_board.spawn_unit(self.players[0], [2, 18])
        unit2 = self.players[0].units.pop()
        self.assertEqual(test_board.distance_between_units(unit1, unit2), 4)


if __name__ == '__main__':
    unittest.main()
