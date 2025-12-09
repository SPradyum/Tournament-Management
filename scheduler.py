from typing import List
from models import Team, Match, Tournament, TournamentType, MatchStatus, SPORT_PRESETS


def generate_round_robin(teams: List[Team]) -> List[Match]:
    if len(teams) < 2:
        return []

    teams = teams.copy()
    if len(teams) % 2 == 1:
        teams.append(Team("__BYE__"))

    matches = []
    match_id = 1
    n = len(teams)

    for _ in range(n - 1):
        for i in range(n // 2):
            t1 = teams[i]
            t2 = teams[n - 1 - i]

            if t1.name != "__BYE__" and t2.name != "__BYE__":
                matches.append(Match(id=match_id, home=t1, away=t2))
                match_id += 1

        teams = [teams[0]] + [teams[-1]] + teams[1:-1]

    return matches


def calculate_league_table(tournament: Tournament):
    preset = SPORT_PRESETS[tournament.sport]

    stats = {
        team.name: {
            "team": team.name,
            "played": 0,
            "won": 0,
            "drawn": 0,
            "lost": 0,
            "sf": 0,
            "sa": 0,
            "sd": 0,
            "points": 0,
        }
        for team in tournament.teams
    }

    for m in tournament.matches:
        if m.status != MatchStatus.COMPLETED:
            continue

        h = stats[m.home.name]
        a = stats[m.away.name]

        h["played"] += 1
        a["played"] += 1

        h["sf"] += m.home_score
        h["sa"] += m.away_score
        a["sf"] += m.away_score
        a["sa"] += m.home_score

        h["sd"] = h["sf"] - h["sa"]
        a["sd"] = a["sf"] - a["sa"]

        if m.home_score > m.away_score:
            h["won"] += 1
            a["lost"] += 1
            h["points"] += preset.win_points
        elif m.home_score < m.away_score:
            a["won"] += 1
            h["lost"] += 1
            a["points"] += preset.win_points
        else:
            if preset.allow_draws:
                h["drawn"] += 1
                a["drawn"] += 1
                h["points"] += preset.draw_points
                a["points"] += preset.draw_points
            else:
                a["won"] += 1
                h["lost"] += 1
                a["points"] += preset.win_points

    table = list(stats.values())
    table.sort(key=lambda r: (-r["points"], -r["sd"], -r["sf"], r["team"].lower()))
    return table
