from enum import Enum

from worldbuilder.role_enum import Role


class OutsiderInfoType(Enum):
    NONE = -1
    PLAYER_IS_ROLE = 0
    AT_LEAST_ONE_ROLE = 1


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
