from cmath import inf
from collections import defaultdict
from itertools import combinations
from math import exp, log
from statistics import median

from game_info import GameInfo
from worldbuilder.info import Info
from worldbuilder.world_scoring.world import World
from worldbuilder.world_scoring.world_validators import INFO_VALIDATORS


def search_world_scores(game_info: GameInfo, learned_info: list[Info]):
    evil_scores: dict[World, float] = _get_evil_scores(
        game_info,
        learned_info,
    )
    outsider_scores: dict[World, float] = _get_outsider_scores(
        game_info,
        learned_info,
    )
    townfolk_scores: dict[World, float] = _get_townsfolk_scores(
        game_info,
        learned_info,
    )

    scores = _build_scores(
        evil_scores=evil_scores,
        outsider_scores=outsider_scores,
        townfolk_scores=townfolk_scores,
    )

    print(evil_scores)
    median_log_score = median(
        score for score in scores.values() if score != -inf
    )
    scores = {
        world: exp(score - median_log_score)
        for world, score in scores.items()
    }

    return _calculate_probabilities(scores, player_count=game_info.player_count)


def search_world_scores_old(game_info: GameInfo, learned_info: list[Info]):
    scores: dict[World, float] = {}
    outsider_count_occurances = game_info.calculate_outsider_counts_odds()
    priors = _calculate_log_world_priors(
        outsider_count_occurances=outsider_count_occurances,
        outsider_count_base=game_info.outsider_count_base,
        townsfolk_count_base=game_info.townsfolk_count_base
    )

    for world in _generate_worlds(game_info):
        score = priors[len(world.outsiders)]

        for info in learned_info:
            assert info.info_type in INFO_VALIDATORS, (
                f"Unhandled InfoType: {info.info_type.name}"
            )
            score += _calculate_log_likelihood(world, info, game_info)

        scores[world] = score

    median_log_score = median(
        score for score in scores.values() if score != -inf
    )
    scores = {
        world: exp(score - median_log_score)
        for world, score in scores.items()
    }

    return _calculate_probabilities(scores, player_count=game_info.player_count)


def _get_evil_scores(game_info: GameInfo, learned_info: list[Info]):
    evil_team_scores: dict[World, float] = {}
    players = list(range(game_info.player_count))

    demon_combos = combinations(
        iterable=players,
        r=game_info.demon_count_base
    )

    evil_teams: list[World] = []
    for demons in demon_combos:
        for minions in combinations(
            iterable=[player for player in players if player not in demons],
            r=game_info.minion_count_base
        ):
            evil_teams.append(World(
                demons=demons,
                minions=minions,
                outsiders=None,
                townsfolk=None,
            ))

    for world in evil_teams:
        score = 0
        for info in learned_info:
            if info.info_type not in INFO_VALIDATORS:
                raise ValueError(
                    f"Unhandled InfoType: {info.info_type.name}"
                )
            score += _calculate_log_likelihood(world, info, game_info)
            print(score)

        evil_team_scores[world] = score

    return evil_team_scores


def _get_outsider_scores(game_info: GameInfo, learned_info: list[Info]):
    outsider_scores: dict[World, float] = {}
    players = list(range(game_info.player_count))
    outsider_count_occurances = game_info.calculate_outsider_counts_odds()
    priors = _calculate_log_world_priors(
        outsider_count_occurances=outsider_count_occurances,
        outsider_count_base=game_info.outsider_count_base,
        townsfolk_count_base=game_info.townsfolk_count_base
    )
    outsider_combos: list[tuple[int, ...]] = []
    for outsider_count in outsider_count_occurances:
        outsider_combos += list(combinations(
            iterable=players,
            r=outsider_count
        ))

    outsiders: list[World] = [
        World(demons=None, minions=None, outsiders=outsiders, townsfolk=None)
        for outsiders
        in outsider_combos
    ]

    for world in outsiders:
        if world.outsiders is None:
            raise ValueError(
                "Outsiders cannot be None " +
                "during outsider score construction!"
            )

        if len(world.outsiders) not in priors:
            raise ValueError(
                f"{len(world.outsiders)} is not in priors!"
            )

        score = priors[len(world.outsiders)]
        for info in learned_info:
            if info.info_type not in INFO_VALIDATORS:
                raise ValueError(
                    f"Unhandled InfoType: {info.info_type.name}"
                )
            score += _calculate_log_likelihood(world, info, game_info)

        outsider_scores[world] = score

    return outsider_scores


