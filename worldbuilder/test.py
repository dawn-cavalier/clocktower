from worldbuilder.info import Info, InfoType
from worldbuilder.role_enum import Role


def generate_test_game():
    learned_info: list[Info] = []
    info = Info(
        info_type=InfoType.PLAYER_IS_ROLE,
        day=0,
        source=0,
        info_trust=1.0,
        seen_roles=[Role.LIBRARIAN],
        target_players=[0],
        is_good=True,
    )
    learned_info.append(info)

    info = Info(
        info_type=InfoType.LIBRARIAN_PING,
        day=0,
        source=0,
        info_trust=1.0,
        seen_roles=[Role.BUTLER],
        target_players=[1, 2],
        is_good=True,
    )
    learned_info.append(info)

    info = Info(
        info_type=InfoType.RAVENKEEPER_PING,
        day=0,
        source=0,
        info_trust=1.0,
        seen_roles=[Role.BUTLER],
        target_players=[2],
        is_good=True,
    )
    learned_info.append(info)

    # info = Info(
    #     info_type=InfoType.RAVENKEEPER_PING,
    #     day=0,
    #     source=0,
    #     info_trust=1.0,
    #     seen_roles=[Role.BUTLER],
    #     target_players=[3],
    #     is_good=True,
    # )
    # learned_info.append(info)

    info = Info(
        info_type=InfoType.RAVENKEEPER_PING,
        day=0,
        source=0,
        info_trust=1.0,
        seen_roles=[Role.BUTLER],
        target_players=[4],
        is_good=True,
    )
    learned_info.append(info)
    return learned_info


def generate_12p_tb_game():
    learned_info: list[Info] = []
    learned_info.append(player_is_role(
        day=0,
        role=Role.UNDERTAKER,
        player=0,
        source=0,
        trust=0.8
    ))

    learned_info.append(player_is_alignment(
        day=0,
        is_good=True,
        player=0,
        source=0,
        trust=1.0
    ))

    info = Info(
        info_type=InfoType.PLAYER_EXECUTED,
        day=1,
        source=-1,
        target_players=[1],
    )
    learned_info.append(info)

    learned_info.append(player_is_role(
        day=2,
        role=Role.IMP,
        player=1,
        source=0,
        trust=0.8
    ))

    # info = Info(
    #     info_type=InfoType.PLAYER_IS_ROLE,
    #     day=1,
    #     source=1,
    #     info_trust=0.5,
    #     seen_roles=[Role.CHEF],
    #     target_players=[1],
    #     is_good=True,
    # )
    # learned_info.append(info)

    # info = Info(
    #     info_type=InfoType.CHEF_NUMBER, day=1, source=1, info_trust=0.5, number=0
    # )
    # learned_info.append(info)

    # info = Info(
    #     info_type=InfoType.PLAYER_IS_ROLE,
    #     day=1,
    #     source=11,
    #     info_trust=0.5,
    #     seen_roles=[Role.UNDERTAKER],
    #     target_players=[11],
    #     is_good=True,
    # )
    # learned_info.append(info)

    # info = Info(
    #     info_type=InfoType.PLAYER_IS_ROLE,
    #     day=1,
    #     source=8,
    #     info_trust=0.5,
    #     seen_roles=[Role.FORTUNE_TELLER],
    #     target_players=[8],
    #     is_good=True,
    # )
    # learned_info.append(info)

    # info = Info(
    #     info_type=InfoType.FORTUNE_TELLER_PING,
    #     day=1,
    #     source=8,
    #     info_trust=0.5,
    #     target_players=[1, 4],
    #     is_yes=True,
    # )
    # learned_info.append(info)

    # info = Info(
    #     info_type=InfoType.PLAYER_IS_ROLE,
    #     day=1,
    #     source=6,
    #     info_trust=0.5,
    #     seen_roles=[Role.INVESTIGATOR],
    #     target_players=[6],
    #     is_good=True,
    # )
    # learned_info.append(info)

    # info = Info(
    #     info_type=InfoType.INVESTIGATOR_PING,
    #     day=1,
    #     source=6,
    #     info_trust=0.5,
    #     seen_roles=[Role.BARON],
    #     target_players=[8, 10],
    #     is_good=True,
    # )
    # learned_info.append(info)

    # info = Info(
    #     info_type=InfoType.PLAYER_NIGHT_DEATH,
    #     day=3,
    #     source=-1,
    #     target_players=[4],
    # )
    # learned_info.append(info)

    return learned_info


def player_is_role(
    day: int,
    role: Role,
    player: int,
    *,
    source: int = -1,
    trust: float = 1.0
):
    return Info(
        info_type=InfoType.PLAYER_IS_ROLE,
        day=day,
        source=source,
        info_trust=trust,
        seen_roles=[role],
        target_players=[player]
    )


def player_is_alignment(
    day: int,
    is_good: bool,
    player: int,
    *,
    source: int = -1,
    trust: float = 1.0
):
    return Info(
        info_type=InfoType.PLAYER_IS_ALIGNMENT,
        day=day,
        source=source,
        info_trust=trust,
        target_players=[player],
        is_good=is_good
    )
