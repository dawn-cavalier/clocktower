
from worldbuilder.exhaustive_search.exhaustive_search import search_worlds_exhaustively  # type: ignore
from worldbuilder.game_info import GameInfo
from worldbuilder.role_enum import Role
from worldbuilder.info import Info, InfoType
import worldbuilder.test as test
from worldbuilder.world_scoring.world_scorer import search_world_scores


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

    # learned_info += test.generate_start_of_game_info(0, True, Role.LIBRARIAN)
    # learned_info += test.generate_investigator_ping(
    #     day=0, source=5, targets=[1, 2], seen_role=Role.BARON
    # )
    # learned_info += test.generate_chef_number(
    #     day=0, source=1, number=2
    # )
    learned_info += test.generate_empath_number(
        day=0, source=2, number=2, living_neighbors=[1, 3]
    )

    is_evil_scores = [0.0 for _ in range(game_info.player_count)]
    is_demon_scores = [0.0 for _ in range(game_info.player_count)]
    is_minion_scores = [0.0 for _ in range(game_info.player_count)]
    is_outsider_scores = [0.0 for _ in range(game_info.player_count)]

    (
        is_evil_scores,
        is_demon_scores,
        is_minion_scores,
        is_outsider_scores
    ) = search_world_scores(game_info, learned_info)

    if sum(is_evil_scores) > 0:
        print(f"Evil Scores:\t{[f"{score:.3f}" for score in is_evil_scores]}")
        print(sum(is_evil_scores))

    if sum(is_demon_scores) > 0:
        print(
            f"Demon Scores:\t{[f"{score:.3f}" for score in is_demon_scores]}")
        print(sum(is_demon_scores))

    if sum(is_minion_scores) > 0:
        print(
            f"Minion Scores:\t{[f"{score:.3f}" for score in is_minion_scores]}"
        )
        print(sum(is_minion_scores))

    if sum(is_outsider_scores) > 0:
        print(
            f"Outside Scores:\t{[f"{score:.3f}" for score in is_outsider_scores]}")
        print(sum(is_outsider_scores))


if __name__ == "__main__":
    main()
    # cProfile.run('main()', sort="cumtime")
