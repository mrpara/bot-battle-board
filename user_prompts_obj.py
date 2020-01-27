class Prompts:
    # This object is in charge of displaying the user prompts and board_matrix state
    def __init__(self, display_user_prompts, display_board):
        self.display_user_prompts = display_user_prompts
        self.display_board = display_board

    def print_board(self, board):
        # Print the board_matrix matrix nicely formatted
        # Code taken from https://stackoverflow.com/questions/13214809/pretty-print-2d-python-list/32159502
        if self.display_board is True:
            output_mtx = []
            for row in board.board_matrix:
                output_mtx.append(['X' if elem is None else elem.id for elem in row])
            s = [[str(e) for e in row] for row in output_mtx]
            lens = [max(map(len, col)) for col in zip(*s)]
            fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
            table = [fmt.format(*row) for row in s]
            print('\n'.join(table))
