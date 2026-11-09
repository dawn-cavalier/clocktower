from worldbuilder.info import Info, InfoType
from worldbuilder.role_enum import Role
from worldbuilder.helper import is_minion, is_outsider, is_townsfolk


def generate_start_of_game_info(player_id: int, odds_sober: float, is_good: bool, role: Role):
    assert 0 <= odds_sober <= 1, "Trust must be between 0-1!"
    learned_info: list[Info] = [
        _player_is_alignment(0, is_good, player_id),
        _player_is_role(
            day=0,
            role=role,
            player=player_id,
            source=player_id,
            odds_sober=odds_sober
        )
    ]
    return learned_info


def generate_virgin_trigger(day: int, trust: float, nominee: int, nominator: int):
    assert 0 <= trust <= 1, "Trust must be between 0-1!"
    learned_info: list[Info] = [
        _player_is_role(day, Role.VIRGIN, nominee, source=-1, odds_sober=1.0),
        Info(
            info_type=InfoType.VIRGIN_EXECUTE,
            day=day,
            source=nominator,
            odds_sober=trust,
            target_players=[nominator],
            is_good=True
        )
    ]
    return learned_info


def generate_washerwoman_ping(day: int, source: int, trust: float, targets: list[int], seen_role: Role):
    assert is_townsfolk(seen_role), "Seen role is not a townsfolk!"
    assert len(targets) == 2, f"Received {len(targets)} when 2 was expected!"
    assert 0 <= trust <= 1, "Trust must be between 0-1!"

    learned_info: list[Info] = [
        Info(
            info_type=InfoType.WASHERWOMAN_PING,
            day=day,
            source=source,
            odds_sober=trust,
            target_players=targets,
            seen_roles=[seen_role]
        )
    ]
    return learned_info


def generate_librarian_ping(day: int, source: int, trust: float, targets: list[int], seen_role: Role):
    assert is_outsider(seen_role), "Seen role is not a outsider!"
    assert len(targets) == 2, f"Received {len(targets)} when 2 was expected!"
    assert 0 <= trust <= 1, "Trust must be between 0-1!"

    learned_info: list[Info] = [
        Info(
            info_type=InfoType.LIBRARIAN_PING,
            day=day,
            source=source,
            odds_sober=trust,
            target_players=targets,
            seen_roles=[seen_role]
        )
    ]
    return learned_info


def generate_investigator_ping(day: int, source: int, trust: float, targets: list[int], seen_role: Role):
    assert is_minion(seen_role), "Seen role is not a minion!"
    assert len(targets) == 2, f"Received {len(targets)} when 2 was expected!"
    assert 0 <= trust <= 1, "Trust must be between 0-1!"

    learned_info: list[Info] = [
        Info(
            info_type=InfoType.INVESTIGATOR_PING,
            day=day,
            source=source,
            odds_sober=trust,
            target_players=targets,
            seen_roles=[seen_role]
        )
    ]
    return learned_info


def generate_chef_number(day: int, source: int, trust: float, number: int):
    assert number >= 0, "Chef Number must be positive!"
    assert 0 <= trust <= 1, "Trust must be between 0-1!"

    learned_info: list[Info] = [
        Info(
            info_type=InfoType.CHEF_NUMBER,
            day=day,
            source=source,
            odds_sober=trust,
            number=number
        )
    ]
    return learned_info


def generate_empath_number(day: int, source: int, trust: float, number: int, living_neighbors: list[int]):
    assert number >= 0, "Empath Number must be positive!"
    assert len(living_neighbors) == 2, "Empath must have two neighbors!"
    assert 0 <= trust <= 1, "Trust must be between 0-1!"

    learned_info: list[Info] = [
        Info(
            info_type=InfoType.EMPATH_NUMBER,
            day=day,
            source=source,
            odds_sober=trust,
            number=number,
            target_players=living_neighbors
        )
    ]
    return learned_info


def generate_fortune_teller_ping(day: int, source: int, trust: float, is_yes: bool, target_players: list[int]):
    assert len(target_players) == 2, "Fortune Teller must target two players!"
    assert 0 <= trust <= 1, "Trust must be between 0-1!"

    learned_info: list[Info] = [
        Info(
            info_type=InfoType.FORTUNE_TELLER_PING,
            day=day,
            source=source,
            odds_sober=trust,
            is_yes=is_yes,
            target_players=target_players
        )
    ]
    return learned_info


def _player_is_role(
    day: int,
    role: Role,
    player: int,
    *,
    source: int = -1,
    odds_sober: float = 1.0
):
    return Info(
        info_type=InfoType.PLAYER_IS_ROLE,
        day=day,
        source=source,
        odds_sober=odds_sober,
        seen_roles=[role],
        target_players=[player]
    )


def _player_is_alignment(
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
        odds_sober=trust,
        target_players=[player],
        is_good=is_good
    )
