"""
Scrape Upcoming Premier League Fixtures from FotMob

This script fetches upcoming Premier League fixtures from FotMob and saves them
in a format ready for prediction by the Elastic Net model.

Usage:
    python3 scrape_upcoming_fixtures.py
"""

import json
import time
import requests
from datetime import datetime
from typing import List, Dict, Optional

# Configuration
LEAGUE_ID = 47  # Premier League
FOTMOB_BASE_URL = "https://www.fotmob.com"
OUTPUT_FILE = "../data/current_season/upcoming_fixtures.json"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127 Safari/537.36"

def fetch_league_overview(league_id: int = LEAGUE_ID) -> Optional[Dict]:
    """
    Fetch league overview data from FotMob API
    Returns JSON with fixtures, standings, and other league data
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

def extract_upcoming_fixtures(league_data: Dict) -> List[Dict]:
    """
    Extract upcoming fixtures from league overview data
    Returns list of fixtures with home team, away team, date, and time
    Only includes matches scheduled after today's date
    """
    fixtures = []
    today = datetime.now().date()
    
    # Try to find fixtures in various possible locations in the JSON
    matches_data = None
    
    # Check for matches in different possible structures
    if "matches" in league_data:
        matches_data = league_data["matches"]
    elif "fixtures" in league_data:
        matches_data = league_data["fixtures"]
    elif "allMatches" in league_data:
        matches_data = league_data["allMatches"]
    
    if not matches_data:
        print("⚠ No matches data found in league response")
        return fixtures
    
    # Process matches
    for match in matches_data:
        try:
            # Extract match details
            status = match.get("status", {})
            
            # Only include upcoming/scheduled matches (not finished)
            if isinstance(status, dict):
                started = status.get("started", False)
                finished = status.get("finished", False)
                
                # Skip finished or ongoing matches
                if started or finished:
                    continue
            
            # Extract date/time to check if it's in the future
            match_time_utc = match.get("status", {}).get("utcTime") if isinstance(match.get("status"), dict) else None
            
            # Skip if no timestamp or match is in the past
            if match_time_utc:
                try:
                    dt = datetime.fromisoformat(match_time_utc.replace('Z', '+00:00'))
                    match_date = dt.date()
                    
                    # Skip matches that have already passed
                    if match_date < today:
                        continue
                except Exception:
                    pass
            
            # Extract teams
            home_team = match.get("home", {}).get("name") or match.get("homeTeam", {}).get("name")
            away_team = match.get("away", {}).get("name") or match.get("awayTeam", {}).get("name")
            
            if not home_team or not away_team:
                continue
            
            # Extract date/time
            match_time_utc = match.get("status", {}).get("utcTime") if isinstance(match.get("status"), dict) else None
            
            # Parse datetime
            match_date = "TBD"
            match_time = "TBD"
            
            if match_time_utc:
                try:
                    dt = datetime.fromisoformat(match_time_utc.replace('Z', '+00:00'))
                    match_date = dt.strftime("%Y-%m-%d")
                    match_time = dt.strftime("%H:%M")
                except Exception:
                    pass
            
            # Get match ID
            match_id = match.get("id")
            
            fixture = {
                "matchId": match_id,
                "home": home_team,
                "away": away_team,
                "date": match_date,
                "time": match_time,
                "timestamp": match_time_utc
            }
            
            fixtures.append(fixture)
            
        except Exception as e:
            print(f"⚠ Error processing match: {e}")
            continue
    
    return fixtures

def fetch_fixtures_alternative() -> List[Dict]:
    """
    Alternative method: Fetch fixtures from the fixtures endpoint
    Only includes matches scheduled after today's date
    """
    url = f"{FOTMOB_BASE_URL}/api/leagues?id={LEAGUE_ID}&tab=fixtures"
    
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json, text/plain, */*",
        "Referer": f"{FOTMOB_BASE_URL}/",
    }
    
    try:
        print(f"Trying alternative fixtures endpoint...")
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        data = response.json()
        
        fixtures = []
        today = datetime.now().date()
        
        # Look for fixtures in the response
        if "fixtures" in data:
            fixtures_data = data["fixtures"]
            if isinstance(fixtures_data, dict) and "allMatches" in fixtures_data:
                matches = fixtures_data["allMatches"]
            elif isinstance(fixtures_data, list):
                matches = fixtures_data
            else:
                matches = []
            
            for match in matches:
                try:
                    home = match.get("home", {}).get("name")
                    away = match.get("away", {}).get("name")
                    
                    if not home or not away:
                        continue
                    
                    status = match.get("status", {})
                    utc_time = status.get("utcTime") if isinstance(status, dict) else None
                    
                    match_date = "TBD"
                    match_time = "TBD"
                    
                    if utc_time:
                        try:
                            dt = datetime.fromisoformat(utc_time.replace('Z', '+00:00'))
                            match_date_obj = dt.date()
                            
                            # Skip matches that have already passed
                            if match_date_obj < today:
                                continue
                            
                            match_date = dt.strftime("%Y-%m-%d")
                            match_time = dt.strftime("%H:%M")
                        except Exception:
                            pass
                    
                    fixtures.append({
                        "matchId": match.get("id"),
                        "home": home,
                        "away": away,
                        "date": match_date,
                        "time": match_time,
                        "timestamp": utc_time
                    })
                except Exception as e:
                    print(f"⚠ Error processing match: {e}")
                    continue
        
        print(f"✓ Found {len(fixtures)} upcoming fixtures")
        return fixtures
        
    except Exception as e:
        print(f"✗ Alternative method failed: {e}")
        return []

def save_fixtures(fixtures: List[Dict], output_file: str = OUTPUT_FILE):
    """
    Save fixtures to JSON file
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(fixtures, f, ensure_ascii=False, indent=2)
        print(f"✓ Saved {len(fixtures)} fixtures to {output_file}")
        return True
    except Exception as e:
        print(f"✗ Error saving fixtures: {e}")
        return False

