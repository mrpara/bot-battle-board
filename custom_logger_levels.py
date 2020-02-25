from enum import IntEnum

class LoggerLevels(IntEnum):
    PrimaryInformation = 30  # Used for win/lose messages and other critical info
    SecondaryInformation = 20  # Used for board display and turn numbers
    ActionMessage = 10  # Used for various action messages