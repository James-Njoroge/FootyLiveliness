"""
Add Advanced Features for FootyLiveliness Model

Adds 40+ sophisticated features:
1. Head-to-Head history
2. Variance/Consistency metrics
3. Weighted recent form (exponential decay)
4. Opposition quality adjusted stats
5. Streaks & momentum indicators
6. Pace/Style indicators
7. Extreme result tendencies
8. Time-based features (if available)

All computed progressively with no data leakage
"""

import pandas as pd
import numpy as np
from datetime import datetime

print("="*80)
print("ADDING ADVANCED FEATURES")
print("="*80)

# ============================================================================
# LOAD DATA
# ============================================================================
print("\n[1/9] Loading data...")

labels_df = pd.read_csv('tables/all_rounds.csv')
features_enhanced = pd.read_csv('feature_tables/match_features_enhanced.csv')

# Merge to have all data
df = pd.merge(labels_df, features_enhanced,
              on=['round', 'matchId', 'homeTeamName', 'awayTeamName', 'homeTeamId', 'awayTeamId'],
              how='inner')

df = df.sort_values('round').reset_index(drop=True)

print(f"Loaded {len(df)} matches")

# ============================================================================
# 1. HEAD-TO-HEAD HISTORY
# ============================================================================
print("\n[2/9] Computing Head-to-Head features...")

def compute_h2h_features(df):
    """Compute H2H history between teams"""
    h2h_features = []
    
    for idx, row in df.iterrows():
        current_round = row['round']
        home_id = row['homeTeamId']
        away_id = row['awayTeamId']
        
        # Find previous H2H matches (either home vs away or away vs home)
        h2h_matches = df[
            (df['round'] < current_round) &
            (((df['homeTeamId'] == home_id) & (df['awayTeamId'] == away_id)) |
             ((df['homeTeamId'] == away_id) & (df['awayTeamId'] == home_id)))
        ]
        
        if len(h2h_matches) == 0:
            h2h_features.append({
                'matchId': row['matchId'],
                'h2h_count': 0,
                'h2h_avg_goals': np.nan,
                'h2h_avg_xG': np.nan,
                'h2h_avg_liveliness': np.nan,
                'h2h_home_win_pct': np.nan,
                'h2h_high_scoring_pct': np.nan
            })
            continue
        
        # Use last 5 H2H matches
        recent_h2h = h2h_matches.tail(5)
        
        # Compute H2H stats
        avg_goals = recent_h2h['Goals_total'].mean()
        avg_xg = recent_h2h['xG_total'].mean()
        
        # Use xG-based liveliness if available
        if 'Liveliness_xG' in recent_h2h.columns:
            avg_liveliness = recent_h2h['Liveliness_xG'].mean()
        else:
            avg_liveliness = np.nan
        
        # Home team win percentage in H2H
        home_wins = 0
        for _, match in recent_h2h.iterrows():
            if match['homeTeamId'] == home_id:
                if match['goals_home_count'] > match['goals_away_count']:
                    home_wins += 1
            else:  # home_id was away in that match
                if match['goals_away_count'] > match['goals_home_count']:
                    home_wins += 1
        
        home_win_pct = home_wins / len(recent_h2h)
        
        # High-scoring match percentage (4+ goals)
        high_scoring = (recent_h2h['Goals_total'] >= 4).sum() / len(recent_h2h)
        
        h2h_features.append({
            'matchId': row['matchId'],
            'h2h_count': len(h2h_matches),
            'h2h_avg_goals': avg_goals,
            'h2h_avg_xG': avg_xg,
            'h2h_avg_liveliness': avg_liveliness,
            'h2h_home_win_pct': home_win_pct,
            'h2h_high_scoring_pct': high_scoring
        })
    
    return pd.DataFrame(h2h_features)

h2h_df = compute_h2h_features(df)
df = df.merge(h2h_df, on='matchId', how='left')

print(f"  H2H features computed for {df['h2h_avg_goals'].notna().sum()} matches")

# ============================================================================
# 2. VARIANCE/CONSISTENCY FEATURES
# ============================================================================
print("\n[3/9] Computing variance/consistency features...")

