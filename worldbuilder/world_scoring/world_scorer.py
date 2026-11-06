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

    def get_evil_team(self):
        return self.demons + self.minions


def search_world_scores(game_info: GameInfo, learned_info: list[Info]):
    scores: dict[World, float] = {}
    outsider_counts = game_info.get_possible_outsider_counts()
    info_functions = {
        InfoType.NONE:                  __check_nothing__,
        InfoType.PLAYER_DAY_DEATH:      __check_nothing__,
        InfoType.PLAYER_NIGHT_DEATH:    __check_nothing__,
        InfoType.NO_NIGHT_DEATH:        __check_nothing__,
        InfoType.PLAYER_EXECUTED:       __check_nothing__,
        InfoType.PLAYER_IS_ROLE:        __check_invalid_role__,
        InfoType.UNDERTAKER_INFO:       __check_invalid_role__,
        InfoType.RAVENKEEPER_PING:      __check_invalid_role__,
        InfoType.SLAYER_SHOT:           __check_invalid_role__,
        InfoType.VIRGIN_TRIGGER:        __check_invalid_role__,
        InfoType.PLAYER_IS_ALIGNMENT:   __check_invalid_alignment__,
        InfoType.VIRGIN_EXECUTE:        __check_invalid_alignment__,
        InfoType.WASHERWOMAN_PING:      __check_invalid_ping__,
        InfoType.LIBRARIAN_PING:        __check_invalid_ping__,
        InfoType.INVESTIGATOR_PING:     __check_invalid_ping__,
        InfoType.CHEF_NUMBER:           __check_invalid_chef_number__,
        InfoType.EMPATH_NUMBER:         __check_invalid_empath_number__,
        InfoType.FORTUNE_TELLER_PING:   __check_invalid_fortune_teller_ping__
    }

    for world in __generate_worlds__(game_info):
        scores[world] = __calculate_world_prior__(
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

    scores = {world: exp(score) for world, score in scores.items()}

    return __calculate_probabilities__(scores, player_count=game_info.player_count)


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


def __calculate_world_prior__(
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


def __calculate_probabilities__(scores: dict[World, float], player_count: int):
    total = sum(scores.values())
    assert total != 0, "No valid worlds!"
    player_ids = range(player_count)

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


def __check_nothing__(info: Info, world: World, game_info: GameInfo):
    return False


def __check_invalid_role__(info: Info, world: World, game_info: GameInfo):
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


def __check_invalid_alignment__(info: Info, world: World, game_info: GameInfo):
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


def __check_invalid_ping__(info: Info, world: World, game_info: GameInfo):
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
        return True

    # Sage
    if (
        is_demon(seen_role) and
        demons_present_in_team == 0
    ):
        return True

    # Washerwoman and Librarian
    if (
        (is_townsfolk(seen_role) or is_outsider(seen_role)) and
        players_present_in_team == 2
    ):
        return True

    return False


def __check_invalid_chef_number__(info: Info, world: World, game_info: GameInfo):
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
            (evil_team_sorted[current] + 1)
            % game_info.player_count
            == evil_team_sorted[right_neighbor]
        ):
            pair_count += 1

    return number != pair_count


def __check_invalid_empath_number__(info: Info, world: World, game_info: GameInfo):
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


def __check_invalid_fortune_teller_ping__(info: Info, world: World, game_info: GameInfo):

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
        (len(set(demons) & set(target_players)) == 0 and is_yes) and
        (len(set(demons) & set(target_players)) != 0 and not is_yes)
    )
