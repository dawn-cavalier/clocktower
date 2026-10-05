from enum import IntEnum


class InfoType(IntEnum):
    NONE = -1
    WASHERWOMAN_PING = 0
    LIBRARIAN_PING = 1
    INVESTIGATOR_PING = 2
    CHEF_NUMBER = 3
    EMPATH_NUMBER = 4
    FORTUNE_TELLER_PING = 5
    UNDERTAKER_INFO = 6
    RAVENKEEPER_PING = 7
    VIRGIN_PROC = 8
    VIRGIN_EXECUTE = 9
    SLAYER_SHOT = 10
    SLAYER_KILL = 11
    NO_NIGHT_DEATH = 12
    PLAYER_EXECUTED = 13
    PLAYER_NIGHT_DEATH = 14

class Info:
    def __init__(self) -> None:
        pass