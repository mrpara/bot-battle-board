import interpreter
import board
import turn_handler
import player
import cmd
import argparse
import logging
from custom_logger_levels import LoggerLevels

# Setup logging
logger = logging.getLogger(__name__)


class Game:
    def __init__(self, filepaths,
                 board_size=None,
                 turn_limit=10000,
                 unit_limit_pct=0.05,
                 log_level=LoggerLevels.ActionMessage,
                 write_to_file=False,
                 log_path="log.txt"):

        if board_size is None:  # Avoid mutable default argument
            board_size = [20, 20]
        # Verify arguments
        if len(filepaths) < 2:
            raise Exception("Game requires at least two players. "
                            "Provide a file path for the script used for each player")
        if len(filepaths) > board_size[0] * board_size[1]:
            raise Exception("Cannot start game for " + str(len(filepaths)) + " players with board size "
                            + str(board_size) + " (" + str(board_size[0] * board_size[1]) +
                            " tiles). There must be more tiles than players")
        self.strategy_filepaths = filepaths

        # DEFAULT PARAMETERS
        self.board_size = board_size
        self.turn_limit = turn_limit
        self.unit_limit_pct = unit_limit_pct  # The maximum number of allowed units per player, as a percentage
        # of board capacity
        self.log_level = log_level  # Level of log info.
        # Use LoggerLevels.PrimaryInformation to only display win/lose messages,
        # LoggerLevels.SecondaryInformation to also display  turn numbers and the board, and
        # LoggerLevels.ActionMessage to also display action messages
        self.write_to_file = write_to_file
        self.log_path = log_path

        # OBJECT INITIALIZATION
        self.players = {}  # Dict of players, player_id -> player_object
        self.turn_handler = turn_handler.TurnHandler()  # Turn handler in charge of determining which unit acts when
        self.board = board.Board(self.turn_handler, self.players,
                                 self.board_size, self.unit_limit_pct)  # Board and units
        self.user_commands = cmd.Commands(self.board, turn_handler.TurnHandlerInterface(self.turn_handler))
        self.interpreter = interpreter.Interpreter(self.user_commands)

        # CONFIGURE LOGGER
        self.configure_logger()

    def configure_logger(self):
        # Configure the logger and its handlers
        formatter = logging.Formatter('%(message)s')
        handlers = []

        # Handler for stream output
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(self.log_level)
        stream_handler.setFormatter(formatter)
        handlers.append(stream_handler)

        # Handler for file output
        if self.write_to_file:
            file_handler = logging.FileHandler(self.log_path, mode='w', encoding='utf-8')
            file_handler.setLevel(self.log_level)
            file_handler.setFormatter(formatter)
            handlers.append(file_handler)

        logging.basicConfig(handlers=handlers, level=10)

    def populate_players(self):
        # For each player, read their script and analyze it, and create a new player object
        # with the resulting instructions
        for idx, path in enumerate(self.strategy_filepaths):
            with open(path, 'r') as input_file:
                bot_cmds = input_file.read()
            self.players[idx + 1] = player.Player(idx + 1, self.interpreter.analyze(bot_cmds))

    def spawn_initial_units(self):
        # For each player, spawn one unit in a random location on the board_matrix. If the location has already
        # been picked, keep picking random locations until an available one has been found.
        spawn_locs = set()
        newloc = self.board.get_random_location()
        for player_id, player_inst in self.players.items():
            while tuple(newloc) in spawn_locs:
                newloc = self.board.get_random_location()
            spawn_locs.add(tuple(newloc))
            self.board.spawn_unit(player_inst, newloc)

    def turn_limit_reached(self):
        return self.turn_handler.turn_number >= self.turn_limit

    def turn(self):
        # Start turn (resetting all relevant state variables), set context for interpreter, execute script for current
        # acting unit, and end turn
        self.turn_handler.start_turn()
        self.interpreter.set_context(self.turn_handler.current_unit().var_data)
        self.turn_handler.current_player().command_script()
        self.turn_handler.end_turn()
        self.board.print_board()
        self.remove_losing_players()

    def remove_losing_players(self):
        # Check if any players have had all of their units destroyed, and remove them from the players list
        players_to_remove = []
        for player_id, player_r in self.players.items():
            if player_r.num_units() == 0:
                players_to_remove.append(player_id)
                logger.log(LoggerLevels.PrimaryInformation, "Player " + str(player_id) + " eliminated")
        for player_id in players_to_remove:
            del self.players[player_id]

    def announce_winner(self):
        # Check and report the winning player(s).
        # If only one player remains, they win. Otherwise, check number of remaining units per player.
        # The winners are all the players who hold the highest number of remaining units.

        if self.one_player_left():
            winning_player = list(self.players.values())[0]
            logger.log(LoggerLevels.PrimaryInformation, "Player " + str(winning_player.id) + " has won the game")
            return winning_player.id

        #  Make a player id -> remaining units dict, check max value, then get all player ids with this max value
        remaining_units = {player_id: self.players[player_id].num_units() for player_id in self.players}
        max_num_units_left = max(remaining_units.values())
        tied_players = [self.players[player_id] for player_id in remaining_units
                        if self.players[player_id].num_units() == max_num_units_left]

        if len(tied_players) == 1:
            logger.log(LoggerLevels.PrimaryInformation, "Turn limit reached, player " + str(tied_players[0].id)
                       + " wins with " + str(max_num_units_left) + " units remaining")
            return tied_players[0].id

        tied_player_ids = [t_player.id for t_player in tied_players]
        logger.log(LoggerLevels.PrimaryInformation, "Turn limit reached, players " + str(tied_player_ids)
                   + " are tied with " + str(max_num_units_left) + " units remaining")
        return tied_player_ids

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

        return self.announce_winner()


def main():
    # Argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filepaths', nargs='*', help='Filepaths for bot strategy scripts')
    paths = parser.parse_args().filepaths

    game = Game(paths)
    game.start_game()


if __name__ == "__main__":
    main()
