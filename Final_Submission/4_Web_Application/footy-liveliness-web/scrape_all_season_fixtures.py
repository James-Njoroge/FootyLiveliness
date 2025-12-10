"""
Scrape ALL Premier League Fixtures from FotMob (Past + Future)

This script fetches all Premier League fixtures from the current season,
including completed matches (with actual xG data) and upcoming matches.

Usage:
    python3 scrape_all_season_fixtures.py
"""

import json
import time
import requests
from datetime import datetime
from typing import List, Dict, Optional

# Configuration
LEAGUE_ID = 47  # Premier League
SEASON = "2025/2026"  # Current season
FOTMOB_BASE_URL = "https://www.fotmob.com"
OUTPUT_FILE = "../data/current_season/all_fixtures.json"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127 Safari/537.36"

def fetch_league_overview(league_id: int = LEAGUE_ID) -> Optional[Dict]:
    """
    Fetch league overview data from FotMob API
    Returns JSON with all fixtures, standings, and other league data
    """
    url = f"{FOTMOB_BASE_URL}/api/leagues?id={league_id}"
    
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json, text/plain, */*",
        "Referer": f"{FOTMOB_BASE_URL}/",
        "Accept-Language": "en-US,en;q=0.9",
    }
    
    try:
        print(f"Fetching league data from FotMob...")
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        data = response.json()
        print(f"✓ Successfully fetched league data")
        return data
    except requests.exceptions.RequestException as e:
        print(f"✗ Error fetching league data: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"✗ Error parsing JSON response: {e}")
        return None

def fetch_match_details(match_id: int) -> Optional[Dict]:
    """
    Fetch detailed match data including xG for completed matches
    """
    url = f"{FOTMOB_BASE_URL}/api/matchDetails?matchId={match_id}"
    
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json, text/plain, */*",
        "Referer": f"{FOTMOB_BASE_URL}/",
        "Accept-Language": "en-US,en;q=0.9",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"  ⚠ Could not fetch details for match {match_id}: {e}")
        return None

def extract_all_fixtures(league_data: Dict) -> List[Dict]:
    """
    Extract ALL fixtures from league overview data (past and future)
    Returns list of fixtures with home team, away team, date, time, and status
    """
    fixtures = []
    
    # Try to find fixtures in various possible locations in the JSON
    matches_data = None
    
    # Check for matches in different possible structures
    if "fixtures" in league_data and isinstance(league_data["fixtures"], dict):
        # FotMob structure: fixtures -> allMatches
        matches_data = league_data["fixtures"].get("allMatches", [])
    elif "matches" in league_data and isinstance(league_data["matches"], list):
        matches_data = league_data["matches"]
    elif "allMatches" in league_data:
        matches_data = league_data["allMatches"]
    
    if not matches_data:
        print("⚠ No matches data found in league response")
        return fixtures
    
    print(f"\nProcessing {len(matches_data)} matches...")
    
    # Process all matches
    for idx, match in enumerate(matches_data, 1):
        try:
            # Extract match details
            home_team = match.get("home", {}).get("name", "Unknown")
            away_team = match.get("away", {}).get("name", "Unknown")
            match_id = match.get("id")
            
            status = match.get("status", {})
            
            # Determine if match is finished
            is_finished = False
            is_started = False
            if isinstance(status, dict):
                is_started = status.get("started", False)
                is_finished = status.get("finished", False)
            
            # Extract date/time
            match_time_utc = status.get("utcTime") if isinstance(status, dict) else None
            
            if not match_time_utc:
                continue
            
            try:
                dt = datetime.fromisoformat(match_time_utc.replace('Z', '+00:00'))
                match_date = dt.strftime("%Y-%m-%d")
                match_time = dt.strftime("%H:%M")
            except:
                continue
            
            fixture = {
                "matchId": match_id,
                "home": home_team,
                "away": away_team,
                "date": match_date,
                "time": match_time,
                "status": "finished" if is_finished else ("ongoing" if is_started else "upcoming"),
                "actualScore": None,
                "actualXG": None
            }
            
            # For finished matches, fetch actual xG data
            if is_finished and match_id:
                print(f"  [{idx}/{len(matches_data)}] Fetching details for {home_team} vs {away_team}...")
                match_details = fetch_match_details(match_id)
                
                if match_details:
                    # Extract xG data
                    try:
                        # Calculate xG from shot events
                        home_xg = 0.0
                        away_xg = 0.0
                        
                        # Get home and away team IDs from match details
                        general = match_details.get("general", {})
                        home_team_id = general.get("homeTeam", {}).get("id")
                        away_team_id = general.get("awayTeam", {}).get("id")
                        
                        # Extract xG from shotmap events
                        if "content" in match_details and "shotmap" in match_details["content"]:
                            shotmap = match_details["content"]["shotmap"]
                            if "shots" in shotmap:
                                for shot in shotmap["shots"]:
                                    xg_value = shot.get("expectedGoals", 0)
                                    team_id = shot.get("teamId")
                                    
                                    # Skip if xG value is None
                                    if xg_value is None:
                                        continue
                                    
                                    if team_id == home_team_id:
                                        home_xg += xg_value
                                    elif team_id == away_team_id:
                                        away_xg += xg_value
                        
                        # Also get actual score
                        home_score = match.get("home", {}).get("score")
                        away_score = match.get("away", {}).get("score")
                        
                        # Only add xG if we got valid data (> 0)
                        if home_xg > 0 or away_xg > 0:
                            fixture["actualXG"] = {
                                "home": round(float(home_xg), 2),
                                "away": round(float(away_xg), 2),
                                "total": round(float(home_xg) + float(away_xg), 2),
                                "simple_xg": round(float(home_xg) + float(away_xg) + min(float(home_xg), float(away_xg)), 2)
                            }
                        
                        if home_score is not None and away_score is not None:
                            fixture["actualScore"] = {
                                "home": home_score,
                                "away": away_score
                            }
                        
                        print(f"    ✓ Got xG: {home_xg} - {away_xg}")
                    except Exception as e:
                        print(f"    ⚠ Could not extract xG: {e}")
                
                # Rate limiting
                time.sleep(0.5)
            
            fixtures.append(fixture)
            
            # Progress indicator for upcoming matches
            if not is_finished and idx % 50 == 0:
                print(f"  Processed {idx}/{len(matches_data)} matches...")
            
        except Exception as e:
            print(f"  ⚠ Error processing match: {e}")
            continue
    
    return fixtures

