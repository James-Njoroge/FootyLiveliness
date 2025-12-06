import os
import json
import math
import csv
from collections import defaultdict
from typing import Any, Dict, Iterable, List, Optional, Tuple

try:
    import pandas as pd  # type: ignore
except Exception:  # pragma: no cover
    pd = None


def read_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def coerce_float(v: Any) -> Optional[float]:
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip()
    if s == "":
        return None
    try:
        return float(s)
    except ValueError:
        for ch in [" ", "(", ")", "%"]:
            s = s.replace(ch, " ")
        parts = [p for p in s.split() if p]
        for p in parts:
            try:
                return float(p)
            except ValueError:
                continue
    return None


def to_name(x: Any) -> Optional[str]:
    if x is None:
        return None
    if isinstance(x, str):
        return x
    if isinstance(x, dict):
        return x.get("fullName") or x.get("name") or x.get("firstName") or None
    return str(x)


def find_stats_groups(match_json: Dict[str, Any]) -> List[Dict[str, Any]]:
    content = match_json.get("content") or {}
    stats_root = content.get("stats") or {}
    periods = stats_root.get("Periods") or {}
    stats_all = periods.get("All") or {}
    if isinstance(stats_all, dict):
        sg = stats_all.get("stats", [])
    else:
        sg = stats_all
    return sg if isinstance(sg, list) else []


def find_pair_stat(stats_groups: List[Dict[str, Any]], key: str) -> Tuple[Optional[float], Optional[float]]:
    for group in stats_groups:
        items = group.get("stats")
        if isinstance(items, list):
            for it in items:
                if it.get("key") == key:
                    vals = it.get("stats", [])
                    if isinstance(vals, list) and len(vals) >= 2:
                        hv = coerce_float(vals[0])
                        av = coerce_float(vals[1])
                        return hv, av
    return None, None


def extract_index_rows(index_path: str) -> List[Dict[str, Any]]:
    raw = read_json(index_path)
    rows: List[Dict[str, Any]] = []
    for r in raw:
        rnd = r.get("round")
        for m in r.get("matches", []):
            rows.append(
                {
                    "round": rnd,
                    "matchId": m.get("matchId"),
                    "home": m.get("home"),
                    "away": m.get("away"),
                    "matchUrl": m.get("matchUrl"),
                    "jsonPath": m.get("jsonPath"),
                }
            )
    return rows


