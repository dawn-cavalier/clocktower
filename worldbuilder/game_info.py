from itertools import combinations

from worldbuilder.helper import get_outsider_mod, is_demon, is_minion
from worldbuilder.role_enum import Role


class GameInfo:
    player_count: int

    demon_count_base: int
    minion_count_base: int
    outsider_count_base: int
    townsfolk_count_base: int

    script: list[Role]

    __possible_outsider_counts__: list[int] | None = None

    def __init__(self, player_count: int, script: list[Role]) -> None:
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
        if self.__possible_outsider_counts__ is not None:
            return self.__possible_outsider_counts__

        possible_outsider_counts: list[int] = [self.outsider_count_base]
        possible_outsider_dict: dict[int, float] = {
            self.outsider_count_base: 0
        }
        roles_with_mods = [role for role in self.script if len(
            get_outsider_mod(role)) > 1 or get_outsider_mod(role)[0] != 0]

        minion_roles_with_mods = [
            role for role in roles_with_mods if is_minion(role)]
        if len(minion_roles_with_mods) > 0:
            new_outsider_dict = dict(possible_outsider_dict)
            minions = [get_outsider_mod(role)
                       for role in self.script if is_minion(role)]

            for combo in combinations(minions, self.minion_count_base):
                sum_dic: dict[int, float] = {0: 0}
                for minion_mods in combo:
                    new_sum_dic: dict[int, float] = {0: 0}
                    for mod in minion_mods:
                        for mod_sum in sum_dic:
                            if mod_sum + mod in new_sum_dic:
                                new_sum_dic[mod_sum + mod] += 1 / \
                                    len(minion_mods)
                            else:
                                new_sum_dic[mod_sum + mod] = 1 / \
                                    len(minion_mods)

                    sum_dic = new_sum_dic

                for mod_sum, mod_occurance in sum_dic.items():
                    for count in possible_outsider_dict:
                        if mod_sum + count in new_outsider_dict:
                            new_outsider_dict[mod_sum + count] += mod_occurance
                        else:
                            new_outsider_dict[mod_sum + count] = mod_occurance

            possible_outsider_dict = new_outsider_dict

        print(possible_outsider_dict)
        return possible_outsider_counts
