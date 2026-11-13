from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations

from helper import get_outsider_modifiers, is_demon, is_minion, is_outsider, is_townsfolk
from role_enum import Role


@dataclass
class GameInfo:
    PLAYER_TYPE_COUNTS = {
        7:  (5, 0, 1, 1),
        8:  (5, 1, 1, 1),
        9:  (5, 2, 1, 1),
        10: (7, 0, 2, 1),
        11: (7, 1, 2, 1),
        12: (7, 2, 2, 1),
        13: (9, 0, 3, 1),
        14: (9, 1, 3, 1),
        15: (9, 2, 3, 1),
    }

    NOT_IMPLEMENTED_ROLES = {
        Role.SUMMONER,
        Role.XAAN,
        Role.LIL_MONSTA,
        Role.LORD_OF_TYPHON,
        Role.LEGION,
        Role.KAZALI,
        Role.ATHEIST,
    }

    player_count: int

    demon_count_base: int
    minion_count_base: int
    outsider_count_base: int
    townsfolk_count_base: int

    script: set[Role]

    def __init__(self, player_count: int, script: set[Role]) -> None:
        self.player_count = player_count
        self.script = script
        (
            self.townsfolk_count_base,
            self.outsider_count_base,
            self.minion_count_base,
            self.demon_count_base
        ) = self._get_player_type_counts(player_count)

        self._check_script_valid()

    def get_townsfolk_roles(self):
        return [role for role in self.script if is_townsfolk(role)]

    def get_outsider_roles(self):
        return [role for role in self.script if is_outsider(role)]

    def get_minion_roles(self):
        return [role for role in self.script if is_minion(role)]

    def get_demon_roles(self):
        return [role for role in self.script if is_demon(role)]

    def calculate_outsider_counts(self, *, present_roles: list[Role] | None = None) -> list[int]:
        # TODO: Handle Townsfolk and Outsiders with modifiers.
        present_roles = [] if present_roles is None else present_roles
        demon_count = self.demon_count_base
        minion_count = self.minion_count_base

        outsider_mods = {self.outsider_count_base}

        # Handles present roles
        for role in present_roles:
            if is_demon(role):
                demon_count -= 1
            elif is_minion(role):
                minion_count -= 1

            outsider_mods = {
                existing_mod + modifier
                for existing_mod in outsider_mods
                for modifier in get_outsider_modifiers(role)
            }

        for role_type, count in (
            (is_demon, demon_count),
            (is_minion, minion_count)
        ):
            available_modifiers = [
                get_outsider_modifiers(role)
                for role in self.script
                if role_type(role) and
                role not in present_roles
            ]
            combos = list(combinations(
                available_modifiers, count
            ))
            outsider_mods = self._process_outsider_mods_combos(
                combos,
                outsider_mods
            )

        # Finalizing Dict Scores
        is_negative_modifier_sum_present = any(
            modifier < 0
            for modifier
            in outsider_mods
        )

        if is_negative_modifier_sum_present:
            # Godfather, Hermit
            negative_multi_modifiers = [
                modifiers
                for modifiers
                in [
                    get_outsider_modifiers(role)
                    for role in self.script
                    if is_minion(role) or is_demon(role)
                ]
                if len(modifiers) > 1 and any(mod < 0 for mod in modifiers)
            ]
            nmm_length = len(negative_multi_modifiers)
            if nmm_length == 0:
                outsider_mods.add(0)

            elif nmm_length == 1:
                modifier = negative_multi_modifiers[0]
                offset = max(modifier) - min(modifier)
                negative_mod_sums = sorted([
                    modifier for modifier in outsider_mods if modifier < 0
                ], reverse=True)

                for mod_sum in negative_mod_sums:
                    outsider_mods.add(mod_sum + offset)

            elif nmm_length == 2:
                raise NotImplementedError(
                    "Hermit and Godfather together are currently unsupported!"
                )
            else:
                raise ValueError(
                    f"Expected 0-2 negative multi modifiers and {nmm_length} was received!\n" +
                    f"Mods are {negative_multi_modifiers}."
                )

        return [mod for mod in outsider_mods if mod >= 0]

    def calculate_outsider_counts_odds(self):
        # TODO: Handle Townsfolk and Outsiders with modifiers.
        possible_outsider_dict: defaultdict[int, float] = defaultdict(float)
        possible_outsider_dict[self.outsider_count_base] = 1

        demon_modifiers = [
            get_outsider_modifiers(role)
            for role in self.script
            if is_demon(role)
        ]

        demon_combos = list(combinations(
            demon_modifiers, self.demon_count_base))

        possible_outsider_dict = self._process_outsider_counts_combos(
            possible_outsider_dict,
            demon_combos
        )

        minion_modifiers = [
            get_outsider_modifiers(role)
            for role in self.script
            if is_minion(role)
        ]
        minion_combos = list(combinations(
            minion_modifiers, self.minion_count_base))

        possible_outsider_dict = self._process_outsider_counts_combos(
            possible_outsider_dict,
            minion_combos
        )

        # Finalizing Dict Scores
        is_negative_modifier_sum_present = any(
            modifier < 0 for modifier in possible_outsider_dict
        )

        if is_negative_modifier_sum_present:
            # Godfather, Hermit
            negative_multi_modifiers = [
                modifiers
                for modifiers
                in demon_modifiers + minion_modifiers
                if len(modifiers) > 1 and any(mod < 0 for mod in modifiers)
            ]
            nmm_length = len(negative_multi_modifiers)
            if nmm_length == 0:
                possible_outsider_dict[0] += sum(
                    count for mod, count in possible_outsider_dict.items() if mod < 0
                )

            elif nmm_length == 1:
                modifier = negative_multi_modifiers[0]
                offset = max(modifier) - min(modifier)
                negative_mod_sums = sorted([
                    modifier for modifier in possible_outsider_dict if modifier < 0
                ], reverse=True)

                for mod_sum in negative_mod_sums:
                    possible_outsider_dict[
                        mod_sum + offset
                    ] += possible_outsider_dict[mod_sum]
                    possible_outsider_dict[mod_sum] = 0

                possible_outsider_dict[0] += sum(
                    count for mod, count in possible_outsider_dict.items() if mod < 0
                )
            elif nmm_length == 2:
                raise NotImplementedError(
                    "Hermit and Godfather together are currently unsupported!"
                )
            else:
                raise ValueError(
                    f"Expected 0-2 negative multi modifiers and {nmm_length} was received!\n" +
                    f"Mods are {negative_multi_modifiers}."
                )

        possible_outsider_dict = defaultdict(float, {
            mod: count for (mod, count) in possible_outsider_dict.items() if mod >= 0
        })

        total = sum(possible_outsider_dict.values())
        for mod, value in possible_outsider_dict.items():
            possible_outsider_dict[mod] = value/total

        return possible_outsider_dict

    def _process_outsider_mods_combos(
        self,
        combos: list[tuple[list[int], ...]],
        outsider_mods: set[int]
    ):
        new_outsider_mods: set[int] = set()
        for combo in combos:
            mod_sums: set[int] = {0}
            for role in combo:
                new_mod_sums: set[int] = set()
                for modifier in role:
                    for mod_sum in mod_sums:
                        new_mod_sums.add(mod_sum + modifier)

                mod_sums = new_mod_sums

            for existing_mod in outsider_mods:
                for modifier in mod_sums:
                    new_outsider_mods.add(modifier + existing_mod)

        return new_outsider_mods

    def _process_outsider_counts_combos(
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

    def _get_player_type_counts(self, player_count: int):
        if player_count not in self.PLAYER_TYPE_COUNTS:
            raise NotImplementedError(
                f"Player Count {player_count} is not implemented.")

        return self.PLAYER_TYPE_COUNTS[player_count]

    def _check_script_valid(self):
        townsfolk = [role for role in self.script if is_townsfolk(role)]
        outsiders = [role for role in self.script if is_outsider(role)]
        minions = [role for role in self.script if is_minion(role)]
        demons = [role for role in self.script if is_demon(role)]

        (
            townsfolk_count,
            outsider_count,
            minion_count,
            demon_count
        ) = self._get_player_type_counts(max(self.PLAYER_TYPE_COUNTS))

        if len(demons) < demon_count:
            raise ValueError("Script doesn't have enough demons!")

        if len(minions) < minion_count:
            raise ValueError("Script doesn't have enough minions!")

        needed_outsiders = max(
            self.calculate_outsider_counts()
        ) - self.outsider_count_base + outsider_count
        if len(outsiders) < needed_outsiders:
            raise ValueError("Script doesn't have enough outsiders!")

        if len(townsfolk) < townsfolk_count:
            raise ValueError("Script doesn't have enough outsiders!")

        not_implemented_roles = self.NOT_IMPLEMENTED_ROLES & self.script

        if not_implemented_roles:
            raise NotImplementedError(
                f"Roles: {not_implemented_roles} are not implemented."
            )
