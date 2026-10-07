from worldbuilder.demonInfo import DemonInfo, DemonInfoType
from worldbuilder.helper import is_demon


def get_demon_score(
    info_indices: list[int], learned_info: list[DemonInfo], demon: int, team: list[int]
) -> float:
    demon_score = 0.0
     
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

                if demon not in info.target_players:
                    continue

                for role in info.seen_roles:
                    if is_demon(role):
                        demon_score = 1/len(info.seen_roles)

            case _:
                raise ValueError(f"Unhandled InfoType: {info.info_type.name}")

    return demon_score
