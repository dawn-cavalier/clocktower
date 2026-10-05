from worldbuilder.helper import get_all_posibilities, get_info_trust
from worldbuilder.evilTeamInfo import EvilTeamInfo, EvilTeamInfoType
from worldbuilder.evilTeamHelper import (
    get_possible_evil_teams,
    get_player_appearances,
)

PLAYER_COUNT = 12
EVIL_COUNT = 3


def main() -> None:
    return


def test1():
    # Append only list!
    learned_info: list[EvilTeamInfo] = []

    # Set index zero to be a NONE info object
    learned_info.append(EvilTeamInfo(info_type=EvilTeamInfoType.NONE, source=-1, day=0))

    ### Learned information
    # Self is good
    new_info = EvilTeamInfo(
        info_type=EvilTeamInfoType.ALIGNMENT_KNOWN,
        source=0,
        day=0,
        is_good=True,
        target_players=[0],
    )
    new_info.info_trust = 1.0
    learned_info.append(new_info)

    possibilities = get_all_posibilities(len(learned_info[1:]))

    player_scores = [0.0 for _ in range(PLAYER_COUNT)]
    for possibility in possibilities:
        info_trust = get_info_trust(possibility, learned_info)
        possible_teams = get_possible_evil_teams(possibility, learned_info, EVIL_COUNT)

        possibility_player_scores: list[float] = [0.0 for _ in range(PLAYER_COUNT)]

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
