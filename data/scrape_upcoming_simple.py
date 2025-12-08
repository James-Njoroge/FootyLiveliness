"""
Scrape upcoming Premier League matches from FotMob
Simplified version using regular Selenium (no selenium-wire)
"""

import os, json, time
from typing import List, Dict
import pandas as pd
from datetime import datetime, timezone

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# =========================
# Config
# =========================
LEAGUE_ID = 47
LEAGUE_SLUG = "premier-league"
SEASON_SLUG = "2025-2026"  # Updated to 2025/26 season
CHROMEDRIVER_PATH = os.path.expanduser("/opt/homebrew/bin/chromedriver")
HEADLESS = True  # Run in background
OUTPUT_FILE = "../web-app/src/utils/live_matches.json"
HISTORICAL_DATA_PATH = "./tables/all_rounds.csv"  # Relative to data/ directory

# FotMob fixtures URL - use fixtures tab to get only upcoming matches
FIXTURES_URL = f"https://www.fotmob.com/leagues/{LEAGUE_ID}/fixtures/{LEAGUE_SLUG}"

# Team ID mapping
TEAM_IDS = {
    'Liverpool': 8650, 'Manchester City': 8456, 'Arsenal': 9825, 'Chelsea': 8455,
    'Manchester United': 10260, 'Tottenham': 8586, 'Tottenham Hotspur': 8586,
    'Newcastle': 10261, 'Newcastle United': 10261, 'Aston Villa': 10252,
    'Brighton': 10204, 'Brighton & Hove Albion': 10204, 'Brentford': 9937,
    'Wolves': 8602, 'Wolverhampton Wanderers': 8602, 'Bournemouth': 8678,
    'AFC Bournemouth': 8678, 'Everton': 8668, 'Fulham': 9879,
    'West Ham': 8654, 'West Ham United': 8654, 'Crystal Palace': 9826,
    'Southampton': 8466, 'Leicester': 8197, 'Leicester City': 8197,
    'Luton': 8667, 'Luton Town': 8667, 'Nottingham Forest': 10203,
    'Ipswich': 9937, 'Ipswich Town': 9937,
}

def init_driver(headless: bool = True):
    """Initialize Chrome driver"""
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1920,1080")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option('useAutomationExtension', False)
    
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=opts)
    driver.set_page_load_timeout(45)
    return driver

def fetch_upcoming_fixtures():
    """Fetch upcoming fixtures from FotMob"""
    print("="*60)
    print("FETCHING UPCOMING PREMIER LEAGUE FIXTURES")
    print("="*60)
    print(f"\nURL: {FIXTURES_URL}\n")
    
    driver = init_driver(headless=HEADLESS)
    upcoming_matches = []
    
    try:
        driver.get(FIXTURES_URL)
        print("✓ Page loaded, waiting for content...")
        time.sleep(5)  # Let page fully load
        
        # Try to find upcoming matches section
        try:
            # Look for match containers with team names
            # Try to find divs or sections that contain match info
            match_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/matches/') and contains(@href, '#')]")
            
            print(f"Found {len(match_elements)} potential match elements")
            
            seen_ids = set()
            for element in match_elements:
                try:
                    # Get match URL
                    href = element.get_attribute("href")
                    if not href:
                        continue
                    
                    # Extract match ID from different URL formats
                    match_id = None
                    if "/matches/" in href and "#" in href:
                        # Format: /matches/...#4506263
                        match_id = href.split("#")[-1].split("?")[0]
                    elif "/match/" in href:
                        # Format: /match/4506263
                        match_id = href.split("/match/")[-1].split("/")[0].split("#")[0].split("?")[0]
                    
                    if not match_id or not match_id.isdigit() or match_id in seen_ids:
                        continue
                    
                    seen_ids.add(match_id)
                    
                    # Try to extract team names from URL first
                    team_names = None
                    try:
                        # Extract from URL: /matches/team1-vs-team2/...#id
                        if "/matches/" in href or "/fixtures/" in href:
                            url_part = href.split("/matches/")[1].split("/")[0] if "/matches/" in href else href.split("/fixtures/")[1].split("/")[0]
                            # Format: "tottenham-hotspur-vs-liverpool"
                            if "-vs-" in url_part:
                                parts = url_part.split("-vs-")
                                home = parts[0].replace("-", " ").title()
                                away = parts[1].replace("-", " ").title()
                                team_names = (home, away)
                    except Exception as e:
                        if len(seen_ids) <= 3:
                            print(f"    Debug - Error extracting teams: {e}")
                        
                    # Debug: print first few
                    if len(seen_ids) <= 5:
                        print(f"    Match {match_id}: {team_names if team_names else 'NO TEAMS'}")
                    
                    # Skip the text parsing since we got teams from URL
                    if team_names:
                        print(f"  ✓ {team_names[0]} vs {team_names[1]}")
                        
                        upcoming_matches.append({
                            'id': len(upcoming_matches) + 1,
                            'matchId': match_id,
                            'homeTeam': team_names[0],
                            'awayTeam': team_names[1],
                            'homeTeamId': TEAM_IDS.get(team_names[0]),
                            'awayTeamId': TEAM_IDS.get(team_names[1]),
                            'matchUrl': href,
                        })
                        print(f"  ✓ {team_names[0]} vs {team_names[1]}")
                    
                except Exception as e:
                    continue
            
            print(f"\n✓ Extracted {len(upcoming_matches)} upcoming matches\n")
            
        except Exception as e:
            print(f"⚠ Error finding matches: {e}")
        
        return upcoming_matches
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return []
        
    finally:
        driver.quit()

