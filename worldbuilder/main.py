from worldbuilder.demonHelper import check_for_demon
from worldbuilder.helper import get_all_posibilities, get_info_trust
from worldbuilder.evilTeamHelper import get_possible_evil_teams
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

        # Filter Evil Teams based on Demon info
        demon_info = [info.get_demon_info() for info in learned_info]
        possible_demons = check_for_demon(
            possibility, demon_info, possible_evil_teams)

        if len(possible_evil_teams) > 0:
            evil_player_scores = [
                sum(1 for t in possible_evil_teams if player_id in t)
                * info_trust
                / len(possible_evil_teams)
                for player_id in range(PLAYER_COUNT)
            ]

        if len(possible_demons) > 0:
            demon_player_scores = [
                sum(1 / len(d) for d in possible_demons if player_id in d)
                * info_trust
                / len(possible_demons)
                for player_id in range(PLAYER_COUNT)
            ]

        for player, player_score in enumerate(evil_player_scores):
            is_evil_scores[player] += player_score

        for player, player_score in enumerate(demon_player_scores):
            is_demon_scores[player] += player_score

        # Print
        print(f"{possibility} ({info_trust:.4f}): {len(possible_evil_teams)}")

    # TODO: Review this bandaid
    if sum(is_evil_scores) > 0:
        is_evil_scores = [
            EVIL_COUNT * score / sum(is_evil_scores) for score in is_evil_scores
        ]
    print(f"Evil Scores:\t{[f"{score:.2f}" for score in is_evil_scores]}")
    # print(sum(is_evil_scores))

    # TODO: Review this bandaid
    if sum(is_demon_scores) > 0:
        is_demon_scores = [score / sum(is_demon_scores)
                           for score in is_demon_scores]
    print(f"Demon Scores:\t{[f"{score:.2f}" for score in is_demon_scores]}")
    # print(sum(is_demon_scores))


def testTBRoles(learned_info: list[Info]):
    # TODO: Should Info Source have it's own enum?
    info = Info(
        info_type=InfoType.STORYTELLER_GIVEN_ROLE,
        day=0,
        source=0,
        seen_roles=[Role.SLAYER],
        target_players=[0],
        is_good=True,
    )
    learned_info.append(info)

    info = Info(
        info_type=InfoType.SLAYER_KILL,
        day=0,
        source=0,
        info_trust=0.5,
        target_players=[2],
        is_good=False
    )
    learned_info.append(info)

    # info = Info(
    #     info_type=InfoType.FORTUNE_TELLER_PING,
    #     day=0,
    #     source=0,
    #     info_trust=0.5,
    #     target_players=[1, 2],
    #     is_yes=True
    # )
    # learned_info.append(info)

    # info = Info(
    #     info_type=InfoType.RAVENKEEPER_PING,
    #     day=0,
    #     source=0,
    #     info_trust=0.8,
    #     seen_roles=[Role.IMP],
    #     target_players=[11],
    #     # TODO: Should this be included or inferred off the role?
    #     is_good=False,
    # )
    # learned_info.append(info)

    # info = Info(
    #     info_type=InfoType.RAVENKEEPER_PING,
    #     day=0,
    #     source=0,
    #     info_trust=0.8,
    #     seen_roles=[Role.IMP],
    #     target_players=[10],
    #     # TODO: Should this be included or inferred off the role?
    #     is_good=False,
    # )
    # learned_info.append(info)

    # info = Info(
    #     info_type=InfoType.CHEF_NUMBER, day=0, source=0, info_trust=0.8, number=0
    # )
    # learned_info.append(info)

    # # info = Info(
    #     info_type=InfoType.WASHERWOMAN_PING,
    #     day=1,
    #     source=11,
    #     info_trust=0.8,
    #     seen_roles=[Role.EMPATH],
    #     target_players=[1, 2],
    # )
    # learned_info.append(info)

    # info = Info(
    #     info_type=InfoType.EMPATH_NUMBER,
    #     day=1,
    #     source=1,
    #     info_trust=0.8,
    #     target_players=[0, 2],
    #     number=1,
    # )
    # learned_info.append(info)

    # info = Info(
    #     info_type=InfoType.PLAYER_EXECUTED,
    #     day=1,
    #     source=-1,
    #     target_players=[10],
    # )
    # learned_info.append(info)

    # info = Info(
    #     info_type=InfoType.UNDERTAKER_INFO,
    #     day=3,
    #     source=2,
    #     info_trust=0.8,
    #     target_players=[10],
    #     seen_roles=[Role.BARON],
    #     is_good=False,
    # )
    # learned_info.append(info)

    # info = Info(
    #     info_type=InfoType.PLAYER_NIGHT_DEATH,
    #     day=1,
    #     source=-1,
    #     target_players=[1],
    # )
    # learned_info.append(info)

    # info = Info(
    #     info_type=InfoType.VIRGIN_TRIGGER,
    #     day=3,
    #     source=5,
    #     seen_roles=[Role.VIRGIN],
    #     target_players=[5],
    #     is_good=True,
    # )
    # learned_info.append(info)

    # info = Info(
    #     info_type=InfoType.VIRGIN_EXECUTE,
    #     day=3,
    #     source=-1,
    #     target_players=[3],
    #     is_good=True,
    # )
    # learned_info.append(info)

    # info = Info(
    #     info_type=InfoType.PLAYER_EXECUTED,
    #     day=1,
    #     source=-1,
    #     target_players=[3],
    # )
    # learned_info.append(info)

    # info = Info(
    #     info_type=InfoType.UNDERTAKER_INFO,
    #     day=3,
    #     source=2,
    #     info_trust=0.8,
    #     target_players=[3],
    #     seen_roles=[Role.INVESTIGATOR],
    #     is_good=True,
    # )
    # learned_info.append(info)


if __name__ == "__main__":
    main()
