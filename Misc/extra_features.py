"""
Add Contextual Features to Feature Table

Computes from existing match results:
1. League position & points after each round
2. Points differential between teams
3. Form trajectory (last 3 vs previous 5 matches)
4. Home/Away strength differential
5. Goal difference trends

All computed progressively (no data leakage)
"""

import pandas as pd
import numpy as np

print("="*80)
print("ADDING CONTEXTUAL FEATURES")
print("="*80)

# ============================================================================
# LOAD DATA
# ============================================================================
print("\n[1/5] Loading existing data...")

labels_df = pd.read_csv('tables/all_rounds.csv')
features_df = pd.read_csv('feature_tables/match_features_wide.csv')

print(f"Loaded {len(labels_df)} matches")

# ============================================================================
# COMPUTE PROGRESSIVE LEAGUE STANDINGS
# ============================================================================
print("\n[2/5] Computing league standings after each round...")

# Sort by round
labels_df = labels_df.sort_values('round').reset_index(drop=True)

# Initialize standings tracker
# We'll track cumulative stats for each team
team_stats = {}

# For each team, initialize stats
all_teams = set(labels_df['homeTeamId'].unique()) | set(labels_df['awayTeamId'].unique())
for team_id in all_teams:
    team_stats[team_id] = {
        'points': 0,
        'goals_for': 0,
        'goals_against': 0,
        'wins': 0,
        'draws': 0,
        'losses': 0,
        'home_points': 0,
        'away_points': 0,
        'home_gf': 0,
        'away_gf': 0,
        'home_ga': 0,
        'away_ga': 0
    }

# Store standings for each match (BEFORE the match is played)
match_standings = []

for idx, row in labels_df.iterrows():
    current_round = row['round']
    home_id = row['homeTeamId']
    away_id = row['awayTeamId']
    
    # Get current standings BEFORE this match
    home_stats = team_stats[home_id].copy()
    away_stats = team_stats[away_id].copy()
    
    # Compute goal difference
    home_gd = home_stats['goals_for'] - home_stats['goals_against']
    away_gd = away_stats['goals_for'] - away_stats['goals_against']
    
    # Store pre-match standings
    match_standings.append({
        'matchId': row['matchId'],
        'home_points_before': home_stats['points'],
        'away_points_before': away_stats['points'],
        'home_gd_before': home_gd,
        'away_gd_before': away_gd,
        'home_wins_before': home_stats['wins'],
        'away_wins_before': away_stats['wins'],
        'home_home_points': home_stats['home_points'],  # Points earned at home
        'away_away_points': away_stats['away_points']   # Points earned away
    })
    
    # Update standings AFTER this match (for next matches)
    home_goals = row['goals_home_count']
    away_goals = row['goals_away_count']
    
    # Update goals
    team_stats[home_id]['goals_for'] += home_goals
    team_stats[home_id]['goals_against'] += away_goals
    team_stats[home_id]['home_gf'] += home_goals
    team_stats[home_id]['home_ga'] += away_goals
    
    team_stats[away_id]['goals_for'] += away_goals
    team_stats[away_id]['goals_against'] += home_goals
    team_stats[away_id]['away_gf'] += away_goals
    team_stats[away_id]['away_ga'] += home_goals
    
    # Update points and results
    if home_goals > away_goals:  # Home win
        team_stats[home_id]['points'] += 3
        team_stats[home_id]['wins'] += 1
        team_stats[home_id]['home_points'] += 3
        team_stats[away_id]['losses'] += 1
    elif home_goals < away_goals:  # Away win
        team_stats[away_id]['points'] += 3
        team_stats[away_id]['wins'] += 1
        team_stats[away_id]['away_points'] += 3
        team_stats[home_id]['losses'] += 1
    else:  # Draw
        team_stats[home_id]['points'] += 1
        team_stats[home_id]['draws'] += 1
        team_stats[home_id]['home_points'] += 1
        team_stats[away_id]['points'] += 1
        team_stats[away_id]['draws'] += 1
        team_stats[away_id]['away_points'] += 1

standings_df = pd.DataFrame(match_standings)

# Compute league position for each match
# Need to rank teams by points, then GD, within each round
labels_df = labels_df.merge(standings_df, on='matchId', how='left')

