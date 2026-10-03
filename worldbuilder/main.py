from info import Info, InfoType

PLAYER_COUNT = 12
EVIL_COUNT = 3


def main() -> None:
    all_teams: list[list[int]] = []
    # TODO: Handle different evil counts
    for possibility_i in range(PLAYER_COUNT):
        for j in range(possibility_i + 1, PLAYER_COUNT):
            for k in range(j + 1, PLAYER_COUNT):
                all_teams.append([possibility_i, j, k])

    # Append only list!
    learned_info: list[Info] = []

    # Set index zero to be a NONE info object
    learned_info.append(Info(info_type=InfoType.NONE, source=-1, day=0))

    # Learned information
    learned_info.append(
        Info(
            info_type=InfoType.ALIGNMENT_KNOWN,
            source=-1,
            day=0,
            is_good=True,
            target_players=[0],
        )
    )
    learned_info.append(Info(info_type=InfoType.NUMBER_CHEF, source=0, day=0, number=2))
    learned_info.append(
        Info(
            info_type=InfoType.ALIGNMENT_KNOWN,
            source=3,
            day=1,
            is_good=True,
            target_players=[3],
        )
    )
    learned_info.append(
        Info(
            info_type=InfoType.AT_LEAST_ONE_GOOD,
            source=3,
            day=1,
            is_good=True,
            target_players=[7, 8],
        )
    )
    learned_info.append(
        Info(
            info_type=InfoType.ALIGNMENT_KNOWN,
            source=7,
            day=1,
            is_good=True,
            target_players=[7],
        )
    )

    # TODO: Move to it's own function
    num_possibilities = 2 ** len(learned_info[1:])
    possibilities: list[list[int]] = []

    for possibility_i in range(num_possibilities):
        new_possibility: list[int] = []
        for bit in range(len(learned_info[1:])):
            if possibility_i >> bit & 1:
                new_possibility.append(bit + 1)
            else:
                new_possibility.append(-(bit+1))
        possibilities.append(new_possibility)

    print(possibilities)


def transformPlayerGood(
    evil_teams: list[list[int]], target_player: int
) -> list[list[int]]:
    return [key for key in evil_teams if target_player not in key]


def transformPlayerEvil(
    evil_teams: list[tuple[int, int, int]], target_player: int
) -> list[tuple[int, int, int]]:
    return [key for key in evil_teams if target_player in key]


def transformChefNumber(
    evil_teams: list[tuple[int, int, int]], chef_number: int
) -> list[tuple[int, int, int]]:
    return_value: list[tuple[int, int, int]] = []

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


if __name__ == "__main__":
    main()
