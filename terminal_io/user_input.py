from globals.data.game_info import GameInfo
from globals.enums.role_enum import Role


def ask_for_game_info() -> GameInfo:
    player_count = _ask_for_player_count()
    script = _ask_for_script()

    game_info: GameInfo = GameInfo(
        player_count=player_count,
        script=script
    )

    return game_info


def _ask_for_player_count() -> int:
    valid = False
    x = -1
    while not valid:
        user_input = input("How many players: ")
        if user_input.isdigit():
            x = int(user_input)
            if 7 <= x <= 15:
                valid = True

    return x


# TODO: Implement this!
def _ask_for_script() -> set[Role]:
    TROUBLE_BREWING = {
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
    return TROUBLE_BREWING
