import interpreter
import board_obj
import turn_handler

# def turn

turn_handler = turn_handler.TurnHandler()
tst_board = board_obj.Board(turn_handler)
intr = interpreter.Interpreter(tst_board, turn_handler)
with open("test.txt", 'r') as input_file:
    test_script = input_file.read()
print(test_script)
# a = intr.analyze("iff(eq(get_unit_id(), 1), prnt(get_unit_id()) spawn(), prnt(0) move())")

#get_unit_id()
a = intr.analyze(test_script)
for i in range(500):
    print("Turn number " + str(intr.turn_handler.turn_number))
    print("Acting unit: " + str(intr.turn_handler.current_unit().id))
    intr.turn_handler.start_turn()
    a()
    intr.turn_handler.end_turn()
    tst_board.print_board()

# print(intr.board.current_unit().var_data)

# intr.board.start_turn()0

# b = intr.analyze("define(x, 2) define(g, 5)")
# a = intr.analyze("define(h, 7)")
# b = intr.analyze("prnt(5)   \n  define(f, 9) \n define(j, 6)")
# b = intr.analyze("prnt(5)  prnt(78)")

# a()
# print(intr.board.current_unit().var_data)
# b()
# b()
# print(intr.board.current_unit().var_data)