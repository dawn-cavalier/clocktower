from enum import IntEnum


class EvilTeamInfoType(IntEnum):
    NONE = -1
    ALIGNMENT_KNOWN = 0
    AT_LEAST_ONE_GOOD = 1
    AT_LEAST_ONE_EVIL = 2
    EXACTLY_ONE_EVIL = 3
    NUMBER_CHEF = 4
    NUMBER_EMPATH = 5
    FORTUNE_TELLER_RESPONSE = 6


class EvilTeamInfo:
    info_type: EvilTeamInfoType
    source: int
    invert: bool
    day: int
    number: int | None
    is_good: bool | None
    is_yes: bool | None
    target_players: list[int] | None

    info_trust = 1.0

    def __init__(
        self,
        info_type: EvilTeamInfoType,
        source: int,
        day: int,
        *,
        number: int | None = None,
        is_good: bool | None = None,
        is_yes: bool | None = None,
        target_players: list[int] | None = None,
    ) -> None:
        self.info_type = info_type
        self.source = source
        self.day = day

        self.number = number
        self.is_good = is_good
        self.is_yes = is_yes
        self.target_players = target_players
