from terminal_io.user_input import ask_for_game_info


def main():
    game_info = ask_for_game_info()
    # storyteller = ask_for_storyteller()

    # players = generate_players(game_info)
    # grimoire = storyteller.generate_grimoire(game_info)

    # game = Game(
    #     game_info=game_info,
    #     storyteller=storyteller,
    #     players=players,
    #     grimoire=grimoire,
    # )

    # game_state = GameState.GAME_START
    # while True:
    #     if game_state == GameState.EXIT:
    #         break
    #     game_state, game = updater_by_game_state[game_state](game)


if __name__ == "__main__":
    main()
