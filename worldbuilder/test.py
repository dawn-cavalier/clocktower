from worldbuilder.Info import Info, InfoType
from worldbuilder.role_enum import Role


def testTBGame1(learned_info: list[Info]):
    # TODO: Should info be bundled together to reduce checking impossible worlds?
    # TODO: Should Info Source have it's own enum? How would you do this?
    info = Info(
        info_type=InfoType.PLAYER_IS_ROLE,
        day=0,
        source=0,
        info_trust=1.0,
        seen_roles=[Role.MAYOR],
        target_players=[0],
        is_good=True,
    )
    learned_info.append(info)

    info = Info(
        info_type=InfoType.PLAYER_IS_ROLE,
        day=1,
        source=1,
        info_trust=0.5,
        seen_roles=[Role.CHEF],
        target_players=[1],
        is_good=True,
    )
    learned_info.append(info)

    info = Info(
        info_type=InfoType.CHEF_NUMBER, day=1, source=1, info_trust=0.5, number=0
    )
    learned_info.append(info)

    info = Info(
        info_type=InfoType.PLAYER_IS_ROLE,
        day=1,
        source=11,
        info_trust=0.5,
        seen_roles=[Role.UNDERTAKER],
        target_players=[11],
        is_good=True,
    )
    learned_info.append(info)

    info = Info(
        info_type=InfoType.PLAYER_IS_ROLE,
        day=1,
        source=8,
        info_trust=0.5,
        seen_roles=[Role.FORTUNE_TELLER],
        target_players=[8],
        is_good=True,
    )
    learned_info.append(info)

    info = Info(
        info_type=InfoType.FORTUNE_TELLER_PING,
        day=1,
        source=8,
        info_trust=0.5,
        target_players=[1, 4],
        is_yes=True,
    )
    learned_info.append(info)

    info = Info(
        info_type=InfoType.PLAYER_IS_ROLE,
        day=1,
        source=6,
        info_trust=0.5,
        seen_roles=[Role.INVESTIGATOR],
        target_players=[6],
        is_good=True,
    )
    learned_info.append(info)

    info = Info(
        info_type=InfoType.INVESTIGATOR_PING,
        day=1,
        source=6,
        info_trust=0.5,
        seen_roles=[Role.BARON],
        target_players=[8, 10],
        is_good=True,
    )
    learned_info.append(info)

    info = Info(
        info_type=InfoType.PLAYER_EXECUTED,
        day=1,
        source=-1,
        target_players=[1],
    )

