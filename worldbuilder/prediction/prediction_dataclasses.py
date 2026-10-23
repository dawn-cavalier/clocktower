"""
Contains the paramenter struct and the return object
for the prediction calculator.
"""
from dataclasses import dataclass, field


@dataclass
class GameState:
    """
    Stores the all calculated game state.\n
    This includes the night, day and execution deaths,
    as well as the computed possible evil teams,
    demons and outsider groups.
    """
    night_deaths: list[int] = field(default_factory=list[int])
    day_deaths: list[int] = field(default_factory=list[int])
    execution_deaths: list[int] = field(default_factory=list[int])

    evil_teams: list[list[int]] = field(default_factory=list[list[int]])
    outsiders: list[list[int]] = field(default_factory=list[list[int]])
    demons: list[int] = field(default_factory=list[int])


@dataclass
class Predictions:
    """
    Stores the different scores that the predicition
    calculator returns.
    """
    evil_player_scores: list[float] = field(default_factory=list[float])
    demon_player_scores: list[float] = field(default_factory=list[float])
    outsider_player_scores: list[float] = field(default_factory=list[float])
