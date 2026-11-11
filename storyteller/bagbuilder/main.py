from random import choices

from game_info import GameInfo
from role_enum import Role
from helper import get_outsider_modifiers


def main() -> None:
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
    outsider_odds = game_info.calculate_outsider_counts_odds()

    selected_demon_count = game_info.demon_count_base
    selected_minion_count = game_info.minion_count_base
    selected_outsider_count = choices(
        population=list(outsider_odds.keys()),
        weights=list(outsider_odds.values()),
        k=1,
    )[0]
    selected_townsfolk_count = (
        game_info.townsfolk_count_base +
        game_info.outsider_count_base -
        selected_outsider_count
    )

    outsider_modifier = selected_outsider_count - game_info.outsider_count_base
    minions_with_mods = [
        role
        for role
        in game_info.get_minion_roles()
        if get_outsider_modifiers(role) != [0]
    ]
    
    for role in minions_with_mods:
        for modifier in get_outsider_modifiers(role):
            print(modifier)

    print(choices(population=game_info.get_demon_roles(), k=selected_demon_count))
    print(choices(population=game_info.get_minion_roles(), k=selected_minion_count))
    print(choices(population=game_info.get_outsider_roles(), k=selected_outsider_count))
    print(choices(population=game_info.get_townsfolk_roles(),
          k=selected_townsfolk_count))


if __name__ == "__main__":
    main()
