from worldbuilder.game_info import GameInfo
from worldbuilder.role_enum import Role


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

SECTS_AND_VIOLETS = {
    # Townsfolk
    Role.CLOCKMAKER,
    Role.DREAMER,
    Role.SNAKE_CHARMER,
    Role.MATHEMATICIAN,
    Role.FLOWERGIRL,
    Role.TOWN_CRIER,
    Role.ORACLE,
    Role.SAVANT,
    Role.SEAMSTRESS,
    Role.PHILOSOPHER,
    Role.ARTIST,
    Role.JUGGLER,
    Role.SAGE,
    # Outsiders
    Role.MUTANT,
    Role.SWEETHEART,
    Role.BARBER,
    Role.KLUTZ,
    # Minions
    Role.EVIL_TWIN,
    Role.WITCH,
    Role.CERENOVUS,
    Role.PIT_HAG,
    # Demons
    Role.FANG_GU,
    Role.VIGORMORTIS,
    Role.NO_DASHII,
    Role.VORTOX
}

BAD_MOON_RISING = {
    # Townsfolk
    Role.GRANDMOTHER,
    Role.SAILOR,
    Role.CHAMBERMAID,
    Role.EXORCIST,
    Role.INNKEEPER,
    Role.GAMBLER,
    Role.GOSSIP,
    Role.COURTIER,
    Role.PROFESSOR,
    Role.MINSTREL,
    Role.TEA_LADY,
    Role.PACIFIST,
    Role.FOOL,
    # Outsiders
    Role.GOON,
    Role.LUNATIC,
    Role.TINKER,
    Role.MOONCHILD,
    # Minions
    Role.GODFATHER,
    Role.DEVILS_ADVOCATE,
    Role.ASSASSIN,
    Role.MASTERMIND,
    # Demons
    Role.ZOMBUUL,
    Role.PUKKA,
    Role.SHABALOTH,
    Role.PO
}


def test_init():
    game_info = GameInfo(7, TROUBLE_BREWING)
    assert game_info.demon_count_base == 1
    assert game_info.minion_count_base == 1
    assert game_info.outsider_count_base == 0
    assert game_info.townsfolk_count_base == 5

    game_info = GameInfo(8, TROUBLE_BREWING)
    assert game_info.demon_count_base == 1
    assert game_info.minion_count_base == 1
    assert game_info.outsider_count_base == 1
    assert game_info.townsfolk_count_base == 5

    game_info = GameInfo(9, TROUBLE_BREWING)
    assert game_info.demon_count_base == 1
    assert game_info.minion_count_base == 1
    assert game_info.outsider_count_base == 2
    assert game_info.townsfolk_count_base == 5

    game_info = GameInfo(10, TROUBLE_BREWING)
    assert game_info.demon_count_base == 1
    assert game_info.minion_count_base == 2
    assert game_info.outsider_count_base == 0
    assert game_info.townsfolk_count_base == 7

    game_info = GameInfo(11, TROUBLE_BREWING)
    assert game_info.demon_count_base == 1
    assert game_info.minion_count_base == 2
    assert game_info.outsider_count_base == 1
    assert game_info.townsfolk_count_base == 7

    game_info = GameInfo(12, TROUBLE_BREWING)
    assert game_info.demon_count_base == 1
    assert game_info.minion_count_base == 2
    assert game_info.outsider_count_base == 2
    assert game_info.townsfolk_count_base == 7

    game_info = GameInfo(13, TROUBLE_BREWING)
    assert game_info.demon_count_base == 1
    assert game_info.minion_count_base == 3
    assert game_info.outsider_count_base == 0
    assert game_info.townsfolk_count_base == 9

    game_info = GameInfo(14, TROUBLE_BREWING)
    assert game_info.demon_count_base == 1
    assert game_info.minion_count_base == 3
    assert game_info.outsider_count_base == 1
    assert game_info.townsfolk_count_base == 9

    game_info = GameInfo(15, TROUBLE_BREWING)
    assert game_info.demon_count_base == 1
    assert game_info.minion_count_base == 3
    assert game_info.outsider_count_base == 2
    assert game_info.townsfolk_count_base == 9

    is_invalid = False
    try:
        game_info = GameInfo(-1, TROUBLE_BREWING)
    except ValueError:
        is_invalid = True

    assert is_invalid


def test_get_possible_outsider_counts_TB():
    outsider_mods: dict[int, float] = GameInfo(
        9, TROUBLE_BREWING
    ).get_possible_outsider_counts()

    assert 2 in outsider_mods
    assert abs(outsider_mods[2] - 0.75) <= 1e-9

    assert 4 in outsider_mods
    assert abs(outsider_mods[4] - 0.25) <= 1e-9

    outsider_mods: dict[int, float] = GameInfo(
        12, TROUBLE_BREWING
    ).get_possible_outsider_counts()

    assert 2 in outsider_mods
    assert abs(outsider_mods[2] - 0.5) <= 1e-9

    assert 4 in outsider_mods
    assert abs(outsider_mods[4] - 0.5) <= 1e-9

    outsider_mods: dict[int, float] = GameInfo(
        15, TROUBLE_BREWING
    ).get_possible_outsider_counts()

    assert 2 in outsider_mods
    assert abs(outsider_mods[2] - 0.25) <= 1e-9

    assert 4 in outsider_mods
    assert abs(outsider_mods[4] - 0.75) <= 1e-9


