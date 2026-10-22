from itertools import combinations

from worldbuilder.helper import get_outsider_mod, is_demon, is_minion, is_outsider, is_townsfolk
from worldbuilder.role_enum import Role


class GameInfo:
    player_count: int

    demon_count_base: int
    minion_count_base: int
    outsider_count_base: int
    townsfolk_count_base: int

    script: set[Role]

    __possible_outsider_dict__: dict[int, float] | None = None

    def __init__(self, player_count: int, script: set[Role]) -> None:
        self.player_count = player_count
        self.script = script
        self.demon_count_base = 1

        match player_count:
            case 7:
                self.townsfolk_count_base = 5
                self.outsider_count_base = 0
                self.minion_count_base = 1
            case 8:
                self.townsfolk_count_base = 5
                self.outsider_count_base = 1
                self.minion_count_base = 1
            case 9:
                self.townsfolk_count_base = 5
                self.outsider_count_base = 2
                self.minion_count_base = 1
            case 10:
                self.townsfolk_count_base = 7
                self.outsider_count_base = 0
                self.minion_count_base = 2
            case 11:
                self.townsfolk_count_base = 7
                self.outsider_count_base = 1
                self.minion_count_base = 2
            case 12:
                self.townsfolk_count_base = 7
                self.outsider_count_base = 2
                self.minion_count_base = 2
            case 13:
                self.townsfolk_count_base = 9
                self.outsider_count_base = 0
                self.minion_count_base = 3
            case 14:
                self.townsfolk_count_base = 9
                self.outsider_count_base = 1
                self.minion_count_base = 3
            case 15:
                self.townsfolk_count_base = 9
                self.outsider_count_base = 2
                self.minion_count_base = 3
            case _:
                raise ValueError(f"Player Count {player_count} is invalid.")

    def get_possible_outsider_counts(self):
        if self.__possible_outsider_dict__ is not None:
            return self.__possible_outsider_dict__
        
        possible_outsider_dict: dict[int, float] = {
            self.outsider_count_base: 1.0
        }
        roles_with_mods = [role for role in self.script if len(
            get_outsider_mod(role)) > 1 or get_outsider_mod(role)[0] != 0]

        demon_roles_with_mods = [
            role for role in roles_with_mods if is_demon(role)]
        if len(demon_roles_with_mods) > 0:
            new_outsider_dict = dict(possible_outsider_dict)
            demon_mods_list = [get_outsider_mod(role)
                                for role in self.script if is_demon(role)]

            for combo in combinations(demon_mods_list, self.demon_count_base):
                self.__process_combo__(
                    combo, possible_outsider_dict, new_outsider_dict)

            possible_outsider_dict = new_outsider_dict


        minion_roles_with_mods = [
            role for role in roles_with_mods if is_minion(role)]
        if len(minion_roles_with_mods) > 0:
            new_outsider_dict: dict[int, float] = {}
            minion_mods_list = [get_outsider_mod(role)
                                for role in self.script if is_minion(role)]

            for combo in combinations(minion_mods_list, self.minion_count_base):
                self.__process_combo__(
                    combo, possible_outsider_dict, new_outsider_dict)

            possible_outsider_dict = new_outsider_dict

            original_sum = sum(possible_outsider_dict.values())
            for index, value in possible_outsider_dict.items():
                value = value / original_sum
                possible_outsider_dict[index] = value

        # TODO: Does this  need to handle the different counts?
        townsfolk_roles_with_mods = [
            role for role in roles_with_mods if is_townsfolk(role)]
        if len(townsfolk_roles_with_mods) > 0:
            new_outsider_dict: dict[int, float] = {}
            townsfolk_mods_list = [get_outsider_mod(role)
                                for role in self.script if is_townsfolk(role)]

            for combo in combinations(townsfolk_mods_list, self.townsfolk_count_base):
                self.__process_combo__(
                    combo, possible_outsider_dict, new_outsider_dict)

            possible_outsider_dict = new_outsider_dict

            original_sum = sum(possible_outsider_dict.values())
            for index, value in possible_outsider_dict.items():
                value = value / original_sum
                possible_outsider_dict[index] = value

        # TODO: Does this  need to handle the different counts?
        outsider_roles_with_mods = [
            role for role in roles_with_mods if is_outsider(role)]
        if len(outsider_roles_with_mods) > 0:
            new_outsider_dict: dict[int, float] = {}
            outsider_mods_list = [get_outsider_mod(role)
                                for role in self.script if is_outsider(role)]

            for combo in combinations(outsider_mods_list, self.outsider_count_base):
                self.__process_combo__(
                    combo, possible_outsider_dict, new_outsider_dict)

            possible_outsider_dict = new_outsider_dict

            original_sum = sum(possible_outsider_dict.values())
            for index, value in possible_outsider_dict.items():
                value = value / original_sum
                possible_outsider_dict[index] = value

        self.__possible_outsider_dict__ = possible_outsider_dict
        return possible_outsider_dict

    def __process_combo__(
        self,
        combo: tuple[list[int], ...],
        possible_outsider_dict: dict[int, float],
        new_outsider_dict: dict[int, float]
    ):
        sum_dic: dict[int, float] = {}
        for minion_mods in combo:
            new_sum_dic: dict[int, float] = {}
            for mod in minion_mods:
                if len(sum_dic) > 0:
                    for mod_sum in sum_dic:
                        if mod_sum + mod in new_sum_dic:
                            new_sum_dic[mod_sum + mod] += 1 / \
                                len(minion_mods)
                        else:
                            new_sum_dic[mod_sum + mod] = 1 / \
                                len(minion_mods)
                else:
                    if mod in new_sum_dic:
                        new_sum_dic[mod] += 1 / \
                            len(minion_mods)
                    else:
                        new_sum_dic[mod] = 1 / \
                            len(minion_mods)

            sum_dic = new_sum_dic

        for mod_sum, mod_occurance in sum_dic.items():
            for count, occurance in possible_outsider_dict.items():
                if mod_sum + count in new_outsider_dict:
                    new_outsider_dict[mod_sum + count] += mod_occurance * occurance
                else:
                    new_outsider_dict[mod_sum + count] = mod_occurance * occurance
