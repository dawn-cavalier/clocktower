from dataclasses import dataclass
from itertools import combinations

from worldbuilder.game_info import GameInfo
from worldbuilder.helper import is_demon, is_minion, is_outsider, is_townsfolk
from worldbuilder.info import Info
from worldbuilder.info_type import InfoType


@dataclass(frozen=True)
class World:
    demons: tuple[int, ...]
    minions: tuple[int, ...]
    outsiders: tuple[int, ...]
    townsfolk: tuple[int, ...]

    def get_evil_team(self):
        return self.demons + self.minions


def search_world_scores(game_info: GameInfo, learned_info: list[Info]):
    player_ids = range(game_info.player_count)

    scores: dict[World, float] = {}
    outsider_counts = game_info.get_possible_outsider_counts()

    # World Processing
    for world in __generate_worlds__(game_info):
        mod = len(world.outsiders) - game_info.outsider_count_base
        total = 1
        for i in range(mod):
            total *= (game_info.outsider_count_base + i + 1) / (game_info.townsfolk_count_base - i)

        scores[world] = outsider_counts[len(world.outsiders)] * total

        for info in learned_info:
            match info.info_type:
                case (
                    InfoType.NONE |
                    InfoType.FORTUNE_TELLER_PING |
                    InfoType.PLAYER_DAY_DEATH |
                    InfoType.PLAYER_NIGHT_DEATH |
                    InfoType.NO_NIGHT_DEATH |
                    InfoType.PLAYER_EXECUTED
                ):
                    continue
                case (
                    InfoType.PLAYER_IS_ROLE |
                    InfoType.UNDERTAKER_INFO |
                    InfoType.RAVENKEEPER_PING |
                    InfoType.SLAYER_SHOT |
                    InfoType.VIRGIN_TRIGGER
                ):
                    assert info.target_players is not None, (
                        f"{info.info_type.name} has no target players!"
                    )
                    assert len(info.target_players) == 1, (
                        f"{info.info_type.name} received " +
                        f"{len(info.target_players)} players when 1 was expected!"
                    )
                    assert info.seen_roles is not None, (
                        f"{info.info_type.name} has no seen roles!"
                    )
                    assert len(info.seen_roles) == 1, (
                        f"{info.info_type.name} received " +
                        f"{len(info.seen_roles)} roles when 1 was expected!"
                    )

                    target_player = info.target_players[0]
                    seen_role = info.seen_roles[0]

                    if is_demon(seen_role) and target_player not in world.demons:
                        scores[world] *= 1 - info.info_trust
                    if is_minion(seen_role) and target_player not in world.minions:
                        scores[world] *= 1 - info.info_trust
                    if is_outsider(seen_role) and target_player not in world.outsiders:
                        scores[world] *= 1 - info.info_trust
                    if is_townsfolk(seen_role) and target_player not in world.townsfolk:
                        scores[world] *= 1 - info.info_trust

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
                    evil_team = world.get_evil_team()
                    if is_good and player in evil_team:
                        scores[world] *= 1 - info.info_trust

                    if not is_good and player not in evil_team:
                        scores[world] *= 1 - info.info_trust

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
                    demons = world.demons
                    minions = world.minions
                    evil_team = world.get_evil_team()

                    players_present_in_team = sum(
                        player in target_players for player in evil_team
                    )
                    minions_present_in_team = sum(
                        player in target_players for player in minions
                    )
                    demons_present_in_team = sum(
                        player in target_players for player in demons
                    )

                    # Investigator
                    if (
                        is_minion(seen_role) and
                        minions_present_in_team == 0
                    ):
                        scores[world] *= 1 - info.info_trust

                    # Sage
                    if (
                        is_demon(seen_role) and
                        demons_present_in_team == 0
                    ):
                        scores[world] *= 1 - info.info_trust

                    # Washerwoman and Librarian
                    if (
                        (is_townsfolk(seen_role) or is_outsider(seen_role)) and
                        players_present_in_team == 2
                    ):
                        scores[world] *= 1 - info.info_trust

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
                    evil_team_sorted = sorted(world.get_evil_team())

                    for current in range(evil_player_count):
                        right_neighbor = (current + 1) % evil_player_count

                        if (
                            (evil_team_sorted[current] +
                             1) % game_info.player_count
                            == evil_team_sorted[right_neighbor]
                        ):
                            pair_count += 1

                    if number != pair_count:
                        scores[world] *= 1 - info.info_trust

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
                    evil_team = world.get_evil_team()

                    evil_neighbors = 0
                    for neighbor in target_players:
                        if neighbor in evil_team:
                            evil_neighbors += 1

                    if evil_neighbors != number:
                        scores[world] *= 1 - info.info_trust

                case _:
                    raise ValueError(
                        f"Unhandled InfoType: {info.info_type.name}")

    # Evil Team Scoring
    total = sum(scores.values())
    assert total != 0, "No valid worlds!"

    is_demon_scores = [
        sum(
            score for world, score in scores.items()
            if player in world.demons
        ) / total
        for player in player_ids
    ]

    is_minion_scores = [
        sum(
            score for world, score in scores.items()
            if player in world.minions
        ) / total
        for player in player_ids
    ]

    is_outsider_scores = [
        sum(
            score for world, score in scores.items()
            if player in world.outsiders
        ) / total
        for player in player_ids
    ]

    is_townsfolk_scores = [
        sum(
            score for world, score in scores.items()
            if player in world.townsfolk
        ) / total
        for player in player_ids
    ]

    return (
        is_demon_scores,
        is_minion_scores,
        is_outsider_scores,
        is_townsfolk_scores
    )


def __generate_worlds__(game_info: GameInfo):
    player_ids = range(game_info.player_count)
    outsider_counts = game_info.get_possible_outsider_counts()

    for demons in combinations(
        player_ids,
        game_info.demon_count_base
    ):
        non_demons = tuple(
            player for player in
            player_ids
            if player not in demons
        )
        for minions in combinations(
            non_demons,
            game_info.minion_count_base
        ):
            good_players = tuple(
                player for player in non_demons
                if player not in minions
            )
            for outsider_count in outsider_counts:
                for outsiders in combinations(
                    good_players,
                    outsider_count
                ):
                    townsfolk = tuple(
                        player for player in good_players
                        if player not in outsiders
                    )
                    yield World(
                        demons=demons,
                        minions=minions,
                        outsiders=outsiders,
                        townsfolk=townsfolk
                    )
