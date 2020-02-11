import logging

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(1)


class Unit:
    # Class representing the basic unit (bot) and its state
    def __init__(self, board, unit_id, player, initial_loc, initial_hp=3):
        self.board = board  # The board_matrix the unit is on
        self.var_data = {}  # holds user-defined variable data

        # Unit identification
        self.id = unit_id
        self.player = player

        # State variables
        self.loc = initial_loc
        self.hp = initial_hp
        self.spawn_timer = 0
        self.charge_timer = 0
        self.charge_strength = 0
        self.unit_turn_number = 0
        self.defending = False
        self.performed_critical_action = False  # Critical actions are user-commands such as attack() or move(),
        # which may not be performed more than once a turn

    def set_spawn(self, interval):
        # Begin spawn countdown. After interval units have passed and timer reaches 0, a new unit will be spawned.
        # In the meantime the unit is unable to act
        self.spawn_timer += interval

    def on_new_turn(self):
        # Reset or update relevant state variables
        self.unit_turn_number += 1
        self.defending = False
        self.performed_critical_action = False
        self.decrement_spawn_timer_and_spawn_if_ready()
        self.decrement_charge_timer_and_attack_if_ready()

    def decrement_spawn_timer_and_spawn_if_ready(self):
        # Decrement spawn timer (if active) and spawn new unit when it hits 0, returning the state of the spawn
        # (True if spawn succeeded, False if not)
        if self.spawn_timer > 0:
            self.spawn_timer -= 1
            if self.spawn_timer == 0:
                return self.board.spawn_in_adjacent_location(self.player, self.loc)
        return False

    def decrement_hp(self, dmg):
        # Reduce hp, check if unit dies (return True if it does, False otherwise - for testing purposes)
        self.hp -= dmg
        logger.log(10, "Unit " + str(self.id) + " took " + str(dmg) + " damage")
        if self.hp <= 0:
            self.kill()
            return True
        return False

    def kill(self):
        # Despawn unit from board_matrix
        self.board.despawn_unit(self)
        logger.log(10, "Unit " + str(self.id) + " destroyed")

    def defend(self):
        # Enter defense mode (unit will block next attack against it)
        self.defending = True

    def attack(self, dmg):
        # Attack adjacent enemy for dmg points of damage
        self.board.attack_adjacent_enemy(self, dmg)

    def charge_attack(self, num_turns):
        # Set timer on charge attack, or simply attack if called to wait 0 turns
        if num_turns == 0:
            self.attack(1)
        else:
            logger.log(10, "Unit " + str(self.id) + " is charging an attack!")
            self.charge_timer = num_turns

    def decrement_charge_timer_and_attack_if_ready(self):
        # Decrement charge timer (if active) and attack when it hits 0
        if self.charge_timer > 0:
            self.charge_timer -= 1
            self.charge_strength += 1
            if self.charge_timer == 0:
                dmg = (self.charge_strength + 1) * (self.charge_strength + 2) / 2
                self.attack(int(dmg))
                self.charge_strength = 0

    def damage(self, dmg):
        # Unit is under attack for dmg points of damage. Check if unit is defending. If it is, break defense.
        # Otherwise, unit hp is decremented
        if self.defending:
            self.defending = False
            logger.log(10, "Unit " + str(self.id) + " defense broken")
            return
        self.decrement_hp(dmg)

    def fortify(self):
        # Fortify command: gain 1 hp
        self.hp += 1

    def get_turn_number(self):
        # Return the number of turns this unit has been alive
        return self.unit_turn_number

    def can_act(self):
        # Verify that unit is able to act (has not performed a critical action this turn, and no timer is active)
        return self.spawn_timer == 0 \
               and self.charge_timer == 0 \
               and self.performed_critical_action is False

    def perform_critical_action(self):
        # Setter for critical action
        self.performed_critical_action = True
