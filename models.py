from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class TournamentType(str, Enum):
    ROUND_ROBIN = "Round Robin"
    KNOCKOUT = "Knockout"


class MatchStatus(str, Enum):
    NOT_PLAYED = "Not Played"
    COMPLETED = "Completed"


@dataclass
class SportPreset:
    name: str
    win_points: int
    draw_points: int
    loss_points: int
    allow_draws: bool = True


SPORT_PRESETS = {
    "Universal": SportPreset("Universal", 3, 1, 0),
    "Football": SportPreset("Football", 3, 1, 0),
    "Basketball": SportPreset("Basketball", 2, 1, 0, False),
    "Cricket": SportPreset("Cricket", 2, 1, 0),
    "Volleyball": SportPreset("Volleyball", 2, 1, 1),
    "Badminton": SportPreset("Badminton", 1, 0, 0, False),
    "Kabaddi": SportPreset("Kabaddi", 2, 1, 0),
}


@dataclass
class Team:
    name: str


@dataclass
class Match:
    id: int
    home: Team
    away: Team
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    status: MatchStatus = MatchStatus.NOT_PLAYED

    def set_result(self, home_points: int, away_points: int):
        self.home_score = home_points
        self.away_score = away_points
        self.status = MatchStatus.COMPLETED


@dataclass
class Tournament:
    name: str
    sport: str
    tournament_type: TournamentType
    teams: List[Team] = field(default_factory=list)
    matches: List[Match] = field(default_factory=list)
