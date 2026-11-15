from abc import ABC, abstractmethod

from globals.data.game_info import GameInfo


class Storyteller(ABC):
    @abstractmethod
    def generate_grimoire(self, game_info: GameInfo) -> None:
        raise NotImplementedError
