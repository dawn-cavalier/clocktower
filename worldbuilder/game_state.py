
from worldbuilder.game_info import GameInfo
from worldbuilder.role_enum import Role


class GameState:
    evil_teams: list[list[int]] = []
    outsiders: list[list[int]] = []

    demons: list[int] = []
    night_deaths: list[int] = []
    day_deaths: list[int] = []
    execution_deaths: list[int] = []

    evil_player_scores: list[float]
    demon_player_scores: list[float]
    outsider_player_scores: list[float]

    __second_order_demons__: list[int] = []

    __NIGHT_INSURANCE__ = {Role.SCARLET_WOMAN, Role.IMP}
    __DAY_INSURANCE__ = {Role.SCARLET_WOMAN}

    def __init__(self, game_info: GameInfo) -> None:
        self.evil_player_scores: list[float] = [
            0.0 for _ in range(game_info.player_count)]
        self.demon_player_scores: list[float] = [
            0.0 for _ in range(game_info.player_count)]
        self.outsider_player_scores: list[float] = [
            0.0 for _ in range(game_info.player_count)
        ]

    def process(self, game_info: GameInfo, info_trust: float):
        if len(game_info.script & self.__NIGHT_INSURANCE__) == 0:
            self.demons = [
                demon for demon in self.demons if demon not in self.night_deaths]

        if len(game_info.script & self.__DAY_INSURANCE__) == 0:
            self.demons = [
                demon for demon in self.demons if
                demon not in self.execution_deaths or demon not in self.day_deaths
            ]

        self.evil_teams = [evil_team for evil_team in self.evil_teams if len(
            [demon for demon in self.demons if demon in evil_team]) > 0]

        self.evil_player_scores = self.__calculate_evil_scores__(
            self.evil_teams,
            game_info,
            info_trust
        )

        self.demon_player_scores = self.__calculate_demon_scores__(
            self.evil_teams,
            self.demons,
            game_info,
            info_trust
        )

        self.outsider_player_scores = self.__calculate_outsider_scores__(
            self.evil_teams,
            self.outsiders,
            game_info,
            info_trust
        )

    def __calculate_evil_scores__(
        self,
        evil_teams: list[list[int]],
        game_info: GameInfo,
        info_trust: float
    ):
        if len(evil_teams) == 0:
            return [0.0 for _ in range(game_info.player_count)]

        return [
            sum(1 for t in evil_teams if player_id in t)
            * info_trust
            / len(evil_teams)
            for player_id in range(game_info.player_count)
        ]

    def __calculate_demon_scores__(
        self,
        evil_teams: list[list[int]],
        demons: list[int],
        game_info: GameInfo,
        info_trust: float
    ):
        if len(demons) == 0:
            return [0.0 for _ in range(game_info.player_count)]

        demon_worlds = [[demon for demon in demons if demon in team]
                        for team in evil_teams]

        night_insurance = game_info.script & self.__NIGHT_INSURANCE__
        day_insurance = game_info.script & self.__DAY_INSURANCE__
        if len(night_insurance) != 0 or len(day_insurance) != 0:
            pass

        return [
            sum(1 / len(d) for d in demon_worlds if player_id in d)
            * info_trust
            / len(demon_worlds)
            for player_id in range(game_info.player_count)
        ]

    def __calculate_outsider_scores__(
        self,
        evil_teams: list[list[int]],
        outsiders: list[list[int]],
        game_info: GameInfo,
        info_trust: float
    ):
        outsider_worlds = [[group for group in outsiders if len(set(group) & set(
            evil_team)) == 0] for evil_team in evil_teams]
        outsider_player_scores = [0.0 for _ in range(game_info.player_count)]

        world_count = len(outsider_worlds)
        for world in outsider_worlds:
            outsider_world_scores = self.__process_outsider_world__(
                world,
                game_info.player_count,
                game_info.get_possible_outsider_counts(),
                world_count,
                info_trust
            )
            outsider_player_scores = [score + outsider_world_scores[player]
                                      for player, score in enumerate(outsider_player_scores)]
        return outsider_player_scores

    def __process_outsider_world__(
        self,
        world: list[list[int]],
        player_count: int,
        possible_outsider_counts: dict[int, float],
        world_count: int,
        info_trust: float,
    ):
        outsider_player_scores = [0.0 for _ in range(player_count)]
        outsider_guess_size: dict[int, int] = {}
        for count in possible_outsider_counts:
            guess_size = len(
                [o for o in world if len(o) == count])
            if guess_size > 0:
                outsider_guess_size[count] = guess_size

        for group in world:
            size = len(group)
            weight = self.__calculate_outsider_weight__(
                possible_outsider_counts, outsider_guess_size, size
            )

            group_size_population = outsider_guess_size.get(size)
            if group_size_population is None:
                raise ValueError(
                    f"Getting count for unknown size: {size} for {outsider_guess_size}")

            for player in group:
                outsider_player_scores[player] += info_trust * \
                    weight / (world_count * group_size_population)

        return outsider_player_scores

    def __calculate_outsider_weight__(
        self,
        possible_outsider_counts: dict[int, float],
        outsider_guess_size: dict[int, int],
        size: int
    ):
        if len(outsider_guess_size) == 1:
            return 1.0

        if len(outsider_guess_size) < len(possible_outsider_counts):
            # TODO: For characters with two mods, like Godfather,
            #       this does not correctly redistrute the -1 into
            #       the +1 when the -1 is eliminated.
            total = 0.0
            for guess_size in outsider_guess_size:
                result = possible_outsider_counts.get(guess_size)
                if result is None:
                    raise ValueError(
                        f"Attempting to access invalid outsider count: {guess_size}")
                total += result
            result = possible_outsider_counts.get(size)
            if result is None:
                raise ValueError(
                    f"Attempting to access invalid outsider count: {size}")
            return result / total

        result = possible_outsider_counts.get(size)
        if result is None:
            raise ValueError(
                f"Attempting to access invalid outsider count: {size}")
        return result
