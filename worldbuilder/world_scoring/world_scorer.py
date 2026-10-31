from itertools import combinations

from worldbuilder.game_info import GameInfo
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
    evil_teams_score_dict: dict[tuple[int, ...], float] = {
        team: 1.0 for team in all_evil_teams
    }

    for world_key in evil_teams_score_dict:
        for info in learned_info:
            match info.info_type:
                case InfoType.NONE:
                    continue
                case InfoType.PLAYER_IS_ALIGNMENT:
                    if info.target_players is None:
                        raise ValueError(
                            f"{info.info_type.name} has no target players!")
                    if info.is_good is None:
                        raise ValueError(
                            f"{info.info_type.name} has no stated alignment!")
                    if len(info.target_players) != 1:
                        raise ValueError(
                            f"{info.info_type.name} received {len(info.target_players)} players when 1 was expected!"
                        )

                case _:
                    raise ValueError(
                        f"Unhandled InfoType: {info.info_type.name}")

    return (is_evil_scores, is_demon_scores, is_backup_demon_scores, is_outsider_scores)
