from info import Info, InfoType
from helper import build_world, get_all_posibilities

PLAYER_COUNT = 12
EVIL_COUNT = 3


def main() -> None:
    # Append only list!
    learned_info: list[Info] = []

    # Set index zero to be a NONE info object
    learned_info.append(Info(info_type=InfoType.NONE, source=-1, day=0))

    ### Learned information
    # Self is good
    new_info = Info(
        info_type=InfoType.ALIGNMENT_KNOWN,
        source=0,
        day=0,
        is_good=True,
        target_players=[0],
    )
    new_info.info_trust = 1.0
    learned_info.append(new_info)

    # CHEF
    new_info = Info(info_type=InfoType.NUMBER_CHEF, source=0, day=0, number=0)
    new_info.info_trust = 1.0
    learned_info.append(new_info)

    # NOBLE
    new_info = Info(info_type=InfoType.EXACTLY_ONE_EVIL, source=0, day=0, target_players=[2, 5, 7])
    new_info.info_trust = 1.0
    learned_info.append(new_info)

    possibilities = get_all_posibilities(len(learned_info[1:]))

    player_scores = [0.0 for _ in range(PLAYER_COUNT)]
    for possibility in possibilities:
        possibility_player_scores = build_world(possibility, learned_info, EVIL_COUNT)

        for i, player_score in enumerate(possibility_player_scores):
            player_scores[i] += player_score*0.25

        # If Recluse
        possibility_player_scores = build_world(possibility, learned_info, EVIL_COUNT+1)

        for i, player_score in enumerate(possibility_player_scores):
            player_scores[i] += player_score*0.75


    print([f"{score:.2f}" for score in player_scores])
    print(sum(player_scores))


if __name__ == "__main__":
    main()
