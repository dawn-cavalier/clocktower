from enum import Enum


class EvilTeamInfoType(Enum):
    NONE = -1
    ALIGNMENT_KNOWN = 0
    AT_LEAST_ONE_GOOD = 1
    AT_LEAST_ONE_EVIL = 2
    EXACTLY_ONE_EVIL = 3
    CHEF_NUMBER = 4
    EMPATH_NUMBER = 5


class EvilTeamInfo:
    info_type: EvilTeamInfoType
    source: int
    invert: bool
    day: int
    info_trust: float

    number: int | None
    is_good: bool | None
    is_yes: bool | None
    target_players: list[int] | None


    def __init__(
        self,
        info_type: EvilTeamInfoType,
        source: int,
        day: int,
        info_trust: float = 1.0,
        *,
        number: int | None = None,
        is_good: bool | None = None,
        is_yes: bool | None = None,
        target_players: list[int] | None = None,
    ) -> None:
        self.info_type = info_type
        self.source = source
        self.day = day
        self.info_trust = info_trust

        self.number = number
        self.is_good = is_good
        self.is_yes = is_yes
        self.target_players = target_players
