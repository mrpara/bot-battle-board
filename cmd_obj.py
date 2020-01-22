import inspect


# noinspection SpellCheckingInspection
class Commands:
    # This class handles verification and execution of allowable user-input commands
    def __init__(self, board, turn_handler):
        self.board = board
        self.turn_handler = turn_handler

    def verify_command(self, cmd, args):
        # Chceck that input command is defined in this class, and correct number of arguments is provided
        try:
            num_expected_args = len(inspect.signature(getattr(self, cmd)).parameters)
        except AttributeError:
            raise Exception("Unknown command " + cmd + "()!")
        if len(args) != num_expected_args:
            raise Exception("Invalid number of arguments; expected " + str(num_expected_args)
                            + " and got " + str(len(args)))

    def execute_command(self, cmd, args):
        if self.turn_handler.current_unit().can_act is True:
            return getattr(self, cmd)(*args)
        return None

    def define(self, symb, val):
        self.turn_handler.current_unit().var_data[symb] = val
        return True

    def get_unit_id(self):
        return self.turn_handler.current_unit().id

    @staticmethod
    def attack():
        print("attacking!")

    def move(self):
        self.turn_handler.perform_critical_action()
        unit_id = self.turn_handler.current_unit().id
        current_loc = self.turn_handler.current_unit().loc
        new_loc = self.board.get_free_adjacent_loc(current_loc)
        if new_loc is None:
            return
        self.board.move_unit(unit_id, new_loc)

    def spawn(self):
        self.turn_handler.perform_critical_action()
        self.turn_handler.current_unit().set_spawn(3)
        print("Setting spawn for unit " + str(self.turn_handler.current_unit().id) + " belonging to player " +
              str(self.turn_handler.current_unit().player_id) + " in 3 turns")

    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def sub(a, b):
        return a - b

    @staticmethod
    def mul(a, b):
        return a * b

    @staticmethod
    def div(a, b):
        if b == 0:
            raise Exception("Division by 0")
        return a / b

    @staticmethod
    def eq(a, b):
        return a == b

    @staticmethod
    def gt(a, b):
        return a > b

    @staticmethod
    def gqt(a, b):
        return a >= b

    @staticmethod
    def lt(a, b):
        return a < b

    @staticmethod
    def lqt(a, b):
        return a <= b

    @staticmethod
    def neg(a):
        return not a

    @staticmethod
    def prnt(a):
        print(a)

    @staticmethod
    def iff(pred, if_true, if_false):
        if pred:
            return if_true()
        else:
            return if_false()
