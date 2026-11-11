from itertools import combinations

from helper import is_demon, is_minion, is_outsider, is_townsfolk
from worldbuilder.info import Info
from worldbuilder.info_type import InfoType
from role_enum import Role


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


def test_count_possible_outputs():
    info = Info(
        info_type=InfoType.CHEF_NUMBER,
        day=0,
        source=0,
        odds_sober=1.0,
        number=1,
        target_players=[0, 1],
        seen_roles=[Role.LIBRARIAN]
    )

    assert info.count_possible_outputs(
        player_count=12, evil_count=3
    ) == 3

    info.info_type = InfoType.EMPATH_NUMBER
    assert info.count_possible_outputs(
        player_count=12
    ) == 3

    for info_type, class_func in (
        (InfoType.WASHERWOMAN_PING, is_townsfolk),
        (InfoType.LIBRARIAN_PING, is_outsider),
        (InfoType.INVESTIGATOR_PING, is_minion),
        (InfoType.SAGE_PING, is_demon),
    ):
        info.info_type = info_type
        valid_player_pair_count = sum(1 for _ in combinations(range(11), 2))
        role_count = sum(class_func(role) for role in TROUBLE_BREWING)
        if info_type is InfoType.WASHERWOMAN_PING:
            role_count -= 1

        if info_type is InfoType.SAGE_PING:
            role_count = 1

        assert info.count_possible_outputs(
            player_count=12, script=TROUBLE_BREWING
        ) == valid_player_pair_count * role_count

    for info_type in (
        InfoType.NONE,
        InfoType.PLAYER_DAY_DEATH,
        InfoType.PLAYER_EXECUTED,
        InfoType.PLAYER_NIGHT_DEATH,
        InfoType.NO_NIGHT_DEATH,
        InfoType.VIRGIN_EXECUTE,
        InfoType.VIRGIN_TRIGGER,
        InfoType.SLAYER_SHOT
    ):
        info.info_type = info_type
        assert info.count_possible_outputs() == 1

    info.info_type = InfoType.FORTUNE_TELLER_PING
    assert info.count_possible_outputs() == 2

    info.info_type = InfoType.PLAYER_IS_ALIGNMENT
    assert info.count_possible_outputs() == 2

    for info_type in (
        InfoType.RAVENKEEPER_PING,
        InfoType.UNDERTAKER_INFO
    ):
        info.info_type = info_type
        assert info.count_possible_outputs(
            script=TROUBLE_BREWING) == len(TROUBLE_BREWING) - 1

    # info.info_type = InfoType.PLAYER_IS_ROLE
    # assert info.count_possible_outputs(
    #     script=TROUBLE_BREWING) == len(TROUBLE_BREWING)
