from dataclasses import dataclass
from enum import Enum
from math import comb

from helper import is_minion, is_outsider, is_townsfolk
from worldbuilder.info_type import InfoType
from role_enum import Role


class Param(Enum):
    SEEN_ROLES = 0
    TARGET_PLAYERS = 1
    NUMBER = 2
    IS_YES = 3
    IS_GOOD = 4


@dataclass
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
    odds_sober: float = 1.0

    def __init__(
        self,
        info_type: InfoType,
        day: int,
        source: int,
        odds_sober: float = 1.0,
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

        self.seen_roles = seen_roles
        self.target_players = target_players
        self.number = number
        self.is_yes = is_yes
        self.is_good = is_good

        self.odds_sober = odds_sober

        # TODO: Need to figure out how to better enforce
        #       these objects being correctly constructed
        # Validation
        if 0.0 > odds_sober or odds_sober > 1.0:
            raise ValueError(
                f"Info trust was {odds_sober} when it was expected to be between 0 and 1!"
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
                InfoType.SAGE_PING |
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
                raise NotImplementedError(
                    f"Unhandled InfoType: {info_type.name}"
                )

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

    def count_possible_outputs(
        self,
        *,
        player_count: int = -1,
        evil_count: int = -1,
        script: set[Role] | None = None
    ):
        script = script if script else set()
        match self.info_type:
            case (
                InfoType.NONE |
                InfoType.PLAYER_DAY_DEATH |
                InfoType.PLAYER_EXECUTED |
                InfoType.PLAYER_NIGHT_DEATH |
                InfoType.NO_NIGHT_DEATH |
                InfoType.VIRGIN_EXECUTE |
                InfoType.VIRGIN_TRIGGER |
                InfoType.SLAYER_SHOT
            ):
                return 1
            case InfoType.PLAYER_IS_ROLE:
                # TODO: Add Drunk, Lunatic and Marionette handling here
                assert len(script) > 0, (
                    f"Script param is required for {self.info_type.name}!"
                )
                assert self.seen_roles is not None, (
                    f"{self.info_type.name} has no seen roles!"
                )
                assert len(self.seen_roles) == 1, (
                    f"{self.info_type.name} received " +
                    f"{len(self.seen_roles)} roles when 1 was expected!"
                )
                seen_role = self.seen_roles[0]
                # TODO: Handle Hermit, Lunatic, and Marionette
                if is_townsfolk(seen_role) and Role.DRUNK in script:
                    return 2

                return 1
            case InfoType.PLAYER_IS_ALIGNMENT:
                # TODO: Add Drunk, Lunatic and Marionette handling here
                return 2
            case InfoType.RAVENKEEPER_PING | InfoType.UNDERTAKER_INFO:
                assert len(script) > 0, (
                    f"Script param is required for {self.info_type.name}!"
                )
                return len(script) - 1
            case InfoType.CHEF_NUMBER:
                assert evil_count > 0, (
                    f"Evil Counts Param required for {self.info_type.name}!"
                )
                return evil_count
            case InfoType.EMPATH_NUMBER:
                return 3
            case InfoType.FORTUNE_TELLER_PING:
                return 2
            case InfoType.WASHERWOMAN_PING:
                assert len(script) > 0, (
                    f"Script param is required for {self.info_type.name}!"
                )
                townsfolk_role_count = sum(
                    is_townsfolk(role)
                    for role
                    in script
                ) - 1

                return (
                    townsfolk_role_count *
                    comb(player_count - 1, 2)
                )
            case InfoType.LIBRARIAN_PING:
                assert len(script) > 0, (
                    f"Script param is required for {self.info_type.name}!"
                )
                outsider_role_count = sum(
                    is_outsider(role)
                    for role
                    in script
                )

                return (
                    outsider_role_count *
                    comb(player_count - 1, 2)
                )
            case InfoType.INVESTIGATOR_PING:
                assert len(script) > 0, (
                    f"Script param is required for {self.info_type.name}!"
                )
                outsider_role_count = sum(
                    is_minion(role)
                    for role
                    in script
                )

                return (
                    outsider_role_count *
                    comb(player_count - 1, 2)
                )
            case InfoType.SAGE_PING:
                return comb(player_count - 1, 2)

            case _:
                raise ValueError(
                    f"{self.info_type.name} is currently unhandled!"
                )
