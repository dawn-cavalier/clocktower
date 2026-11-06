from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations
from math import exp, log

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

    # TODO: Cache this?
    def get_evil_team(self):
        return self.demons + self.minions


def search_world_scores(game_info: GameInfo, learned_info: list[Info]):
    scores: dict[World, float] = {}
    outsider_counts = game_info.get_possible_outsider_counts()
    info_functions = {
        InfoType.NONE:                  _check_nothing,
        InfoType.PLAYER_DAY_DEATH:      _check_nothing,
        InfoType.PLAYER_NIGHT_DEATH:    _check_nothing,
        InfoType.NO_NIGHT_DEATH:        _check_nothing,
        InfoType.PLAYER_EXECUTED:       _check_nothing,
        InfoType.PLAYER_IS_ROLE:        _check_invalid_role,
        InfoType.UNDERTAKER_INFO:       _check_invalid_role,
        InfoType.RAVENKEEPER_PING:      _check_invalid_role,
        InfoType.SLAYER_SHOT:           _check_invalid_role,
        InfoType.VIRGIN_TRIGGER:        _check_invalid_role,
        InfoType.PLAYER_IS_ALIGNMENT:   _check_invalid_alignment,
        InfoType.VIRGIN_EXECUTE:        _check_invalid_alignment,
        InfoType.WASHERWOMAN_PING:      _check_invalid_ping,
        InfoType.LIBRARIAN_PING:        _check_invalid_ping,
        InfoType.INVESTIGATOR_PING:     _check_invalid_ping,
        InfoType.CHEF_NUMBER:           _check_invalid_chef_number,
        InfoType.EMPATH_NUMBER:         _check_invalid_empath_number,
        InfoType.FORTUNE_TELLER_PING:   _check_invalid_fortune_teller_ping
    }

    for world in _generate_worlds(game_info):
        scores[world] = _calculate_world_prior(
            world=world,
            outsider_counts=outsider_counts,
            outsider_count_base=game_info.outsider_count_base,
            townsfolk_count_base=game_info.townsfolk_count_base
        )

        for info in learned_info:
            assert info.info_type in info_functions, (
                f"Unhandled InfoType: {info.info_type.name}"
            )

            if info_functions[info.info_type](info, world, game_info):
                scores[world] += info.inverse_trust_log

    max_log_score = min(scores.values())
    scores = {
        world: exp(score-max_log_score)
        for world, score in scores.items()
    }

    return _calculate_probabilities(scores, player_count=game_info.player_count)


def _generate_worlds(game_info: GameInfo):
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


def _calculate_world_prior(
    world: World,
    outsider_counts: defaultdict[int, float],
    outsider_count_base: int,
    townsfolk_count_base: int
):
    mod = len(world.outsiders) - outsider_count_base
    total = 0
    for i in range(abs(mod)):
        if mod > 0:
            total += log(
                (outsider_count_base + i + 1) /
                (townsfolk_count_base - i)
            )
        if mod < 0:
            total += log(
                (townsfolk_count_base + i + 1) /
                (outsider_count_base - i)
            )

    assert len(world.outsiders) in outsider_counts, (
        f"Had {len(world.outsiders)} outsiders in world when " +
        f"{outsider_counts.keys()} were the possible counts!"
    )
    return log(outsider_counts[len(world.outsiders)]) + total


def _calculate_probabilities(scores: dict[World, float], player_count: int):
    total = sum(scores.values())
    assert total != 0, "No valid worlds!"
    is_demon_scores = [0.0 for _ in range(player_count)]
    is_minion_scores = [0.0 for _ in range(player_count)]
    is_outsider_scores = [0.0 for _ in range(player_count)]
    is_townsfolk_scores = [0.0 for _ in range(player_count)]

    for world, score in scores.items():
        for player in world.demons:
            is_demon_scores[player] += score
        for player in world.minions:
            is_minion_scores[player] += score
        for player in world.outsiders:
            is_outsider_scores[player] += score
        for player in world.townsfolk:
            is_townsfolk_scores[player] += score

    is_demon_scores = [score / total for score in is_demon_scores]
    is_minion_scores = [score / total for score in is_minion_scores]
    is_outsider_scores = [score / total for score in is_outsider_scores]
    is_townsfolk_scores = [score / total for score in is_townsfolk_scores]

    return (
        is_demon_scores,
        is_minion_scores,
        is_outsider_scores,
        is_townsfolk_scores
    )


