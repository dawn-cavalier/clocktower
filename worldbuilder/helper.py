from itertools import combinations

from worldbuilder.role_enum import Role


def calculate_combinations(count: int, player_count: int):
    return [list(c) for c in combinations(range(player_count), count)]


def is_townsfolk(role: Role) -> bool:
    return Role.ACROBAT <= role <= Role.WASHERWOMAN


def is_outsider(role: Role) -> bool:
    return Role.BARBER <= role <= Role.ZEALOT


def is_minion(role: Role) -> bool:
    return Role.ASSASSIN <= role <= Role.XAAN


def is_demon(role: Role) -> bool:
    return Role.AL_HADIKHIA <= role <= Role.ZOMBUUL


def get_outsider_mod(role: Role) -> list[int]:
    # TODO: Review this for all outsider mods
    # TODO: How do we handle in game character changes?
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
