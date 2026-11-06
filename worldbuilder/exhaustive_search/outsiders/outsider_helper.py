from itertools import combinations

from worldbuilder.game_info import GameInfo
from worldbuilder.helper import is_outsider
from worldbuilder.exhaustive_search.outsiders.outsiders_info import OutsiderInfo, OutsiderInfoType
from worldbuilder.info import Info
from worldbuilder.info_type import InfoType


def determine_outsider_groups(
    info_indices: list[int],
    learned_info: list[OutsiderInfo],
    game_info: GameInfo,
):
    outsider_counts = game_info.get_possible_outsider_counts()
    player_count = game_info.player_count

    base_outsider_combinations: list[list[int]] = []
    for outsider_count in outsider_counts:
        base_outsider_combinations += [
            list(c)
            for c in combinations(range(player_count), outsider_count)
        ]

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
                        f"{info.info_type.name} received {len(info.target_players)} " +
                        "players when 1 was expected!"
                    )
                if info.seen_roles is None:
                    raise ValueError(
                        f"{info.info_type.name} has no stated role!")
                if len(info.seen_roles) != 1:
                    raise ValueError(
                        f"{info.info_type.name} received {len(info.seen_roles)} " +
                        "roles when 1 was expected!"
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

            case OutsiderInfoType.AT_LEAST_ONE_IS_OUTSIDER:
                if info.target_players is None:
                    raise ValueError(
                        f"{info.info_type.name} has no target players!")
                if info.seen_roles is None:
                    raise ValueError(
                        f"{info.info_type.name} has no stated role!")
                if len(info.seen_roles) != 1:
                    raise ValueError(
                        f"{info.info_type.name} received {len(info.seen_roles)} " +
                        "roles when 1 was expected!"
                    )

                role = info.seen_roles[0]
                players = info.target_players

                if not is_outsider(role):
                    raise ValueError(f"Role: {role.name} is not an outsider!")

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


def convert_outsider_info(info: Info) -> OutsiderInfo:
    match info.info_type:
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
            | InfoType.PLAYER_DAY_DEATH
        ):
            new_info = OutsiderInfo(
                info_type=OutsiderInfoType.NONE,
                source=info.source,
                day=info.day,
            )
            return new_info
        case (
            InfoType.PLAYER_IS_ROLE
            | InfoType.UNDERTAKER_INFO
            | InfoType.RAVENKEEPER_PING
            | InfoType.VIRGIN_TRIGGER
        ):
            new_info = OutsiderInfo(
                info_type=OutsiderInfoType.PLAYER_IS_ROLE,
                source=info.source,
                day=info.day,
                seen_roles=info.seen_roles,
                target_players=info.target_players,
            )
            return new_info
        case InfoType.LIBRARIAN_PING:
            new_info = OutsiderInfo(
                info_type=OutsiderInfoType.AT_LEAST_ONE_IS_OUTSIDER,
                source=info.source,
                day=info.day,
                seen_roles=info.seen_roles,
                target_players=info.target_players,
            )
            return new_info
        case InfoType.WASHERWOMAN_PING | InfoType.INVESTIGATOR_PING:
            new_info = OutsiderInfo(
                info_type=OutsiderInfoType.AT_LEAST_ONE_NOT_OUTSIDER,
                source=info.source,
                day=info.day,
                target_players=info.target_players,
            )
            return new_info

        case _:
            raise ValueError(f"Unhandled InfoType: {info.info_type.name}")