def _get_townsfolk_scores(game_info: GameInfo, learned_info: list[Info]):
    townsfolk_scores: dict[World, float] = {}
    players = list(range(game_info.player_count))
    townsfolk_count_occurances = game_info.calculate_townsfolk_counts()

    townsfolk_combos: list[tuple[int, ...]] = []
    for townsfolk_count in townsfolk_count_occurances:
        townsfolk_combos += list(combinations(
            iterable=players,
            r=townsfolk_count
        ))

    townsfolks: list[World] = [
        World(demons=None, minions=None, outsiders=None, townsfolk=townfolk)
        for townfolk
        in townsfolk_combos
    ]

    for world in townsfolks:
        score = 0
        for info in learned_info:
            if info.info_type not in INFO_VALIDATORS:
                raise ValueError(
                    f"Unhandled InfoType: {info.info_type.name}"
                )
            score += _calculate_log_likelihood(world, info, game_info)

        townsfolk_scores[world] = score

    return townsfolk_scores


def _build_scores(
    evil_scores: dict[World, float],
    outsider_scores: dict[World, float],
    townfolk_scores: dict[World, float]
):
    scores: dict[World, float] = {}
    for evil_world, evil_score in evil_scores.items():
        demons = evil_world.demons
        minions = evil_world.minions
        if demons is None:
            raise ValueError("Evil World missing demons!")
        if minions is None:
            raise ValueError("Evil World missing minions!")

        for outsider_world, outsider_score in outsider_scores.items():
            outsiders = outsider_world.outsiders
            if outsiders is None:
                raise ValueError("Outsider World missing outsiders!")

            if set(outsiders) & set(demons + minions):
                continue

            for townsfolk_world, townfolk_score in townfolk_scores.items():
                townfolk = townsfolk_world.townsfolk
                if townfolk is None:
                    raise ValueError("Townfolk World missing townfolk!")

                if set(townfolk) & set(demons + minions + outsiders):
                    continue

                scores[World(
                    demons=demons,
                    minions=minions,
                    outsiders=outsiders,
                    townsfolk=townfolk
                )] = evil_score + outsider_score + townfolk_score

    return scores


def _generate_worlds(game_info: GameInfo):
    player_ids = range(game_info.player_count)
    outsider_counts = game_info.calculate_outsider_counts_odds()

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
                        townsfolk=townsfolk,
                    )


def _calculate_log_world_priors(
    outsider_count_occurances: defaultdict[int, float],
    outsider_count_base: int,
    townsfolk_count_base: int
):
    priors: dict[int, float] = {}
    for possible_count in outsider_count_occurances:
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
        priors[possible_count] = log(
            outsider_count_occurances[possible_count] * total)

    return priors


def _calculate_log_likelihood(world: World, info: Info, game_info: GameInfo):
    odds_sober = info.odds_sober
    possible_outputs = info.count_possible_outputs(
        player_count=game_info.player_count,
        evil_count=max(game_info.get_evil_counts()),
        script=game_info.script
    )
    if possible_outputs <= 0:
        raise ValueError(
            f"{info.info_type.name} received {possible_outputs} possible outputs " +
            "when a greater than zero number of inputs was expected!"
        )

    is_arbitary_chance = 1.0 / possible_outputs

    is_inconsistent = INFO_VALIDATORS[info.info_type](
        info=info,
        world=world,
        game_info=game_info
    )

    if is_inconsistent is None:
        return 0.0

    truthful_likelihood = 1.0
    if is_inconsistent:
        truthful_likelihood = 0.0

    likelihood = (
        odds_sober * truthful_likelihood
        + (1.0 - odds_sober) * is_arbitary_chance
    )

    if likelihood == 0:
        return -inf

    return log(likelihood)


def _calculate_probabilities(scores: dict[World, float], player_count: int):
    total = sum(scores.values())
    assert total != 0, "No valid worlds!"
    is_demon_scores = [0.0 for _ in range(player_count)]
    is_minion_scores = [0.0 for _ in range(player_count)]
    is_outsider_scores = [0.0 for _ in range(player_count)]
    is_townsfolk_scores = [0.0 for _ in range(player_count)]

    for world, score in scores.items():
        if world.demons is None:
            raise ValueError("Cannot evaluate a world with None demons.")
        if world.minions is None:
            raise ValueError("Cannot evaluate a world with None minions.")
        if world.outsiders is None:
            raise ValueError("Cannot evaluate a world with None outsiders.")
        if world.townsfolk is None:
            raise ValueError("Cannot evaluate a world with None townsfolk.")

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
