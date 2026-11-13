import random as r

from game_info import GameInfo
from helper import get_bag_outsider_modification, is_outsider
from role_enum import Role


def build_random_bag(game_info: GameInfo):
    bag: list[Role] = []

    while (
        len(bag) != game_info.player_count or
        not _is_bag_valid(bag, game_info.outsider_count_base)
    ):
        bag = []
        bag += r.sample(
            population=list(game_info.get_demon_roles()),
            k=game_info.demon_count_base
        )

        bag += r.sample(
            population=list(game_info.get_minion_roles()),
            k=game_info.minion_count_base
        )
        bag += r.sample(
            population=(
                list(game_info.get_townsfolk_roles()) +
                list(game_info.get_outsider_roles())
            ),
            k=game_info.townsfolk_count_base + game_info.outsider_count_base
        )

    r.shuffle(bag)
    return bag


def _is_bag_valid(bag: list[Role], outsider_count_base: int):
    if len(bag) == 0:
        return False

    outsider_counts = get_bag_outsider_modification(bag)

    present_outsider_mod = sum(
        is_outsider(role)
        for role in bag
    ) - outsider_count_base
    return present_outsider_mod in outsider_counts
