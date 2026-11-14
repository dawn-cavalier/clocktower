from abc import ABC, abstractmethod


class Storyteller(ABC):
    @abstractmethod
    def generate_grimoire(self) -> None:
        raise NotImplementedError
