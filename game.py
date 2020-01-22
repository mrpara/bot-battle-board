import interpreter
import board_obj

tst_board = board_obj.Board()
intr = interpreter.Interpreter(tst_board)
# n = intr.analyze("iff(lt(5,3), prnt(mul(3, 5)), prnt(div(10, 2)))")
# n()
# a = intr.analyze("spawn()")
#a()
#a()
#a()

a = intr.analyze("iff(eq(get_unit_id(), 1), prnt(get_unit_id()) spawn(), prnt(0) move())")

#get_unit_id()
intr.board.start_turn()
a()
for i in range(500):
    intr.board.start_turn()
    a()
# print(intr.board.current_unit().var_data)

intr.board.start_turn()

# b = intr.analyze("define(x, 2) define(g, 5)")
# a = intr.analyze("define(h, 7)")
b = intr.analyze("prnt(5)   \n  define(f, 9) \n define(j, 6)")
# b = intr.analyze("prnt(5)  prnt(78)")

# a()
# print(intr.board.current_unit().var_data)
# b()
b()
print(intr.board.current_unit().var_data)