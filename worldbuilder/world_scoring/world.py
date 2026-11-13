from dataclasses import dataclass


@dataclass(frozen=True)
class World:
    demons: tuple[int, ...] | None
    minions: tuple[int, ...] | None
    outsiders: tuple[int, ...] | None
    townsfolk: tuple[int, ...] | None

    # TODO: Cache this?
    def get_evil_team(self):
        result: tuple[int, ...] = tuple()
        if self.demons is not None:
            result += self.demons
        if self.minions is not None:
            result += self.minions
        return result
