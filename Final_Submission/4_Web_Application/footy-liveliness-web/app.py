"""
Flask API for Footy Liveliness Predictions

Serves predictions for upcoming Premier League matches
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import pickle
import numpy as np
import pandas as pd
import json
import os
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
CORS(app)

# Load model artifacts
print("Loading model artifacts...")
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

with open('feature_names.pkl', 'rb') as f:
    feature_names = pickle.load(f)

with open('team_stats.pkl', 'rb') as f:
    team_stats = pickle.load(f)

print(f"✓ Model loaded ({len(feature_names)} features)")

# Load fixtures from scraped data (try all_fixtures.json first, then upcoming_fixtures.json)
ALL_FIXTURES_FILE = "../data/current_season/all_fixtures.json"
UPCOMING_FIXTURES_FILE = "../data/current_season/upcoming_fixtures.json"

def load_fixtures():
    """Load fixtures from JSON file, fallback to mock data if not available"""
    # Try all_fixtures.json first (includes past and future matches)
    try:
        if os.path.exists(ALL_FIXTURES_FILE):
            with open(ALL_FIXTURES_FILE, 'r', encoding='utf-8') as f:
                fixtures = json.load(f)
                if fixtures:
                    print(f"✓ Loaded {len(fixtures)} fixtures from {ALL_FIXTURES_FILE}")
                    finished = sum(1 for f in fixtures if f.get('status') == 'finished')
                    upcoming = sum(1 for f in fixtures if f.get('status') == 'upcoming')
                    print(f"  • {finished} finished matches, {upcoming} upcoming matches")
                    return fixtures
    except Exception as e:
        print(f"⚠ Error loading all_fixtures file: {e}")
    
    # Fallback to upcoming_fixtures.json
    try:
        if os.path.exists(UPCOMING_FIXTURES_FILE):
            with open(UPCOMING_FIXTURES_FILE, 'r', encoding='utf-8') as f:
                fixtures = json.load(f)
                if fixtures:
                    print(f"✓ Loaded {len(fixtures)} fixtures from {UPCOMING_FIXTURES_FILE}")
                    # Add status field if not present
                    for fixture in fixtures:
                        if 'status' not in fixture:
                            fixture['status'] = 'upcoming'
                    return fixtures
    except Exception as e:
        print(f"⚠ Error loading upcoming_fixtures file: {e}")
    
    # Fallback to mock data
    print("⚠ Using mock fixtures (run scrape_all_season_fixtures.py to get real data)")
    return [
        {"home": "Arsenal", "away": "Manchester City", "date": "2025-01-15", "time": "20:00", "status": "upcoming"},
        {"home": "Liverpool", "away": "Chelsea", "date": "2025-01-15", "time": "17:30", "status": "upcoming"},
        {"home": "Manchester United", "away": "Tottenham Hotspur", "date": "2025-01-16", "time": "16:30", "status": "upcoming"},
        {"home": "Newcastle United", "away": "Aston Villa", "date": "2025-01-16", "time": "19:00", "status": "upcoming"},
        {"home": "Brighton & Hove Albion", "away": "West Ham United", "date": "2025-01-17", "time": "20:00", "status": "upcoming"},
        {"home": "Brentford", "away": "Nottingham Forest", "date": "2025-01-18", "time": "15:00", "status": "upcoming"},
        {"home": "Everton", "away": "Fulham", "date": "2025-01-18", "time": "15:00", "status": "upcoming"},
        {"home": "Leicester City", "away": "Crystal Palace", "date": "2025-01-18", "time": "15:00", "status": "upcoming"},
        {"home": "Southampton", "away": "AFC Bournemouth", "date": "2025-01-18", "time": "15:00", "status": "upcoming"},
        {"home": "Wolverhampton Wanderers", "away": "Ipswich Town", "date": "2025-01-19", "time": "16:00", "status": "upcoming"},
    ]

ALL_FIXTURES = load_fixtures()

def create_features_for_match(home_team, away_team):
    """
    Create feature vector for a match using latest team stats
    """
    # Get team stats (use league average if team not found)
    home_stats = team_stats.get(home_team, {})
    away_stats = team_stats.get(away_team, {})
    
    # Create feature vector with defaults
    features = {}
    
    for feat in feature_names:
        if 'Home_' in feat:
            features[feat] = home_stats.get(feat, 1.5)  # League average defaults
        elif 'Away_' in feat:
            features[feat] = away_stats.get(feat, 1.5)
        elif feat == 'Home_days_rest':
            features[feat] = 7.0  # Assume 1 week rest
        elif feat == 'DaysRestDiff':
            features[feat] = 0.0
        elif feat == 'LeagueAvg_xG_perMatch_sofar':
            features[feat] = 2.8
        elif feat == 'LeagueAvg_Corners_perMatch_sofar':
            features[feat] = 10.0
        elif feat == 'HomeFlag':
            features[feat] = 1.0
        else:
            features[feat] = 0.0
    
    return np.array([features[f] for f in feature_names]).reshape(1, -1)

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "model": "Elastic Net", "features": len(feature_names)})

@app.route('/api/predict', methods=['POST'])
def predict():
    """Predict liveliness for a single match"""
    data = request.json
    home_team = data.get('home')
    away_team = data.get('away')
    
    if not home_team or not away_team:
        return jsonify({"error": "Missing home or away team"}), 400
    
    # Create features
    X = create_features_for_match(home_team, away_team)
    X_scaled = scaler.transform(X)
    
    # Predict
    prediction = model.predict(X_scaled)[0]
    
    return jsonify({
        "home": home_team,
        "away": away_team,
        "predicted_liveliness": round(float(prediction), 2)
    })

@app.route('/api/upcoming', methods=['GET'])
def upcoming():
    """Get all fixtures (past and future) with predictions"""
    # Reload fixtures to get latest data
    global ALL_FIXTURES
    ALL_FIXTURES = load_fixtures()
    
    predictions = []
    
    for fixture in ALL_FIXTURES:
        # Create features
        X = create_features_for_match(fixture['home'], fixture['away'])
        X_scaled = scaler.transform(X)
        
        # Predict
        prediction = model.predict(X_scaled)[0]
        
        pred_dict = {
            "home": fixture['home'],
            "away": fixture['away'],
            "date": fixture.get('date', 'TBD'),
            "time": fixture.get('time', 'TBD'),
            "predicted_liveliness": round(float(prediction), 2),
            "status": fixture.get('status', 'upcoming')
        }
        
        # Add matchId if available
        if 'matchId' in fixture:
            pred_dict['matchId'] = fixture['matchId']
        
        # Add actual data if available (for finished matches)
        if fixture.get('actualXG'):
            pred_dict['actualXG'] = fixture['actualXG']
        if fixture.get('actualScore'):
            pred_dict['actualScore'] = fixture['actualScore']
        
        predictions.append(pred_dict)
    
    # Sort by predicted liveliness (descending)
    predictions.sort(key=lambda x: x['predicted_liveliness'], reverse=True)
    
    # Add rank
    for i, pred in enumerate(predictions, 1):
        pred['rank'] = i
    
    return jsonify(predictions)

@app.route('/api/refresh-fixtures', methods=['POST'])
def refresh_fixtures():
    """Manually trigger fixture refresh (useful after running scraper)"""
    global UPCOMING_FIXTURES
    UPCOMING_FIXTURES = load_upcoming_fixtures()
    return jsonify({
        "status": "success",
        "fixtures_count": len(UPCOMING_FIXTURES),
        "message": f"Loaded {len(UPCOMING_FIXTURES)} fixtures"
    })

@app.route('/api/stats', methods=['GET'])
def stats():
    """Get model statistics"""
    return jsonify({
        "model": "Elastic Net",
        "target": "Simple xG (xG_total + min(xG_home, xG_away))",
        "performance": {
            "r2": 0.8205,
            "mae": 0.452,
            "top10_hit_rate": 90.0
        },
        "features": len(feature_names),
        "training_season": "2024/25",
        "training_matches": 380
    })

if __name__ == '__main__':
    print("\n" + "="*80)
    print("FOOTY LIVELINESS API")
    print("="*80)
    print("\nEndpoints:")
    print("  GET  /api/health           - Health check")
    print("  GET  /api/upcoming         - Get ranked upcoming fixtures")
    print("  POST /api/predict          - Predict single match")
    print("  POST /api/refresh-fixtures - Reload fixtures from file")
    print("  GET  /api/stats            - Model statistics")
    print("\n" + "="*80)
    print("\nTo scrape latest fixtures:")
    print("  python3 scrape_upcoming_fixtures.py")
    print("\n" + "="*80)
    print("\nStarting server on http://localhost:5001")
    print("="*80 + "\n")
    
    # Use PORT from environment variable (for Render) or default to 5001
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, port=port, host='0.0.0.0')
