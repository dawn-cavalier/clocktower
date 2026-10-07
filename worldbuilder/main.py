from worldbuilder.demonHelper import get_demon_scores
from worldbuilder.helper import get_all_posibilities, get_info_trust
from worldbuilder.evilTeamHelper import (
    get_possible_evil_teams,
    get_player_appearances,
)
from worldbuilder.info import Info, InfoType
from worldbuilder.rolesEnum import Role

PLAYER_COUNT = 12
EVIL_COUNT = 3


def main() -> None:
    # script = [
    #     # Townsfolk
    #     Role.WASHERWOMAN,
    #     Role.LIBRARIAN,
    #     Role.INVESTIGATOR,
    #     Role.CHEF,
    #     Role.EMPATH,
    #     Role.FORTUNE_TELLER,
    #     Role.UNDERTAKER,
    #     Role.MONK,
    #     Role.RAVENKEEPER,
    #     Role.VIRGIN,
    #     Role.SLAYER,
    #     Role.SOLDIER,
    #     Role.MAYOR,
    #     # Outsiders
    #     Role.BUTLER,
    #     Role.DRUNK,
    #     Role.RECLUSE,
    #     Role.SAINT,
    #     # Minions
    #     Role.POISONER,
    #     Role.SPY,
    #     Role.SCARLET_WOMAN,
    #     Role.BARON,
    #     # Demons
    #     Role.IMP,
    # ]

    # Append only list!
    learned_info: list[Info] = []

    # Set index zero to be a NONE info object
    learned_info.append(Info(info_type=InfoType.NONE, day=-1, source=-1))

    testTBRoles(learned_info=learned_info)

    possibilities = get_all_posibilities(len(learned_info[1:]))

    is_evil_scores = [0.0 for _ in range(PLAYER_COUNT)]
    is_demon_scores = [0.0 for _ in range(PLAYER_COUNT)]

    total_evil_teams_unweighted = 0

    for possibility in possibilities:
        info_trust = get_info_trust(possibility, learned_info)
        evil_player_scores: list[float] = [0.0 for _ in range(PLAYER_COUNT)]
        demon_player_scores: list[float] = [0.0 for _ in range(PLAYER_COUNT)]

        # TODO: Determine how necessary this is
        if info_trust <= 0.0:
            continue

        # Get Evil Teams
        evil_team_info = [info.get_evil_team_info() for info in learned_info]
        possible_evil_teams = get_possible_evil_teams(
            possibility, evil_team_info, EVIL_COUNT
        )
        evil_player_scores = [
            info_trust
            * get_player_appearances(
                possible_teams=possible_evil_teams, target_player=player_id
            )
            for player_id in range(PLAYER_COUNT)
        ]
        total_evil_teams_unweighted += len(possible_evil_teams)

        # Predict Demon for Evil Teams
        demon_info = [info.get_demon_info() for info in learned_info]
        for team in possible_evil_teams:
            print(get_demon_scores(possibility, demon_info, team, PLAYER_COUNT))

        for i, player_score in enumerate(evil_player_scores):
            is_evil_scores[i] += player_score

        # Demon Score Printing
        for i, player_score in enumerate(demon_player_scores):
            is_demon_scores[i] += player_score


        # ## Print
        # # Evil Player Scores
        # print(f"{possibility} ({info_trust:.4f}): {len(possible_evil_teams)}")


    print([f"{score:.2f}" for score in is_evil_scores])
    print(sum(is_evil_scores))

    # Normalization to have it be the range [0.0 - 1.0]
    is_demon_scores = [score / total_evil_teams_unweighted for score in is_demon_scores]
    print([f"{score:.2f}" for score in is_demon_scores])
    print(sum(is_demon_scores))

    return


def testTBRoles(learned_info: list[Info]):
    # TODO: Should Info Source have it's own enum?
    info = Info(
        info_type=InfoType.STORYTELLER_GIVEN_ROLE,
        day=0,
        source=0,
        seen_roles=[Role.CHEF],
        target_players=[0],
        is_good=True,
    )
    learned_info.append(info)

    # info = Info(
    #     info_type=InfoType.CHEF_NUMBER, day=0, source=0, info_trust=0.8, number=0
    # )
    # learned_info.append(info)

    # info = Info(
    #     info_type=InfoType.WASHERWOMAN_PING,
    #     day=1,
    #     source=11,
    #     seen_roles=[Role.EMPATH],
    #     target_players=[1, 2],
    # )
    # info.info_trust = 0.5
    # learned_info.append(info)

    # info = Info(
    #     info_type=InfoType.EMPATH_NUMBER,
    #     day=1,
    #     source=1,
    #     target_players=[0, 2],
    #     number=1,
    # )
    # info.info_trust = 0.5
    # learned_info.append(info)

    # info = Info(
    #     info_type=InfoType.PLAYER_EXECUTED,
    #     day=1,
    #     source=-1,
    #     target_players=[10],
    # )
    # info.info_trust = 0.5
    # learned_info.append(info)

    # info = Info(
    #     info_type=InfoType.UNDERTAKER_INFO,
    #     day=3,
    #     source=2,
    #     target_players=[10],
    #     seen_roles=[Role.BARON],
    #     is_good=False,
    # )
    # info.info_trust = 0.5
    # learned_info.append(info)

    # info = Info(info_type=InfoType.VIRGIN_TRIGGER, day=3, source=5)
    # info.info_trust = 1.0
    # learned_info.append(info)

    # info = Info(info_type=InfoType.VIRGIN_EXECUTE, day=3, source=-1, target_players=[3])
    # info.info_trust = 1.0
    # learned_info.append(info)

    # info = Info(
    #     info_type=InfoType.UNDERTAKER_INFO,
    #     day=3,
    #     source=2,
    #     target_players=[3],
    #     seen_roles=[Role.INVESTIGATOR],
    #     is_good=True,
    # )
    # info.info_trust = 0.5
    # learned_info.append(info)


if __name__ == "__main__":
    main()
