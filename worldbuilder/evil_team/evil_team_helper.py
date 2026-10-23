from worldbuilder.game_info import GameInfo
from worldbuilder.evil_team.evil_team_info import EvilTeamInfo, EvilTeamInfoType
from worldbuilder.evil_team.evil_team_transformers import (
    transform_chef_number,
    transform_player_good,
    transform_player_evil,
    transform_at_least_one_good,
    transform_at_least_one_evil,
    transform_exactly_one_evil,
    transform_empath_number,
)
from worldbuilder.helper import calculate_combinations


def get_possible_evil_teams(
    info_indices: list[int],
    learned_info: list[EvilTeamInfo],
    game_info: GameInfo,
):
    evil_count = game_info.minion_count_base + game_info.demon_count_base
    player_count = game_info.player_count

    possible_teams: list[list[int]] = []
    possible_teams += calculate_combinations(evil_count, player_count)

    for info_index in info_indices:
        is_inverted = info_index < 0

        info_index = max(info_index, 0)
        info = learned_info[info_index]

        # Ignore the information
        if is_inverted:
            continue

        match info.info_type:
            case EvilTeamInfoType.NONE:
                continue
            case EvilTeamInfoType.ALIGNMENT_KNOWN:
                if info.target_players is None:
                    raise ValueError(f"{info.info_type.name} has no target players!")
                if info.is_good is None:
                    raise ValueError(f"{info.info_type.name} has no stated alignment!")
                if len(info.target_players) != 1:
                    raise ValueError(
                        f"{info.info_type.name} received {len(info.target_players)} players when 1 was expected!"
                    )

                if info.is_good:
                    possible_teams = transform_player_good(
                        evil_teams=possible_teams, target_player=info.target_players[0]
                    )
                else:
                    possible_teams = transform_player_evil(
                        evil_teams=possible_teams, target_player=info.target_players[0]
                    )
            case EvilTeamInfoType.AT_LEAST_ONE_GOOD:
                if info.target_players is None:
                    raise ValueError(f"{info.info_type.name} has no target players!")

                possible_teams = transform_at_least_one_good(
                    evil_teams=possible_teams, target_players=info.target_players
                )
            case EvilTeamInfoType.AT_LEAST_ONE_EVIL:
                if info.target_players is None:
                    raise ValueError(f"{info.info_type.name} has no target players!")

                possible_teams = transform_at_least_one_evil(
                    evil_teams=possible_teams, target_players=info.target_players
                )
            case EvilTeamInfoType.EXACTLY_ONE_EVIL:
                if info.target_players is None:
                    raise ValueError(f"{info.info_type.name} has no target players!")

                possible_teams = transform_exactly_one_evil(
                    evil_teams=possible_teams, target_players=info.target_players
                )
            case EvilTeamInfoType.CHEF_NUMBER:
                if info.number is None:
                    raise ValueError(f"{info.info_type.name} has no number!")

                possible_teams = transform_chef_number(
                    evil_teams=possible_teams,
                    chef_number=info.number,
                    player_count=player_count,
                )
            case EvilTeamInfoType.EMPATH_NUMBER:
                if info.number is None:
                    raise ValueError(f"{info.info_type.name} has no number!")
                if info.target_players is None:
                    raise ValueError(f"{info.info_type.name} has no target players!")

                possible_teams = transform_empath_number(
                    evil_teams=possible_teams,
                    empath_number=info.number,
                    neighbors=info.target_players,
                )
            case _:
                raise ValueError(f"Unhandled InfoType: {info.info_type.name}")

    return possible_teams
