"""
Fetch upcoming Premier League matches from FotMob and prepare features for prediction
"""

import requests
import json
import pandas as pd
from datetime import datetime
import sys
import os

# Add parent directory to path to import from main project
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

def fetch_upcoming_fixtures():
    """Fetch upcoming Premier League fixtures from FotMob"""
    print("Fetching upcoming Premier League fixtures from FotMob...")
    
    # FotMob API endpoint for Premier League (league ID: 47)
    url = "https://www.fotmob.com/api/leagues?id=47"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Extract upcoming matches
        upcoming_matches = []
        
        # Look for matches in the fixtures section
        if 'matches' in data:
            matches = data['matches']
            if 'allMatches' in matches:
                for match in matches['allMatches']:
                    # Only include matches that haven't started yet
                    if match.get('status', {}).get('started') == False:
                        match_info = {
                            'matchId': match.get('id'),
                            'homeTeam': match.get('home', {}).get('name'),
                            'awayTeam': match.get('away', {}).get('name'),
                            'homeTeamId': match.get('home', {}).get('id'),
                            'awayTeamId': match.get('away', {}).get('id'),
                            'round': match.get('round'),
                            'kickoffTime': match.get('status', {}).get('utcTime'),
                            'matchUrl': f"https://www.fotmob.com/matches/{match.get('id')}"
                        }
                        upcoming_matches.append(match_info)
        
        print(f"✓ Found {len(upcoming_matches)} upcoming matches")
        return upcoming_matches
        
    except Exception as e:
        print(f"✗ Error fetching fixtures: {e}")
        return []

def load_historical_data():
    """Load historical match data to compute team statistics"""
    print("\nLoading historical data...")
    
    try:
        # Load the labels and features from your existing data
        labels_path = '../../tables/all_rounds.csv'
        features_path = '../../feature_tables/match_features_enhanced.csv'
        
        if os.path.exists(labels_path) and os.path.exists(features_path):
            labels_df = pd.read_csv(labels_path)
            features_df = pd.read_csv(features_path)
            
            print(f"✓ Loaded {len(labels_df)} historical matches")
            return labels_df, features_df
        else:
            print("✗ Historical data files not found")
            return None, None
            
    except Exception as e:
        print(f"✗ Error loading historical data: {e}")
        return None, None

def compute_team_features(team_name, historical_data, features_data):
    """Compute rolling features for a team based on their last 5 matches"""
    
    # Filter matches for this team (home or away)
    team_matches = historical_data[
        (historical_data['homeTeamName'] == team_name) | 
        (historical_data['awayTeamName'] == team_name)
    ].sort_values('round', ascending=False).head(5)
    
    if len(team_matches) < 3:
        # Not enough data, return default values
        return None
    
    # Get corresponding features
    team_features = features_data[
        features_data['matchId'].isin(team_matches['matchId'])
    ]
    
    # Calculate rolling averages (simplified - you'd need more complex logic for home/away split)
    features = {
        'xG_att_90': team_features['home_xG_att_90'].mean() if len(team_features) > 0 else 1.5,
        'SoT_att_90': team_features['home_SoT_att_90'].mean() if len(team_features) > 0 else 4.0,
        'BigCh_att_90': team_features['home_BigCh_att_90'].mean() if len(team_features) > 0 else 2.0,
        'Corn_att_90': team_features['home_Corn_att_90'].mean() if len(team_features) > 0 else 5.0,
        'ToB_att_90': team_features['home_ToB_att_90'].mean() if len(team_features) > 0 else 15.0,
        'xGA_def_90': team_features['home_xGA_def_90'].mean() if len(team_features) > 0 else 1.5,
        'SoT_agst_90': team_features['home_SoT_agst_90'].mean() if len(team_features) > 0 else 4.0,
        'BigCh_agst_90': team_features['home_BigCh_agst_90'].mean() if len(team_features) > 0 else 2.0,
    }
    
    return features

def prepare_match_features(upcoming_matches, historical_data, features_data):
    """Prepare features for upcoming matches"""
    print("\nPreparing features for upcoming matches...")
    
    prepared_matches = []
    
    for match in upcoming_matches:
        print(f"  Processing: {match['homeTeam']} vs {match['awayTeam']}")
        
        # Get features for both teams
        home_features = compute_team_features(match['homeTeam'], historical_data, features_data)
        away_features = compute_team_features(match['awayTeam'], historical_data, features_data)
        
        if home_features is None or away_features is None:
            print(f"    ⚠ Skipping - insufficient historical data")
            continue
        
        # Combine features
        match_features = {
            'home_xG_att_90': home_features['xG_att_90'],
            'home_SoT_att_90': home_features['SoT_att_90'],
            'home_BigCh_att_90': home_features['BigCh_att_90'],
            'home_Corn_att_90': home_features['Corn_att_90'],
            'home_ToB_att_90': home_features['ToB_att_90'],
            'home_xGA_def_90': home_features['xGA_def_90'],
            'home_SoT_agst_90': home_features['SoT_agst_90'],
            'home_BigCh_agst_90': home_features['BigCh_agst_90'],
            'away_xG_att_90': away_features['xG_att_90'],
            'away_SoT_att_90': away_features['SoT_att_90'],
            'away_BigCh_att_90': away_features['BigCh_att_90'],
            'away_Corn_att_90': away_features['Corn_att_90'],
            'away_ToB_att_90': away_features['ToB_att_90'],
            'away_xGA_def_90': away_features['xGA_def_90'],
            'away_SoT_agst_90': away_features['SoT_agst_90'],
            'away_BigCh_agst_90': away_features['BigCh_agst_90'],
            # Add default values for contextual features (would need league table data)
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
        
        prepared_match = {
            **match,
            'features': match_features,
            'homeForm': 'WWDLD',  # Placeholder
            'awayForm': 'DWWLD',  # Placeholder
        }
        
        prepared_matches.append(prepared_match)
        print(f"    ✓ Features prepared")
    
    return prepared_matches

def save_to_json(matches, filename='upcoming_matches.json'):
    """Save prepared matches to JSON file"""
    output_path = os.path.join(os.path.dirname(__file__), filename)
    
    with open(output_path, 'w') as f:
        json.dump(matches, f, indent=2)
    
    print(f"\n✓ Saved {len(matches)} matches to {filename}")
    return output_path

def main():
    print("="*60)
    print("FETCHING LIVE UPCOMING PREMIER LEAGUE MATCHES")
    print("="*60)
    
    # Step 1: Fetch upcoming fixtures
    upcoming_matches = fetch_upcoming_fixtures()
    
    if not upcoming_matches:
        print("\n✗ No upcoming matches found or error fetching data")
        return
    
    # Step 2: Load historical data
    historical_data, features_data = load_historical_data()
    
    if historical_data is None:
        print("\n⚠ Warning: No historical data available")
        print("   Saving fixtures without features...")
        save_to_json(upcoming_matches, 'upcoming_fixtures_raw.json')
        return
    
    # Step 3: Prepare features
    prepared_matches = prepare_match_features(upcoming_matches, historical_data, features_data)
    
    if not prepared_matches:
        print("\n✗ No matches could be prepared with features")
        return
    
    # Step 4: Save to JSON
    output_file = save_to_json(prepared_matches)
    
    print("\n" + "="*60)
    print("✅ SUCCESS!")
    print("="*60)
    print(f"Next steps:")
    print(f"1. Review the data in: {output_file}")
    print(f"2. Use the Flask API to get predictions")
    print(f"3. Update the frontend to load this data")
    print("="*60)

if __name__ == '__main__':
    main()