# For each round, compute rankings
for round_num in labels_df['round'].unique():
    round_matches = labels_df[labels_df['round'] == round_num]
    
    if len(round_matches) == 0:
        continue
    
    # Get all teams and their pre-match stats
    round_standings = []
    for team_id in all_teams:
        # Find any match in this round with this team to get their pre-match stats
        home_match = round_matches[round_matches['homeTeamId'] == team_id].iloc[0] if len(round_matches[round_matches['homeTeamId'] == team_id]) > 0 else None
        away_match = round_matches[round_matches['awayTeamId'] == team_id].iloc[0] if len(round_matches[round_matches['awayTeamId'] == team_id]) > 0 else None
        
        if home_match is not None:
            points = home_match['home_points_before']
            gd = home_match['home_gd_before']
        elif away_match is not None:
            points = away_match['away_points_before']
            gd = away_match['away_gd_before']
        else:
            continue
        
        round_standings.append({
            'team_id': team_id,
            'points': points,
            'gd': gd
        })
    
    # Rank teams
    round_standings_df = pd.DataFrame(round_standings)
    round_standings_df = round_standings_df.sort_values(['points', 'gd'], ascending=[False, False])
    round_standings_df['position'] = range(1, len(round_standings_df) + 1)
    
    # Map back to matches
    for idx, row in labels_df[labels_df['round'] == round_num].iterrows():
        home_pos = round_standings_df[round_standings_df['team_id'] == row['homeTeamId']]['position'].values
        away_pos = round_standings_df[round_standings_df['team_id'] == row['awayTeamId']]['position'].values
        
        labels_df.at[idx, 'home_position'] = home_pos[0] if len(home_pos) > 0 else np.nan
        labels_df.at[idx, 'away_position'] = away_pos[0] if len(away_pos) > 0 else np.nan

print(f"  Computed standings for {len(labels_df)} matches")

# ============================================================================
# COMPUTE FORM FEATURES
# ============================================================================
print("\n[3/5] Computing form trajectory features...")

def compute_form_features(df):
    """Compute last 3 matches vs previous 5 matches form"""
    df = df.sort_values('round').copy()
    
    form_features = []
    
    for idx, row in df.iterrows():
        team_id = row['homeTeamId']  # We'll do this for both home and away
        current_round = row['round']
        
        # Get team's previous matches
        prev_matches = df[
            ((df['homeTeamId'] == team_id) | (df['awayTeamId'] == team_id)) &
            (df['round'] < current_round)
        ]
        
        if len(prev_matches) < 3:
            form_features.append({
                'matchId': row['matchId'],
                'team_type': 'home',
                'last3_points': np.nan,
                'last3_goals': np.nan,
                'prev5_points': np.nan,
                'prev5_goals': np.nan,
                'form_trend': np.nan
            })
            continue
        
        # Last 3 matches
        last3 = prev_matches.tail(3)
        
        # Previous 5 matches (matches 4-8 from most recent)
        if len(prev_matches) >= 8:
            prev5 = prev_matches.iloc[-8:-3]
        else:
            prev5 = prev_matches.iloc[:-3] if len(prev_matches) > 3 else pd.DataFrame()
        
        # Compute points and goals for last 3
        last3_points = 0
        last3_goals = 0
        for _, match in last3.iterrows():
            is_home = match['homeTeamId'] == team_id
            home_goals = match['goals_home_count']
            away_goals = match['goals_away_count']
            
            if is_home:
                last3_goals += home_goals
                if home_goals > away_goals:
                    last3_points += 3
                elif home_goals == away_goals:
                    last3_points += 1
            else:
                last3_goals += away_goals
                if away_goals > home_goals:
                    last3_points += 3
                elif away_goals == home_goals:
                    last3_points += 1
        
        # Compute for previous 5
        prev5_points = 0
        prev5_goals = 0
        if len(prev5) > 0:
            for _, match in prev5.iterrows():
                is_home = match['homeTeamId'] == team_id
                home_goals = match['goals_home_count']
                away_goals = match['goals_away_count']
                
                if is_home:
                    prev5_goals += home_goals
                    if home_goals > away_goals:
                        prev5_points += 3
                    elif home_goals == away_goals:
                        prev5_points += 1
                else:
                    prev5_goals += away_goals
                    if away_goals > home_goals:
                        prev5_points += 3
                    elif away_goals == home_goals:
                        prev5_points += 1
            
            # Normalize to per-match
            prev5_points = prev5_points / len(prev5) * 3  # Scale to match last3
            prev5_goals = prev5_goals / len(prev5) * 3
        else:
            prev5_points = np.nan
            prev5_goals = np.nan
        
        # Form trend (improving if last3 > prev5)
        if not np.isnan(prev5_points):
            form_trend = last3_points - prev5_points
        else:
            form_trend = np.nan
        
        form_features.append({
            'matchId': row['matchId'],
            'team_type': 'home',
            'last3_points': last3_points,
            'last3_goals': last3_goals,
            'prev5_points': prev5_points,
            'prev5_goals': prev5_goals,
            'form_trend': form_trend
        })
    
    return pd.DataFrame(form_features)

