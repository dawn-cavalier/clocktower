from worldbuilder.Info import Info
from worldbuilder.role_enum import Role


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


def is_townsfolk(role: Role) -> bool:
    return Role.ACROBAT <= role <= Role.WASHERWOMAN


def is_outsider(role: Role) -> bool:
    return Role.BARBER <= role <= Role.ZEALOT


def is_minion(role: Role) -> bool:
    return Role.ASSASSIN <= role <= Role.XAAN


def is_demon(role: Role) -> bool:
    return Role.AL_HADIKHIA <= role <= Role.ZOMBUUL
