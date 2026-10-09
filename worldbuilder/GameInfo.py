from worldbuilder.RoleEnum import Role


class GameInfo:
    player_count: int

    demon_count_base: int
    minion_count_base: int
    outsider_count_base: int
    townsfolk_count_base: int

    script: list[Role]

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
