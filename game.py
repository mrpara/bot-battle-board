import interpreter
import board
import turn_handler
import player
import cmd
from feedback import Feedback
import tkinter as tk
from tkinter import filedialog
from random import randint


class Game:
    def __init__(self):
        # DEFAULT PARAMETERS
        self.num_players = 2
        self.board_size = [20, 20]
        self.turn_limit = 10000
        self.unit_limit_pct = 0.05  # The maximum number of allowed units per player, as a percentage of board capacity
        self.display_messages = True
        self.display_board = True
        self.write_to_file = False
        self.default_path = "C:/Users/user1/Dropbox/strategies/bot-battle-board"
        self.log_path = "log.txt"

        # OBJECT INITIALIZATION
        self.players = {}  # Dict of players, player_id -> player_object
        Feedback(self.display_messages, self.display_board, self.write_to_file, self.log_path)
        self.turn_handler = turn_handler.TurnHandler()  # Turn handler in charge of determining which unit acts when
        self.board = board.Board(self.turn_handler, self.players,
                                 self.board_size, self.unit_limit_pct)  # Board and units
        self.user_commands = cmd.Commands(self.board, self.turn_handler)
        self.interpreter = interpreter.Interpreter(self.turn_handler, self.user_commands)

    def get_user_input(self):
        # Read user input script
        script_path = filedialog.askopenfilename(initialdir=self.default_path, filetypes=[("TXT", "*.txt")])
        with open(script_path, 'r') as input_file:
            bot_cmds = input_file.read()
        return bot_cmds

    def populate_players(self):
        # For each player, read their script and analyze it, and create a new player object
        # with the resulting instructions
        for i in range(self.num_players):
            bot_cmds = self.get_user_input()
            self.players[i + 1] = player.Player(i + 1, self.interpreter.analyze(bot_cmds))

    def spawn_initial_units(self):
        # For each player, spawn one unit in a random location on the board_matrix. If the location has already
        # been picked, keep picking random locations until an available one has been found.
        spawn_locs = set()
        newloc = self.board.get_random_location()
        for player_id in self.players:
            while tuple(newloc) in spawn_locs:
                newloc = self.board.get_random_location()
            spawn_locs.add(tuple(newloc))
            self.board.spawn_unit(player_id, newloc)

    def turn_limit_reached(self):
        return self.turn_handler.turn_number >= self.turn_limit

    def turn(self):
        # Start turn (resetting all relevant state variables), execute script for current acting unit, and end turn
        self.turn_handler.start_turn()
        Feedback().display_message("Turn number " + str(self.interpreter.turn_handler.turn_number))
        Feedback().display_message("Acting unit: " + str(self.interpreter.turn_handler.current_unit().id))
        self.players[self.turn_handler.current_player()].command_script()
        self.turn_handler.end_turn()
        Feedback().print_board(self.board)
        self.remove_losing_players()

    def remove_losing_players(self):
        # Check if any players have had all of their units destroyed, and remove them from the players list
        players_to_remove = []
        for player_id, player in self.players.items():
            if player.num_units() == 0:
                players_to_remove.append(player_id)
                Feedback().display_message("Player " + str(player_id) + " eliminated")
        for player_id in players_to_remove:
            del self.players[player_id]

    def announce_winner(self):
        # Check and report the winning player(s).
        # If only one player remains, they win. Otherwise, check number of remaining units per player.
        # The winners are all the players who hold the highest number of remaining units.

        if self.one_player_left():
            Feedback().display_message("Player " + str(list(self.players)[0]) + " has won the game")
            return

        #  Make a player id -> remaining units dict, check max value, then get all player ids with this max value
        remaining_units = {player_id: self.players[player_id].num_units() for player_id in self.players}
        max_num_units_left = max(remaining_units.values())
        tied_players = [player_id for player_id in remaining_units
                        if remaining_units[player_id] == max_num_units_left]

        if len(tied_players) == 1:
            Feedback().display_message("Turn limit reached, player " + str(tied_players[0]) +
                                       " wins with " + str(max_num_units_left) + " units remaining")
            return

        Feedback().display_message("Turn limit reached, players " + str(tied_players) +
                                   " are tied with " + str(max_num_units_left) + " units remaining")

    def one_player_left(self):
        # Game ends when only one player has surviving units (or if turn limit is reached)
        return len(self.players) == 1

    def game_ended(self):
        return self.turn_limit_reached() or self.one_player_left()

    def start_game(self):
        self.populate_players()
        self.spawn_initial_units()

        while not self.game_ended():
            self.turn()

        self.announce_winner()


if __name__ == "__main__":
    root = tk.Tk()  # Prevents blank window from showing up because of the call to filedialog
    root.withdraw()

    game = Game()
    game.start_game()
