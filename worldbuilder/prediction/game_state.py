from worldbuilder.demon.demon_helper import determine_demons
from worldbuilder.evil_team.evil_team_helper import determine_possible_evil_teams
from worldbuilder.game_info import GameInfo
from worldbuilder.info import Info
from worldbuilder.info_type import InfoType
from worldbuilder.outsiders.outsider_helper import determine_possible_outsider_groups
from worldbuilder.prediction.prediction_dataclasses import GameState


def build_game_state(learned_info: list[Info], possibility: list[int], game_info: GameInfo):
    game_state: GameState = GameState()

    (
        game_state.night_deaths,
        game_state.day_deaths,
        game_state.execution_deaths
    ) = __get_dead_players__(
        learned_info)

    evil_team_info = [info.get_evil_team_info() for info in learned_info]
    game_state.evil_teams = determine_possible_evil_teams(
        possibility, evil_team_info, game_info
    )

    demon_info = [info.get_demon_info() for info in learned_info]
    game_state.demons = determine_demons(
        possibility, demon_info, game_info)

    # Get possible Outsiders combinations
    outsider_info = [info.get_outsider_info() for info in learned_info]
    game_state.outsiders = determine_possible_outsider_groups(
        possibility, outsider_info, game_info
    )

    if len(game_info.script & game_info.__NIGHT_INSURANCE__) == 0:
        game_state.demons = [
            demon for demon in game_state.demons if demon not in game_state.night_deaths]

    if len(game_info.script & game_info.__DAY_INSURANCE__) == 0:
        game_state.demons = [
            demon for demon in game_state.demons if
            demon not in game_state.execution_deaths or demon not in game_state.day_deaths
        ]

    game_state.evil_teams = [evil_team for evil_team in game_state.evil_teams if len(
        [demon for demon in game_state.demons if demon in evil_team]) > 0]

    return game_state


def __get_dead_players__(learned_info: list[Info]):
    night_deaths: list[int] = []
    day_deaths: list[int] = []
    execution_deaths: list[int] = []
    for info in learned_info:
        info_type = info.info_type
        match info_type:
            case InfoType.PLAYER_NIGHT_DEATH:
                if info.target_players is None:
                    raise ValueError(
                        f"{info.info_type.name} has no target players!")

                night_deaths += info.target_players
            case InfoType.PLAYER_DAY_DEATH:
                if info.target_players is None:
                    raise ValueError(
                        f"{info.info_type.name} has no target players!")

                day_deaths += info.target_players
            case InfoType.PLAYER_EXECUTED:
                if info.target_players is None:
                    raise ValueError(
                        f"{info.info_type.name} has no target players!")

                execution_deaths += info.target_players
            case _:
                pass
    return (night_deaths, day_deaths, execution_deaths)
