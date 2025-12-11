"""
Train and Save Best Model for Web App

Trains Elastic Net on Simple xG target using 2024/25 season data
Saves model and scaler for deployment
"""

import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import ElasticNetCV
from sklearn.preprocessing import StandardScaler

print("="*80)
print("TRAINING AND SAVING BEST MODEL FOR WEB APP")
print("="*80)

# Load data
print("\n[1/4] Loading data...")
targets_df = pd.read_csv('../target_metric_experiments/targets_comparison.csv')
features_df = pd.read_csv('../data/feature_tables/match_features_wide.csv')

# Rename columns
features_df = features_df.rename(columns={
    'Round': 'round',
    'HomeTeam': 'homeTeamName',
    'AwayTeam': 'awayTeamName'
})

# Merge
df = pd.merge(targets_df, features_df,
              on=['round', 'homeTeamName', 'awayTeamName'],
              how='inner')

print(f"Loaded {len(df)} matches")

# Prepare data
print("\n[2/4] Preparing features...")

# Feature columns (from your experiments)
feature_cols = [col for col in features_df.columns 
                if col not in ['round', 'homeTeamName', 'awayTeamName', 'SLS_Fplus']]

print(f"Using {len(feature_cols)} features")

# Use all data for training (for deployment)
X = df[feature_cols].values
y = df['target_1_simple_xg'].values

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train model
print("\n[3/4] Training Elastic Net model...")

alphas = np.logspace(-3, 1, 20)
l1_ratios = [0.1, 0.3, 0.5, 0.7, 0.9, 0.95, 0.99]
model = ElasticNetCV(alphas=alphas, l1_ratio=l1_ratios, cv=5, max_iter=10000)
model.fit(X_scaled, y)

print(f"Best alpha: {model.alpha_:.4f}")
print(f"Best l1_ratio: {model.l1_ratio_:.2f}")

# Save model and scaler
print("\n[4/4] Saving model artifacts...")

with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

# Save feature names
with open('feature_names.pkl', 'wb') as f:
    pickle.dump(feature_cols, f)

# Save team statistics for predictions
team_stats = {}
for team in set(df['homeTeamName'].unique()) | set(df['awayTeamName'].unique()):
    # Get latest stats for this team
    home_matches = df[df['homeTeamName'] == team].sort_values('round', ascending=False)
    away_matches = df[df['awayTeamName'] == team].sort_values('round', ascending=False)
    
    if len(home_matches) > 0:
        latest_home = home_matches.iloc[0]
        team_stats[team] = {col: latest_home[col] for col in feature_cols if 'Home_' in col or col in ['Home_days_rest', 'LeagueAvg_xG_perMatch_sofar', 'LeagueAvg_Corners_perMatch_sofar']}
    elif len(away_matches) > 0:
        latest_away = away_matches.iloc[0]
        team_stats[team] = {col: latest_away[col] for col in feature_cols if 'Away_' in col}

with open('team_stats.pkl', 'wb') as f:
    pickle.dump(team_stats, f)

print("✓ Saved model.pkl")
print("✓ Saved scaler.pkl")
print("✓ Saved feature_names.pkl")
print("✓ Saved team_stats.pkl")

print("\n" + "="*80)
print("MODEL READY FOR DEPLOYMENT!")
print("="*80)
print("\nModel: Elastic Net")
print("Target: Simple xG")
print(f"Features: {len(feature_cols)}")
print(f"Training samples: {len(df)}")
print("\nFiles created:")
print("  - model.pkl (trained model)")
print("  - scaler.pkl (feature scaler)")
print("  - feature_names.pkl (feature list)")
print("  - team_stats.pkl (latest team stats)")
print("="*80)
