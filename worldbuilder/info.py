from enum import Enum

from worldbuilder.info_type import InfoType
from worldbuilder.role_enum import Role


class Param(Enum):
    SEEN_ROLES = 0
    TARGET_PLAYERS = 1
    NUMBER = 2
    IS_YES = 3
    IS_GOOD = 4


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

        # TODO: Need to figure out how to better enforce
        #       these objects being correctly constructed
        # Validation
        assert 0.0 <= info_trust <= 1.0, (
            f"Info trust was {info_trust} when it was expected to be between 0 and 1!"
        )

        required_params: list[Param] = []
        match info_type:
            case InfoType.NONE | InfoType.NO_NIGHT_DEATH:
                pass
            case (
                InfoType.WASHERWOMAN_PING |
                InfoType.LIBRARIAN_PING |
                InfoType.INVESTIGATOR_PING |
                InfoType.UNDERTAKER_INFO |
                InfoType.RAVENKEEPER_PING |
                InfoType.VIRGIN_TRIGGER |
                InfoType.PLAYER_IS_ROLE
            ):
                required_params = [Param.SEEN_ROLES, Param.TARGET_PLAYERS]
            case InfoType.CHEF_NUMBER | InfoType.EMPATH_NUMBER:
                required_params = [Param.NUMBER]
            case InfoType.FORTUNE_TELLER_PING:
                required_params = [Param.TARGET_PLAYERS, Param.IS_YES]
            case InfoType.VIRGIN_EXECUTE | InfoType.PLAYER_IS_ALIGNMENT:
                required_params = [Param.TARGET_PLAYERS, Param.IS_GOOD]
            case (
                InfoType.SLAYER_SHOT |
                InfoType.PLAYER_DAY_DEATH |
                InfoType.PLAYER_EXECUTED |
                InfoType.PLAYER_NIGHT_DEATH
            ):
                required_params = [Param.TARGET_PLAYERS]
            case _:
                raise ValueError(
                    f"Unhandled InfoType: {info_type.name}")

        if Param.SEEN_ROLES in required_params and seen_roles is None:
            raise ValueError(
                f"{info_type.name} missing seen roles!"
            )

        if Param.TARGET_PLAYERS in required_params and target_players is None:
            raise ValueError(
                f"{info_type.name} missing target players!"
            )

        if Param.NUMBER in required_params and number is None:
            raise ValueError(
                f"{info_type.name} missing seen number!"
            )

        if Param.IS_YES in required_params and is_yes is None:
            raise ValueError(
                f"{info_type.name} missing yes/no flag!"
            )

        if Param.IS_GOOD in required_params and is_good is None:
            raise ValueError(
                f"{info_type.name} missing is good flag!"
            )
