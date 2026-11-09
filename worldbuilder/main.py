
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
        trust=1.0,
        is_good=False,
        role=Role.SPY
    )
    # learned_info += info_builder.generate_investigator_ping(
    #     day=0,
    #     source=0,
    #     trust=0.8,
    #     targets=[1, 2],
    #     seen_role=Role.BARON,
    # )

    (
        demon_scores,
        minion_scores,
        outsider_scores,
        townsfolk_scores
    ) = search_world_scores(game_info, learned_info)

    if sum(demon_scores) > 0:
        print(
            f"Demon Scores:\t\t{[f"{score:.3f}" for score in demon_scores]}")
        print(sum(demon_scores))

    if sum(minion_scores) > 0:
        print(
            f"Minion Scores:\t\t{[f"{score:.3f}" for score in minion_scores]}"
        )
        print(sum(minion_scores))

    if sum(outsider_scores) > 0:
        print(
            f"Outsider Scores:\t{[f"{score:.3f}" for score in outsider_scores]}")
        print(sum(outsider_scores))

    if sum(townsfolk_scores) > 0:
        print(
            f"Townsfolk Scores:\t{[f"{score:.3f}" for score in townsfolk_scores]}")
        print(sum(townsfolk_scores))


if __name__ == "__main__":
    main()

    # tracemalloc.start()
    # main()
    # print(tracemalloc.get_traced_memory())
    # tracemalloc.stop()

    # cProfile.run('main()', sort="cumtime")
