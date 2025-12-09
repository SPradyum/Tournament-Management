import json
from typing import Any, Dict
from models import Tournament, Team, Match, MatchStatus, TournamentType


def tournament_to_dict(t: Tournament) -> Dict[str, Any]:
    return {
        "name": t.name,
        "sport": t.sport,
        "type": t.tournament_type.value,
        "teams": [tm.name for tm in t.teams],
        "matches": [
            {
                "id": m.id,
                "home": m.home.name,
                "away": m.away.name,
                "home_score": m.home_score,
                "away_score": m.away_score,
                "status": m.status.value,
            }
            for m in t.matches
        ],
    }


def save_tournament_json(tournament: Tournament, filename: str):
    with open(filename, "w") as f:
        json.dump(tournament_to_dict(tournament), f, indent=2)


def load_tournament_json(filename: str) -> Tournament:
    with open(filename, "r") as f:
        data = json.load(f)

    t = Tournament(data["name"], data["sport"], TournamentType(data["type"]))
    t.teams = [Team(name) for name in data["teams"]]
    lookup = {tm.name: tm for tm in t.teams}

    for m in data["matches"]:
        t.matches.append(
            Match(
                id=m["id"],
                home=lookup[m["home"]],
                away=lookup[m["away"]],
                home_score=m["home_score"],
                away_score=m["away_score"],
                status=MatchStatus(m["status"]),
            )
        )
    return t