def extract_from_match(match_json: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any], List[Dict[str, Any]], List[Dict[str, Any]]]:
    general = match_json.get("general", {})
    header = match_json.get("header", {})
    match_id = general.get("matchId") or header.get("matchId")
    try:
        match_id = int(match_id)
    except Exception:
        pass

    teams_obj = header.get("teams") or []
    teams = teams_obj if isinstance(teams_obj, list) else []
    home_team = teams[0] if len(teams) >= 1 else {}
    away_team = teams[1] if len(teams) >= 2 else {}

    match_row: Dict[str, Any] = {
        "matchId": match_id,
        "leagueId": general.get("leagueId"),
        "leagueName": general.get("leagueName"),
        "matchRound": general.get("matchRound"),
        "coverageLevel": general.get("coverageLevel"),
        "matchTimeUTC": general.get("matchTimeUTC"),
        "matchTimeUTCDate": general.get("matchTimeUTCDate"),
        "started": general.get("started"),
        "finished": general.get("finished"),
        "homeTeamId": (general.get("homeTeam") or {}).get("id"),
        "homeTeamName": (general.get("homeTeam") or {}).get("name"),
        "awayTeamId": (general.get("awayTeam") or {}).get("id"),
        "awayTeamName": (general.get("awayTeam") or {}).get("name"),
        "homeScore": home_team.get("score"),
        "awayScore": away_team.get("score"),
        "statusUtcTime": (header.get("status") or {}).get("utcTime"),
        "statusFinished": (header.get("status") or {}).get("finished"),
        "statusScoreStr": (header.get("status") or {}).get("scoreStr"),
    }

    stats_groups = find_stats_groups(match_json)
    xG_h, xG_a = find_pair_stat(stats_groups, "expected_goals")
    sh_h, sh_a = find_pair_stat(stats_groups, "total_shots")
    sot_h, sot_a = find_pair_stat(stats_groups, "ShotsOnTarget")
    bc_h, bc_a = find_pair_stat(stats_groups, "big_chance")
    c_h, c_a = find_pair_stat(stats_groups, "corners")
    tob_h, tob_a = find_pair_stat(stats_groups, "touches_opp_box")

    stats_row: Dict[str, Any] = {
        "matchId": match_id,
        "homeTeamName": match_row["homeTeamName"],
        "awayTeamName": match_row["awayTeamName"],
        "xG_home": xG_h,
        "xG_away": xG_a,
        "shots_home": sh_h,
        "shots_away": sh_a,
        "sot_home": sot_h,
        "sot_away": sot_a,
        "bigch_home": bc_h,
        "bigch_away": bc_a,
        "corners_home": c_h,
        "corners_away": c_a,
        "tob_home": tob_h,
        "tob_away": tob_a,
    }

    goal_rows: List[Dict[str, Any]] = []
    ev = header.get("events") or {}
    for side_key, side_flag in [("homeTeamGoals", "home"), ("awayTeamGoals", "away")]:
        bucket = ev.get(side_key) or {}
        if isinstance(bucket, dict):
            for _scorer, items in bucket.items():
                if not isinstance(items, list):
                    continue
                for g in items:
                    sm = g.get("shotmapEvent", {}) if isinstance(g, dict) else {}
                    goal_rows.append(
                        {
                            "matchId": match_id,
                            "teamSide": side_flag,
                            "time": g.get("time"),
                            "type": g.get("type"),
                            "playerId": g.get("playerId"),
                            "playerName": g.get("fullName") or g.get("nameStr"),
                            "assistPlayerId": g.get("assistPlayerId"),
                            "assistPlayer": g.get("assistInput"),
                            "newScore_home": (g.get("newScore") or [None, None])[0],
                            "newScore_away": (g.get("newScore") or [None, None])[1],
                            "x": sm.get("x"),
                            "y": sm.get("y"),
                            "expectedGoals": sm.get("expectedGoals"),
                            "expectedGoalsOnTarget": sm.get("expectedGoalsOnTarget"),
                            "shotType": sm.get("shotType"),
                            "situation": sm.get("situation"),
                            "period": sm.get("period"),
                            "isFromInsideBox": sm.get("isFromInsideBox"),
                        }
                    )

    lineup_rows: List[Dict[str, Any]] = []
    lineup = (match_json.get("content") or {}).get("lineup") or {}
    for side_key, side_flag in [("homeTeam", "home"), ("awayTeam", "away")]:
        team = lineup.get(side_key) or {}
        team_name = team.get("teamName") or team.get("name") or (
            ((general.get("homeTeam") or {}).get("name") if side_flag == "home" else (general.get("awayTeam") or {}).get("name"))
        )
        for is_starter, list_key in [(True, "starters"), (False, "subs")]:
            arr = team.get(list_key, [])
            if not isinstance(arr, list):
                continue
            for itm in arr:
                player = itm.get("player") if isinstance(itm, dict) else None
                p = player if isinstance(player, dict) else (itm if isinstance(itm, dict) else {})
                pid = p.get("id") or p.get("playerId")
                pname = to_name(p.get("name")) or p.get("fullName") or p.get("nameStr")
                lineup_rows.append(
                    {
                        "matchId": match_id,
                        "teamSide": side_flag,
                        "teamName": team_name,
                        "isStarter": is_starter,
                        "playerId": pid,
                        "playerName": pname,
                        "positionId": itm.get("positionId") if isinstance(itm, dict) else None,
                        "shirtNumber": itm.get("shirtNumber") if isinstance(itm, dict) else None,
                    }
                )

    return match_row, stats_row, goal_rows, lineup_rows


