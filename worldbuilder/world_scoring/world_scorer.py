from itertools import combinations, permutations

from worldbuilder.game_info import GameInfo
from worldbuilder.helper import is_demon, is_minion, is_outsider, is_townsfolk
from worldbuilder.info import Info
from worldbuilder.info_type import InfoType


def search_world_scores(game_info: GameInfo, learned_info: list[Info]):
    is_evil_scores = [0.0 for _ in range(game_info.player_count)]
    is_demon_scores = [0.0 for _ in range(game_info.player_count)]
    is_backup_demon_scores = [0.0 for _ in range(game_info.player_count)]
    is_outsider_scores = [0.0 for _ in range(game_info.player_count)]


    all_evil_teams = combinations(
        range(game_info.player_count),
        game_info.demon_count_base + game_info.minion_count_base
    )
    evil_teams_scores: dict[tuple[int, ...], float] = {
        team: 1.0 for team in all_evil_teams
    }

    # World Processing
    for evil_team in evil_teams_scores:
        for info in learned_info:
            match info.info_type:
                case (
                    InfoType.NONE |
                    InfoType.PLAYER_IS_ROLE |
                    InfoType.UNDERTAKER_INFO |
                    InfoType.FORTUNE_TELLER_PING |
                    InfoType.PLAYER_DAY_DEATH |
                    InfoType.PLAYER_NIGHT_DEATH |
                    InfoType.NO_NIGHT_DEATH |
                    InfoType.PLAYER_EXECUTED
                ):
                    continue

                case (
                    InfoType.PLAYER_IS_ALIGNMENT |
                    InfoType.VIRGIN_EXECUTE
                ):
                    if info.target_players is None:
                        raise ValueError(
                            f"{info.info_type.name} has no target players!"
                        )
                    if info.is_good is None:
                        raise ValueError(
                            f"{info.info_type.name} has no stated alignment!"
                        )
                    if len(info.target_players) != 1:
                        raise ValueError(
                            f"{info.info_type.name} received " +
                            f"{len(info.target_players)} players when 1 was expected!"
                        )
                    is_good = info.is_good
                    player = info.target_players[0]
                    if is_good and player in evil_team:
                        evil_teams_scores[evil_team] *= 1 - info.info_trust

                    if not is_good and player not in evil_team:
                        evil_teams_scores[evil_team] *= 1 - info.info_trust

                case (
                    InfoType.WASHERWOMAN_PING |
                    InfoType.LIBRARIAN_PING |
                    InfoType.INVESTIGATOR_PING
                ):
                    if info.target_players is None:
                        raise ValueError(
                            f"{info.info_type.name} has no target players!"
                        )
                    if info.seen_roles is None:
                        raise ValueError(
                            f"{info.info_type.name} has no seen roles!"
                        )
                    if len(info.target_players) != 2:
                        raise ValueError(
                            f"{info.info_type.name} received " +
                            f"{len(info.target_players)} players when 2 was expected!"
                        )
                    if len(info.seen_roles) != 1:
                        raise ValueError(
                            f"{info.info_type.name} received " +
                            f"{len(info.seen_roles)} roles when 1 was expected!"
                        )

                    target_players = info.target_players
                    seen_role = info.seen_roles[0]
                    players_present_in_team = len([
                        player for player in evil_team if player in target_players
                    ])

                    # Investigator or Sage
                    if (
                        (is_minion(seen_role) or is_demon(seen_role)) and
                        players_present_in_team == 0
                    ):
                        evil_teams_scores[evil_team] *= 1 - info.info_trust

                    # Washerwoman and Librarian
                    if (
                        (is_townsfolk(seen_role) or is_outsider(seen_role)) and
                        players_present_in_team == 2
                    ):
                        evil_teams_scores[evil_team] *= 1 - info.info_trust

                case _:
                    raise ValueError(
                        f"Unhandled InfoType: {info.info_type.name}")

    # Evil Team Scoring
    total = sum(score for _, score in evil_teams_scores.items())
    is_evil_scores = [
        sum(
            score/total for world,
            score in evil_teams_scores.items() if player in world
        )
        for player in range(game_info.player_count)
    ]

    return (
        is_evil_scores,
        is_demon_scores,
        is_backup_demon_scores,
        is_outsider_scores
    )
