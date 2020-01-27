class Unit:
    # Class representing the basic unit (bot) and its state
    def __init__(self, board, unit_id, player_id, initial_loc):
        self.board = board  # The board_matrix the unit is on
        self.var_data = {}  # holds user-defined variable data

        # Unit identification
        self.id = unit_id
        self.player_id = player_id

        # State variables
        self.loc = initial_loc
        self.hp = 3
        self.spawn_timer = 0
        self.can_act = True
        self.defending = False

    def set_spawn(self, interval):
        # Begin spawn countdown. After interval units have passed and timer reaches 0, a new unit will be spawned.
        # In the meantime the unit is unable to act
        self.spawn_timer += interval
        self.can_act = False

    def on_new_turn(self):
        # Reset or update relevant state variables
        self.defending = False
        self.decrement_spawn_timer_and_spawn_if_ready()

    def decrement_spawn_timer_and_spawn_if_ready(self):
        # Decrement spawn timer (if active) and spawn new unit when it hits 0
        if self.spawn_timer > 0:
            self.spawn_timer -= 1
            if self.spawn_timer == 0:
                self.board.spawn_in_adjacent_location(self.player_id, self.loc)
                print(self.board.num_allies_around_unit(self))
                self.can_act = True

    def decrement_hp(self, dmg):
        # Reduce hp, check if unit dies
        self.hp -= dmg
        print("Unit " + str(self.id) + " took " + str(dmg) + " damage")
        if self.hp <= 0:
            self.kill()

    def kill(self):
        # Despawn unit from board_matrix
        self.board.despawn_unit(self)
        print("Unit " + str(self.id) + " destroyed")

    def defend(self):
        # Enter defense mode (unit will block next attack against it)
        self.defending = True

    def damage(self, dmg):
        # Unit is under attack for dmg points of damage. Check if unit is defending. If it is, break defense.
        # Otherwise, unit hp is decremented
        if self.defending is True:
            self.defending = False
            print("Unit " + str(self.id) + " defense broken")
            return
        self.decrement_hp(dmg)
