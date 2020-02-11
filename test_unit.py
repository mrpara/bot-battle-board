import unittest
import board
import turn_handler
import player


class TestUnit(unittest.TestCase):
    # Class for unit testing the Unit object
    def setUp(self):
        self.turn_handler = turn_handler.TurnHandler()
        self.players = {0: player.Player(0, None), 1: player.Player(1, None), 2: player.Player(2, None)}

    def test_decrement_spawn_timer(self):
        # Spawn a unit, set its spawn timer and decrement it 3 times. First two times should only lower spawn
        # timer and return False, third should return True as a unit is spawned
        test_board = board.Board(self.turn_handler, self.players, [20, 20], 0.5)
        test_board.spawn_unit(self.players[0], [0, 0])
        unit = self.players[0].units.pop()
        unit.set_spawn(3)
        self.assertEqual(unit.spawn_timer, 3)
        self.assertFalse(unit.decrement_spawn_timer_and_spawn_if_ready())
        self.assertEqual(unit.spawn_timer, 2)
        self.assertFalse(unit.decrement_spawn_timer_and_spawn_if_ready())
        self.assertEqual(unit.spawn_timer, 1)
        self.assertTrue(unit.decrement_spawn_timer_and_spawn_if_ready())
        self.assertEqual(unit.spawn_timer, 0)

    def test_decrement_hp(self):
        # Spawn a unit, test that causing 1 damage won't kill it. Then cause 2 more damage, killing it.
        # Then spawn another unit, cause 10 damage and test that it dies immediately.
        test_board = board.Board(self.turn_handler, self.players, [20, 20], 0.5)
        test_board.spawn_unit(self.players[0], [0, 0])
        unit1 = self.turn_handler.current_unit()
        self.assertFalse(unit1.decrement_hp(1))
        self.assertTrue(unit1.decrement_hp(2))
        test_board.spawn_unit(self.players[0], [0, 0])
        unit2 = self.turn_handler.current_unit()
        self.assertTrue(unit2.decrement_hp(10))

    def test_charge_attack(self):
        # Test that a charge attack called with argument 0 attacks immediately.
        # Higher charge times are tested in test_decrease_charge_timer below
        test_board = board.Board(self.turn_handler, self.players, [20, 20], 0.5)
        test_board.spawn_unit(self.players[0], [0, 0])
        unit1 = self.players[0].units.pop()
        test_board.spawn_unit(self.players[1], [0, 1])
        unit2 = self.players[1].units.pop()
        unit1.charge_attack(0)
        self.assertEqual(unit2.hp, 2)

    def test_decrement_charge_timer(self):
        # Test that charge attacks are timed and executed correctly.
        # Set charge to 1, and test that the enemy takes 3 damage after 1 call to decrement_charge_timer
        # Then set to 2 and test that the enemy takes 6 damage after 2 calls
        test_board = board.Board(self.turn_handler, self.players, [20, 20], 0.5)
        test_board.spawn_unit(self.players[0], [0, 0])
        unit1 = self.players[0].units.pop()
        test_board.spawn_unit(self.players[1], [0, 1], 10)
        unit2 = self.players[1].units.pop()
        unit1.charge_attack(1)
        self.assertEqual(unit2.hp, 10)
        unit1.decrement_charge_timer_and_attack_if_ready()
        self.assertEqual(unit2.hp, 7)
        unit1.charge_attack(2)
        unit1.decrement_charge_timer_and_attack_if_ready()
        self.assertEqual(unit2.hp, 7)
        unit1.decrement_charge_timer_and_attack_if_ready()
        self.assertEqual(unit2.hp, 1)

    def test_damage(self):
        # Test that attempting to cause a unit damage while defending will not cause damage, but break defense
        # Then test that causing damage when not defending causes the desired amount of damage
        test_board = board.Board(self.turn_handler, self.players, [20, 20], 0.5)
        test_board.spawn_unit(self.players[0], [0, 0])
        unit1 = self.players[0].units.pop()
        unit1.defend()
        unit1.damage(1)
        self.assertFalse(unit1.defending)
        self.assertEqual(unit1.hp, 3)
        unit1.damage(2)
        self.assertEqual(unit1.hp, 1)


if __name__ == '__main__':
    unittest.main()
