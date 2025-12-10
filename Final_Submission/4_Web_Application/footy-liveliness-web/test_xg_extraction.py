import requests
import json

# Test xG extraction for one match
match_id = 4813374
url = f"https://www.fotmob.com/api/matchDetails?matchId={match_id}"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Accept": "application/json",
}

print(f"Fetching match {match_id}...")
response = requests.get(url, headers=headers, timeout=10)
match_details = response.json()

print(f"Match: {match_details.get('general', {}).get('matchName')}")
print(f"Status: {'Finished' if match_details.get('general', {}).get('finished') else 'Not finished'}")

# Get team IDs from general section
general = match_details.get("general", {})
home_team_id = general.get("homeTeam", {}).get("id")
away_team_id = general.get("awayTeam", {}).get("id")
home_team_name = general.get("homeTeam", {}).get("name")
away_team_name = general.get("awayTeam", {}).get("name")

print(f"\nHome: {home_team_name} (ID: {home_team_id})")
print(f"Away: {away_team_name} (ID: {away_team_id})")

# Calculate xG from shotmap
home_xg = 0.0
away_xg = 0.0

if "content" in match_details and "shotmap" in match_details["content"]:
    shotmap = match_details["content"]["shotmap"]
    if "shots" in shotmap:
        print(f"\nFound {len(shotmap['shots'])} shots")
        for shot in shotmap["shots"]:
            xg_value = shot.get("expectedGoals", 0)
            team_id = shot.get("teamId")
            player_name = shot.get("playerName", "Unknown")
            
            if team_id == home_team_id:
                home_xg += xg_value
                print(f"  Home shot by {player_name}: xG = {xg_value:.3f}")
            elif team_id == away_team_id:
                away_xg += xg_value
                print(f"  Away shot by {player_name}: xG = {xg_value:.3f}")

print(f"\n✅ Total xG:")
print(f"  Home ({home_team_name}): {home_xg:.2f}")
print(f"  Away ({away_team_name}): {away_xg:.2f}")
print(f"  Total: {home_xg + away_xg:.2f}")
print(f"  Simple xG: {home_xg + away_xg + min(home_xg, away_xg):.2f}")
