"""Module providing the various possible world transformations."""

# VIRGIN, UNDERTAKER, RAVENKEEPER
def transform_player_good(
    evil_teams: list[list[int]], target_player: int
) -> list[list[int]]:
    return [key for key in evil_teams if target_player not in key]

# UNDERTAKER, RAVENKEEPER
def transform_player_evil(
    evil_teams: list[list[int]], target_player: int
) -> list[list[int]]:
    return [key for key in evil_teams if target_player in key]

# LIBRARIAN, WASHERWOMAN 
def transform_at_least_one_good(evil_teams: list[list[int]], target_players: list[int]):
    new_evil_teams: list[list[int]] = []
    for team in evil_teams:
        valid = True
        # TODO: Error checking
        for index in range(len(team) - len(target_players) + 1):
            if team[index: index + len(target_players)] == target_players:
                valid = False
                break

        if valid:
            new_evil_teams.append(team)

    return new_evil_teams

# INVESTIGATOR
def transform_at_least_one_evil(evil_teams: list[list[int]], target_players: list[int]):
    new_evil_teams: list[list[int]] = []
    # TODO: Review this for 1 demon 1 minion games
    for team in evil_teams:
        for player in target_players:
            if player in team:
                new_evil_teams.append(team)
                break

    return new_evil_teams

# NOBLE
def transform_exactly_one_evil(evil_teams: list[list[int]], target_players: list[int]):
    new_evil_teams: list[list[int]] = []
    for team in evil_teams:
        count = 0
        for player in target_players:
            if player in team:
                count += 1

        if count == 1:
            new_evil_teams.append(team)

    return new_evil_teams

# CHEF
# TODO: Handle evil teams of different sizes
def transform_chef_number(
    evil_teams: list[list[int]], chef_number: int, player_count: int
) -> list[list[int]]:
    return_value: list[list[int]] = []

    match chef_number:
        case 0:
            for team in evil_teams:
                valid = True
                for current, _ in enumerate(team):
                    right_neighbor = current + 1
                    adjustment = 1
                    if right_neighbor == len(team):
                        right_neighbor = 0
                        adjustment -= player_count

                    if team[current] + adjustment == team[right_neighbor]:
                        valid = False
                        break

                if not valid:
                    continue

                return_value += [
                    (team),
                ]
        case 1:
            for team in evil_teams:
                # Right/ no overflow
                if team[0] + 2 == team[1] + 1 == team[2]:
                    continue

                # Center / overflow
                if team[0] + 1 == team[1] == team[2] + 1 - player_count:
                    continue

                # Left / overflow
                if team[0] == team[1] + 2 - player_count == team[2] + 1 - player_count:
                    continue

                if (
                    team[0] + 1 == team[1]
                    or team[1] + 1 == team[2]
                    or team[2] + 1 - player_count == team[0]
                ):
                    return_value += [
                        (team),
                    ]
        case 2:
            for team in evil_teams:
                # Right/ no overflow
                if team[0] + 2 == team[1] + 1 == team[2]:
                    return_value += [
                        (team),
                    ]

                # Center / overflow
                if team[0] + 1 == team[1] == team[2] + 2 - player_count:
                    return_value += [
                        (team),
                    ]

                # Left / overflow
                if team[0] == team[1] + 2 - player_count == team[2] + 1 - player_count:
                    return_value += [
                        (team),
                    ]
        case _:
            raise ValueError("Invalid Chef Number")

    return return_value
