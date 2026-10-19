
from worldbuilder.game_info import GameInfo


class GameState:
    evil_teams: list[list[int]]
    outsiders: list[list[int]]

    demons: list[int]
    dead_players: list[int]

    evil_player_scores: list[float]
    demon_player_scores: list[float]
    outsider_player_scores: list[float]

    def __init__(self, game_info: GameInfo) -> None:
        self.evil_player_scores: list[float] = [
            0.0 for _ in range(game_info.player_count)]
        self.demon_player_scores: list[float] = [
            0.0 for _ in range(game_info.player_count)]
        self.outsider_player_scores: list[float] = [
            0.0 for _ in range(game_info.player_count)
        ]

    def process(self, game_info: GameInfo):
        self.demons = [demon for demon in self.demons if demon not in self.dead_players]
        self.evil_teams = [evil_team for evil_team in self.evil_teams if len(
            [demon for demon in self.demons if demon in evil_team]) > 0]

    def update_scores(self, game_info: GameInfo, info_trust: float):
        self.__update_evil_scores__(game_info, info_trust)
        self.__update_demon_scores__(game_info, info_trust)
        self.__update_outsider_scores__(game_info, info_trust)

    def __update_evil_scores__(self, game_info: GameInfo, info_trust: float):
        if len(self.evil_teams) == 0:
            return

        self.evil_player_scores = [
            sum(1 for t in self.evil_teams if player_id in t)
            * info_trust
            / len(self.evil_teams)
            for player_id in range(game_info.player_count)
        ]

    def __update_demon_scores__(self, game_info: GameInfo, info_trust: float):
        if len(self.demons) == 0:
            return

        self.demon_player_scores = [
            sum(1 for d in self.demons if player_id == d)
            * info_trust
            / len(self.demons)
            for player_id in range(game_info.player_count)
        ]

    def __update_outsider_scores__(self, game_info: GameInfo, info_trust: float):
        outsider_worlds = [[group for group in self.outsiders if len(set(group) & set(
            evil_team)) == 0] for evil_team in self.evil_teams]

        world_count = len(outsider_worlds)
        for world in outsider_worlds:
            outsider_guess_size: dict[int, int] = {}
            for count in game_info.get_possible_outsider_counts():
                guess_size = len(
                    [o for o in world if len(o) == count])
                if guess_size > 0:
                    outsider_guess_size[count] = guess_size

            for group in world:
                size = len(group)
                weight = self.__get_outsider_weight__(
                    game_info, outsider_guess_size, size)

                group_size_population = outsider_guess_size.get(size)
                if group_size_population is None:
                    raise ValueError(
                        f"Getting count for unknown size: {size} for {outsider_guess_size}")

                for player in group:
                    self.outsider_player_scores[player] += info_trust * \
                        weight / (world_count * group_size_population)

    def __get_outsider_weight__(self, game_info: GameInfo, outsider_guess_size: dict[int, int], size: int):
        if len(outsider_guess_size) == 1:
            return 1.0

        if len(outsider_guess_size) < len(game_info.get_possible_outsider_counts()):
            # TODO: For characters with two mods, like Godfather,
            #       this does not correctly redistrute the -1 into
            #       the +1 when the -1 is eliminated.
            total = 0.0
            for guess_size in outsider_guess_size:
                result = game_info.get_possible_outsider_counts().get(guess_size)
                if result is None:
                    raise ValueError(
                        f"Attempting to access invalid outsider count: {guess_size}")
                total += result
            result = game_info.get_possible_outsider_counts().get(size)
            if result is None:
                raise ValueError(
                    f"Attempting to access invalid outsider count: {size}")
            return result / total

        result = game_info.get_possible_outsider_counts().get(size)
        if result is None:
            raise ValueError(
                f"Attempting to access invalid outsider count: {size}")
        return result
