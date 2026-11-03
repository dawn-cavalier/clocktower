from enum import Enum
from itertools import combinations, permutations

from worldbuilder.game_info import GameInfo
from worldbuilder.helper import is_demon, is_minion, is_outsider, is_townsfolk
from worldbuilder.info import Info
from worldbuilder.info_type import InfoType
from worldbuilder.role_enum import Role


class RoleGroup(Enum):
    DEMON = 0
    MINION = 1
    OUTSIDER = 2
    TOWNSFOLK = 3


def search_world_scores(game_info: GameInfo, learned_info: list[Info]):
    is_evil_scores = [0.0 for _ in range(game_info.player_count)]
    is_demon_scores = [0.0 for _ in range(game_info.player_count)]
    is_minion_scores = [0.0 for _ in range(game_info.player_count)]
    is_outsider_scores = [0.0 for _ in range(game_info.player_count)]

    all_evil_teams = permutations(
        range(game_info.player_count),
        game_info.demon_count_base + game_info.minion_count_base
    )
    scores: dict[tuple[int, ...], float] = {
        team: 1.0 for team in all_evil_teams
    }

    # World Processing
    for evil_team in scores:
        for info in learned_info:
            match info.info_type:
                case (
                    InfoType.NONE |

                    InfoType.PLAYER_IS_ROLE |
                    InfoType.UNDERTAKER_INFO |
                    InfoType.RAVENKEEPER_PING |
                    InfoType.VIRGIN_TRIGGER |
                    InfoType.SLAYER_SHOT |

                    InfoType.FORTUNE_TELLER_PING |

                    InfoType.PLAYER_DAY_DEATH |
                    InfoType.PLAYER_NIGHT_DEATH |
                    InfoType.NO_NIGHT_DEATH |
                    InfoType.PLAYER_EXECUTED
                ):
                    continue

                case (
                    InfoType.PLAYER_IS_ALIGNMENT |
                    InfoType.VIRGIN_EXECUTE
                ):
                    assert info.target_players is not None, (
                        f"{info.info_type.name} has no target players!"
                    )
                    assert info.is_good is not None, (
                        f"{info.info_type.name} has no stated alignment!"
                    )
                    assert len(info.target_players) == 1, (
                        f"{info.info_type.name} received " +
                        f"{len(info.target_players)} players when 1 was expected!"
                    )

                    is_good = info.is_good
                    player = info.target_players[0]
                    if is_good and player in evil_team:
                        scores[evil_team] *= 1 - info.info_trust

                    if not is_good and player not in evil_team:
                        scores[evil_team] *= 1 - info.info_trust

                case (
                    InfoType.WASHERWOMAN_PING |
                    InfoType.LIBRARIAN_PING |
                    InfoType.INVESTIGATOR_PING
                ):
                    assert info.target_players is not None, (
                        f"{info.info_type.name} has no target players!"
                    )
                    assert info.seen_roles is not None, (
                        f"{info.info_type.name} has no seen roles!"
                    )
                    assert len(info.target_players) == 2, (
                        f"{info.info_type.name} received " +
                        f"{len(info.target_players)} players when 2 was expected!"
                    )
                    assert len(info.seen_roles) == 1, (
                        f"{info.info_type.name} received " +
                        f"{len(info.seen_roles)} roles when 1 was expected!"
                    )

                    target_players = info.target_players
                    seen_role = info.seen_roles[0]
                    demon = evil_team[0]
                    minions = evil_team[1:]

                    players_present_in_team = sum(
                        player in target_players for player in evil_team
                    )
                    minions_present_in_team = sum(
                        player in target_players for player in minions
                    )

                    # Investigator
                    if (
                        is_minion(seen_role) and
                        minions_present_in_team == 0
                    ):
                        scores[evil_team] *= 1 - info.info_trust

                    # Sage
                    if (
                        is_demon(seen_role) and
                        demon not in target_players
                    ):
                        scores[evil_team] *= 1 - info.info_trust

                    # Washerwoman and Librarian
                    if (
                        (is_townsfolk(seen_role) or is_outsider(seen_role)) and
                        players_present_in_team == 2
                    ):
                        scores[evil_team] *= 1 - info.info_trust

                case InfoType.CHEF_NUMBER:
                    assert info.number is not None, (
                        f"{info.info_type.name} was expected!"
                    )

                    number = info.number
                    pair_count = 0
                    evil_player_count = (
                        game_info.demon_count_base +
                        game_info.minion_count_base
                    )
                    evil_team_sorted = sorted(evil_team)

                    for current in range(evil_player_count):
                        right_neighbor = (current + 1) % evil_player_count

                        if (
                            (evil_team_sorted[current] +
                             1) % game_info.player_count
                            == evil_team_sorted[right_neighbor]
                        ):
                            pair_count += 1

                    if number != pair_count:
                        scores[evil_team] *= 1 - info.info_trust

                case InfoType.EMPATH_NUMBER:
                    assert info.target_players is not None, (
                        f"{info.info_type.name} has no target players!"
                    )
                    assert len(info.target_players) == 2, (
                        f"{info.info_type.name} received " +
                        f"{len(info.target_players)} players when 2 was expected!"
                    )
                    assert info.number is not None, (
                        f"{info.info_type.name} was expected!"
                    )
                    number = info.number
                    target_players = info.target_players

                    evil_neighbors = 0
                    for neighbor in target_players:
                        if neighbor in evil_team:
                            evil_neighbors += 1

                    if evil_neighbors != number:
                        scores[evil_team] *= 1 - info.info_trust

                case _:
                    raise ValueError(
                        f"Unhandled InfoType: {info.info_type.name}")

    # Evil Team Scoring
    total = sum(scores.values())
    assert total != 0, "No valid worlds!"

    is_evil_scores = [
        sum(
            score for world, score in scores.items()
            if player in world
        ) / total
        for player in range(game_info.player_count)
    ]

    is_demon_scores = [
        sum(
            score for world, score in scores.items()
            if player == world[0]
        ) / total
        for player in range(game_info.player_count)
    ]

    is_minion_scores = [
        sum(
            score for world, score in scores.items()
            if player in world[1:]
        ) / total
        for player in range(game_info.player_count)
    ]

    return (
        is_evil_scores,
        is_demon_scores,
        is_minion_scores,
        is_outsider_scores
    )
