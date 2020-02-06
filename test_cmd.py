import unittest
import board
import turn_handler

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.turn_handler = turn_handler.TurnHandler()

    def test_unit_limit(self):
        with self.assertRaises(Exception):
            board.Board(self.turn_handler, {}, [20, 20], -1)
        with self.assertRaises(Exception):
            board.Board(self.turn_handler, {}, [20, 20], 0)
        with self.assertRaises(Exception):
            board.Board(self.turn_handler, {}, [20, 20], 1.2)

if __name__ == '__main__':
    unittest.main()