def load_historical_data():
    """Load historical match data"""
    try:
        if os.path.exists(HISTORICAL_DATA_PATH):
            df = pd.read_csv(HISTORICAL_DATA_PATH)
            print(f"✓ Loaded {len(df)} historical matches")
            return df
        else:
            print(f"⚠ Historical data not found at {HISTORICAL_DATA_PATH}")
            return None
    except Exception as e:
        print(f"❌ Error loading historical data: {e}")
        return None

def calculate_team_features(team_name: str, historical_df: pd.DataFrame, is_home: bool = True) -> Dict:
    """Calculate rolling features for a team from their last 5 matches"""
    
    if historical_df is None or len(historical_df) == 0:
        return get_default_features()
    
    # Get team's last 5 matches (as home team)
    home_matches = historical_df[historical_df['HomeTeam'] == team_name].tail(5)
    # Get team's last 5 matches (as away team)
    away_matches = historical_df[historical_df['AwayTeam'] == team_name].tail(5)
    
    features = {}
    
    # Calculate attacking features (when playing at home/away)
    if is_home and len(home_matches) >= 3:
        features['xG_att_90'] = home_matches['xG_home'].mean()
        features['SoT_att_90'] = home_matches['ShotsOnTarget_home'].mean()
        features['BigCh_att_90'] = home_matches['BigChances_home'].mean()
        features['Corn_att_90'] = home_matches['Corners_home'].mean()
        features['ToB_att_90'] = home_matches['TouchesOppBox_home'].mean()
        # Defensive (what they concede at home)
        features['xGA_def_90'] = home_matches['xG_away'].mean()
        features['SoT_agst_90'] = home_matches['ShotsOnTarget_away'].mean()
        features['BigCh_agst_90'] = home_matches['BigChances_away'].mean()
    elif not is_home and len(away_matches) >= 3:
        features['xG_att_90'] = away_matches['xG_away'].mean()
        features['SoT_att_90'] = away_matches['ShotsOnTarget_away'].mean()
        features['BigCh_att_90'] = away_matches['BigChances_away'].mean()
        features['Corn_att_90'] = away_matches['Corners_away'].mean()
        features['ToB_att_90'] = away_matches['TouchesOppBox_away'].mean()
        # Defensive (what they concede away)
        features['xGA_def_90'] = away_matches['xG_home'].mean()
        features['SoT_agst_90'] = away_matches['ShotsOnTarget_home'].mean()
        features['BigCh_agst_90'] = away_matches['BigChances_home'].mean()
    else:
        return get_default_features()
    
    return features

