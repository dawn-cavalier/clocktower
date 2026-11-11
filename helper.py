from role_enum import Role

_MODIFIER_DICT = {
    Role.VIGORMORTIS:   [-1],
    Role.FANG_GU:       [1],
    Role.BARON:         [2],
    Role.HERMIT:        [-1, 0],
    Role.GODFATHER:     [-1, 1],
    Role.BALLOONIST:    [0, 1],
    Role.HUNTSMAN:      [0, 1],
}

def is_townsfolk(role: Role) -> bool:
    return Role.ACROBAT <= role <= Role.WASHERWOMAN


def is_outsider(role: Role) -> bool:
    return Role.BARBER <= role <= Role.ZEALOT


def is_minion(role: Role) -> bool:
    return Role.ASSASSIN <= role <= Role.XAAN


def is_demon(role: Role) -> bool:
    return Role.AL_HADIKHIA <= role <= Role.ZOMBUUL


def get_outsider_modifiers(role: Role) -> list[int]:
    # TODO: Review this for all outsider mods
    # TODO: How do we handle in game character changes?
    if role in (Role.KAZALI, Role.LORD_OF_TYPHON, Role.XAAN):
        raise NotImplementedError(
            f"Role {role.name} is currently unhandled!")

    if role not in _MODIFIER_DICT:
        return [0]

    return _MODIFIER_DICT[role]
