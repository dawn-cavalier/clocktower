from worldbuilder.info import Info, InfoType
from worldbuilder.role_enum import Role
from worldbuilder.helper import is_minion, is_outsider, is_townsfolk


def generate_start_of_game_info(player_id: int, is_good: bool, role: Role):
    learned_info: list[Info] = [
        __player_is_alignment__(0, is_good, player_id),
        __player_is_role__(0, role, player_id, source=player_id, trust=0.8)
    ]
    return learned_info


def generate_virgin_trigger(day: int, nominee: int, nominator: int):
    learned_info: list[Info] = [
        __player_is_role__(day, Role.VIRGIN, nominee, source=-1, trust=1.0),
        Info(
            info_type=InfoType.VIRGIN_EXECUTE,
            day=day,
            source=nominator,
            info_trust=0.8,
            target_players=[nominator],
            is_good=True
        )
    ]
    return learned_info


def generate_washerwoman_ping(day: int, source: int, targets: list[int], seen_role: Role):
    assert is_townsfolk(seen_role), "Seen role is not a townsfolk!"
    assert len(targets) == 2, f"Received {len(targets)} when 2 was expected!"

    learned_info: list[Info] = [
        Info(
            info_type=InfoType.WASHERWOMAN_PING,
            day=day,
            source=source,
            info_trust=0.8,
            target_players=targets,
            seen_roles=[seen_role]
        )
    ]
    return learned_info


def generate_librarian_ping(day: int, source: int, targets: list[int], seen_role: Role):
    assert is_outsider(seen_role), "Seen role is not a outsider!"
    assert len(targets) == 2, f"Received {len(targets)} when 2 was expected!"

    learned_info: list[Info] = [
        Info(
            info_type=InfoType.LIBRARIAN_PING,
            day=day,
            source=source,
            info_trust=0.8,
            target_players=targets,
            seen_roles=[seen_role]
        )
    ]
    return learned_info


def generate_investigator_ping(day: int, source: int, targets: list[int], seen_role: Role):
    assert is_minion(seen_role), "Seen role is not a minion!"
    assert len(targets) == 2, f"Received {len(targets)} when 2 was expected!"

    learned_info: list[Info] = [
        Info(
            info_type=InfoType.INVESTIGATOR_PING,
            day=day,
            source=source,
            info_trust=0.8,
            target_players=targets,
            seen_roles=[seen_role]
        )
    ]
    return learned_info


def generate_chef_number(day: int, source: int, number: int):
    assert number >= 0, "Chef Number must be positive!"

    learned_info: list[Info] = [
        Info(
            info_type=InfoType.CHEF_NUMBER,
            day=day,
            source=source,
            info_trust=0.8,
            number=number
        )
    ]
    return learned_info


def generate_empath_number(day: int, source: int, number: int, living_neighbors: list[int]):
    assert number >= 0, "Empath Number must be positive!"
    assert len(living_neighbors) == 2, "Empath must have two neighbors!"

    learned_info: list[Info] = [
        Info(
            info_type=InfoType.EMPATH_NUMBER,
            day=day,
            source=source,
            info_trust=1,
            number=number,
            target_players=living_neighbors
        )
    ]
    return learned_info


def __player_is_role__(
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


def __player_is_alignment__(
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