# Compute for home teams
print("  Computing home team form...")
home_form = compute_form_features(labels_df)
home_form.columns = ['matchId', 'team_type_h', 'home_last3_points', 'home_last3_goals', 
                     'home_prev5_points', 'home_prev5_goals', 'home_form_trend']
home_form = home_form.drop('team_type_h', axis=1)

# Compute for away teams (need to swap home/away in the function)
labels_df_swapped = labels_df.copy()
labels_df_swapped['homeTeamId'] = labels_df['awayTeamId']
labels_df_swapped['awayTeamId'] = labels_df['homeTeamId']

print("  Computing away team form...")
away_form = compute_form_features(labels_df_swapped)
away_form.columns = ['matchId', 'team_type_a', 'away_last3_points', 'away_last3_goals',
                     'away_prev5_points', 'away_prev5_goals', 'away_form_trend']
away_form = away_form.drop('team_type_a', axis=1)

# Merge form features
labels_df = labels_df.merge(home_form, on='matchId', how='left')
labels_df = labels_df.merge(away_form, on='matchId', how='left')

print(f"  Form features computed")

# ============================================================================
# COMPUTE CONTEXTUAL FEATURES
# ============================================================================
print("\n[4/5] Computing contextual features...")

# Position differential
labels_df['position_diff'] = labels_df['home_position'] - labels_df['away_position']

# Points differential
labels_df['points_diff'] = labels_df['home_points_before'] - labels_df['away_points_before']

# Goal difference differential
labels_df['gd_diff'] = labels_df['home_gd_before'] - labels_df['away_gd_before']

# Home advantage strength (home points ratio)
labels_df['home_strength_ratio'] = labels_df['home_home_points'] / (labels_df['home_points_before'] + 1)  # +1 to avoid div by 0
labels_df['away_strength_ratio'] = labels_df['away_away_points'] / (labels_df['away_points_before'] + 1)

# High stakes match (both teams in top 6 or both in bottom 6)
labels_df['both_top6'] = ((labels_df['home_position'] <= 6) & (labels_df['away_position'] <= 6)).astype(int)
labels_df['both_bottom6'] = ((labels_df['home_position'] >= 15) & (labels_df['away_position'] >= 15)).astype(int)

# Position battle (positions within 3 of each other)
labels_df['close_positions'] = (abs(labels_df['position_diff']) <= 3).astype(int)

print(f"  Contextual features computed")

# ============================================================================
# MERGE WITH FEATURES TABLE AND SAVE
# ============================================================================
print("\n[5/5] Merging with features table and saving...")

# Select new features to add
new_features = labels_df[[
    'matchId',
    'home_position', 'away_position', 'position_diff',
    'home_points_before', 'away_points_before', 'points_diff',
    'home_gd_before', 'away_gd_before', 'gd_diff',
    'home_last3_points', 'home_last3_goals', 'home_form_trend',
    'away_last3_points', 'away_last3_goals', 'away_form_trend',
    'home_strength_ratio', 'away_strength_ratio',
    'both_top6', 'both_bottom6', 'close_positions'
]]

# Merge with existing features
features_enhanced = features_df.merge(new_features, on='matchId', how='left')

# Save enhanced features
features_enhanced.to_csv('feature_tables/match_features_enhanced.csv', index=False)

print(f"✓ Saved enhanced features: {len(features_enhanced)} matches")
print(f"  Total features: {len(features_enhanced.columns)}")

# Show sample
print("\n" + "="*80)
print("SAMPLE OF NEW FEATURES (Round 10)")
print("="*80)

sample = features_enhanced[features_enhanced['round'] == 10][
    ['homeTeamName', 'awayTeamName', 'home_position', 'away_position', 
     'points_diff', 'home_form_trend', 'away_form_trend']
].head(3)
print(sample.to_string(index=False))

print("\n" + "="*80)
print("COMPLETE!")
print("="*80)
print("\nGenerated: feature_tables/match_features_enhanced.csv")
print("\nNew contextual features added:")
print("  • League position (home/away)")
print("  • Points & goal difference")
print("  • Form trajectory (last 3 vs previous 5)")
print("  • Home/away strength ratios")
print("  • High-stakes indicators (top 6 battles, relegation fights)")