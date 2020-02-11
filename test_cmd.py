import unittest
import cmd
import board
import player
import turn_handler


class TestCmd(unittest.TestCase):
    # Class for unit testing the cmd object
    # Note that the majority of methods in cmd are just calls to methods of other objects which are tested directly,
    # calls to python commands (such as add, div, etc), or getters and setters which do not require tests
    def setUp(self):
        self.turn_handler = turn_handler.TurnHandler()
        self.players = {0: player.Player(0, None), 1: player.Player(1, None), 2: player.Player(2, None)}

    def test_verify_command(self):
        # Test the CommandInspector's verify_command method
        # First test that an exception is raised if an unknown command is supplies
        test_board = board.Board(self.turn_handler, self.players, [20, 20], 0.05)
        test_cmd = cmd.Commands(test_board, self.turn_handler)
        with self.assertRaises(Exception):
            cmd.CommandsInspector.verify_commands(test_cmd, "nonexistent_command", [])
        # Test that an exception is raised if a known command is called with the wrong number of arguments
        with self.assertRaises(Exception):
            cmd.CommandsInspector.verify_commands(test_cmd, "add", [1, 1, 1])

    def test_critical_action(self):
        # Test that critical actions cannot be performed more than once per turn
        test_board = board.Board(self.turn_handler, self.players, [20, 20], 0.05)
        test_cmd = cmd.Commands(test_board, self.turn_handler)
        test_board.spawn_unit(self.players[0], [0, 0])
        self.assertTrue(test_cmd.move())
        self.assertFalse(test_cmd.move())
        self.assertFalse(test_cmd.attack())


if __name__ == '__main__':
    unittest.main()
