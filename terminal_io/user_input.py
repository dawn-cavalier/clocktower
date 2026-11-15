from typing import Any
import builtins

from globals.data.game_info import GameInfo
from globals.enums.role_enum import Role
from storyteller.base_storyteller import Storyteller
from storyteller.random_storyteller import RandomStoryteller


def ask_for_storyteller() -> Storyteller:
    return RandomStoryteller()


def ask_for_game_info() -> GameInfo:
    player_count = _ask_for_player_count()
    script = _ask_for_script()

    game_info: GameInfo = GameInfo(
        player_count=player_count,
        script=script
    )

    return game_info


def _ask_for_player_count() -> int:
    # TODO: Remove magic numbers!
    # 7 = min player count, 15 = max player count
    x = _ask_for_input(
        message="How many players: ",
        expected_input_type=int,
        valid_input=list(range(7, 16)),
        retry=True,
        error_message="Invalid Player Count!"
    )
    assert isinstance(x, int), f"Input value {x} is not an int!"
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


def _ask_for_input(
    message: str,
    expected_input_type: type,
    valid_input: list[Any] | None = None,
    retry: bool = True,
    error_message: str | None = None,
):
    is_restricted = valid_input is not None

    while True:
        user_input = input(message)
        converted_input = _convert_str_to_type(
            user_input,
            expected_input_type
        )

        is_correct_type = isinstance(converted_input, expected_input_type)
        is_valid = not is_restricted or converted_input in valid_input
        if not retry or (is_correct_type and is_valid):
            return converted_input

        if error_message:
            print(error_message)


def _convert_str_to_type(
    str_to_convert: str,
    target_type: type
) -> Any | None:
    match target_type:
        case builtins.str:
            return str_to_convert
        case builtins.int:
            if not str_to_convert.isdecimal():
                return None
            return int(str_to_convert)
        case _:
            raise NotImplementedError(f"Type {target_type} not handled!")
