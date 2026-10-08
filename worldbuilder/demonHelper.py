from worldbuilder.demonInfo import DemonInfo, DemonInfoType
from worldbuilder.helper import is_demon


def get_demon_scores(
    info_indices: list[int], learned_info: list[DemonInfo], possible_teams: list[list[int]], player_count: int
):
    for original_team in list(possible_teams):
        team = list(original_team)

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
                            f"{info.info_type.name} has no target players!")
                    if info.seen_roles is None:
                        raise ValueError(
                            f"{info.info_type.name} has no stated role!")
                    if len(info.target_players) != 1:
                        raise ValueError(
                            f"{info.info_type.name} received {len(info.target_players)} players when 1 was expected!")
                    if len(info.seen_roles) != 1:
                        raise ValueError(
                            f"{info.info_type.name} received {len(info.seen_roles)} players when 1 was expected!")

                    role = info.seen_roles[0]
                    player = info.target_players[0]

                    if is_demon(role):
                        team = [p for p in team if p == player]
                    else:
                        team = [p for p in team if p != player]

                case _:
                    raise ValueError(
                        f"Unhandled InfoType: {info.info_type.name}")

        # If there's no valid demon on these assumptions, remove the team from possible teams
        if len(team) == 0:
            possible_teams.remove(original_team)
