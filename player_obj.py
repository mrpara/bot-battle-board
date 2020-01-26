import numpy as np
from collections import deque
from random import randint


class Player:
    # This object represents a player and holds their unit, commands, etc
    def __init__(self, id):
        self.id = id
        self.units = set()

    def num_units(self):
        return len(self.units)