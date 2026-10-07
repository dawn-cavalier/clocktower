from worldbuilder.demonInfo import DemonInfo, DemonInfoType
from worldbuilder.helper import is_demon


def get_demon_scores(
    info_indices: list[int], learned_info: list[DemonInfo], team: list[int], player_count: int
) -> list[float]:
    demon_scores = [0.0 for _ in range(player_count)]
     
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
            case DemonInfoType.IS_CHARACTER:
                if info.target_players is None:
                    raise ValueError(f"{info.info_type.name} has no target players!")
                if info.seen_roles is None:
                    raise ValueError(f"{info.info_type.name} has no stated role!")

                targeted_team_members = [player for player in team if player in info.target_players]

                for role in info.seen_roles:
                    if is_demon(role):
                        if len(targeted_team_members) == 0:
                            # IDK, blow up?
                            continue




                if len(targeted_team_members) == 0:
                    continue


            case _:
                raise ValueError(f"Unhandled InfoType: {info.info_type.name}")

    return demon_scores
