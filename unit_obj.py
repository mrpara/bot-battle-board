import numpy as np
from collections import deque
from random import randint


class Unit:
    def __init__(self, unit_id, player_id, initial_loc):
        self.id = unit_id
        self.player_id = player_id
        self.var_data = {}
        self.loc = initial_loc
        self.hp = 3
