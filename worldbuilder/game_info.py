from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations

from worldbuilder.helper import get_outsider_mod, is_demon, is_minion
from worldbuilder.role_enum import Role


@dataclass
class GameInfo:
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

    def get_possible_outsider_mods(self, *, present_roles: list[Role] | None = None):
        # TODO: Handle Townsfolk and Outsiders with modifiers.
        present_roles = [] if present_roles is None else present_roles
        demon_count = self.demon_count_base
        minion_count = self.minion_count_base

        outsider_mods = [self.outsider_count_base]

        # Handles present roles
        for role in present_roles:
            new_outsider_mods: list[int] = []
            if is_demon(role):
                demon_count -= 1
            if is_minion(role):
                minion_count -= 1

            for role_mod in get_outsider_mod(role):
                for saved_mod in outsider_mods:
                    if role_mod + saved_mod not in new_outsider_mods:
                        new_outsider_mods.append(role_mod + saved_mod)

            outsider_mods = new_outsider_mods

        demon_modifiers = [
            get_outsider_mod(role)
            for role in self.script
            if is_demon(role) and
            role not in present_roles
        ]

        demon_combos = list(combinations(
            demon_modifiers, demon_count
        ))

        new_outsider_mods: list[int] = []
        for combo in demon_combos:
            for role in combo:
                for modifier in role:
                    for exisiting_mod in outsider_mods:
                        if modifier + exisiting_mod not in new_outsider_mods:
                            new_outsider_mods.append(modifier + exisiting_mod)

        if new_outsider_mods:
            outsider_mods = new_outsider_mods

        minion_modifiers = [
            get_outsider_mod(role)
            for role in self.script
            if is_minion(role) and
            role not in present_roles
        ]

        minion_combos = list(combinations(
            minion_modifiers, minion_count
        ))

        new_outsider_mods: list[int] = []
        for combo in minion_combos:
            for role in combo:
                for modifier in role:
                    for exisiting_mod in outsider_mods:
                        if modifier + exisiting_mod not in new_outsider_mods:
                            new_outsider_mods.append(modifier + exisiting_mod)

        if new_outsider_mods:
            outsider_mods = new_outsider_mods

        outsider_mods = [mod for mod in outsider_mods if mod >= 0]
        if outsider_mods:
            return outsider_mods

        return [0]

    def get_possible_outsider_counts(self):
        # TODO: Handle Townsfolk and Outsiders with modifiers.
        possible_outsider_dict: defaultdict[int, float] = defaultdict(float)
        possible_outsider_dict[self.outsider_count_base] = 1

        demon_modifiers = [
            get_outsider_mod(role)
            for role in self.script
            if is_demon(role)
        ]

        demon_combos = list(combinations(
            demon_modifiers, self.demon_count_base))

        possible_outsider_dict = self._process_combos(
            possible_outsider_dict,
            demon_combos
        )

        minion_modifiers = [
            get_outsider_mod(role)
            for role in self.script
            if is_minion(role)
        ]
        minion_combos = list(combinations(
            minion_modifiers, self.minion_count_base))

        possible_outsider_dict = self._process_combos(
            possible_outsider_dict,
            minion_combos
        )

        # Finalizing Dict Scores
        is_negative_modifier_sum_present = any(
            modifier for modifier in possible_outsider_dict if modifier < 0
        )

        if is_negative_modifier_sum_present:
            # Godfather, Hermit
            negative_multi_modifiers = [
                modifiers for modifiers in
                demon_modifiers + minion_modifiers
                if len(modifiers) > 1 and any(mod for mod in modifiers if mod < 0)
            ]
            nmm_length = len(negative_multi_modifiers)
            if nmm_length == 0:
                possible_outsider_dict[0] += sum(
                    count for mod, count in possible_outsider_dict.items() if mod < 0
                )
                possible_outsider_dict = defaultdict(float, {
                    mod: count for (mod, count) in possible_outsider_dict.items() if mod >= 0
                })

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
                possible_outsider_dict = defaultdict(float, {
                    mod: count for (mod, count) in possible_outsider_dict.items() if mod >= 0
                })

            elif nmm_length == 2:
                raise NotImplementedError(
                    "Hermit and Godfather together are currently unsupported!"
                )
            else:
                raise ValueError(
                    f"Expected 0-2 negative multi modifiers and {nmm_length} was received!\n" +
                    f"Mods are {negative_multi_modifiers}."
                )

        total = sum(possible_outsider_dict.values())
        for mod, value in possible_outsider_dict.items():
            possible_outsider_dict[mod] = value/total

        return possible_outsider_dict

    def _process_combos(
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