def get_default_features():
    """Return default feature values"""
    return {
        'xG_att_90': 1.5,
        'SoT_att_90': 4.0,
        'BigCh_att_90': 2.0,
        'Corn_att_90': 5.0,
        'ToB_att_90': 15.0,
        'xGA_def_90': 1.5,
        'SoT_agst_90': 4.0,
        'BigCh_agst_90': 2.0,
    }

def enrich_with_features(matches: List[Dict], historical_df: pd.DataFrame) -> List[Dict]:
    """Add features to each match"""
    print("\n📊 Calculating features for matches...")
    
    enriched = []
    for match in matches:
        home_team = match.get('homeTeam')
        away_team = match.get('awayTeam')
        
        if not home_team or not away_team:
            continue
        
        print(f"  Processing: {home_team} vs {away_team}")
        
        # Calculate features
        home_features = calculate_team_features(home_team, historical_df, is_home=True)
        away_features = calculate_team_features(away_team, historical_df, is_home=False)
        
        # Build full feature set
        match_data = {
            **match,
            'round': 16,  # Update this based on current round
            'kickoffTime': 'TBD',
            'homePosition': 10,
            'awayPosition': 10,
            'homeForm': 'WWDLD',
            'awayForm': 'DWWLD',
            'features': {
                # Home team features
                'home_xG_att_90': home_features['xG_att_90'],
                'home_SoT_att_90': home_features['SoT_att_90'],
                'home_BigCh_att_90': home_features['BigCh_att_90'],
                'home_Corn_att_90': home_features['Corn_att_90'],
                'home_ToB_att_90': home_features['ToB_att_90'],
                'home_xGA_def_90': home_features['xGA_def_90'],
                'home_SoT_agst_90': home_features['SoT_agst_90'],
                'home_BigCh_agst_90': home_features['BigCh_agst_90'],
                # Away team features
                'away_xG_att_90': away_features['xG_att_90'],
                'away_SoT_att_90': away_features['SoT_att_90'],
                'away_BigCh_att_90': away_features['BigCh_att_90'],
                'away_Corn_att_90': away_features['Corn_att_90'],
                'away_ToB_att_90': away_features['ToB_att_90'],
                'away_xGA_def_90': away_features['xGA_def_90'],
                'away_SoT_agst_90': away_features['SoT_agst_90'],
                'away_BigCh_agst_90': away_features['BigCh_agst_90'],
                # Context features
                'home_position': 10,
                'away_position': 10,
                'points_diff': 0,
                'gd_diff': 0,
                'home_last3_points': 5,
                'home_last3_goals': 4,
                'home_form_trend': 0,
                'away_last3_points': 5,
                'away_last3_goals': 4,
                'away_form_trend': 0,
                'home_strength_ratio': 0.5,
                'away_strength_ratio': 0.5,
            }
        }
        
        enriched.append(match_data)
        print(f"    ✓ Features calculated")
    
    return enriched

def save_to_json(matches: List[Dict]):
    """Save matches to JSON file"""
    output_path = os.path.join(os.path.dirname(__file__), OUTPUT_FILE)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(matches, f, indent=2)
    
    print(f"\n💾 Saved {len(matches)} matches to: {output_path}")
    return output_path

def main():
    print("Starting upcoming matches scraper...")
    
    # Fetch upcoming fixtures
    matches = fetch_upcoming_fixtures()
    
    if not matches:
        print("\n⚠ No upcoming matches found")
        print("The app will use sample data")
        return
    
    # Load historical data
    historical_df = load_historical_data()
    
    # Enrich with features
    enriched_matches = enrich_with_features(matches, historical_df)
    
    if not enriched_matches:
        print("\n⚠ No matches could be enriched")
        return
    
    # Save to JSON
    save_to_json(enriched_matches)
    
    print("\n" + "="*60)
    print("✅ SUCCESS!")
    print("="*60)
    print(f"Fetched {len(enriched_matches)} upcoming matches")
    print("Web app will use this data on next refresh")
    print("="*60)

if __name__ == '__main__':
    main()
