import unittest
import board
import turn_handler
import player

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.turn_handler = turn_handler.TurnHandler()
        self.players = {0: player.Player(0, None)}


    def test_unit_limit(self):
        # Test the unit limit feature. Unit limit must be greater than zero and less than one
        with self.assertRaises(Exception):
            board.Board(self.turn_handler, {}, [20, 20], -1)
        with self.assertRaises(Exception):
            board.Board(self.turn_handler, {}, [20, 20], 0)
        with self.assertRaises(Exception):
            board.Board(self.turn_handler, {}, [20, 20], 1.2)

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



if __name__ == '__main__':
    unittest.main()