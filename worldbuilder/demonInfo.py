from enum import IntEnum


class DemonInfoType(IntEnum):
    NONE = -1
    ALIGNMENT_KNOWN = 0
    AT_LEAST_ONE_GOOD = 1
    AT_LEAST_ONE_EVIL = 2
    EXACTLY_ONE_EVIL = 3
    NUMBER_CHEF = 4
    NUMBER_EMPATH = 5
    FORTUNE_TELLER_RESPONSE = 6


class DemonInfo:
    info_type: DemonInfoType
    source: int
    invert: bool
    day: int
    number: int | None
    is_good: bool | None
    is_yes: bool | None
    target_players: list[int] | None

    info_trust = 1.0
