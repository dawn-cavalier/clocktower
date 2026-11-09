from worldbuilder.game_info import GameInfo
from worldbuilder.info import Info
from worldbuilder.info_type import InfoType
from worldbuilder.role_enum import Role
from worldbuilder.world_scoring.world import World
import worldbuilder.world_scoring.world_validators as world_validators

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
GAME_INFO = GameInfo(player_count=8, script=TROUBLE_BREWING)
WORLD = World(
    demons=(0,),
    minions=(1,),
    outsiders=(2,),
    townsfolk=(3, 4, 5, 6, 7)
)


def test_nothing():
    info = Info(
        info_type=InfoType.NONE,
        day=0,
        source=0
    )
    assert not world_validators._check_nothing(  # type: ignore
        info, WORLD,
        GAME_INFO
    )


def test_check_valid_roles():
    info = Info(
        info_type=InfoType.PLAYER_IS_ROLE,
        day=0,
        source=0,
        seen_roles=[Role.IMP],
        target_players=[0]
    )
    assert not world_validators._check_is_invalid_role(  # type: ignore
        info, WORLD,
        GAME_INFO
    )

    info = Info(
        info_type=InfoType.PLAYER_IS_ROLE,
        day=0,
        source=1,
        seen_roles=[Role.SPY],
        target_players=[1]
    )
    assert not world_validators._check_is_invalid_role(  # type: ignore
        info, WORLD,
        GAME_INFO
    )

    info = Info(
        info_type=InfoType.PLAYER_IS_ROLE,
        day=0,
        source=0,
        seen_roles=[Role.DRUNK],
        target_players=[2]
    )
    assert not world_validators._check_is_invalid_role(  # type: ignore
        info, WORLD,
        GAME_INFO
    )

    info = Info(
        info_type=InfoType.PLAYER_IS_ROLE,
        day=0,
        source=0,
        seen_roles=[Role.WASHERWOMAN],
        target_players=[3]
    )
    assert not world_validators._check_is_invalid_role(  # type: ignore
        info, WORLD,
        GAME_INFO
    )


def test_check_invalid_roles():
    info = Info(
        info_type=InfoType.PLAYER_IS_ROLE,
        day=0,
        source=0,
        seen_roles=[Role.WASHERWOMAN],
        target_players=[0]
    )
    assert world_validators._check_is_invalid_role(  # type: ignore
        info, WORLD,
        GAME_INFO
    )


def test_check_invalid_outsider_mod():
    game_info = GameInfo(player_count=8, script=TROUBLE_BREWING)
    info = Info(
        info_type=InfoType.PLAYER_IS_ROLE,
        day=0,
        source=0,
        seen_roles=[Role.BARON],
        target_players=[1]
    )
    assert world_validators._check_is_invalid_role(  # type: ignore
        info, WORLD,
        game_info
    )

    game_info = GameInfo(player_count=8, script=SECTS_AND_VIOLETS)
    info = Info(
        info_type=InfoType.PLAYER_IS_ROLE,
        day=0,
        source=0,
        seen_roles=[Role.FANG_GU],
        target_players=[0]
    )
    assert world_validators._check_is_invalid_role(  # type: ignore
        info, WORLD,
        game_info
    )


def test_check_valid_alignment():
    info = Info(
        info_type=InfoType.PLAYER_IS_ALIGNMENT,
        day=0,
        source=0,
        target_players=[0],
        is_good=False
    )
    assert not world_validators._check_is_invalid_alignment(  # type: ignore
        info, WORLD,
        GAME_INFO
    )

    info = Info(
        info_type=InfoType.PLAYER_IS_ALIGNMENT,
        day=0,
        source=1,
        target_players=[1],
        is_good=False
    )
    assert not world_validators._check_is_invalid_alignment(  # type: ignore
        info, WORLD,
        GAME_INFO
    )

    info = Info(
        info_type=InfoType.PLAYER_IS_ALIGNMENT,
        day=0,
        source=1,
        target_players=[2],
        is_good=True
    )
    assert not world_validators._check_is_invalid_alignment(  # type: ignore
        info, WORLD,
        GAME_INFO
    )

    info = Info(
        info_type=InfoType.PLAYER_IS_ALIGNMENT,
        day=0,
        source=1,
        target_players=[3],
        is_good=True
    )
    assert not world_validators._check_is_invalid_alignment(  # type: ignore
        info, WORLD,
        GAME_INFO
    )


def test_check_invalid_alignment():
    info = Info(
        info_type=InfoType.PLAYER_IS_ALIGNMENT,
        day=0,
        source=0,
        target_players=[0],
        is_good=True
    )
    assert world_validators._check_is_invalid_alignment(  # type: ignore
        info, WORLD,
        GAME_INFO
    )


def test_check_valid_ping():
    # Washerwoman
    info = Info(
        info_type=InfoType.WASHERWOMAN_PING,
        day=0,
        source=0,
        seen_roles=[Role.CHEF],
        target_players=[0, 1]
    )
    assert world_validators._check_is_invalid_ping(  # type: ignore
        info, WORLD,
        GAME_INFO
    )

    # Librarian
    info = Info(
        info_type=InfoType.LIBRARIAN_PING,
        day=0,
        source=0,
        seen_roles=[Role.RECLUSE],
        target_players=[0, 1]
    )
    assert world_validators._check_is_invalid_ping(  # type: ignore
        info, WORLD,
        GAME_INFO
    )

    # Investigator
    info = Info(
        info_type=InfoType.INVESTIGATOR_PING,
        day=0,
        source=0,
        seen_roles=[Role.POISONER],
        target_players=[0, 2]
    )
    assert world_validators._check_is_invalid_ping(  # type: ignore
        info, WORLD,
        GAME_INFO
    )

    # Sage
    info = Info(
        info_type=InfoType.SAGE_PING,
        day=0,
        source=0,
        seen_roles=[Role.IMP],
        target_players=[1, 2]
    )
    assert world_validators._check_is_invalid_ping(  # type: ignore
        info, WORLD,
        GAME_INFO
    )


