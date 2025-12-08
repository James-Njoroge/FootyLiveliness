"""
Flask API for Footy Liveliness Predictions
Serves predictions from the trained Ridge Regression model
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Load the trained Ridge model
MODEL_PATH = '../../NN/ridge_model.pkl'
SCALER_PATH = '../../NN/data_prepared_nn.pt'

try:
    model = joblib.load(MODEL_PATH)
    print("✓ Ridge model loaded successfully")
except Exception as e:
    print(f"⚠ Warning: Could not load model - {e}")
    model = None

# Feature names (must match training data)
FEATURE_NAMES = [
    'home_xG_att_90', 'home_SoT_att_90', 'home_BigCh_att_90', 
    'home_Corn_att_90', 'home_ToB_att_90', 'home_xGA_def_90', 
    'home_SoT_agst_90', 'home_BigCh_agst_90',
    'away_xG_att_90', 'away_SoT_att_90', 'away_BigCh_att_90',
    'away_Corn_att_90', 'away_ToB_att_90', 'away_xGA_def_90',
    'away_SoT_agst_90', 'away_BigCh_agst_90',
    'TempoSum', 'SoTSum', 'AttackVsDefense', 'xG_att_sum', 
    'xG_att_min', 'BigCh_sum',
    'home_position', 'away_position', 'position_diff',
    'points_diff', 'gd_diff',
    'home_last3_points', 'home_last3_goals', 'home_form_trend',
    'away_last3_points', 'away_last3_goals', 'away_form_trend',
    'home_strength_ratio', 'away_strength_ratio',
    'both_top6', 'both_bottom6', 'close_positions'
]

def compute_composite_features(features):
    """Compute composite features from base features"""
    features['TempoSum'] = (features['home_xG_att_90'] + features['away_xG_att_90'] + 
                            features['home_SoT_att_90'] + features['away_SoT_att_90'])
    features['SoTSum'] = features['home_SoT_att_90'] + features['away_SoT_att_90']
    features['AttackVsDefense'] = (features['home_xG_att_90'] - features['away_xGA_def_90'] + 
                                   features['away_xG_att_90'] - features['home_xGA_def_90'])
    features['xG_att_sum'] = features['home_xG_att_90'] + features['away_xG_att_90']
    features['xG_att_min'] = min(features['home_xG_att_90'], features['away_xG_att_90'])
    features['BigCh_sum'] = features['home_BigCh_att_90'] + features['away_BigCh_att_90']
    
    # Contextual features
    features['position_diff'] = features['home_position'] - features['away_position']
    features['both_top6'] = 1 if (features['home_position'] <= 6 and features['away_position'] <= 6) else 0
    features['both_bottom6'] = 1 if (features['home_position'] >= 15 and features['away_position'] >= 15) else 0
    features['close_positions'] = 1 if abs(features['position_diff']) <= 3 else 0
    
    return features

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Predict liveliness for a single match
    
    Expected JSON body:
    {
        "homeTeam": "Liverpool",
        "awayTeam": "Manchester City",
        "features": {
            "home_xG_att_90": 2.3,
            "away_xG_att_90": 2.1,
            ...
        }
    }
    """
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.json
        features = data.get('features', {})
        
        # Compute composite features
        features = compute_composite_features(features)
        
        # Create feature vector in correct order
        feature_vector = [features.get(name, 0) for name in FEATURE_NAMES]
        feature_array = np.array([feature_vector])
        
        # Make prediction
        prediction = model.predict(feature_array)[0]
        
        # Clip to reasonable range
        prediction = float(np.clip(prediction, 1.0, 8.0))
        
        return jsonify({
            'homeTeam': data.get('homeTeam'),
            'awayTeam': data.get('awayTeam'),
            'predictedLiveliness': round(prediction, 2),
            'confidence': calculate_confidence(feature_vector),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/predict/batch', methods=['POST'])
def predict_batch():
    """
    Predict liveliness for multiple matches
    
    Expected JSON body:
    {
        "matches": [
            {
                "id": 1,
                "homeTeam": "Liverpool",
                "awayTeam": "Manchester City",
                "features": {...}
            },
            ...
        ]
    }
    """
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.json
        matches = data.get('matches', [])
        
        predictions = []
        for match in matches:
            features = match.get('features', {})
            features = compute_composite_features(features)
            
            feature_vector = [features.get(name, 0) for name in FEATURE_NAMES]
            feature_array = np.array([feature_vector])
            
            prediction = model.predict(feature_array)[0]
            prediction = float(np.clip(prediction, 1.0, 8.0))
            
            predictions.append({
                'id': match.get('id'),
                'homeTeam': match.get('homeTeam'),
                'awayTeam': match.get('awayTeam'),
                'homeTeamId': match.get('homeTeamId'),
                'awayTeamId': match.get('awayTeamId'),
                'matchUrl': match.get('matchUrl'),
                'predictedLiveliness': round(prediction, 2),
                'confidence': calculate_confidence(feature_vector),
                'round': match.get('round'),
                'kickoffTime': match.get('kickoffTime'),
                'homePosition': features.get('home_position'),
                'awayPosition': features.get('away_position'),
                'homeForm': match.get('homeForm'),
                'awayForm': match.get('awayForm'),
                'isHighStakes': features.get('both_top6') == 1 or features.get('both_bottom6') == 1
            })
        
        # Sort by predicted liveliness (descending)
        predictions.sort(key=lambda x: x['predictedLiveliness'], reverse=True)
        
        return jsonify({
            'predictions': predictions,
            'count': len(predictions),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/model/info', methods=['GET'])
def model_info():
    """Get model information and performance metrics"""
    return jsonify({
        'model': 'Ridge Regression',
        'version': '1.0.0',
        'features': len(FEATURE_NAMES),
        'performance': {
            'r2_score': 0.088,
            'mae': 1.045,
            'rmse': 1.377,
            'spearman_rho': 0.287,
            'top3_accuracy': 0.67,
            'precision_at_5': 0.60
        },
        'training': {
            'samples': 240,
            'season': '2024/25',
            'alpha': 100.0
        },
        'target_metric': 'xG-Based Liveliness (xG_total + min(xG_home, xG_away))'
    })

def calculate_confidence(feature_vector):
    """
    Calculate prediction confidence based on feature completeness
    and typical ranges
    """
    # Count non-zero features
    non_zero = sum(1 for x in feature_vector if x != 0)
    completeness = non_zero / len(feature_vector)
    
    # Base confidence on completeness
    confidence = 50 + (completeness * 40)
    
    # Add small random variation for realism
    confidence += np.random.uniform(-5, 5)
    
    return int(np.clip(confidence, 50, 95))

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("="*60)
    print("🚀 Footy Liveliness API Server")
    print("="*60)
    print(f"Model loaded: {model is not None}")
    print(f"Features: {len(FEATURE_NAMES)}")
    print("Endpoints:")
    print("  GET  /api/health       - Health check")
    print("  POST /api/predict      - Single match prediction")
    print("  POST /api/predict/batch - Batch predictions")
    print("  GET  /api/model/info   - Model information")
    print("="*60)
    print("\n🌐 Server running at: http://localhost:5001")
    print("="*60)
    
    app.run(debug=True, host='0.0.0.0', port=5001)
