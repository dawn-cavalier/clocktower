from worldbuilder.game_info import GameInfo
from worldbuilder.demon.demon_helper import check_for_demon
from worldbuilder.outsiders.outsider_helper import get_possible_outsiders
from worldbuilder.role_enum import Role
from worldbuilder.helper import get_all_posibilities, get_info_trust
from worldbuilder.evil_team.evil_team_helper import get_possible_evil_teams
from worldbuilder.info import Info, InfoType
from worldbuilder.test import test_12p_tb_game, test_role  # type: ignore

import cProfile  # type: ignore


def main() -> None:
    script = [
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
    ]

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

    lost_trust = 0.0
    for possibility in possibilities:
        info_trust = get_info_trust(possibility, learned_info)
        evil_player_scores: list[float] = [
            0.0 for _ in range(game_info.player_count)]
        demon_player_scores: list[float] = [
            0.0 for _ in range(game_info.player_count)]
        outsider_player_scores: list[float] = [
            0.0 for _ in range(game_info.player_count)
        ]

        # TODO: Determine how necessary this is
        if info_trust <= 0.0:
            continue

        # TODO: Is it faster to get Demons and filter teams based on them?
        # Get Evil Teams
        evil_team_info = [info.get_evil_team_info() for info in learned_info]
        possible_evil_teams = get_possible_evil_teams(
            possibility, evil_team_info, game_info
        )

        if len(possible_evil_teams) == 0:
            continue

        # Filter Evil Teams based on Demon info
        demon_info = [info.get_demon_info() for info in learned_info]
        possible_demons = check_for_demon(
            possibility, demon_info, possible_evil_teams, game_info)

        if len(possible_demons) == 0:
            lost_trust += info_trust

        if len(possible_evil_teams) == 0 or len(possible_demons) == 0:
            continue

        # Get possible Outsiders combinations
        outsider_info = [info.get_outsider_info() for info in learned_info]
        possible_outsiders_groups = get_possible_outsiders(
            possibility, outsider_info, possible_evil_teams, game_info
        )

        # TODO: So the thing is possible evil teams and possible demons should be the same length
        # This currently doesn't show that relationship
        if len(possible_evil_teams) > 0:
            evil_player_scores = [
                sum(1 for t in possible_evil_teams if player_id in t)
                * info_trust
                / len(possible_evil_teams)
                for player_id in range(game_info.player_count)
            ]

        if len(possible_demons) > 0:
            # TODO: What if there is more than one demon?
            demon_player_scores = [
                sum(1 / len(d) for d in possible_demons if player_id in d)
                * info_trust
                / len(possible_demons)
                for player_id in range(game_info.player_count)
            ]

        if len(possible_outsiders_groups) > 0:
            group_count = len(possible_outsiders_groups)
            for outsider_group in possible_outsiders_groups:
                outsider_guess_size: dict[int, int] = {}
                for count in game_info.get_possible_outsider_counts():
                    guess_size = len(
                        [o for o in outsider_group if len(o) == count])
                    if guess_size > 0:
                        outsider_guess_size[count] = guess_size

                for outsiders in outsider_group:
                    size = len(outsiders)
                    weight: float
                    if len(outsider_guess_size) == 1:
                        weight = 1.0
                    elif len(outsider_guess_size) < len(game_info.get_possible_outsider_counts()):
                        total = 0.0
                        for guess_size in outsider_guess_size:
                            result = game_info.get_possible_outsider_counts().get(guess_size)
                            if result is None:
                                raise ValueError(
                                    f"Attempting to access invalid outsider count: {guess_size}")
                            total += result
                        result = game_info.get_possible_outsider_counts().get(size)
                        if result is None:
                            raise ValueError(
                                f"Attempting to access invalid outsider count: {size}")
                        weight = result / total
                    else:
                        result = game_info.get_possible_outsider_counts().get(size)
                        if result is None:
                            raise ValueError(
                                f"Attempting to access invalid outsider count: {size}")
                        weight = result

                    group_size_population = outsider_guess_size.get(size)

                    if group_size_population is None:
                        raise ValueError(
                            f"Getting count for unknown size: {size} for {outsider_guess_size}")

                    for outsider in outsiders:
                        outsider_player_scores[outsider] += info_trust * weight / \
                            (group_size_population * group_count)

        for player, player_score in enumerate(evil_player_scores):
            is_evil_scores[player] += player_score

        for player, player_score in enumerate(demon_player_scores):
            is_demon_scores[player] += player_score

        for player, player_score in enumerate(outsider_player_scores):
            is_outsider_scores[player] += player_score

        # print(
        #     f"{possibility}:\n\tTrust Score: {info_trust:.4f}\n\tEvil Teams: {len(possible_evil_teams)}"
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
