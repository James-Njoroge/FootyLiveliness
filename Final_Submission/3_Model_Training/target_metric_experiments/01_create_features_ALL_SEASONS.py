"""
Generate Features for All Seasons (2022/23, 2023/24, 2024/25)

Creates rolling 5-match pre-match features for each team across all seasons.
Adds season indicator and contextual features.
"""

import pandas as pd
import numpy as np
import json
import os
import glob
from collections import defaultdict

print("="*80)
print("GENERATING FEATURES FOR ALL SEASONS")
print("="*80)

# ============================================================================
# STEP 1: LOAD AND PROCESS ALL SEASONS
# ============================================================================
print("\n[1/5] Loading data from all seasons...")

seasons = [
    ('2022-23', '../data/22-23_PL_Data_raw'),
    ('2023-24', '../data/23-24_PL_Data_raw'),
    ('2024-25', '../data/24-25_PL_Data_raw')
]

all_matches = []

for season_name, data_dir in seasons:
    print(f"\n  Processing {season_name}...")
    
    if not os.path.exists(data_dir):
        print(f"    Warning: {data_dir} not found, skipping...")
        continue
    
    season_matches = 0
    
    for round_num in range(38):
        round_dir = os.path.join(data_dir, f'round_{round_num}')
        
        if not os.path.exists(round_dir):
            continue
        
        json_files = glob.glob(os.path.join(round_dir, '*_matchDetails_*.json'))
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    match_data = json.load(f)
                
                general = match_data['general']
                header = match_data['header']
                stats_all = match_data['content']['stats']['Periods']['All']['stats']
                
                # Helper function
                def get_stat(stats_list, key):
                    for category in stats_list:
                        for stat in category['stats']:
                            if stat['key'] == key:
                                return stat['stats']
                    return [None, None]
                
                # Extract stats
                xg = get_stat(stats_all, 'expected_goals')
                sot = get_stat(stats_all, 'ShotsOnTarget')
                bigch = get_stat(stats_all, 'big_chance')
                corners = get_stat(stats_all, 'corners')
                shots = get_stat(stats_all, 'total_shots')
                
                match = {
                    'season': season_name,
                    'round': round_num,
                    'homeTeamName': general['homeTeam']['name'],
                    'awayTeamName': general['awayTeam']['name'],
                    'homeTeamId': general['homeTeam']['id'],
                    'awayTeamId': general['awayTeam']['id'],
                    'goals_home': header['teams'][0]['score'],
                    'goals_away': header['teams'][1]['score'],
                    'xG_home': float(xg[0]) if xg[0] is not None else 0.0,
                    'xG_away': float(xg[1]) if xg[1] is not None else 0.0,
                    'shots_home': int(shots[0]) if shots[0] is not None else 0,
                    'shots_away': int(shots[1]) if shots[1] is not None else 0,
                    'sot_home': int(sot[0]) if sot[0] is not None else 0,
                    'sot_away': int(sot[1]) if sot[1] is not None else 0,
                    'bigch_home': int(bigch[0]) if bigch[0] is not None else 0,
                    'bigch_away': int(bigch[1]) if bigch[1] is not None else 0,
                    'corners_home': int(corners[0]) if corners[0] is not None else 0,
                    'corners_away': int(corners[1]) if corners[1] is not None else 0,
                }
                
                all_matches.append(match)
                season_matches += 1
                
            except Exception as e:
                continue
    
    print(f"    ✓ Processed {season_matches} matches from {season_name}")

df = pd.DataFrame(all_matches)
df = df.sort_values(['season', 'round']).reset_index(drop=True)

print(f"\n  Total matches: {len(df)}")
print(f"  Seasons: {df['season'].unique().tolist()}")

# ============================================================================
# STEP 2: CREATE ROLLING FEATURES (WITHIN EACH SEASON)
# ============================================================================
print("\n[2/5] Creating rolling 5-match pre-match features...")

# Stats to compute rolling averages for
rolling_stats = ['xG_home', 'xG_away', 'shots_home', 'shots_away', 
                 'sot_home', 'sot_away', 'bigch_home', 'bigch_away', 
                 'corners_home', 'corners_away']

# Initialize feature columns
for stat in rolling_stats:
    df[f'{stat}_rolling_home'] = np.nan
    df[f'{stat}_rolling_away'] = np.nan

