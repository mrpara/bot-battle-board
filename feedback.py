class Singleton(type):
    # Simple singleton metaclass implementation
    instance = None

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instance


class Feedback(metaclass=Singleton):
    # This object is in charge of displaying messages ("unit x attacked" etc) and board state
    def __init__(self, display_messages=True, display_board=True, write_to_file=False, file_path="log.txt"):
        self.display_messages = display_messages
        self.display_board = display_board
        self.write_to_file = write_to_file
        self.file_path = file_path
        if write_to_file is True:
            open(self.file_path, 'w').close()

    def display_message(self, message):
        if self.display_messages is True:
            print(message)
        self.to_file(message + '\n')

    def print_board(self, board):
        # Print the board_matrix matrix nicely formatted
        # Code taken from https://stackoverflow.com/questions/13214809/pretty-print-2d-python-list/32159502
        if self.display_board is True or self.write_to_file is True:
            output_mtx = []
            for row in board.board_matrix:
                output_mtx.append(['X' if elem is None else elem.id for elem in row])
            s = [[str(e) for e in row] for row in output_mtx]
            lens = [max(map(len, col)) for col in zip(*s)]
            fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
            table = [fmt.format(*row) for row in s]
            table_formatted = '\n'.join(table)

            if self.display_board is True:
                print(table_formatted)
            if self.write_to_file is True:
                self.to_file(table_formatted + '\n')

    def to_file(self, message):
        if self.write_to_file is not True:
            return
        with open(self.file_path, 'a') as file:
            file.write(message)
