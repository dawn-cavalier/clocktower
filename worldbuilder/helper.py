PLAYER_COUNT = 12
EVIL_COUNT = 3
from info import Info, InfoType

def build_world(info_indices: list[int], learned_info: list[Info]) -> list[float]:
    possible_teams: list[list[int]] = []

    # TODO: Handle different evil counts
    for i in range(PLAYER_COUNT):
        for j in range(i + 1, PLAYER_COUNT):
            for k in range(j + 1, PLAYER_COUNT):
                possible_teams.append([i, j, k])

    score = 1.0

    for info_index in info_indices:
        is_inverted = info_index < 0

        info = learned_info[abs(info_index)]
        if is_inverted:
            score = score * (1.0 - info.info_trust)
        else:
            score = score * info.info_trust

        info_index = max(info_index, 0)
        info = learned_info[info_index]

        match info.info_type:
            case InfoType.NONE:
                continue
            case InfoType.ALIGNMENT_KNOWN:
                if info.target_players is None:
                    raise ValueError(f"{info.info_type.name} has no target players!")

                # Ignore the information
                if is_inverted:
                    continue

                if info.is_good:
                    possible_teams = transform_player_good(
                        possible_teams, info.target_players[0]
                    )
                else:
                    possible_teams = transform_player_evil(
                        possible_teams, info.target_players[0]
                    )
            case InfoType.NUMBER_CHEF:
                if info.number is None:
                    raise ValueError(f"{info.info_type.name} has no number!")

                possible_teams = transform_chef_number(possible_teams, info.number)
            case _:
                raise ValueError(f"Unhandles InfoType: {info.info_type.name}")

    player_scores: list[float] = [
        score
        * get_player_appearances(possible_teams=possible_teams, target_player=player_id)
        for player_id in range(PLAYER_COUNT)
    ]

    # print(f"{info_indices} ({score}): {len(possible_teams)}/220")
    return player_scores


def get_player_appearances(possible_teams: list[list[int]], target_player: int) -> int:
    total = 0
    for team in possible_teams:
        if target_player in team:
            total += 1
    return total


def transform_player_good(
    evil_teams: list[list[int]], target_player: int
) -> list[list[int]]:
    return [key for key in evil_teams if target_player not in key]


def transform_player_evil(
    evil_teams: list[list[int]], target_player: int
) -> list[list[int]]:
    return [key for key in evil_teams if target_player in key]


def transform_chef_number(
    evil_teams: list[list[int]], chef_number: int
) -> list[list[int]]:
    return_value: list[list[int]] = []

    match chef_number:
        case 0:
            for key in evil_teams:
                if (
                    key[0] + 1 == key[1]
                    or key[1] + 1 == key[2]
                    or key[2] + 1 - PLAYER_COUNT == key[0]
                ):
                    continue

                return_value += [
                    (key),
                ]
        case 1:
            for key in evil_teams:
                # Right/ no overflow
                if key[0] + 2 == key[1] + 1 == key[2]:
                    continue

                # Center / overflow
                if key[0] + 1 == key[1] == key[2] + 1 - PLAYER_COUNT:
                    continue

                # Left / overflow
                if key[0] == key[1] + 2 - PLAYER_COUNT == key[2] + 1 - PLAYER_COUNT:
                    continue

                if (
                    key[0] + 1 == key[1]
                    or key[1] + 1 == key[2]
                    or key[2] + 1 - PLAYER_COUNT == key[0]
                ):
                    return_value += [
                        (key),
                    ]
        case 2:
            for key in evil_teams:
                # Right/ no overflow
                if key[0] + 2 == key[1] + 1 == key[2]:
                    return_value += [
                        (key),
                    ]

                # Center / overflow
                if key[0] + 1 == key[1] == key[2] + 2 - PLAYER_COUNT:
                    return_value += [
                        (key),
                    ]

                # Left / overflow
                if key[0] == key[1] + 2 - PLAYER_COUNT == key[2] + 1 - PLAYER_COUNT:
                    return_value += [
                        (key),
                    ]
        case _:
            raise ValueError("Invalid Chef Number")

    return return_value
