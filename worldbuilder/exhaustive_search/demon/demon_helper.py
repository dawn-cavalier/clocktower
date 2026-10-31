from worldbuilder.exhaustive_search.demon.demon_info import DemonInfo, DemonInfoType
from worldbuilder.game_info import GameInfo
from worldbuilder.helper import is_demon
from worldbuilder.info import Info
from worldbuilder.info_type import InfoType

# TODO: Does this handle different demon counts. Please check.


def determine_demons(
    info_indices: list[int],
    learned_info: list[DemonInfo],
    game_info: GameInfo,
):
    base_demons: list[int] = [_ for _ in range(game_info.player_count)]

    for info_index in info_indices:
        is_inverted = info_index < 0

        # Ignore the information
        if is_inverted:
            continue

        info_index = max(info_index, 0)
        info = learned_info[info_index]

        # No longer possible to have a demon, stop looking
        if len(base_demons) == 0:
            break

        match info.info_type:
            case DemonInfoType.NONE:
                continue
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
                    base_demons = [d for d in base_demons if d == player]
                else:
                    base_demons = [d for d in base_demons if d != player]

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
                if len([d for d in base_demons if d in players]) == 0:
                    continue

                if is_demon(role):
                    base_demons = [d for d in base_demons if d in players]

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
                    base_demons = [d for d in base_demons if d in players]
                else:
                    base_demons = [d for d in base_demons if d not in players]

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

                base_demons = [d for d in base_demons if d not in players]

            case _:
                raise ValueError(
                    f"Unhandled InfoType: {info.info_type.name}")

    return base_demons

def convert_demon_info(info: Info) -> DemonInfo:
    match info.info_type:
        case (
            InfoType.NONE
            | InfoType.PLAYER_IS_ALIGNMENT
            | InfoType.CHEF_NUMBER
            | InfoType.EMPATH_NUMBER
            | InfoType.VIRGIN_EXECUTE
            | InfoType.NO_NIGHT_DEATH
            | InfoType.PLAYER_EXECUTED
            | InfoType.PLAYER_NIGHT_DEATH
            | InfoType.PLAYER_DAY_DEATH
        ):
            new_info = DemonInfo(
                info_type=DemonInfoType.NONE,
                source=info.source,
                day=info.day,
                info_trust=info.info_trust,
            )
            return new_info

        case (
            InfoType.PLAYER_IS_ROLE
            | InfoType.UNDERTAKER_INFO
            | InfoType.RAVENKEEPER_PING
            | InfoType.VIRGIN_TRIGGER
        ):
            new_info = DemonInfo(
                info_type=DemonInfoType.IS_ROLE,
                source=info.source,
                day=info.day,
                info_trust=info.info_trust,
                target_players=info.target_players,
                seen_roles=info.seen_roles,
            )
            return new_info

        case (
            InfoType.WASHERWOMAN_PING
            | InfoType.LIBRARIAN_PING
            | InfoType.INVESTIGATOR_PING
        ):
            new_info = DemonInfo(
                info_type=DemonInfoType.AT_LEAST_ONE_IS_ROLE,
                source=info.source,
                day=info.day,
                info_trust=info.info_trust,
                target_players=info.target_players,
                seen_roles=info.seen_roles,
            )
            return new_info

        case InfoType.FORTUNE_TELLER_PING:
            new_info = DemonInfo(
                info_type=DemonInfoType.FORTUNE_TELLER_PING,
                source=info.source,
                day=info.day,
                info_trust=info.info_trust,
                target_players=info.target_players,
                is_yes=info.is_yes,
            )
            return new_info

        case InfoType.SLAYER_SHOT:
            new_info = DemonInfo(
                info_type=DemonInfoType.SLAYER_SHOT,
                source=info.source,
                day=info.day,
                info_trust=info.info_trust,
                target_players=info.target_players,
            )
            return new_info

        case _:
            raise ValueError(f"Unhandled InfoType: {info.info_type.name}")
