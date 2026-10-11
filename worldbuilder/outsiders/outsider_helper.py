from worldbuilder.game_info import GameInfo
from worldbuilder.helper import add_all_possible_combinations, is_outsider
from worldbuilder.outsiders.outsiders_info import OutsiderInfo, OutsiderInfoType


def get_possible_outsiders(
    info_indices: list[int],
    learned_info: list[OutsiderInfo],
    possible_evil_teams: list[list[int]],
    game_info: GameInfo,
):
    outsider_counts = game_info.get_possible_outsider_counts()
    player_count = game_info.player_count

    possible_outsiders: list[list[int]] = []
    for outsider_count in outsider_counts:
        add_all_possible_combinations(possible_outsiders, outsider_count, player_count)

    for info_index in info_indices:
        is_inverted = info_index < 0

        info_index = max(info_index, 0)
        info = learned_info[info_index]

        # Ignore the information
        if is_inverted:
            continue

        match info.info_type:
            case OutsiderInfoType.NONE:
                continue

            case OutsiderInfoType.PLAYER_IS_ROLE:
                if info.target_players is None:
                    raise ValueError(f"{info.info_type.name} has no target players!")
                if len(info.target_players) != 1:
                    raise ValueError(
                        f"{info.info_type.name} received {len(info.target_players)} players when 1 was expected!"
                    )
                if info.seen_roles is None:
                    raise ValueError(f"{info.info_type.name} has no stated role!")
                if len(info.seen_roles) != 1:
                    raise ValueError(
                        f"{info.info_type.name} received {len(info.seen_roles)} roles when 1 was expected!"
                    )

                player = info.target_players[0]
                role = info.seen_roles[0]

                if is_outsider(role):
                    possible_outsiders = [
                        outsiders
                        for outsiders in possible_outsiders
                        if player in outsiders
                    ]
                else:
                    possible_outsiders = [
                        outsiders
                        for outsiders in possible_outsiders
                        if player not in outsiders
                    ]

            case OutsiderInfoType.AT_LEAST_ONE_ROLE:
                if info.target_players is None:
                    raise ValueError(f"{info.info_type.name} has no target players!")
                if info.seen_roles is None:
                    raise ValueError(f"{info.info_type.name} has no stated role!")

            case _:
                raise ValueError(f"Unhandled InfoType: {info.info_type.name}")

    return possible_outsiders