def convert(input_dir: str, output_dir: str) -> None:
    index_path = os.path.join(input_dir, "index.json")
    if not os.path.exists(index_path):
        raise FileNotFoundError(f"index.json not found in {input_dir}")

    ensure_dir(output_dir)

    index_rows = extract_index_rows(index_path)

    matches_rows: List[Dict[str, Any]] = []
    stats_rows: List[Dict[str, Any]] = []
    goals_rows: List[Dict[str, Any]] = []
    lineup_rows: List[Dict[str, Any]] = []

    for row in index_rows:
        round_no = row.get("round")
        json_rel = row.get("jsonPath")
        if not json_rel:
            continue
        fpath = os.path.join(input_dir, json_rel)
        if not os.path.exists(fpath):
            fpath = os.path.join(input_dir, os.path.basename(json_rel))
        if not os.path.exists(fpath):
            continue

        m = read_json(fpath)
        match_row, stats_row, goal_rows, lu_rows = extract_from_match(m)
        match_row["round"] = round_no
        stats_row["round"] = round_no
        for gr in goal_rows:
            gr["round"] = round_no
        for lr in lu_rows:
            lr["round"] = round_no

        matches_rows.append(match_row)
        stats_rows.append(stats_row)
        goals_rows.extend(goal_rows)
        lineup_rows.extend(lu_rows)

    def write_csv(name: str, rows: List[Dict[str, Any]]) -> None:
        out_path = os.path.join(output_dir, name)
        if not rows:
            # still write an empty file with no rows but ensure it exists
            with open(out_path, "w", newline="", encoding="utf-8") as f:
                pass
            return
        # stable column order
        cols = list({k for r in rows for k in r.keys()})
        # prefer common keys first
        preferred = [
            "round",
            "matchId",
            "homeTeamName",
            "awayTeamName",
        ]
        # only include preferred keys that actually exist in this table
        ordered = [c for c in preferred if c in cols] + [c for c in cols if c not in preferred]
        if pd is not None:
            df = pd.DataFrame(rows)
            df = df.reindex(columns=ordered)
            df.to_csv(out_path, index=False)
        else:
            with open(out_path, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=ordered)
                w.writeheader()
                for r in rows:
                    w.writerow(r)

    write_csv("index.csv", index_rows)
    write_csv("matches.csv", matches_rows)
    write_csv("team_stats.csv", stats_rows)
    write_csv("goals.csv", goals_rows)
    write_csv("lineup_players.csv", lineup_rows)

    # Build a single consolidated table: one row per match
    matches_by_id = {r.get("matchId"): r for r in matches_rows}
    stats_by_id = {r.get("matchId"): r for r in stats_rows}

    goals_by_id = defaultdict(lambda: {
        "home": {"count": 0, "timeline": []},
        "away": {"count": 0, "timeline": []},
    })
    for g in goals_rows:
        mid = g.get("matchId")
        side = g.get("teamSide")
        if mid is None or side not in ("home", "away"):
            continue
        goals_by_id[mid][side]["count"] += 1
        goals_by_id[mid][side]["timeline"].append((g.get("time"), g.get("playerName")))

    lineup_by_id = defaultdict(lambda: {
        "home": {"starters": 0, "subs": 0},
        "away": {"starters": 0, "subs": 0},
    })
    for lr in lineup_rows:
        mid = lr.get("matchId")
        side = lr.get("teamSide")
        if mid is None or side not in ("home", "away"):
            continue
        if lr.get("isStarter"):
            lineup_by_id[mid][side]["starters"] += 1
        else:
            lineup_by_id[mid][side]["subs"] += 1

    consolidated_rows: List[Dict[str, Any]] = []
    for mid, mrow in matches_by_id.items():
        out = dict(mrow)  # start with match metadata
        srow = stats_by_id.get(mid, {})
        # merge team stats
        for k, v in srow.items():
            if k == "matchId":
                continue
            out[k] = v

        # add goals aggregates
        ginfo = goals_by_id.get(mid, {"home": {"count": 0, "timeline": []}, "away": {"count": 0, "timeline": []}})
        h_tl = sorted(ginfo["home"]["timeline"], key=lambda x: (x[0] is None, x[0]))
        a_tl = sorted(ginfo["away"]["timeline"], key=lambda x: (x[0] is None, x[0]))
        out["goals_home_count"] = ginfo["home"]["count"]
        out["goals_away_count"] = ginfo["away"]["count"]
        out["goals_total_count"] = ginfo["home"]["count"] + ginfo["away"]["count"]
        out["scorers_home"] = ";".join([p for _, p in h_tl if p]) if h_tl else ""
        out["scorers_away"] = ";".join([p for _, p in a_tl if p]) if a_tl else ""

        # add lineup aggregates
        linfo = lineup_by_id.get(mid, {"home": {"starters": 0, "subs": 0}, "away": {"starters": 0, "subs": 0}})
        out["starters_home_count"] = linfo["home"]["starters"]
        out["starters_away_count"] = linfo["away"]["starters"]
        out["subs_home_count"] = linfo["home"]["subs"]
        out["subs_away_count"] = linfo["away"]["subs"]
        out["players_home_count"] = linfo["home"]["starters"] + linfo["home"]["subs"]
        out["players_away_count"] = linfo["away"]["starters"] + linfo["away"]["subs"]

        consolidated_rows.append(out)

    write_csv("all_in_one.csv", consolidated_rows)


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    default_in = os.path.join(here, "24-25_PL_Data_raw")
    default_out = os.path.join(here, "24-25_PL_Data_csv")

    in_dir = os.environ.get("RAW_PL_DATA_DIR", default_in)
    out_dir = os.environ.get("PL_DATA_CSV_DIR", default_out)
    convert(in_dir, out_dir)
    print(f"CSV written to: {out_dir}")


if __name__ == "__main__":
    main()
