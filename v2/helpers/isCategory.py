from enums.roles import *

def isTownsfolk(role: Role) -> bool:
    return role >= Role.WASHERWOMAN and role <= Role.MAYOR


def isOutsider(role: Role) -> bool:
    return role >= Role.BUTLER and role <= Role.DRUNK


def isMinion(role: Role) -> bool:
    return role >= Role.POISONER and role <= Role.SCARLET_WOMAN


def isDemon(role: Role) -> bool:
    return role >= Role.IMP and role <= Role.IMP
