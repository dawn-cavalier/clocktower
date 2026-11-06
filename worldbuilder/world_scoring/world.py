from dataclasses import dataclass


@dataclass(frozen=True)
class World:
    demons: tuple[int, ...]
    minions: tuple[int, ...]
    outsiders: tuple[int, ...]
    townsfolk: tuple[int, ...]

    # TODO: Cache this?
    def get_evil_team(self):
        return self.demons + self.minions
