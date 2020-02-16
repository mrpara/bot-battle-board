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
        # Game object should crash if called with less than 2 paths (players), or more players than the number of
        # tiles on the board.
        paths_test = [self.paths[0]]
        with self.assertRaises(Exception):
            game.Game(paths_test)
        paths_test = [self.paths[0]] * 150  # 150 players
        with self.assertRaises(Exception):
            game.Game(paths_test, board_size=[10, 10])  # Attempt to init game with 100-tile board

    def test_spawn_initial_units(self):
        # This method spawns one unit per player in a random location on the board. Locations may be adjacent, but
        # obviously each location may only hold one unit. So to test, we will fill the board with players and make sure
        # that the board is completely filled without error. There is no need to worry about having more players than
        # tiles since that is checked explicitly in board in it.
        test_game = game.Game([self.paths[0]] * 100, board_size=[10, 10])
        test_game.populate_players()
        test_game.spawn_initial_units()
        for i in range(10):
            for j in range(10):
                self.assertFalse(test_game.board.is_free([i, j]))

    def test_turn(self):
        # Placeholder. At the moment turn() is made up entirely of calls which are tested elsewhere with no internal
        # logic, so nothing to test.
        pass

    def test_remove_losing_players(self):
        # Test that players with no remaining units are removed from self.players when this method is called
        # First, try it with two players (minimum) and don't spawn units for them to begin with
        test_game = game.Game(self.paths, board_size=[10, 10])
        test_game.populate_players()
        self.assertEqual(len(test_game.players), 2)
        test_game.remove_losing_players()
        self.assertEqual(len(test_game.players), 0)

        # Repopulate players, add one unit to one of them. Only the other should be removed now.
        test_game.populate_players()
        self.assertEqual(len(test_game.players), 2)
        test_game.board.spawn_unit(test_game.players[1], [0, 0])
        player1 = test_game.players[1]
        test_game.remove_losing_players()
        self.assertEqual(test_game.players, {1: player1})

        # For the last test, add units to both, call the function, then remove unit from one and check that it is
        # removed
        test_game.populate_players()
        test_game.spawn_initial_units()
        player1 = test_game.players[1]
        test_game.remove_losing_players()
        self.assertEqual(len(test_game.players), 2)
        list(test_game.players[2].units)[0].kill()
        test_game.remove_losing_players()
        self.assertEqual(test_game.players, {1: player1})

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
        # Placeholder. At the moment start_game() does not have enough internal logic to test.
        pass


if __name__ == '__main__':
    unittest.main()
