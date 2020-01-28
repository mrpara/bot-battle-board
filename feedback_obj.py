class Singleton(type):
    # Simple singleton metaclass implementation
    instance = None

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instance


class Feedback(metaclass=Singleton):
    # This object is in charge of displaying messages ("unit x attacked" etc) and board state
    def __init__(self, display_messages=True, display_board=True):
        self.display_messages = display_messages
        self.display_board = display_board

    def display_message(self, message):
        if self.display_messages is True:
            print(message)

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
