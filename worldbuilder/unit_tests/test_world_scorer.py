from worldbuilder import info_builder
from worldbuilder.game_info import GameInfo
from worldbuilder.helper import is_minion
from worldbuilder.info import Info
from worldbuilder.role_enum import Role
from worldbuilder.world_scoring.world_scorer import search_world_scores


TROUBLE_BREWING = {
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

SECTS_AND_VIOLETS = {
    # Townsfolk
    Role.CLOCKMAKER,
    Role.DREAMER,
    Role.SNAKE_CHARMER,
    Role.MATHEMATICIAN,
    Role.FLOWERGIRL,
    Role.TOWN_CRIER,
    Role.ORACLE,
    Role.SAVANT,
    Role.SEAMSTRESS,
    Role.PHILOSOPHER,
    Role.ARTIST,
    Role.JUGGLER,
    Role.SAGE,
    # Outsiders
    Role.MUTANT,
    Role.SWEETHEART,
    Role.BARBER,
    Role.KLUTZ,
    # Minions
    Role.EVIL_TWIN,
    Role.WITCH,
    Role.CERENOVUS,
    Role.PIT_HAG,
    # Demons
    Role.FANG_GU,
    Role.VIGORMORTIS,
    Role.NO_DASHII,
    Role.VORTOX
}

BAD_MOON_RISING = {
    # Townsfolk
    Role.GRANDMOTHER,
    Role.SAILOR,
    Role.CHAMBERMAID,
    Role.EXORCIST,
    Role.INNKEEPER,
    Role.GAMBLER,
    Role.GOSSIP,
    Role.COURTIER,
    Role.PROFESSOR,
    Role.MINSTREL,
    Role.TEA_LADY,
    Role.PACIFIST,
    Role.FOOL,
    # Outsiders
    Role.GOON,
    Role.LUNATIC,
    Role.TINKER,
    Role.MOONCHILD,
    # Minions
    Role.GODFATHER,
    Role.DEVILS_ADVOCATE,
    Role.ASSASSIN,
    Role.MASTERMIND,
    # Demons
    Role.ZOMBUUL,
    Role.PUKKA,
    Role.SHABALOTH,
    Role.PO
}

ACCECPTABLE_ERROR = 1e-9


def test_base_setup():
    for i in range(7, 16):
        _check_world_scores_tb(i)
        _check_world_scores_snv(i)
        _check_world_scores_bmr(i)


def test_learning_baron_tb():
    for i in range(7, 10):
        game_info = GameInfo(player_count=i, script=TROUBLE_BREWING)
        learned_info: list[Info] = []
        learned_info += info_builder.generate_start_of_game_info(
            player_id=0,
            odds_sober=1.0,
            is_good=False,
            role=Role.BARON
        )

        (
            is_demon_scores,
            is_minion_scores,
            is_outsider_scores,
            is_townsfolk_scores
        ) = search_world_scores(game_info, learned_info)

        _check_sums(
            is_demon_scores,
            is_minion_scores,
            is_outsider_scores,
            is_townsfolk_scores,
            game_info
        )

        assert abs(
            sum(is_outsider_scores) -
            (game_info.outsider_count_base + 2)
        ) < ACCECPTABLE_ERROR


def test_ravenkeeper_learning_demon_tb():
    odds_sober = 0.9
    for player_count in range(7, 16):
        game_info = GameInfo(player_count=player_count, script=TROUBLE_BREWING)
        learned_info: list[Info] = []
        learned_info += info_builder.generate_ravenkeeper_ping(
            source=0,
            day=0,
            odds_sober=odds_sober,
            seen_role=Role.IMP,
            target=1
        )

        (
            is_demon_scores,
            is_minion_scores,
            is_outsider_scores,
            is_townsfolk_scores
        ) = search_world_scores(game_info, learned_info)

        _check_sums(
            is_demon_scores,
            is_minion_scores,
            is_outsider_scores,
            is_townsfolk_scores,
            game_info
        )

        probability_demon = 1/player_count

        probability_info_correct = odds_sober + \
            (1-odds_sober)/(len(TROUBLE_BREWING) - 1)
        probability_info_incorrect = (1-odds_sober)/(len(TROUBLE_BREWING) - 1)

        probability_info = (
            ((probability_demon) *
             probability_info_correct) +
            ((1-probability_demon) *
             probability_info_incorrect)
        )

        bayes_score = (
            probability_info_correct*probability_demon / probability_info
        )

        assert abs(
            is_demon_scores[1] - bayes_score
        ) < ACCECPTABLE_ERROR


def test_learning_demon_snv():
    for i in range(7, 10):
        game_info = GameInfo(player_count=i, script=TROUBLE_BREWING)
        learned_info: list[Info] = []
        learned_info += info_builder.generate_start_of_game_info(
            player_id=0,
            odds_sober=1.0,
            is_good=False,
            role=Role.BARON
        )

        (
            is_demon_scores,
            is_minion_scores,
            is_outsider_scores,
            is_townsfolk_scores
        ) = search_world_scores(game_info, learned_info)

        _check_sums(
            is_demon_scores,
            is_minion_scores,
            is_outsider_scores,
            is_townsfolk_scores,
            game_info
        )

        assert abs(
            sum(is_outsider_scores) -
            max(game_info.outsider_count_base + 2, 0)
        ) < ACCECPTABLE_ERROR

        game_info = GameInfo(player_count=i, script=SECTS_AND_VIOLETS)
        learned_info: list[Info] = []
        learned_info += info_builder.generate_start_of_game_info(
            player_id=0,
            odds_sober=1.0,
            is_good=False,
            role=Role.FANG_GU
        )

        (
            is_demon_scores,
            is_minion_scores,
            is_outsider_scores,
            is_townsfolk_scores
        ) = search_world_scores(game_info, learned_info)

        _check_sums(
            is_demon_scores,
            is_minion_scores,
            is_outsider_scores,
            is_townsfolk_scores,
            game_info
        )

        assert abs(
            sum(is_outsider_scores) -
            max(game_info.outsider_count_base + 1, 0)
        ) < ACCECPTABLE_ERROR


def _check_world_scores_tb(player_count: int):
    game_info = GameInfo(player_count=player_count, script=TROUBLE_BREWING)
    learned_info: list[Info] = []
    (
        is_demon_scores,
        is_minion_scores,
        is_outsider_scores,
        is_townsfolk_scores
    ) = search_world_scores(game_info, learned_info)

    _check_sums(
        is_demon_scores,
        is_minion_scores,
        is_outsider_scores,
        is_townsfolk_scores,
        game_info
    )

    for score in is_demon_scores:
        assert abs(
            score - game_info.demon_count_base/player_count
        ) <= ACCECPTABLE_ERROR

    for score in is_minion_scores:
        assert abs(
            score - game_info.minion_count_base/player_count
        ) <= ACCECPTABLE_ERROR

    expected_score = (
        (game_info.townsfolk_count_base) -
        (
            2*game_info.minion_count_base /
            sum(
                1 for role in TROUBLE_BREWING if is_minion(role)
            )
        )
    ) / player_count
    for score in is_townsfolk_scores:
        assert abs(
            score - expected_score
        ) <= ACCECPTABLE_ERROR

    expected_score = (
        game_info.outsider_count_base + (
            2*game_info.minion_count_base /
            sum(
                1 for role in TROUBLE_BREWING if is_minion(role)
            )
        )
    ) / player_count
    for score in is_outsider_scores:
        assert abs(
            score - expected_score
        ) <= ACCECPTABLE_ERROR


def _check_world_scores_snv(player_count: int):
    game_info = GameInfo(player_count=player_count, script=SECTS_AND_VIOLETS)
    learned_info: list[Info] = []
    (
        is_demon_scores,
        is_minion_scores,
        is_outsider_scores,
        is_townsfolk_scores
    ) = search_world_scores(game_info, learned_info)
    _check_sums(
        is_demon_scores,
        is_minion_scores,
        is_outsider_scores,
        is_townsfolk_scores,
        game_info
    )

    for score in is_demon_scores:
        assert abs(
            score - game_info.demon_count_base/player_count
        ) <= ACCECPTABLE_ERROR

    for score in is_minion_scores:
        assert abs(
            score - game_info.minion_count_base/player_count
        ) <= ACCECPTABLE_ERROR

    expected_score = (
        (game_info.townsfolk_count_base)
    ) / player_count

    if game_info.outsider_count_base == 0:
        expected_score = (
            (game_info.townsfolk_count_base) - 1/4
        ) / player_count

    for score in is_townsfolk_scores:
        assert abs(
            score - expected_score
        ) <= ACCECPTABLE_ERROR

    expected_score = (
        game_info.outsider_count_base
    ) / player_count

    if game_info.outsider_count_base == 0:
        expected_score = (
            (game_info.outsider_count_base) + 1/4
        ) / player_count

    for score in is_outsider_scores:
        assert abs(
            score - expected_score
        ) <= ACCECPTABLE_ERROR


def _check_world_scores_bmr(player_count: int):
    game_info = GameInfo(player_count=player_count, script=BAD_MOON_RISING)
    learned_info: list[Info] = []
    (
        is_demon_scores,
        is_minion_scores,
        is_outsider_scores,
        is_townsfolk_scores
    ) = search_world_scores(game_info, learned_info)
    _check_sums(
        is_demon_scores,
        is_minion_scores,
        is_outsider_scores,
        is_townsfolk_scores,
        game_info
    )
    for score in is_demon_scores:
        assert abs(
            score - game_info.demon_count_base/player_count
        ) <= ACCECPTABLE_ERROR

    for score in is_minion_scores:
        assert abs(
            score - game_info.minion_count_base/player_count
        ) <= ACCECPTABLE_ERROR

    expected_score = (
        (game_info.townsfolk_count_base)
    ) / player_count

    if game_info.outsider_count_base == 0:
        expected_score = (
            (game_info.townsfolk_count_base) - game_info.minion_count_base/sum(
                1 for role in BAD_MOON_RISING if is_minion(role)
            )
        ) / player_count

    for score in is_townsfolk_scores:
        assert abs(
            score - expected_score
        ) <= ACCECPTABLE_ERROR

    expected_score = (
        game_info.outsider_count_base
    ) / player_count

    if game_info.outsider_count_base == 0:
        expected_score = (
            (game_info.outsider_count_base) + game_info.minion_count_base/sum(
                1 for role in BAD_MOON_RISING if is_minion(role)
            )
        ) / player_count

    for score in is_outsider_scores:
        assert abs(
            score - expected_score
        ) <= ACCECPTABLE_ERROR


def _check_sums(
    is_demon_scores: list[float],
    is_minion_scores: list[float],
    is_outsider_scores: list[float],
    is_townsfolk_scores: list[float],
    game_info: GameInfo
):
    assert abs(sum(is_demon_scores) -
               game_info.demon_count_base) <= ACCECPTABLE_ERROR
    assert abs(sum(is_minion_scores) -
               game_info.minion_count_base) <= ACCECPTABLE_ERROR
    assert (
        abs(
            sum(is_outsider_scores) + sum(is_townsfolk_scores) -
            (game_info.outsider_count_base + game_info.townsfolk_count_base)
        ) <= ACCECPTABLE_ERROR
    )
