import inspect

# noinspection SpellCheckingInspection
class Cmd:
    # This class handles verification and execution of allowable user-input commands
    def __init__(self, board):
        self.board = board

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
        if self.board.can_act is True:
            return getattr(self, cmd)(*args)
        return None

    def define(self, symb, val):
        self.board.current_unit().var_data[symb] = val
        return True

    def get_unit_id(self):
        return self.board.current_unit().id

    @staticmethod
    def attack():
        print("attacking!")

    def move(self):
        unit_id = self.board.current_unit().id
        current_loc = self.board.current_unit().loc
        if self.board.num_free_tiles_around_unit(unit_id) == 0:
            self.board.end_turn()
            return
        new_loc = self.board.get_adjacent_loc(current_loc)
        while not self.board.is_free(new_loc):
            new_loc = self.board.get_adjacent_loc(current_loc)
        self.board.move_unit(unit_id, new_loc)
        self.board.end_turn()
        # print(self.board.board)

    def spawn(self):
        # NEEDS REWORK
        unit_id = self.board.current_unit().id
        player_id = self.board.current_unit().player_id
        current_loc = self.board.current_unit().loc
        if self.board.num_free_tiles_around_unit(unit_id) == 0:
            self.board.end_turn()
            return
        spawn_loc = self.board.get_adjacent_loc(current_loc)
        while not self.board.is_free(spawn_loc):
            spawn_loc = self.board.get_adjacent_loc(current_loc)
        self.board.spawn_unit(player_id, spawn_loc)
        self.board.end_turn()
        print(self.board.board)
        # print(self.board.num_free_tiles_around_unit(unit_id))

    def end_turn(self):
        self.board.can_act = False

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
