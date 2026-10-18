
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

    def process(self):
        self.evil_teams = [evil_team for evil_team in self.evil_teams if len(
            [demon for demon in self.demons if demon in evil_team]) > 0]
