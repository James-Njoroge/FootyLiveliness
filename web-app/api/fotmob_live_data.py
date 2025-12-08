"""
Fetch live upcoming Premier League matches using the fotmob-api package
This handles FotMob's authentication automatically
"""

import json
import sys
from datetime import datetime
from pyfotmob import FotMob

def fetch_upcoming_matches():
    """Fetch upcoming Premier League fixtures using pyfotmob"""
    print("="*60)
    print("FETCHING LIVE PREMIER LEAGUE MATCHES FROM FOTMOB")
    print("="*60)
    
    try:
        # Initialize FotMob client
        fotmob = FotMob()
        
        # Get Premier League data (league ID: 47)
        print("\n📡 Connecting to FotMob API...")
        league_data = fotmob.get_league(league_id=47, tab='overview', season='2024/2025')
        
        # Extract upcoming matches
        upcoming_matches = []
        
        if 'matches' in league_data and 'allMatches' in league_data['matches']:
            all_matches = league_data['matches']['allMatches']
            
            for match in all_matches:
                # Only include matches that haven't started
                if not match.get('status', {}).get('started', True):
                    
                    # Parse kickoff time
                    utc_time = match.get('status', {}).get('utcTime', '')
                    try:
                        dt = datetime.fromisoformat(utc_time.replace('Z', '+00:00'))
                        kickoff_formatted = dt.strftime('%b %d, %Y %I:%M %p EST')
                    except:
                        kickoff_formatted = utc_time
                    
                    match_info = {
                        'id': match.get('id'),
                        'homeTeam': match.get('home', {}).get('name'),
                        'awayTeam': match.get('away', {}).get('name'),
                        'homeTeamId': match.get('home', {}).get('id'),
                        'awayTeamId': match.get('away', {}).get('id'),
                        'round': match.get('round'),
                        'kickoffTime': kickoff_formatted,
                        'matchUrl': f"https://www.fotmob.com/matches/{match.get('id')}",
                        'homePosition': None,  # Will be filled from league table
                        'awayPosition': None,
                        'homeForm': 'N/A',  # Will be filled from team data
                        'awayForm': 'N/A',
                    }
                    
                    upcoming_matches.append(match_info)
            
            print(f"✅ Found {len(upcoming_matches)} upcoming matches")
            
            # Display matches
            if upcoming_matches:
                print("\n📋 Upcoming Matches:")
                for i, match in enumerate(upcoming_matches, 1):
                    print(f"  {i}. {match['homeTeam']} vs {match['awayTeam']}")
                    print(f"     Round {match['round']} - {match['kickoffTime']}")
            
            return upcoming_matches
        else:
            print("❌ No matches data found in API response")
            return []
            
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        print(f"   Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return []

def get_team_stats(team_id):
    """Get team statistics from FotMob"""
    try:
        fotmob = FotMob()
        team_data = fotmob.get_team(team_id=team_id, tab='overview')
        
        # Extract relevant stats
        stats = {
            'form': team_data.get('history', {}).get('form', 'N/A'),
            'position': team_data.get('details', {}).get('position'),
        }
        
        return stats
    except Exception as e:
        print(f"  ⚠ Could not fetch stats for team {team_id}: {e}")
        return None

def enrich_matches_with_stats(matches):
    """Add team statistics to matches"""
    print("\n📊 Enriching matches with team statistics...")
    
    for match in matches:
        print(f"  Processing: {match['homeTeam']} vs {match['awayTeam']}")
        
        # Get home team stats
        home_stats = get_team_stats(match['homeTeamId'])
        if home_stats:
            match['homeForm'] = home_stats.get('form', 'N/A')
            match['homePosition'] = home_stats.get('position')
        
        # Get away team stats
        away_stats = get_team_stats(match['awayTeamId'])
        if away_stats:
            match['awayForm'] = away_stats.get('form', 'N/A')
            match['awayPosition'] = away_stats.get('position')
    
    return matches

def save_to_json(matches, filename='live_matches.json'):
    """Save matches to JSON file"""
    output_path = filename
    
    with open(output_path, 'w') as f:
        json.dump(matches, f, indent=2)
    
    print(f"\n💾 Saved {len(matches)} matches to {filename}")
    return output_path

def main():
    # Fetch upcoming matches
    matches = fetch_upcoming_matches()
    
    if not matches:
        print("\n❌ No matches to process")
        return
    
    # Enrich with team stats (optional - can be slow)
    # Uncomment if you want to fetch team stats
    # matches = enrich_matches_with_stats(matches)
    
    # Save to JSON
    save_to_json(matches, 'live_upcoming_matches.json')
    
    print("\n" + "="*60)
    print("✅ SUCCESS!")
    print("="*60)
    print("\nNext steps:")
    print("1. Review live_upcoming_matches.json")
    print("2. Add features using your historical data")
    print("3. Send to Flask API for predictions")
    print("="*60)

if __name__ == '__main__':
    main()
