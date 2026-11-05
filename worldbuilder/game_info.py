from collections import defaultdict
from itertools import combinations

from worldbuilder.helper import get_outsider_mod, is_demon, is_minion
from worldbuilder.role_enum import Role

# TODO: This entire class is a nightmare, refactor this garbage


class GameInfo:
    player_count: int

    demon_count_base: int
    minion_count_base: int
    outsider_count_base: int
    townsfolk_count_base: int

    script: set[Role]

    __possible_outsider_dict__: dict[int, float] | None = None

    NIGHT_INSURANCE = {Role.SCARLET_WOMAN, Role.IMP}
    DAY_INSURANCE = {Role.SCARLET_WOMAN}

    def __init__(self, player_count: int, script: set[Role]) -> None:
        self.player_count = player_count
        self.script = script
        self.demon_count_base = 1
        (
            self.townsfolk_count_base,
            self.outsider_count_base,
            self.minion_count_base,
            self.demon_count_base
        ) = self.__get_player_type_counts__(player_count)

    def get_possible_outsider_counts(self):
        possible_outsider_dict: defaultdict[int, float] = defaultdict(float)
        possible_outsider_dict[self.outsider_count_base] = 1

        demon_mods = [
            get_outsider_mod(role)
            for role in self.script
            if is_demon(role)
        ]

        demon_combos = list(combinations(demon_mods, self.demon_count_base))

        possible_outsider_dict = self.__process_combos__(
            possible_outsider_dict,
            demon_combos
        )

        minion_mods = [
            get_outsider_mod(role)
            for role in self.script
            if is_minion(role)
        ]
        minion_combos = list(combinations(minion_mods, self.minion_count_base))

        possible_outsider_dict = self.__process_combos__(
            possible_outsider_dict,
            minion_combos
        )

        total = sum(possible_outsider_dict.values())
        for mod, value in possible_outsider_dict.items():
            possible_outsider_dict[mod] = value/total

        return possible_outsider_dict

    def __process_combos__(
        self,
        original_dict: defaultdict[int, float],
        combos: list[tuple[list[int], ...]]
    ):
        new_dict: defaultdict[int, float] = defaultdict(float)
        for count, value in original_dict.items():
            for combo in combos:
                combo_mods: list[int] = [0]
                modifier = 1.0
                for mods in combo:
                    length = len(mods)
                    assert length != 0, "Role has an empty outsider mod list!"
                    assert length in (
                        1, 2
                    ), "Role has more than two outsider mods!"

                    if length == 1:
                        combo_mods = [mods[0] + mod for mod in combo_mods]
                    if length == 2:
                        first_mod_list = [mods[0] + mod for mod in combo_mods]
                        second_mod_list = [mods[1] + mod for mod in combo_mods]
                        combo_mods = first_mod_list + second_mod_list
                        modifier /= 2

                for combo_mod in combo_mods:
                    new_dict[
                        count + combo_mod
                    ] += value * modifier

        return new_dict

    def __get_player_type_counts__(self, player_count: int):
        match player_count:
            case 7:
                townsfolk_count_base = 5
                outsider_count_base = 0
                minion_count_base = 1
            case 8:
                townsfolk_count_base = 5
                outsider_count_base = 1
                minion_count_base = 1
            case 9:
                townsfolk_count_base = 5
                outsider_count_base = 2
                minion_count_base = 1
            case 10:
                townsfolk_count_base = 7
                outsider_count_base = 0
                minion_count_base = 2
            case 11:
                townsfolk_count_base = 7
                outsider_count_base = 1
                minion_count_base = 2
            case 12:
                townsfolk_count_base = 7
                outsider_count_base = 2
                minion_count_base = 2
            case 13:
                townsfolk_count_base = 9
                outsider_count_base = 0
                minion_count_base = 3
            case 14:
                townsfolk_count_base = 9
                outsider_count_base = 1
                minion_count_base = 3
            case 15:
                townsfolk_count_base = 9
                outsider_count_base = 2
                minion_count_base = 3
            case _:
                raise ValueError(f"Player Count {player_count} is invalid.")

        return (townsfolk_count_base, outsider_count_base, minion_count_base, 1)
