from worldbuilder.game_info import GameInfo
from worldbuilder.demon.demon_helper import check_for_demon
from worldbuilder.game_state import GameState
from worldbuilder.outsiders.outsider_helper import get_possible_outsiders
from worldbuilder.role_enum import Role
from worldbuilder.helper import get_all_posibilities, get_dead_players, get_info_trust
from worldbuilder.evil_team.evil_team_helper import get_possible_evil_teams
from worldbuilder.info import Info, InfoType
from worldbuilder.test import test_12p_tb_game, test_role  # type: ignore

import cProfile  # type: ignore


def main() -> None:
    script = {
        # Townsfolk
        Role.WASHERWOMAN,
        Role.LIBRARIAN,
        Role.INVESTIGATOR,
        Role.CHEF,
        Role.EMPATH,
        Role.FORTUNE_TELLER,
        Role.UNDERTAKER,
        Role.MONK,
        Role.RAVENKEEPER,
        Role.VIRGIN,
        Role.SLAYER,
        Role.SOLDIER,
        Role.MAYOR,
        # Outsiders
        Role.BUTLER,
        Role.DRUNK,
        Role.RECLUSE,
        Role.SAINT,
        # Minions
        Role.POISONER,
        Role.SPY,
        Role.SCARLET_WOMAN,
        Role.BARON,
        # Demons
        Role.IMP,
    }

    game_info = GameInfo(player_count=12, script=script)
    # Append only list!
    learned_info: list[Info] = []

    # Set index zero to be a NONE info object
    learned_info.append(Info(info_type=InfoType.NONE, day=-1, source=-1))

    test_12p_tb_game(learned_info=learned_info)
    # test_role(learned_info=learned_info)

    possibilities = get_all_posibilities(len(learned_info[1:]))

    is_evil_scores = [0.0 for _ in range(game_info.player_count)]
    is_demon_scores = [0.0 for _ in range(game_info.player_count)]
    is_outsider_scores = [0.0 for _ in range(game_info.player_count)]

    # Since all player death are 100% certain
    night_deaths, day_deaths, execution_deaths = get_dead_players(learned_info)

    lost_trust = 0.0
    for possibility in possibilities:
        game_state: GameState = GameState(game_info)
        game_state.night_deaths = night_deaths
        game_state.day_deaths = day_deaths
        game_state.execution_deaths = execution_deaths

        info_trust = get_info_trust(possibility, learned_info)
        if info_trust <= 0.0:
            continue

        # Get Evil Teams
        evil_team_info = [info.get_evil_team_info() for info in learned_info]
        possible_evil_teams = get_possible_evil_teams(
            possibility, evil_team_info, game_info
        )

        if len(possible_evil_teams) == 0:
            continue

        game_state.evil_teams = possible_evil_teams

        # Filter Evil Teams based on Demon info
        demon_info = [info.get_demon_info() for info in learned_info]
        possible_demons = check_for_demon(
            possibility, demon_info, game_info)

        if len(possible_demons) == 0:
            lost_trust += info_trust
            continue

        game_state.demons = possible_demons

        # Get possible Outsiders combinations
        outsider_info = [info.get_outsider_info() for info in learned_info]
        possible_outsiders = get_possible_outsiders(
            possibility, outsider_info, game_info
        )

        game_state.outsiders = possible_outsiders

        game_state.process(game_info, info_trust)

        if len(game_state.evil_teams) == 0 or len(game_state.demons) == 0:
            lost_trust += info_trust

        for player, player_score in enumerate(game_state.evil_player_scores):
            is_evil_scores[player] += player_score

        for player, player_score in enumerate(game_state.demon_player_scores):
            is_demon_scores[player] += player_score

        for player, player_score in enumerate(game_state.outsider_player_scores):
            is_outsider_scores[player] += player_score

        # print(
        #     f"{possibility}:\n\t" +
        #     f"Trust Score: {info_trust:.4f}\n\t" +
        #     f"Evil Teams: {len(game_state.evil_teams)}\n\t" +
        #     f"Outsiders: {len(game_state.outsiders)}\n\t" +
        #     f"Demons: {len(game_state.demons)}\n\t"
        # )

    # Account for trust lost during removal
    is_evil_scores = [score / (1-lost_trust) for score in is_evil_scores]
    is_demon_scores = [score / (1-lost_trust) for score in is_demon_scores]
    is_outsider_scores = [score / (1-lost_trust)
                          for score in is_outsider_scores]

    print(f"Player Seat:\t{[f"{player:<4}" for player in range(
        1, game_info.player_count + 1)]}")

    print(f"Evil Scores:\t{[f"{score:.2f}" for score in is_evil_scores]}")
    print(sum(is_evil_scores))

    print(f"Demon Scores:\t{[f"{score:.2f}" for score in is_demon_scores]}")
    print(sum(is_demon_scores))

    print(
        f"Outside Scores:\t{[f"{score:.2f}" for score in is_outsider_scores]}")
    print(sum(is_outsider_scores))


if __name__ == "__main__":
    main()
    # cProfile.run('main()', sort="cumtime")
