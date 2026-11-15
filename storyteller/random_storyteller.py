from globals.data.game_info import GameInfo
from storyteller.base_storyteller import Storyteller


class RandomStoryteller(Storyteller):
    def generate_grimoire(self, game_info: GameInfo) -> None:
        return None