def test_check_invalid_ping():
    info = Info(
        info_type=InfoType.INVESTIGATOR_PING,
        day=0,
        source=0,
        seen_roles=[Role.POISONER],
        target_players=[1, 3]
    )
    assert not world_validators._check_is_invalid_ping(  # type: ignore
        info, WORLD,
        GAME_INFO
    )


def test_check_valid_chef_number():
    info = Info(
        info_type=InfoType.CHEF_NUMBER,
        day=0,
        source=0,
        number=1
    )
    assert not world_validators._check_is_invalid_chef_number(  # type: ignore
        info, WORLD,
        GAME_INFO
    )


def test_check_invalid_chef_number():
    info = Info(
        info_type=InfoType.CHEF_NUMBER,
        day=0,
        source=0,
        number=0
    )
    assert world_validators._check_is_invalid_chef_number(  # type: ignore
        info, WORLD,
        GAME_INFO
    )


def test_check_valid_empath_number():
    info = Info(
        info_type=InfoType.EMPATH_NUMBER,
        day=0,
        source=0,
        number=2,
        target_players=[0, 1]
    )
    assert not world_validators._check_is_invalid_empath_number(  # type: ignore
        info, WORLD,
        GAME_INFO
    )

    info = Info(
        info_type=InfoType.EMPATH_NUMBER,
        day=0,
        source=0,
        number=1,
        target_players=[1, 2]
    )
    assert not world_validators._check_is_invalid_empath_number(  # type: ignore
        info, WORLD,
        GAME_INFO
    )

    info = Info(
        info_type=InfoType.EMPATH_NUMBER,
        day=0,
        source=0,
        number=0,
        target_players=[2, 3]
    )
    assert not world_validators._check_is_invalid_empath_number(  # type: ignore
        info, WORLD,
        GAME_INFO
    )


def test_check_invalid_empath_number():
    info = Info(
        info_type=InfoType.EMPATH_NUMBER,
        day=0,
        source=0,
        number=0,
        target_players=[0, 1]
    )
    assert world_validators._check_is_invalid_empath_number(  # type: ignore
        info, WORLD,
        GAME_INFO
    )

    info = Info(
        info_type=InfoType.EMPATH_NUMBER,
        day=0,
        source=0,
        number=1,
        target_players=[0, 1]
    )
    assert world_validators._check_is_invalid_empath_number(  # type: ignore
        info, WORLD,
        GAME_INFO
    )

    info = Info(
        info_type=InfoType.EMPATH_NUMBER,
        day=0,
        source=0,
        number=0,
        target_players=[1, 2]
    )
    assert world_validators._check_is_invalid_empath_number(  # type: ignore
        info, WORLD,
        GAME_INFO
    )

    info = Info(
        info_type=InfoType.EMPATH_NUMBER,
        day=0,
        source=0,
        number=2,
        target_players=[1, 2]
    )
    assert world_validators._check_is_invalid_empath_number(  # type: ignore
        info, WORLD,
        GAME_INFO
    )

    info = Info(
        info_type=InfoType.EMPATH_NUMBER,
        day=0,
        source=0,
        number=1,
        target_players=[2, 3]
    )
    assert world_validators._check_is_invalid_empath_number(  # type: ignore
        info, WORLD,
        GAME_INFO
    )

    info = Info(
        info_type=InfoType.EMPATH_NUMBER,
        day=0,
        source=0,
        number=2,
        target_players=[2, 3]
    )
    assert world_validators._check_is_invalid_empath_number(  # type: ignore
        info, WORLD,
        GAME_INFO
    )


def test_check_valid_fortune_teller_ping():
    info = Info(
        info_type=InfoType.FORTUNE_TELLER_PING,
        day=0,
        source=0,
        is_yes=True,
        target_players=[0, 1]
    )

    assert not world_validators._check_is_invalid_fortune_teller_ping(  # type: ignore
        info, WORLD,
        GAME_INFO
    )

    info = Info(
        info_type=InfoType.FORTUNE_TELLER_PING,
        day=0,
        source=0,
        is_yes=False,
        target_players=[1, 2]
    )

    assert not world_validators._check_is_invalid_fortune_teller_ping(  # type: ignore
        info, WORLD,
        GAME_INFO
    )


def test_check_invalid_fortune_teller_ping():
    info = Info(
        info_type=InfoType.FORTUNE_TELLER_PING,
        day=0,
        source=0,
        is_yes=False,
        target_players=[0, 1]
    )

    assert world_validators._check_is_invalid_fortune_teller_ping(  # type: ignore
        info, WORLD,
        GAME_INFO
    )

    info = Info(
        info_type=InfoType.FORTUNE_TELLER_PING,
        day=0,
        source=0,
        is_yes=True,
        target_players=[1, 2]
    )

    assert world_validators._check_is_invalid_fortune_teller_ping(  # type: ignore
        info, WORLD,
        GAME_INFO
    )
