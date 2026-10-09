from worldbuilder.Demon.DemonInfo import DemonInfo, DemonInfoType
from worldbuilder.helper import is_demon

# TODO: Does this handle different demon counts. Please check.
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

            # Ignore the information
            if is_inverted:
                continue

            info_index = max(info_index, 0)
            info = learned_info[info_index]
            
            # No longer possible to have a demon, stop looking
            if len(demons) == 0:
                break

            match info.info_type:
                case DemonInfoType.NONE:
                    continue
                case DemonInfoType.IS_DEAD:
                    if info.target_players is None:
                        raise ValueError(
                            f"{info.info_type.name} has no target players!"
                        )

                    players = info.target_players
                    demons = [d for d in demons if d not in players]

                case DemonInfoType.IS_ROLE:
                    if info.target_players is None:
                        raise ValueError(
                            f"{info.info_type.name} has no target players!"
                        )
                    if info.seen_roles is None:
                        raise ValueError(
                            f"{info.info_type.name} has no stated role!")
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

                case DemonInfoType.AT_LEAST_ONE_IS_ROLE:
                    if info.target_players is None:
                        raise ValueError(
                            f"{info.info_type.name} has no target players!"
                        )
                    if info.seen_roles is None:
                        raise ValueError(
                            f"{info.info_type.name} has no stated role!")
                    if len(info.seen_roles) != 1:
                        raise ValueError(
                            f"{info.info_type.name} received {len(info.seen_roles)} players when 1 was expected!"
                        )

                    role = info.seen_roles[0]
                    players = info.target_players

                    # Info about someone not on evil team
                    if len([d for d in demons if d in players]) == 0:
                        continue

                    if is_demon(role):
                        demons = [d for d in demons if d in players]

                case DemonInfoType.FORTUNE_TELLER_PING:
                    if info.target_players is None:
                        raise ValueError(
                            f"{info.info_type.name} has no target players!"
                        )
                    if info.is_yes is None:
                        raise ValueError(
                            f"{info.info_type.name} has yes or no!"
                        )
                        
                    players = info.target_players
                    is_yes = info.is_yes

                    if is_yes:
                        demons = [d for d in demons if d in players]
                    else:
                        demons = [d for d in demons if d not in players]                        

                case DemonInfoType.SLAYER_SHOT:
                    if info.target_players is None:
                        raise ValueError(
                            f"{info.info_type.name} has no target players!"
                        )
                    if len(info.target_players) != 1:
                        raise ValueError(
                            f"{info.info_type.name} received {len(info.target_players)} players when 1 was expected!"
                        )
                        
                    players = info.target_players
                    
                    demons = [d for d in demons if d not in players]
                    

                case DemonInfoType.SLAYER_KILL:
                    if info.target_players is None:
                        raise ValueError(
                            f"{info.info_type.name} has no target players!"
                        )
                    if len(info.target_players) != 1:
                        raise ValueError(
                            f"{info.info_type.name} received {len(info.target_players)} players when 1 was expected!"
                        )
                        
                    players = info.target_players
                    
                    demons = [d for d in demons if d in players]
                    
                case _:
                    raise ValueError(
                        f"Unhandled InfoType: {info.info_type.name}")

        # If there's no valid demon on these assumptions, remove the team from possible teams
        if len(demons) == 0:
            possible_teams.remove(team)
        else:
            possible_demons.append(demons)

    return possible_demons
