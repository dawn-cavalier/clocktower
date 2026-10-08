from worldbuilder.demonInfo import DemonInfo, DemonInfoType
from worldbuilder.helper import is_demon


def check_for_demon(
    info_indices: list[int],
    learned_info: list[DemonInfo],
    possible_teams: list[list[int]],
):
    possible_demons: list[list[int]] = []
    for team in list(possible_teams):
        demons = list(team)

        for info_index in info_indices:
            is_inverted = info_index < 0

            info_index = max(info_index, 0)
            info = learned_info[info_index]

            # Ignore the information
            if is_inverted:
                continue

            match info.info_type:
                case DemonInfoType.NONE:
                    continue
                case DemonInfoType.PLAYER_IS_ROLE:
                    if info.target_players is None:
                        raise ValueError(
                            f"{info.info_type.name} has no target players!"
                        )
                    if info.seen_roles is None:
                        raise ValueError(f"{info.info_type.name} has no stated role!")
                    if len(info.target_players) != 1:
                        raise ValueError(
                            f"{info.info_type.name} received {len(info.target_players)} players when 1 was expected!"
                        )
                    if len(info.seen_roles) != 1:
                        raise ValueError(
                            f"{info.info_type.name} received {len(info.seen_roles)} players when 1 was expected!"
                        )

                    role = info.seen_roles[0]
                    player = info.target_players[0]

                    if is_demon(role):
                        demons = [d for d in demons if d == player]
                    else:
                        demons = [d for d in demons if d != player]

                case _:
                    raise ValueError(f"Unhandled InfoType: {info.info_type.name}")

        # If there's no valid demon on these assumptions, remove the team from possible teams
        if len(demons) == 0:
            possible_teams.remove(team)
        else:
            possible_demons.append(demons)

    return possible_demons
