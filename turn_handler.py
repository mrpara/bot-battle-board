import numpy as np
from unit_obj import Unit
from collections import deque
from random import randint


class TurnHandler:
    def __init__(self):
        self.can_act = False
        self.queue = deque()
        self.turn_number = 0
        self.performed_critical_action = None

    def current_unit(self):
        return self.queue[-1]

    def current_player(self):
        return self.current_unit().player_id

    def start_turn(self):
        self.performed_critical_action = False
        self.current_unit().on_new_turn()
        self.turn_number += 1

    def end_turn(self):
        self.queue.appendleft(self.queue.pop())

    def add_to_queue(self, unit):
        self.queue.appendleft(unit)

    def remove_from_queue(self, unit):
        self.queue.remove(unit)

    def perform_critical_action(self):
        self.performed_critical_action = True