# Track team histories PER SEASON
for season in df['season'].unique():
    season_df = df[df['season'] == season].copy()
    team_history = {}
    
    for idx in season_df.index:
        row = df.loc[idx]
        home_id = row['homeTeamId']
        away_id = row['awayTeamId']
        
        # Initialize team history if needed
        if home_id not in team_history:
            team_history[home_id] = {stat: [] for stat in rolling_stats}
        if away_id not in team_history:
            team_history[away_id] = {stat: [] for stat in rolling_stats}
        
        # Compute rolling averages from PAST matches only
        for stat in rolling_stats:
            # Home team's rolling average
            if len(team_history[home_id][stat]) > 0:
                df.at[idx, f'{stat}_rolling_home'] = np.mean(team_history[home_id][stat][-5:])
            else:
                df.at[idx, f'{stat}_rolling_home'] = 0.0
            
            # Away team's rolling average
            if len(team_history[away_id][stat]) > 0:
                df.at[idx, f'{stat}_rolling_away'] = np.mean(team_history[away_id][stat][-5:])
            else:
                df.at[idx, f'{stat}_rolling_away'] = 0.0
        
        # Update team history AFTER computing features
        team_history[home_id]['xG_home'].append(row['xG_home'])
        team_history[home_id]['xG_away'].append(row['xG_away'])
        team_history[home_id]['shots_home'].append(row['shots_home'])
        team_history[home_id]['shots_away'].append(row['shots_away'])
        team_history[home_id]['sot_home'].append(row['sot_home'])
        team_history[home_id]['sot_away'].append(row['sot_away'])
        team_history[home_id]['bigch_home'].append(row['bigch_home'])
        team_history[home_id]['bigch_away'].append(row['bigch_away'])
        team_history[home_id]['corners_home'].append(row['corners_home'])
        team_history[home_id]['corners_away'].append(row['corners_away'])
        
        team_history[away_id]['xG_home'].append(row['xG_away'])
        team_history[away_id]['xG_away'].append(row['xG_home'])
        team_history[away_id]['shots_home'].append(row['shots_away'])
        team_history[away_id]['shots_away'].append(row['shots_home'])
        team_history[away_id]['sot_home'].append(row['sot_away'])
        team_history[away_id]['sot_away'].append(row['sot_home'])
        team_history[away_id]['bigch_home'].append(row['bigch_away'])
        team_history[away_id]['bigch_away'].append(row['bigch_home'])
        team_history[away_id]['corners_home'].append(row['corners_away'])
        team_history[away_id]['corners_away'].append(row['corners_home'])

print(f"  Created {len([c for c in df.columns if 'rolling' in c])} rolling features")

# ============================================================================
# STEP 3: CREATE AGGREGATE FEATURES
# ============================================================================
print("\n[3/5] Creating aggregate features...")

# Combined team strength
df['xG_combined'] = df['xG_home_rolling_home'] + df['xG_away_rolling_away']
df['shots_combined'] = df['shots_home_rolling_home'] + df['shots_away_rolling_away']
df['sot_combined'] = df['sot_home_rolling_home'] + df['sot_away_rolling_away']
df['bigch_combined'] = df['bigch_home_rolling_home'] + df['bigch_away_rolling_away']
df['corners_combined'] = df['corners_home_rolling_home'] + df['corners_away_rolling_away']

# Difference features (home advantage)
df['xG_diff'] = df['xG_home_rolling_home'] - df['xG_away_rolling_away']
df['shots_diff'] = df['shots_home_rolling_home'] - df['shots_away_rolling_away']

# Season encoding
season_map = {'2022-23': 0, '2023-24': 1, '2024-25': 2}
df['season_encoded'] = df['season'].map(season_map)

print(f"  Total features: {len([c for c in df.columns if 'rolling' in c or 'combined' in c or 'diff' in c])}")

# ============================================================================
# STEP 4: CREATE TARGET METRIC (SIMPLE XG - THE WINNER)
# ============================================================================
print("\n[4/5] Creating target metric (Simple xG)...")

df['xG_total'] = df['xG_home'] + df['xG_away']
df['xG_min'] = df[['xG_home', 'xG_away']].min(axis=1)
df['target_simple_xg'] = df['xG_total'] + df['xG_min']

print(f"  Target metric: Simple xG")
print(f"  Mean: {df['target_simple_xg'].mean():.2f}")
print(f"  Std: {df['target_simple_xg'].std():.2f}")

# ============================================================================
# STEP 5: SAVE RESULTS
# ============================================================================
print("\n[5/5] Saving results...")

# Remove early matches with insufficient history
df_clean = df[df['round'] >= 5].copy()

output_path = 'all_seasons_features.csv'
df_clean.to_csv(output_path, index=False)

print(f"✓ Saved to: {output_path}")
print(f"  Total matches: {len(df_clean)}")
print(f"  Matches per season:")
for season in df_clean['season'].unique():
    count = len(df_clean[df_clean['season'] == season])
    print(f"    {season}: {count}")

print("\n" + "="*80)
print("FEATURES GENERATED FOR ALL SEASONS!")
print("="*80)
print(f"\nNext: Run 02_train_ALL_SEASONS.py to train models")
print("="*80)