def save_fixtures(fixtures: List[Dict], output_file: str = OUTPUT_FILE):
    """Save fixtures to JSON file"""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(fixtures, f, indent=2, ensure_ascii=False)
        print(f"\n✓ Saved {len(fixtures)} fixtures to {output_file}")
        
        # Print summary
        finished = sum(1 for f in fixtures if f["status"] == "finished")
        upcoming = sum(1 for f in fixtures if f["status"] == "upcoming")
        with_xg = sum(1 for f in fixtures if f.get("actualXG") is not None)
        
        print(f"\nSummary:")
        print(f"  • Finished matches: {finished} ({with_xg} with xG data)")
        print(f"  • Upcoming matches: {upcoming}")
        print(f"  • Total: {len(fixtures)}")
        
    except Exception as e:
        print(f"✗ Error saving fixtures: {e}")

def print_fixtures_table(fixtures: List[Dict]):
    """Print fixtures in a formatted table"""
    print("\n" + "="*100)
    print("ALL SEASON FIXTURES")
    print("="*100)
    
    for idx, fixture in enumerate(fixtures, 1):
        status_emoji = "✓" if fixture["status"] == "finished" else "⏰"
        xg_info = ""
        if fixture.get("actualXG"):
            xg = fixture["actualXG"]
            xg_info = f" | xG: {xg['home']:.2f} - {xg['away']:.2f} (Simple: {xg['simple_xg']:.2f})"
        
        print(f"{idx:3d}. {status_emoji} {fixture['home']:30s} vs {fixture['away']:30s} | {fixture['date']} {fixture['time']}{xg_info}")

def main():
    """Main execution function"""
    print("="*100)
    print("FOTMOB PREMIER LEAGUE SEASON SCRAPER")
    print("="*100)
    print(f"League ID: {LEAGUE_ID}")
    print(f"Season: {SEASON}")
    print(f"Output: {OUTPUT_FILE}")
    print(f"Current date: {datetime.now().strftime('%Y-%m-%d')}")
    print("="*100)
    
    # Fetch league data
    league_data = fetch_league_overview()
    if not league_data:
        print("\n✗ Failed to fetch league data. Exiting.")
        return
    
    # Extract all fixtures
    fixtures = extract_all_fixtures(league_data)
    
    if not fixtures:
        print("\n✗ No fixtures found. Exiting.")
        return
    
    # Print fixtures table
    print_fixtures_table(fixtures)
    
    # Save to file
    save_fixtures(fixtures)
    
    print("\n" + "="*100)
    print("✓ SCRAPING COMPLETE")
    print("="*100)
    print("\nNext steps:")
    print("1. Run the Flask API: python3 app.py")
    print("2. The API will use these fixtures for predictions")
    print("3. View predictions at http://localhost:3000")
    print("4. Navigate to past weeks to see predicted vs actual comparison")

if __name__ == "__main__":
    main()
