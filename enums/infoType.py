from enum import IntEnum

class InfoType(IntEnum):
    COUNT_TOWNSFOLK = 0
    COUNT_OUTSIDERS = 1
    COUNT_MINIONS = 2
    COUNT_DEMONS = 3
    COUNT_PLAYERS = 4
    IN_PLAY_ROLE = 5
    
    IS_ROLE = 10
    NOT_IN_PLAY = 11

    