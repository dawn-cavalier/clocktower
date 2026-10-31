from enum import Enum

from worldbuilder.role_enum import Role


class OutsiderInfoType(Enum):
    NONE = -1
    PLAYER_IS_ROLE = 0
    AT_LEAST_ONE_IS_OUTSIDER = 1
    AT_LEAST_ONE_NOT_OUTSIDER = 2

class OutsiderInfo:
    info_type: OutsiderInfoType
    source: int
    day: int

    seen_roles: list[Role] | None
    target_players: list[int] | None

    def __init__(
        self,
        info_type: OutsiderInfoType,
        source: int,
        day: int,
        *,
        seen_roles: list[Role] | None = None,
        target_players: list[int] | None = None,
    ) -> None:
        self.info_type = info_type
        self.source = source
        self.day = day

        self.seen_roles = seen_roles
        self.target_players = target_players
