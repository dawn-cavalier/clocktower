from enum import IntEnum

from worldbuilder.rolesEnum import Role


class DemonInfoType(IntEnum):
    NONE = -1
    IS_ROLE = 0
    AT_LEAST_ONE_IS_ROLE = 1
    IS_DEAD = 2


class DemonInfo:
    info_type: DemonInfoType
    source: int
    invert: bool
    day: int
    info_trust: float

    seen_roles: list[Role] | None
    is_yes: bool | None
    target_players: list[int] | None

    def __init__(
        self,
        info_type: DemonInfoType,
        source: int,
        day: int,
        info_trust: float = 1.0,
        *,
        seen_roles: list[Role] | None = None,
        is_yes: bool | None = None,
        target_players: list[int] | None = None,
    ) -> None:
        self.info_type = info_type
        self.source = source
        self.day = day
        self.info_trust = info_trust
        self.seen_roles = seen_roles

        self.is_yes = is_yes
        self.target_players = target_players
