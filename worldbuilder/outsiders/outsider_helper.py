from worldbuilder.game_info import GameInfo
from worldbuilder.helper import add_all_possible_combinations, is_outsider
from worldbuilder.outsiders.outsiders_info import OutsiderInfo, OutsiderInfoType


def get_possible_outsiders(
    info_indices: list[int],
    learned_info: list[OutsiderInfo],
    game_info: GameInfo,
):
    outsider_counts = game_info.get_possible_outsider_counts()
    player_count = game_info.player_count

    # possible_outsiders: list[list[list[int]]] = []

    base_outsider_combinations: list[list[int]] = []
    for outsider_count in outsider_counts:
        add_all_possible_combinations(
            base_outsider_combinations, outsider_count, player_count
        )

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
                    raise ValueError(
                        f"{info.info_type.name} has no target players!")
                if len(info.target_players) != 1:
                    raise ValueError(
                        f"{info.info_type.name} received {len(info.target_players)} players when 1 was expected!"
                    )
                if info.seen_roles is None:
                    raise ValueError(
                        f"{info.info_type.name} has no stated role!")
                if len(info.seen_roles) != 1:
                    raise ValueError(
                        f"{info.info_type.name} received {len(info.seen_roles)} roles when 1 was expected!"
                    )

                player = info.target_players[0]
                role = info.seen_roles[0]

                if is_outsider(role):
                    base_outsider_combinations = [
                        outsiders
                        for outsiders in base_outsider_combinations
                        if player in outsiders
                    ]
                else:
                    base_outsider_combinations = [
                        outsiders
                        for outsiders in base_outsider_combinations
                        if player not in outsiders
                    ]

            case OutsiderInfoType.AT_LEAST_ONE_ROLE:
                if info.target_players is None:
                    raise ValueError(
                        f"{info.info_type.name} has no target players!")
                if info.seen_roles is None:
                    raise ValueError(
                        f"{info.info_type.name} has no stated role!")
                if len(info.seen_roles) != 1:
                    raise ValueError(
                        f"{info.info_type.name} received {len(info.seen_roles)} roles when 1 was expected!"
                    )

                role = info.seen_roles[0]
                players = info.target_players

                # If it's not an outsider, we ignore the info
                if not is_outsider(role):
                    continue

                new_possible_outsiders: list[list[int]] = []
                for outsiders in base_outsider_combinations:
                    valid = False
                    for player in players:
                        if player in outsiders:
                            valid = True
                            break

                    if valid:
                        new_possible_outsiders.append(outsiders)

                base_outsider_combinations = new_possible_outsiders

            case OutsiderInfoType.AT_LEAST_ONE_NOT_OUTSIDER:
                if info.target_players is None:
                    raise ValueError(
                        f"{info.info_type.name} has no target players!")

                players = info.target_players

                new_possible_outsiders: list[list[int]] = []
                for outsider_combination in base_outsider_combinations:
                    is_one_missing = False
                    for player in players:
                        if player not in outsider_combination:
                            is_one_missing = True
                            break

                    if is_one_missing:
                        new_possible_outsiders.append(outsider_combination)

                base_outsider_combinations = new_possible_outsiders
            case _:
                raise ValueError(f"Unhandled InfoType: {info.info_type.name}")

    return base_outsider_combinations
    # for evil_team in possible_evil_teams:
    #     outsider_combinations: list[list[int]] = list(base_outsider_combinations)
    #     for evil in evil_team:
    #         outsider_combinations = [
    #             outsiders
    #             for outsiders in outsider_combinations
    #             if evil not in outsiders
    #         ]

    #     outsider_combinations = [
    #         outsiders for outsiders in outsider_combinations if len(outsiders) > 0
    #     ]
    #     possible_outsiders.append(outsider_combinations)
    # return possible_outsiders