def main():
    """
    Main execution flow
    """
    print("="*80)
    print("FOTMOB UPCOMING FIXTURES SCRAPER")
    print("="*80)
    print(f"\n📅 Today's date: {datetime.now().strftime('%Y-%m-%d')}")
    print(f"🔍 Fetching matches scheduled from today onwards...\n")
    
    # Method 1: Try league overview endpoint
    league_data = fetch_league_overview()
    fixtures = []
    
    if league_data:
        fixtures = extract_upcoming_fixtures(league_data)
    
    # Method 2: If no fixtures found, try alternative endpoint
    if not fixtures:
        print("\nTrying alternative method...")
        fixtures = fetch_fixtures_alternative()
    
    # Filter and sort fixtures
    if fixtures:
        # Remove duplicates based on matchId
        seen_ids = set()
        unique_fixtures = []
        for f in fixtures:
            if f["matchId"] not in seen_ids:
                seen_ids.add(f["matchId"])
                unique_fixtures.append(f)
        
        # Sort by date
        unique_fixtures.sort(key=lambda x: x.get("timestamp", ""))
        
        print(f"\n{'='*80}")
        print(f"FOUND {len(unique_fixtures)} UPCOMING FIXTURES")
        print(f"{'='*80}\n")
        
        for i, fixture in enumerate(unique_fixtures, 1):
            print(f"{i:2d}. {fixture['home']:25s} vs {fixture['away']:25s} | {fixture['date']} {fixture['time']}")
        
        # Save to file
        print()
        save_fixtures(unique_fixtures)
        
        print(f"\n{'='*80}")
        print("✓ SCRAPING COMPLETE")
        print(f"{'='*80}")
        print(f"\nNext steps:")
        print(f"1. Run the Flask API: python3 app.py")
        print(f"2. The API will use these fixtures for predictions")
        print(f"3. View predictions at http://localhost:3000")
        
    else:
        print("\n✗ No upcoming fixtures found")
        print("\nPossible reasons:")
        print("  - No upcoming matches scheduled")
        print("  - FotMob API structure changed")
        print("  - Network/connection issues")
        print("\nTip: Check https://www.fotmob.com/leagues/47/fixtures/premier-league manually")

if __name__ == "__main__":
    main()
