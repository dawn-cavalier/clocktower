from cmath import inf
from collections import defaultdict
from itertools import combinations
from math import exp, log
from statistics import median

from worldbuilder.game_info import GameInfo
from worldbuilder.info import Info
from worldbuilder.world_scoring.world import World
from worldbuilder.world_scoring.world_validators import INFO_VALIDATORS


def search_world_scores(game_info: GameInfo, learned_info: list[Info]):
    scores: dict[World, float] = {}
    outsider_counts = game_info.calculate_outsider_mod_counts()
    priors = _calculate_world_priors(
        outsider_counts=outsider_counts,
        outsider_count_base=game_info.outsider_count_base,
        townsfolk_count_base=game_info.townsfolk_count_base
    )

    for world in _generate_worlds(game_info):
        scores[world] = priors[len(world.outsiders)]

        for info in learned_info:
            assert info.info_type in INFO_VALIDATORS, (
                f"Unhandled InfoType: {info.info_type.name}"
            )

            if INFO_VALIDATORS[info.info_type](info, world, game_info):
                scores[world] += info.inverse_trust_log

    median_log_score = median(
        score for score in scores.values() if score != -inf
    )
    scores = {
        world: exp(score - median_log_score)
        for world, score in scores.items()
    }

    return _calculate_probabilities(scores, player_count=game_info.player_count)


def _generate_worlds(game_info: GameInfo):
    player_ids = range(game_info.player_count)
    outsider_counts = game_info.calculate_outsider_mod_counts()

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


def _calculate_world_priors(
    outsider_counts: defaultdict[int, float],
    outsider_count_base: int,
    townsfolk_count_base: int
):
    priors: dict[int, float] = {}
    for possible_count in outsider_counts:
        mod = possible_count - outsider_count_base
        total = 1
        for i in range(abs(mod)):
            if mod > 0:
                total *= (
                    (outsider_count_base + i + 1) /
                    (townsfolk_count_base - i)
                )
            if mod < 0:
                total *= (
                    (townsfolk_count_base + i + 1) /
                    (outsider_count_base - i)
                )
        priors[possible_count] = log(outsider_counts[possible_count] * total)

    return priors


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
