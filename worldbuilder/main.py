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

    # testTBRoles(learned_info=learned_info)

    possibilities = get_all_posibilities(
        len([info for info in learned_info if info.source != -1])
    )
    player_scores = [0.0 for _ in range(PLAYER_COUNT)]
    for possibility in possibilities:
        info_trust = get_info_trust(possibility, learned_info)

        # Get Evil Teams
        evil_team_info = [info.get_evil_team_info() for info in learned_info]
        possible_evil_teams = get_possible_evil_teams(
            possibility, evil_team_info, EVIL_COUNT
        )

        possibility_player_scores: list[float] = [0.0 for _ in range(PLAYER_COUNT)]

        if info_trust > 0.0:
            possibility_player_scores = [
                info_trust
                * get_player_appearances(
                    possible_teams=possible_evil_teams, target_player=player_id
                )
                for player_id in range(PLAYER_COUNT)
            ]

        print(f"{possibility} ({info_trust}): {len(possible_evil_teams)}")

        for i, player_score in enumerate(possibility_player_scores):
            player_scores[i] += player_score

    print([f"{score:.2f}" for score in player_scores])
    print(sum(player_scores))

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
    # TODO: Should this be in constructor?
    info.info_trust = 1.0
    learned_info.append(info)

    info = Info(info_type=InfoType.CHEF_NUMBER, day=0, source=0, number=1)
    info.info_trust = 1.0
    learned_info.append(info)

    info = Info(
        info_type=InfoType.WASHERWOMAN_PING,
        day=1,
        source=11,
        seen_roles=[Role.EMPATH],
        target_players=[1, 2],
    )
    info.info_trust = 1.0
    learned_info.append(info)

    info = Info(
        info_type=InfoType.EMPATH_NUMBER,
        day=1,
        source=1,
        target_players=[0, 2],
        number=1,
    )
    info.info_trust = 1.0
    learned_info.append(info)

    info = Info(
        info_type=InfoType.PLAYER_EXECUTED,
        day=1,
        source=-1,
        target_players=[10],
    )
    info.info_trust = 1.0
    learned_info.append(info)

    info = Info(
        info_type=InfoType.UNDERTAKER_INFO,
        day=3,
        source=2,
        target_players=[10],
        seen_roles=[Role.BARON],
        is_good=False,
    )
    info.info_trust = 1.0
    learned_info.append(info)


if __name__ == "__main__":
    main()