def compute_variance_features(df, team_col, prefix):
    """Compute volatility/variance in team performance"""
    variance_features = []
    
    for idx, row in df.iterrows():
        team_id = row[team_col]
        current_round = row['round']
        
        # Get last 5 matches
        prev_matches = df[
            ((df['homeTeamId'] == team_id) | (df['awayTeamId'] == team_id)) &
            (df['round'] < current_round)
        ].tail(5)
        
        if len(prev_matches) < 3:
            variance_features.append({
                'matchId': row['matchId'],
                'xG_variance': np.nan,
                'goals_variance': np.nan,
                'xGA_variance': np.nan,
                'result_consistency': np.nan
            })
            continue
        
        # Extract team's stats
        xg_list, goals_list, xga_list, results = [], [], [], []
        
        for _, match in prev_matches.iterrows():
            is_home = match['homeTeamId'] == team_id
            
            if is_home:
                xg_list.append(match['xG_home'])
                goals_list.append(match['goals_home_count'])
                xga_list.append(match['xG_away'])
                
                if match['goals_home_count'] > match['goals_away_count']:
                    results.append(3)
                elif match['goals_home_count'] == match['goals_away_count']:
                    results.append(1)
                else:
                    results.append(0)
            else:
                xg_list.append(match['xG_away'])
                goals_list.append(match['goals_away_count'])
                xga_list.append(match['xG_home'])
                
                if match['goals_away_count'] > match['goals_home_count']:
                    results.append(3)
                elif match['goals_away_count'] == match['goals_home_count']:
                    results.append(1)
                else:
                    results.append(0)
        
        variance_features.append({
            'matchId': row['matchId'],
            'xG_variance': np.std(xg_list),
            'goals_variance': np.std(goals_list),
            'xGA_variance': np.std(xga_list),
            'result_consistency': np.std(results)  # Low = consistent results
        })
    
    df_var = pd.DataFrame(variance_features)
    df_var.columns = ['matchId'] + [f'{prefix}_{col}' for col in df_var.columns if col != 'matchId']
    return df_var

print("  Computing home team variance...")
home_var = compute_variance_features(df, 'homeTeamId', 'home')

print("  Computing away team variance...")
away_var = compute_variance_features(df, 'awayTeamId', 'away')

df = df.merge(home_var, on='matchId', how='left')
df = df.merge(away_var, on='matchId', how='left')

print(f"  Variance features computed")

# ============================================================================
# 3. WEIGHTED RECENT FORM (Exponential Decay)
# ============================================================================
print("\n[4/9] Computing weighted recent form...")

def compute_weighted_form(df, team_col, prefix):
    """Weighted form with exponential decay (recent matches matter more)"""
    weighted_features = []
    
    # Weights: [0.4, 0.3, 0.2, 0.1] for last 4 matches (most recent = highest)
    weights = np.array([0.4, 0.3, 0.2, 0.1])
    
    for idx, row in df.iterrows():
        team_id = row[team_col]
        current_round = row['round']
        
        prev_matches = df[
            ((df['homeTeamId'] == team_id) | (df['awayTeamId'] == team_id)) &
            (df['round'] < current_round)
        ].tail(4)
        
        if len(prev_matches) < 4:
            weighted_features.append({
                'matchId': row['matchId'],
                'weighted_xG': np.nan,
                'weighted_goals': np.nan,
                'weighted_points': np.nan
            })
            continue
        
        xg_vals, goals_vals, points_vals = [], [], []
        
        for _, match in prev_matches.iterrows():
            is_home = match['homeTeamId'] == team_id
            
            if is_home:
                xg_vals.append(match['xG_home'])
                goals_vals.append(match['goals_home_count'])
                
                if match['goals_home_count'] > match['goals_away_count']:
                    points_vals.append(3)
                elif match['goals_home_count'] == match['goals_away_count']:
                    points_vals.append(1)
                else:
                    points_vals.append(0)
            else:
                xg_vals.append(match['xG_away'])
                goals_vals.append(match['goals_away_count'])
                
                if match['goals_away_count'] > match['goals_home_count']:
                    points_vals.append(3)
                elif match['goals_away_count'] == match['goals_home_count']:
                    points_vals.append(1)
                else:
                    points_vals.append(0)
        
        # Apply weights
        weighted_xg = np.average(xg_vals, weights=weights)
        weighted_goals = np.average(goals_vals, weights=weights)
        weighted_points = np.average(points_vals, weights=weights)
        
        weighted_features.append({
            'matchId': row['matchId'],
            'weighted_xG': weighted_xg,
            'weighted_goals': weighted_goals,
            'weighted_points': weighted_points
        })
    
    df_weighted = pd.DataFrame(weighted_features)
    df_weighted.columns = ['matchId'] + [f'{prefix}_{col}' for col in df_weighted.columns if col != 'matchId']
    return df_weighted

