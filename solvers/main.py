import math

PLAYER_COUNT = 12
EVIL_COUNT = 3


def main() -> None:
    evil_teams: dict[tuple[int, int, int], float] = {}

    # TODO: Handle different evil counts
    for i in range(PLAYER_COUNT):
        for j in range(i + 1 , PLAYER_COUNT):
            for k in range(j + 1, PLAYER_COUNT):
                evil_teams[(i, j, k)] = 0.0

    # playerIsGood(evil_teams, 0)
    # playerIsEvil(evil_teams, 11)

    setChefInfo(evil_teams, 2)

    for key, value in evil_teams.items():
        if value < 0.01:
            continue
        print(f"{key}: {value}")


def playerIsGood(evil_teams: dict[tuple[int, int, int], float], target_player: int):
    for key in [key for key in evil_teams if target_player in key]:
        evil_teams[key] += -math.inf


def playerIsEvil(evil_teams: dict[tuple[int, int, int], float], target_player: int):
    for key in [key for key in evil_teams if target_player not in key]:
        evil_teams[key] += -math.inf


def setChefInfo(
    evil_teams: dict[tuple[int, int, int], float], chef_number: int
) -> None:
    match chef_number:
        case 0:
            for key in evil_teams:
                if (
                    key[0] + 1 == key[1]
                    or key[1] + 1 == key[2]
                    or key[2] + 1 - PLAYER_COUNT == key[0]
                ):
                    continue

                evil_teams[key] += 1
            return
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
                    evil_teams[key] += 1
            return
        case 2:
            for key in evil_teams:
                # Right/ no overflow
                if key[0] + 2 == key[1] + 1 == key[2]:
                    evil_teams[key] += 1

                # Center / overflow
                if key[0] + 1 == key[1] == key[2] + 2 - PLAYER_COUNT:
                    evil_teams[key] += 1

                # Left / overflow
                if key[0] == key[1] + 2 - PLAYER_COUNT == key[2] + 1 - PLAYER_COUNT:
                    evil_teams[key] += 1
            return
        case _:
            return


if __name__ == "__main__":
    main()
