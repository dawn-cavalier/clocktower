from enum import IntEnum


class InfoType(IntEnum):
    NONE = -1
    ALIGNMENT_KNOWN = 0
    AT_LEAST_ONE_GOOD = 1
    AT_LEAST_ONE_EVIL = 2
    NUMBER_CHEF = 3
    NUMBER_EMPATH = 4


class Info:
    info_type: InfoType
    source: int
    invert: bool
    day: int
    number: int | None
    is_good: bool | None
    target_players: list[int] | None

    info_trust = 0.75

    def __init__(
        self,
        info_type: InfoType,
        source: int,
        day: int,
        *,
        number: int | None = None,
        is_good: bool | None = None,
        target_players: list[int] | None = None,
    ) -> None:
        self.info_type = info_type
        self.source = source
        self.day = day

        self.number = number
        self.is_good = is_good
        self.target_players = target_players