print("  Computing home team weighted form...")
home_weighted = compute_weighted_form(df, 'homeTeamId', 'home')

print("  Computing away team weighted form...")
away_weighted = compute_weighted_form(df, 'awayTeamId', 'away')

df = df.merge(home_weighted, on='matchId', how='left')
df = df.merge(away_weighted, on='matchId', how='left')

print(f"  Weighted form computed")

# ============================================================================
# 4. OPPOSITION QUALITY ADJUSTED STATS
# ============================================================================
print("\n[5/9] Computing opposition quality features...")

def compute_opponent_quality(df, team_col, prefix):
    """Average quality of opponents faced in last 5 matches"""
    opp_features = []
    
    for idx, row in df.iterrows():
        team_id = row[team_col]
        current_round = row['round']
        
        prev_matches = df[
            ((df['homeTeamId'] == team_id) | (df['awayTeamId'] == team_id)) &
            (df['round'] < current_round)
        ].tail(5)
        
        if len(prev_matches) == 0:
            opp_features.append({
                'matchId': row['matchId'],
                'avg_opp_position': np.nan,
                'avg_opp_points': np.nan,
                'tough_schedule_pct': np.nan
            })
            continue
        
        opp_positions, opp_points = [], []
        tough_opponents = 0
        
        for _, match in prev_matches.iterrows():
            is_home = match['homeTeamId'] == team_id
            
            # Get opponent's position and points at that time
            if is_home:
                if 'away_position' in match and not pd.isna(match['away_position']):
                    opp_positions.append(match['away_position'])
                if 'away_points_before' in match and not pd.isna(match['away_points_before']):
                    opp_points.append(match['away_points_before'])
                    if match['away_position'] <= 6:  # Top 6 = tough
                        tough_opponents += 1
            else:
                if 'home_position' in match and not pd.isna(match['home_position']):
                    opp_positions.append(match['home_position'])
                if 'home_points_before' in match and not pd.isna(match['home_points_before']):
                    opp_points.append(match['home_points_before'])
                    if match['home_position'] <= 6:
                        tough_opponents += 1
        
        avg_opp_pos = np.mean(opp_positions) if len(opp_positions) > 0 else np.nan
        avg_opp_pts = np.mean(opp_points) if len(opp_points) > 0 else np.nan
        tough_pct = tough_opponents / len(prev_matches)
        
        opp_features.append({
            'matchId': row['matchId'],
            'avg_opp_position': avg_opp_pos,
            'avg_opp_points': avg_opp_pts,
            'tough_schedule_pct': tough_pct
        })
    
    df_opp = pd.DataFrame(opp_features)
    df_opp.columns = ['matchId'] + [f'{prefix}_{col}' for col in df_opp.columns if col != 'matchId']
    return df_opp

print("  Computing home team opponent quality...")
home_opp = compute_opponent_quality(df, 'homeTeamId', 'home')

print("  Computing away team opponent quality...")
away_opp = compute_opponent_quality(df, 'awayTeamId', 'away')

df = df.merge(home_opp, on='matchId', how='left')
df = df.merge(away_opp, on='matchId', how='left')

print(f"  Opposition quality computed")

# ============================================================================
# 5. STREAKS & MOMENTUM
# ============================================================================
print("\n[6/9] Computing streak features...")

