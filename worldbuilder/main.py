from info import Info, InfoType
from helper import build_world

PLAYER_COUNT = 12
EVIL_COUNT = 3


def main() -> None:
    # Append only list!
    learned_info: list[Info] = []

    # Set index zero to be a NONE info object
    learned_info.append(Info(info_type=InfoType.NONE, source=-1, day=0))

    # Learned information
    learned_info.append(
        Info(
            info_type=InfoType.ALIGNMENT_KNOWN,
            source=0,
            day=0,
            is_good=True,
            target_players=[0],
        )
    )
    # learned_info.append(Info(info_type=InfoType.NUMBER_CHEF, source=0, day=0, number=0))
    learned_info.append(
        Info(
            info_type=InfoType.ALIGNMENT_KNOWN,
            source=3,
            day=1,
            is_good=True,
            target_players=[3],
        )
    )
    # learned_info.append(
    #     Info(
    #         info_type=InfoType.AT_LEAST_ONE_GOOD,
    #         source=3,
    #         day=1,
    #         is_good=True,
    #         target_players=[7, 8],
    #     )
    # )
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
                new_possibility.append(-(bit + 1))
        possibilities.append(new_possibility)

    player_scores = [0.0 for _ in range(PLAYER_COUNT)]
    for possibility in possibilities:
        possibility_player_scores = build_world(possibility, learned_info)

        for i, player_score in enumerate(possibility_player_scores):
            player_scores[i] += player_score

    print(player_scores)

if __name__ == "__main__":
    main()
