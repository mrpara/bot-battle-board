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
        test_board.spawn_unit(self.players[0], [0, 0])
        test_board.spawn_unit(self.players[0], [0, 1])
        test_board.spawn_unit(self.players[0], [0, 2])
        test_board.spawn_unit(self.players[0], [0, 3])
        self.assertEqual(self.players[0].num_units(), 4)  # After 4 spawns we should have 4 units
        test_board.spawn_unit(self.players[0], [0, 4])
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
        # Spawn a unit, then spawn an adjacent unit and verify that it is adjacent
        test_board = board.Board(self.turn_handler, self.players, [20, 20], 0.01)
        test_board.spawn_unit(self.players[0], [0, 0])
        unit1 = self.players[0].units.pop()
        test_board.spawn_in_adjacent_location(unit1.player, unit1.loc)
        unit2 = self.players[0].units.pop()
        self.assertTrue(check_adjacent(unit1.loc, unit2.loc, [20, 20]))

    def test_move(self):
        # Spawn a unit, move it to a new location, verify it is now in that location
        test_board = board.Board(self.turn_handler, self.players, [20, 20], 0.01)
        test_board.spawn_unit(self.players[0], [0, 0])
        unit1 = self.players[0].units.pop()
        test_board.move_unit(unit1, [3, 3])
        self.assertTrue(unit1.loc == [3, 3])
        self.assertTrue(test_board.board_matrix[[3, 3]] == unit1)

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


if __name__ == '__main__':
    unittest.main()