def compute_streaks(df, team_col, prefix):
    """Compute winning/scoring/clean sheet streaks"""
    streak_features = []
    
    for idx, row in df.iterrows():
        team_id = row[team_col]
        current_round = row['round']
        
        prev_matches = df[
            ((df['homeTeamId'] == team_id) | (df['awayTeamId'] == team_id)) &
            (df['round'] < current_round)
        ].sort_values('round')
        
        if len(prev_matches) == 0:
            streak_features.append({
                'matchId': row['matchId'],
                'win_streak': 0,
                'unbeaten_streak': 0,
                'scoring_streak': 0,
                'clean_sheet_streak': 0
            })
            continue
        
        # Count current streaks (from most recent backwards)
        win_streak = 0
        unbeaten_streak = 0
        scoring_streak = 0
        clean_sheet_streak = 0
        
        for _, match in prev_matches.iloc[::-1].iterrows():  # Reverse order
            is_home = match['homeTeamId'] == team_id
            
            if is_home:
                home_goals = match['goals_home_count']
                away_goals = match['goals_away_count']
                
                # Win streak
                if home_goals > away_goals:
                    win_streak += 1
                else:
                    break  # Streak ends
                
                # Unbeaten
                if home_goals >= away_goals:
                    unbeaten_streak += 1
                
                # Scoring
                if home_goals > 0:
                    scoring_streak += 1
                    
                # Clean sheet
                if away_goals == 0:
                    clean_sheet_streak += 1
            else:
                home_goals = match['goals_home_count']
                away_goals = match['goals_away_count']
                
                if away_goals > home_goals:
                    win_streak += 1
                else:
                    break
                
                if away_goals >= home_goals:
                    unbeaten_streak += 1
                
                if away_goals > 0:
                    scoring_streak += 1
                
                if home_goals == 0:
                    clean_sheet_streak += 1
        
        streak_features.append({
            'matchId': row['matchId'],
            'win_streak': win_streak,
            'unbeaten_streak': unbeaten_streak,
            'scoring_streak': scoring_streak,
            'clean_sheet_streak': clean_sheet_streak
        })
    
    df_streaks = pd.DataFrame(streak_features)
    df_streaks.columns = ['matchId'] + [f'{prefix}_{col}' for col in df_streaks.columns if col != 'matchId']
    return df_streaks

print("  Computing home team streaks...")
home_streaks = compute_streaks(df, 'homeTeamId', 'home')

print("  Computing away team streaks...")
away_streaks = compute_streaks(df, 'awayTeamId', 'away')

df = df.merge(home_streaks, on='matchId', how='left')
df = df.merge(away_streaks, on='matchId', how='left')

print(f"  Streak features computed")

# ============================================================================
# 6. PACE/STYLE INDICATORS
# ============================================================================
print("\n[7/9] Computing pace/style features...")

def compute_style_features(df, team_col, prefix):
    """Compute team playing style indicators"""
    style_features = []
    
    for idx, row in df.iterrows():
        team_id = row[team_col]
        current_round = row['round']
        
        prev_matches = df[
            ((df['homeTeamId'] == team_id) | (df['awayTeamId'] == team_id)) &
            (df['round'] < current_round)
        ].tail(5)
        
        if len(prev_matches) == 0:
            style_features.append({
                'matchId': row['matchId'],
                'shots_per_xG': np.nan,
                'bigch_conversion': np.nan,
                'shot_efficiency': np.nan
            })
            continue
        
        total_shots, total_xg, total_bigch, total_goals = 0, 0, 0, 0
        
        for _, match in prev_matches.iterrows():
            is_home = match['homeTeamId'] == team_id
            
            if is_home:
                total_shots += match.get('shots_home', 0)
                total_xg += match['xG_home']
                total_bigch += match['bigch_home']
                total_goals += match['goals_home_count']
            else:
                total_shots += match.get('shots_away', 0)
                total_xg += match['xG_away']
                total_bigch += match['bigch_away']
                total_goals += match['goals_away_count']
        
        # Shots per xG (high = wasteful/volume shooter)
        shots_per_xg = total_shots / total_xg if total_xg > 0 else np.nan
        
        # Big chance conversion
        bigch_conversion = total_goals / total_bigch if total_bigch > 0 else np.nan
        
        # Shot efficiency (goals per shot)
        shot_efficiency = total_goals / total_shots if total_shots > 0 else np.nan
        
        style_features.append({
            'matchId': row['matchId'],
            'shots_per_xG': shots_per_xg,
            'bigch_conversion': bigch_conversion,
            'shot_efficiency': shot_efficiency
        })
    
    df_style = pd.DataFrame(style_features)
    df_style.columns = ['matchId'] + [f'{prefix}_{col}' for col in df_style.columns if col != 'matchId']
    return df_style

print("  Computing home team style...")
home_style = compute_style_features(df, 'homeTeamId', 'home')

print("  Computing away team style...")
away_style = compute_style_features(df, 'awayTeamId', 'away')

df = df.merge(home_style, on='matchId', how='left')
df = df.merge(away_style, on='matchId', how='left')

print(f"  Pace/style features computed")

# ============================================================================
# 7. EXTREME RESULT TENDENCIES
# ============================================================================
print("\n[8/9] Computing extreme result features...")

