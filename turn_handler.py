import numpy as np
from unit_obj import Unit
from collections import deque
from random import randint


class TurnHandler:
    def __init__(self):
        self.can_act = False
        self.queue = deque()
        self.turn_number = 0

    def current_unit(self):
        return self.queue[0]

    def start_turn(self):
        self.can_act = True
        self.turn_number += 1

    def end_turn(self):
        self.can_act = False
        self.queue.appendleft(self.queue.pop())

    def add_to_queue(self, unit):
        self.queue.append(unit)
