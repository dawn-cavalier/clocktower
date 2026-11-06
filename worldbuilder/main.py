
import cProfile  # type: ignore
import tracemalloc  # type: ignore
from worldbuilder.game_info import GameInfo
from worldbuilder.role_enum import Role
from worldbuilder.info import Info
import worldbuilder.info_builder as info_builder  # type: ignore
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

    game_info = GameInfo(player_count=10, script=script)
    # Append only list!
    learned_info: list[Info] = []
    learned_info += info_builder.generate_start_of_game_info(
        player_id=0,
        is_good=True,
        trust=0.8,
        role=Role.INVESTIGATOR
    )

    (
        is_demon_scores,
        is_minion_scores,
        is_outsider_scores,
        is_townsfolk_scores
    ) = search_world_scores(game_info, learned_info)

    if sum(is_demon_scores) > 0:
        print(
            f"Demon Scores:\t\t{[f"{score:.3f}" for score in is_demon_scores]}")
        print(sum(is_demon_scores))

    if sum(is_minion_scores) > 0:
        print(
            f"Minion Scores:\t\t{[f"{score:.3f}" for score in is_minion_scores]}"
        )
        print(sum(is_minion_scores))

    if sum(is_outsider_scores) > 0:
        print(
            f"Outsider Scores:\t{[f"{score:.3f}" for score in is_outsider_scores]}")
        print(sum(is_outsider_scores))

    if sum(is_townsfolk_scores) > 0:
        print(
            f"Townsfolk Scores:\t{[f"{score:.3f}" for score in is_townsfolk_scores]}")
        print(sum(is_townsfolk_scores))


if __name__ == "__main__":
    main()

    # tracemalloc.start()
    # main()
    # print(tracemalloc.get_traced_memory())
    # tracemalloc.stop()

    # cProfile.run('main()', sort="cumtime")
