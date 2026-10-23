from worldbuilder.game_info import GameInfo
from worldbuilder.prediction.game_state import build_game_state
from worldbuilder.prediction.prediction_calculator import calculate_predictions
from worldbuilder.role_enum import Role
from worldbuilder.info import Info, InfoType
from worldbuilder.test import test_12p_tb_game


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

    possibilities = __calculate_possibilities__(len(learned_info[1:]))

    is_evil_scores = [0.0 for _ in range(game_info.player_count)]
    is_demon_scores = [0.0 for _ in range(game_info.player_count)]
    is_outsider_scores = [0.0 for _ in range(game_info.player_count)]

    valid_trust = 1.0
    for possibility in possibilities:
        info_trust = __calculate_info_trust__(possibility, learned_info)
        if info_trust <= 0.0:
            continue

        game_state = build_game_state(learned_info, possibility, game_info)
        if len(game_state.evil_teams) == 0 or len(game_state.demons) == 0:
            valid_trust -= info_trust
            continue

        predictions = calculate_predictions(game_state, game_info, info_trust)

        is_evil_scores = [score + predictions.evil_player_scores[player]
                          for player, score in enumerate(is_evil_scores)]

        is_demon_scores = [score + predictions.demon_player_scores[player]
                           for player, score in enumerate(is_demon_scores)]

        is_outsider_scores = [score + predictions.outsider_player_scores[player]
                              for player, score in enumerate(is_outsider_scores)]

        print(
            f"{possibility}:\n\t" +
            f"Trust Score: {info_trust:.4f}\n\t" +
            f"Evil Teams: {len(game_state.evil_teams)}\n\t" +
            f"Outsiders: {len(game_state.outsiders)}\n\t" +
            f"Demons: {len(game_state.demons)}\n\t"
        )

    # Account for trust lost during removal
    is_evil_scores = [score / valid_trust for score in is_evil_scores]
    is_demon_scores = [score / valid_trust for score in is_demon_scores]
    is_outsider_scores = [score / valid_trust for score in is_outsider_scores]

    print(f"Player Seat:\t{[f"{player:<4}" for player in range(
        1, game_info.player_count + 1)]}")

    print(f"Evil Scores:\t{[f"{score:.2f}" for score in is_evil_scores]}")
    print(sum(is_evil_scores))

    print(f"Demon Scores:\t{[f"{score:.2f}" for score in is_demon_scores]}")
    print(sum(is_demon_scores))

    print(
        f"Outside Scores:\t{[f"{score:.2f}" for score in is_outsider_scores]}")
    print(sum(is_outsider_scores))


def __calculate_possibilities__(num_of_info: int):
    num_possibilities = 2**num_of_info
    possibilities: list[list[int]] = []

    for possibility_i in range(num_possibilities):
        new_possibility: list[int] = []
        for bit in range(num_of_info):
            if possibility_i >> bit & 1:
                new_possibility.append(bit + 1)
            else:
                new_possibility.append(-(bit + 1))
        possibilities.append(new_possibility)

    return possibilities


def __calculate_info_trust__(info_indices: list[int], learned_info: list[Info]):
    trust_score = 1.0

    for info_index in info_indices:
        is_inverted = info_index < 0
        info_trust = learned_info[abs(info_index)].info_trust
        if is_inverted:
            trust_score = trust_score * (1.0 - info_trust)
        else:
            trust_score = trust_score * info_trust

    return trust_score


if __name__ == "__main__":
    main()
    # cProfile.run('main()', sort="cumtime")
