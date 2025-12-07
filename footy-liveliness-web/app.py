"""
Flask API for Footy Liveliness Predictions

Serves predictions for upcoming Premier League matches
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import pickle
import numpy as np
import pandas as pd
from datetime import datetime

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

# Mock upcoming fixtures (in production, fetch from API)
UPCOMING_FIXTURES = [
    {"home": "Arsenal", "away": "Manchester City", "date": "2025-01-15", "time": "20:00"},
    {"home": "Liverpool", "away": "Chelsea", "date": "2025-01-15", "time": "17:30"},
    {"home": "Manchester United", "away": "Tottenham Hotspur", "date": "2025-01-16", "time": "16:30"},
    {"home": "Newcastle United", "away": "Aston Villa", "date": "2025-01-16", "time": "19:00"},
    {"home": "Brighton & Hove Albion", "away": "West Ham United", "date": "2025-01-17", "time": "20:00"},
    {"home": "Brentford", "away": "Nottingham Forest", "date": "2025-01-18", "time": "15:00"},
    {"home": "Everton", "away": "Fulham", "date": "2025-01-18", "time": "15:00"},
    {"home": "Leicester City", "away": "Crystal Palace", "date": "2025-01-18", "time": "15:00"},
    {"home": "Southampton", "away": "AFC Bournemouth", "date": "2025-01-18", "time": "15:00"},
    {"home": "Wolverhampton Wanderers", "away": "Ipswich Town", "date": "2025-01-19", "time": "16:00"},
]

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
    """Get all upcoming fixtures with predictions"""
    predictions = []
    
    for fixture in UPCOMING_FIXTURES:
        # Create features
        X = create_features_for_match(fixture['home'], fixture['away'])
        X_scaled = scaler.transform(X)
        
        # Predict
        prediction = model.predict(X_scaled)[0]
        
        predictions.append({
            "home": fixture['home'],
            "away": fixture['away'],
            "date": fixture['date'],
            "time": fixture['time'],
            "predicted_liveliness": round(float(prediction), 2)
        })
    
    # Sort by predicted liveliness (descending)
    predictions.sort(key=lambda x: x['predicted_liveliness'], reverse=True)
    
    # Add rank
    for i, pred in enumerate(predictions, 1):
        pred['rank'] = i
    
    return jsonify(predictions)

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
    print("  GET  /api/health    - Health check")
    print("  GET  /api/upcoming  - Get ranked upcoming fixtures")
    print("  POST /api/predict   - Predict single match")
    print("  GET  /api/stats     - Model statistics")
    print("\n" + "="*80)
    print("\nStarting server on http://localhost:5001")
    print("="*80 + "\n")
    
    app.run(debug=True, port=5001, host='127.0.0.1')
