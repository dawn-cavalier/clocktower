from worldbuilder.info import Info
from worldbuilder.info_type import InfoType
from worldbuilder.role_enum import Role

def get_dead_players(learned_info: list[Info]):
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

def get_info_trust(info_indices: list[int], learned_info: list[Info]):
    trust_score = 1.0

    for info_index in info_indices:
        is_inverted = info_index < 0
        info_trust = learned_info[abs(info_index)].info_trust
        if is_inverted:
            trust_score = trust_score * (1.0 - info_trust)
        else:
            trust_score = trust_score * info_trust

    return trust_score


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


def add_all_possible_combinations(
    possible_teams: list[list[int]], count: int, player_count: int
):
    if count == 1:
        for i in range(player_count):
            possible_teams.append([i])

    if count == 2:
        for i in range(player_count):
            for j in range(i + 1, player_count):
                possible_teams.append([i, j])

    if count == 3:
        for i in range(player_count):
            for j in range(i + 1, player_count):
                for k in range(j + 1, player_count):
                    possible_teams.append([i, j, k])

    if count == 4:
        for i in range(player_count):
            for j in range(i + 1, player_count):
                for k in range(j + 1, player_count):
                    for l in range(k + 1, player_count):
                        possible_teams.append([i, j, k, l])

    if count == 5:
        for i in range(player_count):
            for j in range(i + 1, player_count):
                for k in range(j + 1, player_count):
                    for l in range(k + 1, player_count):
                        for m in range(l + 1, player_count):
                            possible_teams.append([i, j, k, l, m])


def is_townsfolk(role: Role) -> bool:
    return Role.ACROBAT <= role <= Role.WASHERWOMAN


def is_outsider(role: Role) -> bool:
    return Role.BARBER <= role <= Role.ZEALOT


def is_minion(role: Role) -> bool:
    return Role.ASSASSIN <= role <= Role.XAAN


def is_demon(role: Role) -> bool:
    return Role.AL_HADIKHIA <= role <= Role.ZOMBUUL

# TODO: Review this for all outsider mods
# TODO: How do we handle in game character changes?


def get_outsider_mod(role: Role) -> list[int]:
    match role:
        case Role.VIGORMORTIS:
            return [-1]
        case Role.FANG_GU:
            return [1]
        case Role.BARON:
            return [2]
        case Role.HERMIT:
            return [-1, 0]
        case Role.GODFATHER:
            return [-1, 1]
        case Role.BALLOONIST | Role.HUNTSMAN:
            return [0, 1]
        case Role.KAZALI | Role.LORD_OF_TYPHON | Role.XAAN:
            return [-3, -2, -1, 0, 1, 2, 3]
        case _:
            return [0]
