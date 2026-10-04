PLAYER_COUNT = 12
EVIL_COUNT = 3


def transform_player_good(
    evil_teams: list[list[int]], target_player: int
) -> list[list[int]]:
    return [key for key in evil_teams if target_player not in key]


def transform_player_evil(
    evil_teams: list[list[int]], target_player: int
) -> list[list[int]]:
    return [key for key in evil_teams if target_player in key]


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


def transform_at_least_one_evil(evil_teams: list[list[int]], target_players: list[int]):
    new_evil_teams: list[list[int]] = []
    # TODO: Review this for 1 demon 1 minion games
    for team in evil_teams:
        for player in target_players:
            if player in team:
                new_evil_teams.append(team)
                break

    return new_evil_teams

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


def transform_chef_number(
    evil_teams: list[list[int]], chef_number: int
) -> list[list[int]]:
    return_value: list[list[int]] = []

    match chef_number:
        case 0:
            for key in evil_teams:
                if (
                    key[0] + 1 == key[1]
                    or key[1] + 1 == key[2]
                    or key[2] + 1 - PLAYER_COUNT == key[0]
                ):
                    continue

                return_value += [
                    (key),
                ]
        case 1:
            for key in evil_teams:
                # Right/ no overflow
                if key[0] + 2 == key[1] + 1 == key[2]:
                    continue

                # Center / overflow
                if key[0] + 1 == key[1] == key[2] + 1 - PLAYER_COUNT:
                    continue

                # Left / overflow
                if key[0] == key[1] + 2 - PLAYER_COUNT == key[2] + 1 - PLAYER_COUNT:
                    continue

                if (
                    key[0] + 1 == key[1]
                    or key[1] + 1 == key[2]
                    or key[2] + 1 - PLAYER_COUNT == key[0]
                ):
                    return_value += [
                        (key),
                    ]
        case 2:
            for key in evil_teams:
                # Right/ no overflow
                if key[0] + 2 == key[1] + 1 == key[2]:
                    return_value += [
                        (key),
                    ]

                # Center / overflow
                if key[0] + 1 == key[1] == key[2] + 2 - PLAYER_COUNT:
                    return_value += [
                        (key),
                    ]

                # Left / overflow
                if key[0] == key[1] + 2 - PLAYER_COUNT == key[2] + 1 - PLAYER_COUNT:
                    return_value += [
                        (key),
                    ]
        case _:
            raise ValueError("Invalid Chef Number")

    return return_value
