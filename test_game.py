import game
import unittest
import player
import logging

class TestBoard(unittest.TestCase):
    # Class for unit testing the game object
    def setUp(self):
        logging.disable(logging.CRITICAL)  # Disable logging
        self.paths = ["unit_test_files//unit_test_strategy_1.txt", "unit_test_files//unit_test_strategy_2.txt"]

    def test_init(self):
        pass

    def test_populate_players(self):
        pass

    def test_spawn_initial_units(self):
        pass

    def test_turn(self):
        pass

    def test_remove_losing_players(self):
        pass

    def test_announce_winner(self):
        # Test the announce_winner method, which both announces and returns the number of the winning player
        # For the first test, create only one player. The method should return their id as the winner.
        test_game = game.Game(self.paths)
        test_player_1 = player.Player(4, None)
        test_game.players[4] = test_player_1
        test_game.board.spawn_unit(test_player_1, [0, 0])
        self.assertEqual(test_game.announce_winner(), 4)
        # Now add another player with 2 units, they should be the winner
        test_player_2 = player.Player(6, None)
        test_game.players[6] = test_player_2
        test_game.board.spawn_unit(test_player_2, [0, 1])
        test_game.board.spawn_unit(test_player_2, [0, 2])
        self.assertEqual(test_game.announce_winner(), 6)
        # Add one more unit to the first player, and the method should return a list of both as winners
        test_game.board.spawn_unit(test_player_1, [0, 3])
        self.assertEqual(test_game.announce_winner(), [4, 6])

    def test_start_game(self):
        pass


if __name__ == '__main__':
    unittest.main()