def _check_nothing(info: Info, world: World, game_info: GameInfo):
    return False


def _check_invalid_role(info: Info, world: World, game_info: GameInfo):
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

    return (
        (is_demon(seen_role) and target_player not in world.demons) or
        (is_minion(seen_role) and target_player not in world.minions) or
        (is_outsider(seen_role) and target_player not in world.outsiders) or
        (is_townsfolk(seen_role) and target_player not in world.townsfolk)
    )


def _check_invalid_alignment(info: Info, world: World, game_info: GameInfo):
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
    return (
        (is_good and player in evil_team) or
        (not is_good and player not in evil_team)
    )


def _check_invalid_ping(info: Info, world: World, game_info: GameInfo):
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

    seen_role = info.seen_roles[0]
    target_players = set(info.target_players)
    demons = set(world.demons)
    minions = set(world.minions)
    evil_team = set(world.get_evil_team())

    evil_players_present = len(target_players & evil_team)
    minions_present = len(target_players & minions)
    demons_present = len(target_players & demons)

    # Investigator
    if (
        is_minion(seen_role) and
        minions_present == 0
    ):
        return True

    # Sage
    if (
        is_demon(seen_role) and
        demons_present == 0
    ):
        return True

    # Washerwoman and Librarian
    if (
        (is_townsfolk(seen_role) or is_outsider(seen_role)) and
        evil_players_present == 2
    ):
        return True

    return False


def _check_invalid_chef_number(info: Info, world: World, game_info: GameInfo):
    number = info.number
    assert number is not None, (
        f"{info.info_type.name} was expected!"
    )

    pair_count = 0
    # TODO: Handle alignment changes.
    evil_player_count = (
        game_info.demon_count_base +
        game_info.minion_count_base
    )
    evil_team_sorted = sorted(world.get_evil_team())

    for current in range(evil_player_count):
        right_neighbor = (current + 1) % evil_player_count

        if (
            (evil_team_sorted[current] + 1)
            % game_info.player_count
            == evil_team_sorted[right_neighbor]
        ):
            pair_count += 1

    return number != pair_count


def _check_invalid_empath_number(info: Info, world: World, game_info: GameInfo):
    assert info.target_players is not None, (
        f"{info.info_type.name} has no target players!"
    )
    assert len(info.target_players) == 2, (
        f"{info.info_type.name} received " +
        f"{len(info.target_players)} players when 2 was expected!"
    )
    assert info.number is not None, (
        f"{info.info_type.name} is expected to have a number!"
    )
    number = info.number
    target_players = info.target_players
    evil_team = world.get_evil_team()

    evil_neighbors = 0
    for neighbor in target_players:
        if neighbor in evil_team:
            evil_neighbors += 1

    return evil_neighbors != number


def _check_invalid_fortune_teller_ping(info: Info, world: World, game_info: GameInfo):

    assert info.target_players is not None, (
        f"{info.info_type.name} has no target players!"
    )
    assert len(info.target_players) == 2, (
        f"{info.info_type.name} received " +
        f"{len(info.target_players)} players when 2 was expected!"
    )
    assert info.is_yes is not None, (
        f"{info.info_type.name} is expected to have a yes/no!"
    )
    is_yes = info.is_yes
    target_players = info.target_players
    demons = world.demons

    return (
        (len(set(demons) & set(target_players)) == 0 and is_yes) or
        (len(set(demons) & set(target_players)) != 0 and not is_yes)
    )
