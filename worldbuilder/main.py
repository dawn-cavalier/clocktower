from worldbuilder.demon.demonHelper import check_for_demon
from worldbuilder.helper import get_all_posibilities, get_info_trust
from worldbuilder.evilTeam.evilTeamHelper import get_possible_evil_teams
from worldbuilder.info import Info, InfoType
from worldbuilder.test import testTBGame1

PLAYER_COUNT = 12
EVIL_COUNT = 3
DEMON_COUNT = 1


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

    testTBGame1(learned_info=learned_info)

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
        possible_demons = check_for_demon(possibility, demon_info, possible_evil_teams)

        if len(possible_evil_teams) > 0:
            evil_player_scores = [
                sum(1 for t in possible_evil_teams if player_id in t)
                * info_trust
                / len(possible_evil_teams)
                for player_id in range(PLAYER_COUNT)
            ]

        if len(possible_demons) > 0:
            # TODO: What if there is more than one demon?
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
        print(
            f"{possibility}:\n\tTrust Score: {info_trust:.4f}\n\tEvil Teams: {len(possible_evil_teams)}"
        )

    print(f"Player Seat:\t{[f"{player:<4}" for player in range(1, PLAYER_COUNT + 1)]}")

    # TODO: Review this bandaid
    # if sum(is_evil_scores) > 0:
    #     is_evil_scores = [
    #         EVIL_COUNT * score / sum(is_evil_scores) for score in is_evil_scores
    #     ]
    print(f"Evil Scores:\t{[f"{score:.2f}" for score in is_evil_scores]}")
    print(sum(is_evil_scores))

    # TODO: Review this bandaid
    # if sum(is_demon_scores) > 0:
    #     is_demon_scores = [
    #         DEMON_COUNT * score / sum(is_demon_scores) for score in is_demon_scores
    #     ]
    print(f"Demon Scores:\t{[f"{score:.2f}" for score in is_demon_scores]}")
    print(sum(is_demon_scores))



if __name__ == "__main__":
    main()
