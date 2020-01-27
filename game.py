import interpreter
import board_obj
import turn_handler
import player_obj
import cmd_obj
import user_prompts_obj
import tkinter as tk
from tkinter import filedialog
from random import randint

root = tk.Tk()  # Prevents blank window from showing up because of the call to filedialog
root.withdraw()


class Game:
    def __init__(self):
        # DEFAULT PARAMETERS
        self.num_players = 2
        self.board_size = [10, 10]
        self.turn_limit = 500
        self.num_rounds = 3
        self.display_user_prompts = True
        self.display_board = True
        self.default_path = "C:/Users/user1/Dropbox/bot-battle-board"

        # OBJECT INITIALIZATION
        self.players = {}  # Dict of players, player_id -> player_object
        self.turn_handler = turn_handler.TurnHandler()  # Turn handler in charge of determining which unit acts when
        self.board = board_obj.Board(self.turn_handler, self.players, self.board_size)  # Board and the units
        self.user_commands = cmd_obj.Commands(self.board, self.turn_handler)
        self.interpreter = interpreter.Interpreter(self.turn_handler, self.user_commands)
        self.prompts = user_prompts_obj.Prompts(self.display_user_prompts, self.display_board)

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
            self.players[i + 1] = player_obj.Player(i + 1, self.interpreter.analyze(bot_cmds))

    def spawn_initial_units(self):
        # For each player, spawn one unit in a random location on the board_matrix. If the location has already
        # been picked, keep picking random locations until an available one has been found.
        spawn_locs = set()
        newloc = [randint(0, self.board_size[0] - 1), randint(0, self.board_size[1]) - 1]
        for player_id in self.players:
            while tuple(newloc) in spawn_locs:
                newloc = [randint(0, self.board_size[0] - 1), randint(0, self.board_size[1]) - 1]
            spawn_locs.add(tuple(newloc))
            self.board.spawn_unit(player_id, newloc)

    def turn_limit_reached(self):
        return self.turn_handler.turn_number >= self.turn_limit

    def turn(self):
        # Start turn (resetting all relevant state variables), execute script for current acting unit, and end turn
        self.turn_handler.start_turn()
        print("Turn number " + str(self.interpreter.turn_handler.turn_number))
        print("Acting unit: " + str(self.interpreter.turn_handler.current_unit().id))
        self.players[self.turn_handler.current_player()].command_script()
        self.turn_handler.end_turn()
        self.prompts.print_board(self.board)

    def remove_losing_players(self):
        # Check if any players have had all of their units destroyed, and remove them from the players list
        players_to_remove = []
        for player_id in self.players:
            if self.players[player_id].num_units() == 0:
                players_to_remove.append(player_id)
                print("Player " + str(player_id) + " eliminated")
        for player_id in players_to_remove:
            del self.players[player_id]

    def get_winner(self):
        return list(self.players)[0]

    def game_over(self):
        # Game ends when only one player has surviving units (or if turn limit is reached)
        return len(self.players) == 1

    def start_game(self):
        self.populate_players()
        self.spawn_initial_units()

        while not self.turn_limit_reached():
            self.turn()
            self.remove_losing_players()
            if self.game_over():
                print("Player " + str(self.get_winner()) + " has won the game")
                break
        if self.turn_limit_reached():
            print("Tie")


a = Game()
a.start_game()
