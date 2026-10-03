from info import Info, InfoType
from transformers import (
    transform_chef_number,
    transform_player_evil,
    transform_player_good,
    transform_at_least_one_good,
)

PLAYER_COUNT = 12
EVIL_COUNT = 3


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

                # Ignore the information
                if is_inverted:
                    continue

                possible_teams = transform_chef_number(possible_teams, info.number)
            case InfoType.AT_LEAST_ONE_GOOD:
                if info.target_players is None:
                    raise ValueError(f"{info.info_type.name} has no target players!")

                # Ignore the information
                if is_inverted:
                    continue

                possible_teams = transform_at_least_one_good(possible_teams, info.target_players)

            case _:
                raise ValueError(f"Unhandled InfoType: {info.info_type.name}")

    player_scores: list[float] = [
        score
        * get_player_appearances(possible_teams=possible_teams, target_player=player_id)
        for player_id in range(PLAYER_COUNT)
    ]

    print(f"{info_indices} ({score}): {len(possible_teams)}/220")
    return player_scores


def get_player_appearances(
    possible_teams: list[list[int]], target_player: int
) -> float:
    total = 0
    for team in possible_teams:
        if target_player in team:
            total += 1
    return total / len(possible_teams)


def get_all_posibilities(num_of_info: int):
    num_possibilities = 2**num_of_info
    possibilities: list[list[int]] = []

    for possibility_i in range(num_possibilities):
        new_possibility: list[int] = []
        for bit in range(num_of_info):
            if possibility_i >> bit & 1:
                new_possibility.append(bit + 1)
            else:
                new_possibility.append(-(bit + 1))
        possibilities.append(new_possibility)

    return possibilities
