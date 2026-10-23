from worldbuilder.game_info import GameInfo
from worldbuilder.prediction_calculator_dataclasses import GameState, Predictions


def calculate_predictions(game_state: GameState, game_info: GameInfo, info_trust: float):
    predictions: Predictions = Predictions()
    if len(game_info.script & game_info.__NIGHT_INSURANCE__) == 0:
        game_state.demons = [
            demon for demon in game_state.demons if demon not in game_state.night_deaths]

    if len(game_info.script & game_info.__DAY_INSURANCE__) == 0:
        game_state.demons = [
            demon for demon in game_state.demons if
            demon not in game_state.execution_deaths or demon not in game_state.day_deaths
        ]

    game_state.evil_teams = [evil_team for evil_team in game_state.evil_teams if len(
        [demon for demon in game_state.demons if demon in evil_team]) > 0]

    predictions.evil_player_scores = __calculate_evil_scores__(
        game_state.evil_teams,
        game_info.player_count,
        info_trust
    )

    predictions.demon_player_scores = __calculate_demon_scores__(
        game_state.evil_teams,
        game_state.demons,
        game_info.player_count,
        info_trust
    )

    predictions.outsider_player_scores = __calculate_outsider_scores__(
        game_state.evil_teams,
        game_state.outsiders,
        game_info,
        info_trust
    )

    return predictions


def __calculate_evil_scores__(
    evil_teams: list[list[int]],
    player_count: int,
    info_trust: float
):
    if len(evil_teams) == 0:
        return [0.0 for _ in range(player_count)]

    return [
        sum(1 for t in evil_teams if player_id in t)
        * info_trust
        / len(evil_teams)
        for player_id in range(player_count)
    ]


def __calculate_demon_scores__(
    evil_teams: list[list[int]],
    demons: list[int],
    player_count: int,
    info_trust: float
):
    if len(demons) == 0:
        return [0.0 for _ in range(player_count)]

    demon_worlds = [[demon for demon in demons if demon in team]
                    for team in evil_teams]

    return [
        sum(1 / len(d) for d in demon_worlds if player_id in d)
        * info_trust
        / len(demon_worlds)
        for player_id in range(player_count)
    ]


def __calculate_outsider_scores__(
    evil_teams: list[list[int]],
    outsider_groups: list[list[int]],
    game_info: GameInfo,
    info_trust: float
):
    outsider_worlds = [[group for group in outsider_groups if len(set(group) & set(
        evil_team)) == 0] for evil_team in evil_teams]
    outsider_player_scores = [0.0 for _ in range(game_info.player_count)]

    world_count = len(outsider_worlds)
    for world in outsider_worlds:
        outsider_world_scores = __process_outsider_world__(
            world,
            game_info,
            world_count,
            info_trust
        )
        outsider_player_scores = [score + outsider_world_scores[player]
                                  for player, score in enumerate(outsider_player_scores)]
    return outsider_player_scores


def __process_outsider_world__(
    world: list[list[int]],
    game_info: GameInfo,
    world_count: int,
    info_trust: float,
):
    player_count = game_info.player_count
    possible_outsider_counts = game_info.get_possible_outsider_counts()

    outsider_player_scores = [0.0 for _ in range(player_count)]
    outsider_guess_size: dict[int, int] = {}
    for count in possible_outsider_counts:
        guess_size = len(
            [o for o in world if len(o) == count])
        if guess_size > 0:
            outsider_guess_size[count] = guess_size

    for group in world:
        size = len(group)
        weight = __calculate_outsider_weight__(
            possible_outsider_counts, outsider_guess_size, size
        )

        group_size_population = outsider_guess_size.get(size)
        if group_size_population is None:
            raise ValueError(
                f"Getting count for unknown size: {size} for {outsider_guess_size}")

        for player in group:
            outsider_player_scores[player] += info_trust * \
                weight / (world_count * group_size_population)

    return outsider_player_scores


def __calculate_outsider_weight__(
    possible_outsider_counts: dict[int, float],
    outsider_guess_size: dict[int, int],
    size: int
):
    if len(outsider_guess_size) == 1:
        return 1.0

    if len(outsider_guess_size) < len(possible_outsider_counts):
        # TODO: For characters with two mods, like Godfather,
        #       this does not correctly redistrute the -1 into
        #       the +1 when the -1 is eliminated.
        total = 0.0
        for guess_size in outsider_guess_size:
            result = possible_outsider_counts.get(guess_size)
            if result is None:
                raise ValueError(
                    f"Attempting to access invalid outsider count: {guess_size}")
            total += result
        result = possible_outsider_counts.get(size)
        if result is None:
            raise ValueError(
                f"Attempting to access invalid outsider count: {size}")
        return result / total

    result = possible_outsider_counts.get(size)
    if result is None:
        raise ValueError(
            f"Attempting to access invalid outsider count: {size}")
    return result