def test_get_possible_outsider_counts_SNV():
    outsider_mods: dict[int, float] = GameInfo(
        7, SECTS_AND_VIOLETS
    ).get_possible_outsider_counts()

    assert 0 in outsider_mods
    assert abs(outsider_mods[0] - 0.75) <= 1e-9

    assert 1 in outsider_mods
    assert abs(outsider_mods[1] - 0.25) <= 1e-9

    outsider_mods: dict[int, float] = GameInfo(
        9, SECTS_AND_VIOLETS
    ).get_possible_outsider_counts()

    assert 1 in outsider_mods
    assert abs(outsider_mods[1] - 0.25) <= 1e-9

    assert 2 in outsider_mods
    assert abs(outsider_mods[2] - 0.50) <= 1e-9

    assert 3 in outsider_mods
    assert abs(outsider_mods[3] - 0.25) <= 1e-9

    outsider_mods: dict[int, float] = GameInfo(
        10, SECTS_AND_VIOLETS
    ).get_possible_outsider_counts()

    assert 0 in outsider_mods
    assert abs(outsider_mods[0] - 0.75) <= 1e-9

    assert 1 in outsider_mods
    assert abs(outsider_mods[1] - 0.25) <= 1e-9

    outsider_mods: dict[int, float] = GameInfo(
        12, SECTS_AND_VIOLETS
    ).get_possible_outsider_counts()

    assert 1 in outsider_mods
    assert abs(outsider_mods[1] - 0.25) <= 1e-9

    assert 2 in outsider_mods
    assert abs(outsider_mods[2] - 0.50) <= 1e-9

    assert 3 in outsider_mods
    assert abs(outsider_mods[3] - 0.25) <= 1e-9

    outsider_mods: dict[int, float] = GameInfo(
        13, SECTS_AND_VIOLETS
    ).get_possible_outsider_counts()

    assert 0 in outsider_mods
    assert abs(outsider_mods[0] - 0.75) <= 1e-9

    assert 1 in outsider_mods
    assert abs(outsider_mods[1] - 0.25) <= 1e-9

    outsider_mods: dict[int, float] = GameInfo(
        15, SECTS_AND_VIOLETS
    ).get_possible_outsider_counts()

    assert 1 in outsider_mods
    assert abs(outsider_mods[1] - 0.25) <= 1e-9

    assert 2 in outsider_mods
    assert abs(outsider_mods[2] - 0.50) <= 1e-9

    assert 3 in outsider_mods
    assert abs(outsider_mods[3] - 0.25) <= 1e-9


def test_get_possible_outsider_counts_BMR():
    outsider_mods: dict[int, float] = GameInfo(
        7, BAD_MOON_RISING
    ).get_possible_outsider_counts()

    assert 0 in outsider_mods
    assert abs(outsider_mods[0] - 0.75) <= 1e-9

    assert 1 in outsider_mods
    assert abs(outsider_mods[1] - 0.25) <= 1e-9

    outsider_mods: dict[int, float] = GameInfo(
        9, BAD_MOON_RISING
    ).get_possible_outsider_counts()

    assert 1 in outsider_mods
    assert abs(outsider_mods[1] - 0.125) <= 1e-9

    assert 2 in outsider_mods
    assert abs(outsider_mods[2] - 0.75) <= 1e-9

    assert 3 in outsider_mods
    assert abs(outsider_mods[3] - 0.125) <= 1e-9

    outsider_mods: dict[int, float] = GameInfo(
        10, BAD_MOON_RISING
    ).get_possible_outsider_counts()

    assert 0 in outsider_mods
    assert abs(outsider_mods[0] - 0.50) <= 1e-9

    assert 1 in outsider_mods
    assert abs(outsider_mods[1] - 0.50) <= 1e-9

    outsider_mods: dict[int, float] = GameInfo(
        12, BAD_MOON_RISING
    ).get_possible_outsider_counts()

    assert 1 in outsider_mods
    assert abs(outsider_mods[1] - 0.25) <= 1e-9

    assert 2 in outsider_mods
    assert abs(outsider_mods[2] - 0.50) <= 1e-9

    assert 3 in outsider_mods
    assert abs(outsider_mods[3] - 0.25) <= 1e-9

    outsider_mods: dict[int, float] = GameInfo(
        13, BAD_MOON_RISING
    ).get_possible_outsider_counts()

    assert 0 in outsider_mods
    assert abs(outsider_mods[0] - 0.25) <= 1e-9

    assert 1 in outsider_mods
    assert abs(outsider_mods[1] - 0.75) <= 1e-9

    outsider_mods: dict[int, float] = GameInfo(
        15, BAD_MOON_RISING
    ).get_possible_outsider_counts()

    assert 1 in outsider_mods
    assert abs(outsider_mods[1] - 0.375) <= 1e-9

    assert 2 in outsider_mods
    assert abs(outsider_mods[2] - 0.25) <= 1e-9

    assert 3 in outsider_mods
    assert abs(outsider_mods[3] - 0.375) <= 1e-9
