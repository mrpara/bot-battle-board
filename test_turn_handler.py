import unittest
import board
import turn_handler
import player


class TestTurnHandler(unittest.TestCase):
    # Class for unit testing the turn handler object
    def setUp(self):
        self.players = {0: player.Player(0, None), 1: player.Player(1, None), 2: player.Player(2, None)}

    def test_current_unit(self):
        # Spawn a new unit and make sure it is the current unit. Then spawn another and make sure it is still the
        # current unit.
        # The turn handler class doesn't really have any logic to unit test as it is a simple queue, so it is arguable
        # whether this is actually needed.
        test_turn_handler = turn_handler.TurnHandler()
        test_board = board.Board(test_turn_handler, self.players, [20, 20], 0.01)
        test_board.spawn_unit(self.players[0], [0, 0])
        unit1 = self.players[0].units.pop()
        self.assertEqual(unit1, test_turn_handler.current_unit())
        test_board.spawn_unit(self.players[0], [0, 1])
        self.assertEqual(unit1, test_turn_handler.current_unit())

    def test_end_turn(self):
        # Spawn two units. Make sure the first unit spawned is the current unit (top of the queue), then end turn
        # and make sure the second unit is the current unit
        # Similar to above.
        test_turn_handler = turn_handler.TurnHandler()
        test_board = board.Board(test_turn_handler, self.players, [20, 20], 0.01)
        test_board.spawn_unit(self.players[0], [0, 0])
        unit1 = self.players[0].units.pop()
        test_board.spawn_unit(self.players[0], [0, 1])
        unit2 = self.players[0].units.pop()
        self.assertEqual(unit1, test_turn_handler.current_unit())
        test_turn_handler.end_turn()
        self.assertEqual(unit2, test_turn_handler.current_unit())


if __name__ == '__main__':
    unittest.main()
