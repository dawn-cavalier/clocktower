from worldbuilder.evilTeamInfo import EvilTeamInfo, EvilTeamInfoType
from worldbuilder.evilTeamTransformers import (
    transform_chef_number,
    transform_player_good,
    transform_player_evil,
    transform_at_least_one_good,
    transform_at_least_one_evil,
    transform_exactly_one_evil,
    transform_empath_number,
)

PLAYER_COUNT = 12


def get_possible_evil_teams(info_indices: list[int], learned_info: list[EvilTeamInfo], evil_count: int):
    possible_teams: list[list[int]] = []
    # Spy Worlds
    add_all_possible_teams(possible_teams, evil_count - 1)
    # Spy + Recluse / Normal Worlds
    add_all_possible_teams(possible_teams, evil_count)
    # Recluse Worlds
    add_all_possible_teams(possible_teams, evil_count + 1)

    trust_score = 1.0

    for info_index in info_indices:
        is_inverted = info_index < 0

        info = learned_info[abs(info_index)]
        if is_inverted:
            trust_score = trust_score * (1.0 - info.info_trust)
        else:
            trust_score = trust_score * info.info_trust

        # TODO: Account for player trust

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
            case EvilTeamInfoType.NUMBER_CHEF:
                if info.number is None:
                    raise ValueError(f"{info.info_type.name} has no number!")

                possible_teams = transform_chef_number(
                    evil_teams=possible_teams,
                    chef_number=info.number,
                    player_count=PLAYER_COUNT,
                )
            case EvilTeamInfoType.NUMBER_EMPATH:
                if info.number is None:
                    raise ValueError(f"{info.info_type.name} has no number!")
                if info.target_players is None:
                    raise ValueError(f"{info.info_type.name} has no target players!")

                possible_teams = transform_empath_number(
                    evil_teams=possible_teams,
                    empath_number=info.number,
                    neighbors=info.target_players,
                )
            case EvilTeamInfoType.FORTUNE_TELLER_RESPONSE:
                if info.is_yes is None:
                    raise ValueError(f"{info.info_type.name} has no yes or no!")
                if info.target_players is None:
                    raise ValueError(f"{info.info_type.name} has no target players!")

            case _:
                raise ValueError(f"Unhandled InfoType: {info.info_type.name}")

    return (possible_teams, trust_score)


def add_all_possible_teams(possible_teams: list[list[int]], evil_count: int):
    if evil_count == 1:
        for i in range(PLAYER_COUNT):
            possible_teams.append([i])

    if evil_count == 2:
        for i in range(PLAYER_COUNT):
            for j in range(i + 1, PLAYER_COUNT):
                possible_teams.append([i, j])

    if evil_count == 3:
        for i in range(PLAYER_COUNT):
            for j in range(i + 1, PLAYER_COUNT):
                for k in range(j + 1, PLAYER_COUNT):
                    possible_teams.append([i, j, k])

    if evil_count == 4:
        for i in range(PLAYER_COUNT):
            for j in range(i + 1, PLAYER_COUNT):
                for k in range(j + 1, PLAYER_COUNT):
                    for l in range(k + 1, PLAYER_COUNT):
                        possible_teams.append([i, j, k, l])

    if evil_count == 5:
        for i in range(PLAYER_COUNT):
            for j in range(i + 1, PLAYER_COUNT):
                for k in range(j + 1, PLAYER_COUNT):
                    for l in range(k + 1, PLAYER_COUNT):
                        for m in range(l + 1, PLAYER_COUNT):
                            possible_teams.append([i, j, k, l, m])


def get_player_appearances(
    possible_teams: list[list[int]], target_player: int
) -> float:
    if len(possible_teams) == 0:
        return 0

    total = 0
    present_worlds: list[int] = []
    for team in possible_teams:
        if len(team) not in present_worlds:
            present_worlds.append(len(team))

    # TODO: Remove magic numbers
    for team in possible_teams:
        if target_player in team:
            world_type_count = len([t for t in possible_teams if len(t) == len(team)])

            if 2 in present_worlds and 3 in present_worlds and 4 in present_worlds:
                if len(team) == 2:
                    total += (1 / 8) / world_type_count
                if len(team) == 3:
                    total += (4 / 8) / world_type_count
                if len(team) == 4:
                    total += (3 / 8) / world_type_count

            # TODO: double check these numbers
            elif (
                2 not in present_worlds and 3 in present_worlds and 4 in present_worlds
            ):
                if len(team) == 3:
                    total += (4 / 7) / world_type_count
                if len(team) == 4:
                    total += (3 / 7) / world_type_count

            elif (
                2 not in present_worlds
                and 3 not in present_worlds
                and 4 in present_worlds
            ):
                if len(team) == 4:
                    total += 1.0 / world_type_count

    return total


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
