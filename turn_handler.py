from collections import deque
import logging

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(1)


class TurnHandler:
    # This class handles keeping track of turns. Which is the active unit/player, turn order, etc.
    def __init__(self):
        self.queue = deque()
        self.turn_number = 0

    def current_unit(self):
        return self.queue[-1]

    def current_player(self):
        return self.current_unit().player

    def start_turn(self):
        self.turn_number += 1
        logger.log(20, "Turn number " + str(self.turn_number))
        logger.log(20, "Acting unit: " + str(self.current_unit().id))
        self.current_unit().on_new_turn()

    def end_turn(self):
        self.queue.appendleft(self.queue.pop())

    def add_to_queue(self, unit):
        self.queue.appendleft(unit)

    def remove_from_queue(self, unit):
        self.queue.remove(unit)

