"""
Scrape upcoming Premier League fixtures for 2025-26 season from FotMob
"""

import requests
import json
from datetime import datetime
import os

def scrape_upcoming_fixtures():
    """
    Scrape upcoming Premier League fixtures from FotMob API
    """
    print("Scraping upcoming Premier League fixtures from FotMob...")
    
    # FotMob API endpoint for Premier League (league ID: 47)
    url = "https://www.fotmob.com/api/leagues?id=47"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Extract upcoming fixtures
        fixtures = []
        
        # Look for matches in the fixtures section
        if 'matches' in data and 'allMatches' in data['matches']:
            for match in data['matches']['allMatches']:
                # Only include upcoming matches (not finished)
                if match.get('status', {}).get('finished') == False:
                    fixture = {
                        'id': match.get('id'),
                        'home': match.get('home', {}).get('name'),
                        'away': match.get('away', {}).get('name'),
                        'date': match.get('status', {}).get('utcTime'),
                        'round': match.get('round'),
                        'status': match.get('status', {}).get('reason', {}).get('short')
                    }
                    fixtures.append(fixture)
        
        print(f"✓ Found {len(fixtures)} upcoming fixtures")
        
        # Save to JSON
        output_dir = 'data/current_season'
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = f'{output_dir}/upcoming_fixtures.json'
        with open(output_file, 'w') as f:
            json.dump(fixtures, f, indent=2)
        
        print(f"✓ Saved to {output_file}")
        
        # Print fixtures for verification
        print("\nUpcoming fixtures:")
        for i, fixture in enumerate(fixtures[:10], 1):
            date_str = fixture['date'][:10] if fixture['date'] else 'TBD'
            print(f"{i}. {fixture['home']} vs {fixture['away']} — {date_str}")
        
        return fixtures
        
    except Exception as e:
        print(f"✗ Error scraping fixtures: {e}")
        return []

if __name__ == '__main__':
    scrape_upcoming_fixtures()
