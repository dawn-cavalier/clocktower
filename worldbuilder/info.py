from enum import Enum

from worldbuilder.demon.demonInfo import DemonInfo, DemonInfoType
from worldbuilder.evilTeam.evilTeamInfo import EvilTeamInfo, EvilTeamInfoType
from worldbuilder.rolesEnum import Role


# TODO: Sort this so that role information is underneath game information
class InfoType(Enum):
    NONE = -1
    WASHERWOMAN_PING = 0
    LIBRARIAN_PING = 1
    INVESTIGATOR_PING = 2
    CHEF_NUMBER = 3
    EMPATH_NUMBER = 4
    FORTUNE_TELLER_PING = 5
    UNDERTAKER_INFO = 6
    RAVENKEEPER_PING = 7
    VIRGIN_TRIGGER = 8
    VIRGIN_EXECUTE = 9
    SLAYER_SHOT = 10
    SLAYER_KILL = 11
    NO_NIGHT_DEATH = 12
    PLAYER_EXECUTED = 13
    PLAYER_NIGHT_DEATH = 14
    PLAYER_IS_ROLE = 15
    PLAYER_IS_ALIGNMENT = 16


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
            case InfoType.NONE:
                new_info = EvilTeamInfo(
                    info_type=EvilTeamInfoType.NONE,
                    source=self.source,
                    day=self.day,
                    info_trust=self.info_trust,
                )
                return new_info

            case InfoType.PLAYER_IS_ALIGNMENT:
                new_info = EvilTeamInfo(
                    info_type=EvilTeamInfoType.ALIGNMENT_KNOWN,
                    source=self.source,
                    day=self.day,
                    info_trust=self.info_trust,
                    is_good=self.is_good,
                    target_players=self.target_players,
                )
                return new_info

            case InfoType.PLAYER_IS_ROLE:
                new_info = EvilTeamInfo(
                    info_type=EvilTeamInfoType.ALIGNMENT_KNOWN,
                    source=self.source,
                    day=self.day,
                    info_trust=self.info_trust,
                    is_good=self.is_good,
                    target_players=self.target_players,
                )
                return new_info

            case InfoType.WASHERWOMAN_PING:
                new_info = EvilTeamInfo(
                    info_type=EvilTeamInfoType.AT_LEAST_ONE_GOOD,
                    source=self.source,
                    day=self.day,
                    info_trust=self.info_trust,
                    target_players=self.target_players,
                )
                return new_info

            case InfoType.LIBRARIAN_PING:
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

            case InfoType.FORTUNE_TELLER_PING:
                new_info = EvilTeamInfo(
                    info_type=EvilTeamInfoType.NONE,
                    source=self.source,
                    info_trust=self.info_trust,
                    day=self.day,
                )
                return new_info

            case InfoType.UNDERTAKER_INFO:
                new_info = EvilTeamInfo(
                    info_type=EvilTeamInfoType.ALIGNMENT_KNOWN,
                    source=self.source,
                    day=self.day,
                    target_players=self.target_players,
                    info_trust=self.info_trust,
                    is_good=self.is_good,
                )
                return new_info

            case InfoType.RAVENKEEPER_PING:
                new_info = EvilTeamInfo(
                    info_type=EvilTeamInfoType.ALIGNMENT_KNOWN,
                    source=self.source,
                    day=self.day,
                    target_players=self.target_players,
                    info_trust=self.info_trust,
                    is_good=self.is_good,
                )
                return new_info

            case InfoType.VIRGIN_TRIGGER:
                new_info = EvilTeamInfo(
                    info_type=EvilTeamInfoType.ALIGNMENT_KNOWN,
                    source=self.source,
                    day=self.day,
                    target_players=[self.source],
                    info_trust=self.info_trust,
                    is_good=self.is_good,
                )
                return new_info

            case InfoType.VIRGIN_EXECUTE:
                new_info = EvilTeamInfo(
                    info_type=EvilTeamInfoType.ALIGNMENT_KNOWN,
                    source=self.source,
                    day=self.day,
                    target_players=self.target_players,
                    info_trust=self.info_trust,
                    is_good=self.is_good,
                )
                return new_info

            case InfoType.SLAYER_SHOT:
                new_info = EvilTeamInfo(
                    info_type=EvilTeamInfoType.NONE,
                    source=self.source,
                    info_trust=self.info_trust,
                    day=self.day,
                )
                return new_info

            case InfoType.SLAYER_KILL:
                new_info = EvilTeamInfo(
                    info_type=EvilTeamInfoType.ALIGNMENT_KNOWN,
                    source=-1,
                    day=self.day,
                    info_trust=self.info_trust,
                    target_players=self.target_players,
                    is_good=self.is_good,
                )
                return new_info

            case InfoType.NO_NIGHT_DEATH:
                new_info = EvilTeamInfo(
                    info_type=EvilTeamInfoType.NONE,
                    source=self.source,
                    info_trust=self.info_trust,
                    day=self.day,
                )
                return new_info

            case InfoType.PLAYER_EXECUTED:
                new_info = EvilTeamInfo(
                    info_type=EvilTeamInfoType.NONE,
                    source=self.source,
                    info_trust=self.info_trust,
                    day=self.day,
                )
                return new_info

            case InfoType.PLAYER_NIGHT_DEATH:
                new_info = EvilTeamInfo(
                    info_type=EvilTeamInfoType.NONE,
                    source=self.source,
                    info_trust=self.info_trust,
                    day=self.day,
                )
                return new_info

            case _:
                raise ValueError(f"Unhandled InfoType: {self.info_type.name}")

    def get_demon_info(self) -> DemonInfo:
        match self.info_type:
            case InfoType.NONE:
                new_info = DemonInfo(
                    info_type=DemonInfoType.NONE,
                    source=self.source,
                    day=self.day,
                    info_trust=self.info_trust,
                )
                return new_info

            case InfoType.PLAYER_IS_ALIGNMENT:
                new_info = DemonInfo(
                    info_type=DemonInfoType.NONE,
                    source=self.source,
                    day=self.day,
                    info_trust=self.info_trust,
                )
                return new_info

            case InfoType.PLAYER_IS_ROLE:
                new_info = DemonInfo(
                    info_type=DemonInfoType.IS_ROLE,
                    source=self.source,
                    day=self.day,
                    info_trust=self.info_trust,
                    target_players=self.target_players,
                    seen_roles=self.seen_roles,
                )
                return new_info

            case InfoType.WASHERWOMAN_PING:
                new_info = DemonInfo(
                    info_type=DemonInfoType.AT_LEAST_ONE_IS_ROLE,
                    source=self.source,
                    day=self.day,
                    info_trust=self.info_trust,
                    target_players=self.target_players,
                    seen_roles=self.seen_roles,
                )
                return new_info

            case InfoType.LIBRARIAN_PING:
                new_info = DemonInfo(
                    info_type=DemonInfoType.AT_LEAST_ONE_IS_ROLE,
                    source=self.source,
                    day=self.day,
                    info_trust=self.info_trust,
                    target_players=self.target_players,
                    seen_roles=self.seen_roles,
                )
                return new_info

            case InfoType.INVESTIGATOR_PING:
                new_info = DemonInfo(
                    info_type=DemonInfoType.AT_LEAST_ONE_IS_ROLE,
                    source=self.source,
                    day=self.day,
                    info_trust=self.info_trust,
                    target_players=self.target_players,
                    seen_roles=self.seen_roles,
                )
                return new_info

            case InfoType.CHEF_NUMBER:
                new_info = DemonInfo(
                    info_type=DemonInfoType.NONE,
                    source=self.source,
                    day=self.day,
                    info_trust=self.info_trust,
                )
                return new_info

            case InfoType.EMPATH_NUMBER:
                new_info = DemonInfo(
                    info_type=DemonInfoType.NONE,
                    source=self.source,
                    day=self.day,
                    info_trust=self.info_trust,
                )
                new_info.info_trust = 1.0
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

            case InfoType.UNDERTAKER_INFO:
                new_info = DemonInfo(
                    info_type=DemonInfoType.IS_ROLE,
                    source=self.source,
                    day=self.day,
                    info_trust=self.info_trust,
                    target_players=self.target_players,
                    seen_roles=self.seen_roles,
                )
                return new_info

            case InfoType.RAVENKEEPER_PING:
                new_info = DemonInfo(
                    info_type=DemonInfoType.IS_ROLE,
                    source=self.source,
                    day=self.day,
                    info_trust=self.info_trust,
                    target_players=self.target_players,
                    seen_roles=self.seen_roles,
                )
                return new_info

            case InfoType.VIRGIN_TRIGGER:
                new_info = DemonInfo(
                    info_type=DemonInfoType.IS_ROLE,
                    source=self.source,
                    day=self.day,
                    info_trust=self.info_trust,
                    target_players=self.target_players,
                    seen_roles=self.seen_roles,
                )
                return new_info

            case InfoType.VIRGIN_EXECUTE:
                new_info = DemonInfo(
                    info_type=DemonInfoType.NONE,
                    source=self.source,
                    day=self.day,
                    info_trust=self.info_trust,
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

            case InfoType.NO_NIGHT_DEATH:
                new_info = DemonInfo(
                    info_type=DemonInfoType.NONE,
                    source=self.source,
                    day=self.day,
                    info_trust=self.info_trust,
                )
                return new_info

            case InfoType.PLAYER_EXECUTED:
                new_info = DemonInfo(
                    info_type=DemonInfoType.IS_DEAD,
                    source=self.source,
                    day=self.day,
                    info_trust=self.info_trust,
                    target_players=self.target_players,
                )
                return new_info

            case InfoType.PLAYER_NIGHT_DEATH:
                new_info = DemonInfo(
                    info_type=DemonInfoType.IS_DEAD,
                    source=self.source,
                    day=self.day,
                    info_trust=self.info_trust,
                    target_players=self.target_players,
                )
                return new_info

            case _:
                raise ValueError(f"Unhandled InfoType: {self.info_type.name}")
