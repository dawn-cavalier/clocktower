from worldbuilder.demon.demon_info import DemonInfo, DemonInfoType
from worldbuilder.evil_team.evil_team_info import EvilTeamInfo, EvilTeamInfoType
from worldbuilder.info_type import InfoType
from worldbuilder.outsiders.outsiders_info import OutsiderInfo, OutsiderInfoType
from worldbuilder.role_enum import Role


class Info:
    # All the time information
    info_type: InfoType
    day: int
    source: int

    # Some of the time information
    seen_roles: list[Role] | None
    target_players: list[int] | None
    number: int | None
    is_yes: bool | None
    is_good: bool | None

    # Internal Variables
    info_trust: float = 1.0
    invert: bool = False

    def __init__(
        self,
        info_type: InfoType,
        day: int,
        source: int,
        info_trust: float = 1.0,
        *,
        seen_roles: list[Role] | None = None,
        target_players: list[int] | None = None,
        number: int | None = None,
        is_yes: bool | None = None,
        is_good: bool | None = None,
    ) -> None:
        self.info_type = info_type
        self.day = day
        self.source = source
        self.info_trust = info_trust

        self.seen_roles = seen_roles
        self.target_players = target_players
        self.number = number
        self.is_yes = is_yes
        self.is_good = is_good

    def get_evil_team_info(self) -> EvilTeamInfo:
        match self.info_type:
            case (
                InfoType.NONE
                | InfoType.FORTUNE_TELLER_PING
                | InfoType.SLAYER_SHOT
                | InfoType.NO_NIGHT_DEATH
                | InfoType.PLAYER_EXECUTED
                | InfoType.PLAYER_NIGHT_DEATH
            ):
                new_info = EvilTeamInfo(
                    info_type=EvilTeamInfoType.NONE,
                    source=self.source,
                    day=self.day,
                    info_trust=self.info_trust,
                )
                return new_info

            case InfoType.PLAYER_IS_ALIGNMENT | InfoType.PLAYER_IS_ROLE:
                new_info = EvilTeamInfo(
                    info_type=EvilTeamInfoType.ALIGNMENT_KNOWN,
                    source=self.source,
                    day=self.day,
                    info_trust=self.info_trust,
                    is_good=self.is_good,
                    target_players=self.target_players,
                )
                return new_info

            case InfoType.WASHERWOMAN_PING | InfoType.LIBRARIAN_PING:
                new_info = EvilTeamInfo(
                    info_type=EvilTeamInfoType.AT_LEAST_ONE_GOOD,
                    source=self.source,
                    day=self.day,
                    info_trust=self.info_trust,
                    target_players=self.target_players,
                )
                return new_info

            case InfoType.INVESTIGATOR_PING:
                new_info = EvilTeamInfo(
                    info_type=EvilTeamInfoType.AT_LEAST_ONE_EVIL,
                    source=self.source,
                    day=self.day,
                    info_trust=self.info_trust,
                    target_players=self.target_players,
                )
                return new_info

            case InfoType.CHEF_NUMBER:
                new_info = EvilTeamInfo(
                    info_type=EvilTeamInfoType.CHEF_NUMBER,
                    source=self.source,
                    day=self.day,
                    info_trust=self.info_trust,
                    number=self.number,
                )
                return new_info

            case InfoType.EMPATH_NUMBER:
                new_info = EvilTeamInfo(
                    info_type=EvilTeamInfoType.EMPATH_NUMBER,
                    source=self.source,
                    day=self.day,
                    info_trust=self.info_trust,
                    number=self.number,
                    target_players=self.target_players,
                )
                return new_info

            case (
                InfoType.UNDERTAKER_INFO
                | InfoType.RAVENKEEPER_PING
                | InfoType.VIRGIN_TRIGGER
                | InfoType.VIRGIN_EXECUTE
                | InfoType.SLAYER_KILL
            ):
                new_info = EvilTeamInfo(
                    info_type=EvilTeamInfoType.ALIGNMENT_KNOWN,
                    source=self.source,
                    day=self.day,
                    target_players=self.target_players,
                    info_trust=self.info_trust,
                    is_good=self.is_good,
                )
                return new_info

            case _:
                raise ValueError(f"Unhandled InfoType: {self.info_type.name}")

    def get_demon_info(self) -> DemonInfo:
        match self.info_type:
            case (
                InfoType.NONE
                | InfoType.PLAYER_IS_ALIGNMENT
                | InfoType.CHEF_NUMBER
                | InfoType.EMPATH_NUMBER
                | InfoType.VIRGIN_EXECUTE
                | InfoType.NO_NIGHT_DEATH
                | InfoType.PLAYER_EXECUTED
                | InfoType.PLAYER_NIGHT_DEATH
            ):
                new_info = DemonInfo(
                    info_type=DemonInfoType.NONE,
                    source=self.source,
                    day=self.day,
                    info_trust=self.info_trust,
                )
                return new_info

            case (
                InfoType.PLAYER_IS_ROLE
                | InfoType.UNDERTAKER_INFO
                | InfoType.RAVENKEEPER_PING
                | InfoType.VIRGIN_TRIGGER
            ):
                new_info = DemonInfo(
                    info_type=DemonInfoType.IS_ROLE,
                    source=self.source,
                    day=self.day,
                    info_trust=self.info_trust,
                    target_players=self.target_players,
                    seen_roles=self.seen_roles,
                )
                return new_info

            case (
                InfoType.WASHERWOMAN_PING
                | InfoType.LIBRARIAN_PING
                | InfoType.INVESTIGATOR_PING
            ):
                new_info = DemonInfo(
                    info_type=DemonInfoType.AT_LEAST_ONE_IS_ROLE,
                    source=self.source,
                    day=self.day,
                    info_trust=self.info_trust,
                    target_players=self.target_players,
                    seen_roles=self.seen_roles,
                )
                return new_info

            case InfoType.FORTUNE_TELLER_PING:
                new_info = DemonInfo(
                    info_type=DemonInfoType.FORTUNE_TELLER_PING,
                    source=self.source,
                    day=self.day,
                    info_trust=self.info_trust,
                    target_players=self.target_players,
                    is_yes=self.is_yes,
                )
                return new_info

            case InfoType.SLAYER_SHOT:
                new_info = DemonInfo(
                    info_type=DemonInfoType.SLAYER_SHOT,
                    source=self.source,
                    day=self.day,
                    info_trust=self.info_trust,
                    target_players=self.target_players,
                )
                return new_info

            case InfoType.SLAYER_KILL:
                new_info = DemonInfo(
                    info_type=DemonInfoType.SLAYER_KILL,
                    source=self.source,
                    day=self.day,
                    info_trust=self.info_trust,
                    target_players=self.target_players,
                )
                return new_info
            case _:
                raise ValueError(f"Unhandled InfoType: {self.info_type.name}")

    def get_outsider_info(self) -> OutsiderInfo:
        match self.info_type:
            case (
                InfoType.NONE
                | InfoType.CHEF_NUMBER
                | InfoType.EMPATH_NUMBER
                | InfoType.FORTUNE_TELLER_PING
                | InfoType.SLAYER_SHOT
                | InfoType.NO_NIGHT_DEATH
                | InfoType.PLAYER_NIGHT_DEATH
                | InfoType.PLAYER_EXECUTED
                | InfoType.PLAYER_IS_ALIGNMENT
            ):
                new_info = OutsiderInfo(
                    info_type=OutsiderInfoType.NONE,
                    source=self.source,
                    day=self.day,
                )
                return new_info
            case (
                InfoType.PLAYER_IS_ROLE
                | InfoType.UNDERTAKER_INFO
                | InfoType.RAVENKEEPER_PING
                | InfoType.VIRGIN_TRIGGER
                | InfoType.SLAYER_KILL
            ):
                new_info = OutsiderInfo(
                    info_type=OutsiderInfoType.PLAYER_IS_ROLE,
                    source=self.source,
                    day=self.day,
                    seen_roles=self.seen_roles,
                    target_players=self.target_players,
                )
                return new_info
            case InfoType.LIBRARIAN_PING:
                new_info = OutsiderInfo(
                    info_type=OutsiderInfoType.AT_LEAST_ONE_ROLE,
                    source=self.source,
                    day=self.day,
                    seen_roles=self.seen_roles,
                    target_players=self.target_players,
                )
                return new_info
            case InfoType.WASHERWOMAN_PING | InfoType.INVESTIGATOR_PING:
                new_info = OutsiderInfo(
                    info_type=OutsiderInfoType.AT_LEAST_ONE_NOT_OUTSIDER,
                    source=self.source,
                    day=self.day,
                    target_players=self.target_players,
                )
                return new_info

            case _:
                raise ValueError(f"Unhandled InfoType: {self.info_type.name}")
