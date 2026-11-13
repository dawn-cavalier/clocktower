import random as r

from game_info import GameInfo
from role_enum import Role
from storyteller.bagbuilders.random_bag_builder import build_random_bag


def main() -> None:
    r.seed(0)

    script = {
        # Townsfolk
        Role.WASHERWOMAN,
        Role.LIBRARIAN,
        Role.INVESTIGATOR,
        Role.CHEF,
        Role.EMPATH,
        Role.FORTUNE_TELLER,
        Role.UNDERTAKER,
        Role.MONK,
        Role.RAVENKEEPER,
        Role.VIRGIN,
        Role.SLAYER,
        Role.SOLDIER,
        Role.MAYOR,
        # Outsiders
        Role.BUTLER,
        Role.DRUNK,
        Role.RECLUSE,
        Role.SAINT,
        # Minions
        Role.POISONER,
        Role.SPY,
        Role.SCARLET_WOMAN,
        Role.BARON,
        # Demons
        Role.IMP,
    }
    game_info = GameInfo(player_count=12, script=script)


    bag = build_random_bag(game_info)
    print(bag)


if __name__ == "__main__":
    main()
