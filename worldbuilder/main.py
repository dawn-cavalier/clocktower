from info import Info, InfoType
from helper import build_world, get_all_posibilities, get_player_appearances

PLAYER_COUNT = 12
EVIL_COUNT = 3


def main() -> None:
    test1()

def test1():
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

    # # EMPATH
    # new_info = Info(info_type=InfoType.NUMBER_EMPATH, source=0, day=0, number=1, target_players=[1,11])
    # new_info.info_trust = 1.0
    # learned_info.append(new_info)

    # new_info = Info(info_type=InfoType.NUMBER_EMPATH, source=0, day=1, number=0, target_players=[2,11])
    # new_info.info_trust = 1.0
    # learned_info.append(new_info)

    # # CHEF
    # new_info = Info(info_type=InfoType.NUMBER_CHEF, source=0, day=0, number=2)
    # new_info.info_trust = 1.0
    # learned_info.append(new_info)

    # # NOBLE
    # new_info = Info(info_type=InfoType.EXACTLY_ONE_EVIL, source=0, day=0, target_players=[2, 5, 7])
    # new_info.info_trust = 1.0
    # learned_info.append(new_info)

    possibilities = get_all_posibilities(len(learned_info[1:]))

    player_scores = [0.0 for _ in range(PLAYER_COUNT)]
    for possibility in possibilities:
        possible_teams, info_trust = build_world(possibility, learned_info, EVIL_COUNT)

        possibility_player_scores: list[float] =[0.0 for _ in range(PLAYER_COUNT)]

        if info_trust > 0.0:
            possibility_player_scores = [
                info_trust
                * get_player_appearances(
                    possible_teams=possible_teams, target_player=player_id
                )
                for player_id in range(PLAYER_COUNT)
            ]

        print(f"{possibility} ({info_trust}): {len(possible_teams)}")

        for i, player_score in enumerate(possibility_player_scores):
            player_scores[i] += player_score

    print([f"{score:.2f}" for score in player_scores])
    print(sum(player_scores))


if __name__ == "__main__":
    main()
