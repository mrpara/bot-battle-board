import unittest
import cmd
import player
import board
import turn_handler
import interpreter


class TestInterpreter(unittest.TestCase):
    # Class for unit testing the interpreter
    def setUp(self):
        # Setup necessary objects
        self.turn_handler = turn_handler.TurnHandler()
        self.players = {0: player.Player(0, None), 1: player.Player(1, None), 2: player.Player(2, None)}
        self.board = board.Board(self.turn_handler, self.players, [20, 20], 0.01)
        self.cmd = cmd.Commands(self.board, self.turn_handler)

        # The interpreter is mostly static so we can use one instance for all the tests
        self.interpreter = interpreter.Interpreter(self.turn_handler, self.cmd)

    def test_is_number(self):
        # Test is_number method
        self.assertTrue(self.interpreter.is_number(5))
        self.assertTrue(self.interpreter.is_number(-12.5))
        self.assertTrue(self.interpreter.is_number('5'))
        self.assertTrue(self.interpreter.is_number('-12.5'))
        self.assertFalse(self.interpreter.is_number('-12d'))
        self.assertFalse(self.interpreter.is_number('string'))

    def test_parse(self):
        # Test the parse method, which separates the input into different statements, except parts which are in
        # one or  more levels of parentheses. All linebreaks or consecutive whitespaces are converted to one whitespace
        test_input = "   test test2  \n  "
        test_output = ["test", "test2"]
        self.assertEqual(self.interpreter.parse(test_input), test_output)

        test_input = "   test(test2 \ntest3)  "
        test_output = ["test(test2 test3)"]
        self.assertEqual(self.interpreter.parse(test_input), test_output)

        test_input = "   test(test2)  test3"
        test_output = ["test(test2)", "test3"]
        self.assertEqual(self.interpreter.parse(test_input), test_output)

        test_input = "   test((test2)  test3) test4(test5)"
        test_output = ["test((test2) test3)", "test4(test5)"]
        self.assertEqual(self.interpreter.parse(test_input), test_output)

    def test_is_command(self):
        # Test the is_command method
        # A valid command is any string of the form string1(string2), where string 1 may not contain any spaces or
        # linebreaks
        self.assertTrue(self.interpreter.is_command("a(b)"))
        self.assertTrue(self.interpreter.is_command("a2(b c)"))
        self.assertFalse(self.interpreter.is_command("a (b c)"))
        self.assertFalse(self.interpreter.is_command("a(b c) "))
        self.assertFalse(self.interpreter.is_command("ab c)"))
        self.assertFalse(self.interpreter.is_command("a(b c"))

    def test_get_number_value(self):
        # This method gets a string representing a number (assume it has passed is_number), and must return the
        # numeric value. It must return int if it is whole or float if it is not.
        self.assertEqual(self.interpreter.get_number_value("5"), 5)
        self.assertIsInstance(self.interpreter.get_number_value("5"), int)
        self.assertEqual(self.interpreter.get_number_value("-5.0"), -5)
        self.assertIsInstance(self.interpreter.get_number_value("-5.0"), int)
        self.assertAlmostEqual(self.interpreter.get_number_value("5.69"), 5.69)

    def test_get_args(self):
        # Test the get_args method, which extracts the arguments of an input command from the first level of parentheses
        # Note that whitespaces and linebreaks are not ignored here. It can be assumed that the input is a
        # "valid command" as defined in is_command

        # Test base case
        test_input = "dummy(1, 2, 3)"
        test_output = ["1", " 2", " 3"]
        self.assertEqual(self.interpreter.get_args(test_input), test_output)

        # Test linebreak
        test_input = "dummy(1, 2, \n 3)"
        test_output = ["1", " 2", " \n 3"]
        self.assertEqual(self.interpreter.get_args(test_input), test_output)

        # Test that arguments in inner parentheses are not further decomposed
        test_input = "dummy(1, (2, 3))"
        test_output = ["1", " (2, 3)"]
        self.assertEqual(self.interpreter.get_args(test_input), test_output)

        # Test that an exception is raised if imbalanced parentheses are found
        test_input = "dummy(1, 2), 3)"
        with self.assertRaises(Exception):
            self.interpreter.get_args(test_input)
        test_input = "dummy(1, (2, 3)"
        with self.assertRaises(Exception):
            self.interpreter.get_args(test_input)

    def test_get_symbol_value(self):
        # Test the get_symbol_value method
        # This method looks at the current unit (as determined by the turn handler) and returns the value of the
        # provided symbol. If the symbol has not been defined, it raises an exception
        self.board.spawn_unit(self.players[0], [0, 0])
        with self.assertRaises(Exception):
            self.interpreter.get_symbol_value("x")
        self.interpreter.analyze("define(x, 5)")()
        self.assertEqual(self.interpreter.get_symbol_value("x"), 5)

    def test_eval_and_exec_general(self):
        # The eval_and_exec_general method takes a command (string) and a list of arguments, which are in
        # delta function form, i.e. the argument "5" is given as a delta function delta: 5
        # It can be assumed that both the command and the number of arguments are valid as this is checked separately
        # beforehand. Since the execute_command method which actually executes the command is tested separately
        # in test_cmd, here we need only test that the reduction of lambda functions to numbers and symbols (and then
        # symbols->numbers) is done correctly
        self.board.spawn_unit(self.players[0], [0, 0])

        # Test simple number arguments
        test_cmd = "add"
        test_args = [lambda: 5, lambda: 6]
        self.assertEqual(self.interpreter.eval_and_exec_general(test_cmd, test_args), 11)
        # Test case where an argument is a lambda for a symbol
        self.interpreter.analyze("define(x, 8)")()
        test_args = [lambda: "x", lambda: -7]
        self.assertEqual(self.interpreter.eval_and_exec_general(test_cmd, test_args), 1)
        # Test case where an argument is a different analyzed function
        test_cmd = "mul"
        test_args = [lambda: "x", self.interpreter.analyze("div(x, 2)")]
        self.assertEqual(self.interpreter.eval_and_exec_general(test_cmd, test_args), 32)

    def test_eval_and_exec_define(self):
        # As test_eval_and_exec_general, but the command is always "define", and while both arguments are called to
        # be reduced to numbers/symbols, only the second argument is fully resolved. If the first argument is a symbol,
        # it remains one.
        self.board.spawn_unit(self.players[0], [0, 0])

        # Test simple number arguments
        test_args = [lambda: "x", lambda: 5]
        self.interpreter.eval_and_exec_define(test_args)
        self.assertEqual(self.interpreter.get_symbol_value("x"), 5)
        # Test case where an argument is a different analyzed function
        test_args = [lambda: "y", self.interpreter.analyze("add(2, 5.5)")]
        self.interpreter.eval_and_exec_define(test_args)
        self.assertEqual(self.interpreter.get_symbol_value("y"), 7.5)

    def test_eval_and_exec_if_else(self):
        # As test_eval_and_exec_general, but the command is always "if_else", and only the first argument is reduced and
        # resolved.
        self.board.spawn_unit(self.players[0], [0, 0])

        # Test simple number arguments
        test_args = [lambda: True, lambda: 5, lambda: 7]
        self.assertEqual(self.interpreter.eval_and_exec_if_else(test_args), 5)
        # Test case where an argument is a different analyzed function
        test_args = [lambda: False, lambda: 5, self.interpreter.analyze("gt(8, -2)")]
        self.assertTrue(self.interpreter.eval_and_exec_if_else(test_args))

    def test_analyze(self):
        # Test the analyze method, which takes a string as input and returns lambda functions that run the relevant
        # commands. Essentially this test checks that the syntax of the programming language used for the bots behaves
        # as desired.
        self.board.spawn_unit(self.players[0], [0, 0])
        # Test primitives
        self.assertEqual(self.interpreter.analyze("-3")(), -3)
        self.assertEqual(self.interpreter.analyze("test")(), "test")
        # Test the basic case of a legitimate command
        self.assertEqual(self.interpreter.analyze("add(3, 2)")(), 5)
        # Test chained commands by running a define command and then an add using the value. The overall return value
        # should always be the return of the last command
        exc = self.interpreter.analyze("define(x, 2) add(x, 6)")
        self.assertEqual(exc(), 8)
        # Test for persistence (i.e. that defines are "remembered" between calls) and linebreak
        self.interpreter.analyze("define(y, -3) \n   define(z, -2)")()
        self.assertEqual(self.interpreter.analyze("mul(y, z)")(), 6)
        # Test that the false branch of an if statement returns 0
        self.assertEqual(self.interpreter.analyze("if(gt(1, 3), add(1, 1))")(), 0)
        # Test that wrong syntax raises an exception
        with self.assertRaises(Exception):  # Space between command and arguments
            self.interpreter.analyze("mul (2, 8)")()
        with self.assertRaises(Exception):  # Missing parentheses
            self.interpreter.analyze("mul(2, 8")()


if __name__ == '__main__':
    unittest.main()