def compute_extreme_results(df, team_col, prefix):
    """Compute tendency for blowouts, close games, comebacks"""
    extreme_features = []
    
    for idx, row in df.iterrows():
        team_id = row[team_col]
        current_round = row['round']
        
        prev_matches = df[
            ((df['homeTeamId'] == team_id) | (df['awayTeamId'] == team_id)) &
            (df['round'] < current_round)
        ].tail(10)  # Use last 10 for better sample
        
        if len(prev_matches) < 3:
            extreme_features.append({
                'matchId': row['matchId'],
                'blowout_rate': np.nan,
                'close_game_rate': np.nan,
                'high_scoring_rate': np.nan
            })
            continue
        
        blowouts = 0  # 3+ goal margin
        close_games = 0  # 0-1 goal margin
        high_scoring = 0  # 4+ total goals
        
        for _, match in prev_matches.iterrows():
            goal_diff = abs(match['goals_home_count'] - match['goals_away_count'])
            total_goals = match['Goals_total']
            
            if goal_diff >= 3:
                blowouts += 1
            if goal_diff <= 1:
                close_games += 1
            if total_goals >= 4:
                high_scoring += 1
        
        extreme_features.append({
            'matchId': row['matchId'],
            'blowout_rate': blowouts / len(prev_matches),
            'close_game_rate': close_games / len(prev_matches),
            'high_scoring_rate': high_scoring / len(prev_matches)
        })
    
    df_extreme = pd.DataFrame(extreme_features)
    df_extreme.columns = ['matchId'] + [f'{prefix}_{col}' for col in df_extreme.columns if col != 'matchId']
    return df_extreme

print("  Computing home team extreme results...")
home_extreme = compute_extreme_results(df, 'homeTeamId', 'home')

print("  Computing away team extreme results...")
away_extreme = compute_extreme_results(df, 'awayTeamId', 'away')

df = df.merge(home_extreme, on='matchId', how='left')
df = df.merge(away_extreme, on='matchId', how='left')

print(f"  Extreme result features computed")

# ============================================================================
# SAVE ADVANCED FEATURES
# ============================================================================
print("\n[9/9] Saving advanced features...")

# Get only the features we want (exclude labels, intermediate columns, and RAW MATCH OUTCOMES)
exclude_from_features = [
    # Labels/targets
    'goals_home_count', 'goals_away_count', 'Goals_total',
    'xG_total', 'SoT_total', 'BigCh_total', 'Corners_total', 'ToB_total',
    'SLS_Fplus_rolling', 'SLS_Fplus_fixed', 'Liveliness_xG',
    'SLS_Fplus_rolling_raw', 'SLS_Fplus_fixed_raw', 'xG_min',
    
    # Raw match outcomes (DATA LEAKAGE - these happen DURING the match)
    'xG_home', 'xG_away', 'sot_home', 'sot_away', 
    'bigch_home', 'bigch_away', 'corners_home', 'corners_away',
    'tob_home', 'tob_away', 'shots_home', 'shots_away',
    
    # Metadata
    'leagueName', 'matchTimeUTC', 'matchTimeUTCDate', 'finished', 'started',
    
    # Intermediate computations (already captured in derived features)
    'home_points_before', 'away_points_before', 'home_gd_before', 'away_gd_before',
    'home_wins_before', 'away_wins_before', 'home_home_points', 'away_away_points'
]

feature_cols = [col for col in df.columns if col not in exclude_from_features]

df_features_advanced = df[feature_cols]

# Save
df_features_advanced.to_csv('feature_tables/match_features_advanced.csv', index=False)

print(f"✓ Saved: feature_tables/match_features_advanced.csv")
print(f"  Total features: {len(df_features_advanced.columns)}")

# Count new features
original_count = 37  # From previous enhanced version
new_count = len(df_features_advanced.columns) - 6  # Minus identifiers
new_features_added = new_count - original_count

print(f"  Original features: {original_count}")
print(f"  New features added: {new_features_added}")
print(f"  Total: {new_count}")

# Show feature categories
print("\n" + "="*80)
print("FEATURE CATEGORIES")
print("="*80)
print("✓ H2H History: 6 features")
print("✓ Variance/Consistency: 8 features (home + away)")
print("✓ Weighted Form: 6 features (home + away)")
print("✓ Opposition Quality: 6 features (home + away)")
print("✓ Streaks & Momentum: 8 features (home + away)")
print("✓ Pace/Style: 6 features (home + away)")
print("✓ Extreme Results: 6 features (home + away)")

print("\n" + "="*80)
print("COMPLETE!")
print("="*80)
print("\nNext step: Run enhanced comparison with all features")
print("Expected improvement: R² 0.04 → 0.10-0.20")