"""
Generate Labels Table from Raw FotMob JSON Files

Reads from: data/24-25_PL_Data_raw/round_0/ through round_37/
Creates: tables/all_rounds.csv

Generates three liveliness metrics:
1. SLS_Fplus_rolling: Rolling z-scores (rounds 2+)
2. SLS_Fplus_fixed: Fixed z-scores (entire season)
3. Liveliness_xG: xG_total + min(xG_home, xG_away)
"""

import json
import pandas as pd
import numpy as np
import os
import glob

print("="*80)
print("CREATING LABELS TABLE FROM RAW JSON FILES")
print("="*80)

# ============================================================================
# STEP 1: SCAN AND LOAD ALL JSON FILES
# ============================================================================
print("\n[1/5] Scanning raw JSON files...")

data_dir = 'data/24-25_PL_Data_raw/24-25_PL_Data_raw'
all_matches = []

for round_num in range(38):  # rounds 0-37
    round_dir = os.path.join(data_dir, f'round_{round_num}')
    
    if not os.path.exists(round_dir):
        print(f"  Warning: {round_dir} not found, skipping...")
        continue
    
    # Get all JSON files in this round
    json_files = glob.glob(os.path.join(round_dir, '*_matchDetails_*.json'))
    
    print(f"  Round {round_num}: Found {len(json_files)} matches")
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                match_data = json.load(f)
            
            # Extract match info
            general = match_data['general']
            header = match_data['header']
            stats_all = match_data['content']['stats']['Periods']['All']['stats']
            
            # Helper function to find stat by key
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
            tob = get_stat(stats_all, 'touches_opp_box')
            shots = get_stat(stats_all, 'total_shots')
            
            # Build match record
            match = {
                'round': int(general['matchRound']) - 1,  # Convert to 0-indexed
                'matchId': general['matchId'],
                'homeTeamName': general['homeTeam']['name'],
                'awayTeamName': general['awayTeam']['name'],
                'homeTeamId': general['homeTeam']['id'],
                'awayTeamId': general['awayTeam']['id'],
                'leagueName': general['leagueName'],
                'matchTimeUTC': general['matchTimeUTC'],
                'matchTimeUTCDate': general['matchTimeUTCDate'],
                'finished': general['finished'],
                'started': general['started'],
                
                # Scores
                'goals_home_count': header['teams'][0]['score'],
                'goals_away_count': header['teams'][1]['score'],
                
                # Stats (home, away)
                'xG_home': float(xg[0]) if xg[0] is not None else 0.0,
                'xG_away': float(xg[1]) if xg[1] is not None else 0.0,
                'sot_home': int(sot[0]) if sot[0] is not None else 0,
                'sot_away': int(sot[1]) if sot[1] is not None else 0,
                'bigch_home': int(bigch[0]) if bigch[0] is not None else 0,
                'bigch_away': int(bigch[1]) if bigch[1] is not None else 0,
                'corners_home': int(corners[0]) if corners[0] is not None else 0,
                'corners_away': int(corners[1]) if corners[1] is not None else 0,
                'tob_home': int(tob[0]) if tob[0] is not None else 0,
                'tob_away': int(tob[1]) if tob[1] is not None else 0,
                'shots_home': int(shots[0]) if shots[0] is not None else 0,
                'shots_away': int(shots[1]) if shots[1] is not None else 0,
            }
            
            all_matches.append(match)
            
        except Exception as e:
            print(f"    Error processing {json_file}: {e}")
            continue

print(f"\nTotal matches loaded: {len(all_matches)}")

# Convert to DataFrame
df = pd.DataFrame(all_matches)
df = df.sort_values('round').reset_index(drop=True)

print(f"Matches by round: {df['round'].min()} to {df['round'].max()}")

# ============================================================================
# STEP 2: COMPUTE AGGREGATED STATS
# ============================================================================
print("\n[2/5] Computing aggregated match stats...")

df['xG_total'] = df['xG_home'] + df['xG_away']
df['SoT_total'] = df['sot_home'] + df['sot_away']
df['BigCh_total'] = df['bigch_home'] + df['bigch_away']
df['Corners_total'] = df['corners_home'] + df['corners_away']
df['ToB_total'] = df['tob_home'] + df['tob_away']
df['Goals_total'] = df['goals_home_count'] + df['goals_away_count']

print(f"  xG_total: mean={df['xG_total'].mean():.2f}, std={df['xG_total'].std():.2f}")
print(f"  SoT_total: mean={df['SoT_total'].mean():.2f}, std={df['SoT_total'].std():.2f}")

# ============================================================================
# STEP 3: SLS-F+ WITH ROLLING Z-SCORES
# ============================================================================
print("\n[3/5] Computing SLS-F+ with rolling z-scores...")

WEIGHTS = {
    'xG': 0.50,
    'SoT': 0.20,
    'BigCh': 0.10,
    'Corners': 0.10,
    'ToB': 0.10
}

sls_rolling_raw = []

for idx, row in df.iterrows():
    current_round = row['round']
    
    if current_round < 2:
        sls_rolling_raw.append(np.nan)
        continue
    
    hist_df = df[df['round'] < current_round].copy()
    
    if len(hist_df) == 0:
        sls_rolling_raw.append(np.nan)
        continue
    
    means = {
        'xG': hist_df['xG_total'].mean(),
        'SoT': hist_df['SoT_total'].mean(),
        'BigCh': hist_df['BigCh_total'].mean(),
        'Corners': hist_df['Corners_total'].mean(),
        'ToB': hist_df['ToB_total'].mean()
    }
    
    stds = {
        'xG': hist_df['xG_total'].std(),
        'SoT': hist_df['SoT_total'].std(),
        'BigCh': hist_df['BigCh_total'].std(),
        'Corners': hist_df['Corners_total'].std(),
        'ToB': hist_df['ToB_total'].std()
    }
    
    current_stats = {
        'xG': row['xG_total'],
        'SoT': row['SoT_total'],
        'BigCh': row['BigCh_total'],
        'Corners': row['Corners_total'],
        'ToB': row['ToB_total']
    }
    
    z_scores = {}
    for feature in ['xG', 'SoT', 'BigCh', 'Corners', 'ToB']:
        if stds[feature] > 0:
            z_scores[feature] = (current_stats[feature] - means[feature]) / stds[feature]
        else:
            z_scores[feature] = 0
    
    sls_raw = sum(WEIGHTS[feat] * z_scores[feat] for feat in WEIGHTS.keys())
    sls_rolling_raw.append(sls_raw)

df['SLS_Fplus_rolling_raw'] = sls_rolling_raw

valid_scores = df['SLS_Fplus_rolling_raw'].dropna()
mean_raw = valid_scores.mean()
std_raw = valid_scores.std()

df['SLS_Fplus_rolling'] = df['SLS_Fplus_rolling_raw'].apply(
    lambda x: 50 + 15 * (x - mean_raw) / std_raw if not pd.isna(x) else np.nan
)
df['SLS_Fplus_rolling'] = df['SLS_Fplus_rolling'].clip(0, 100)

print(f"  Computed for {df['SLS_Fplus_rolling'].notna().sum()} matches")

# ============================================================================
# STEP 4: SLS-F+ WITH FIXED Z-SCORES
# ============================================================================
print("\n[4/5] Computing SLS-F+ with fixed z-scores...")

season_means = {
    'xG': df['xG_total'].mean(),
    'SoT': df['SoT_total'].mean(),
    'BigCh': df['BigCh_total'].mean(),
    'Corners': df['Corners_total'].mean(),
    'ToB': df['ToB_total'].mean()
}

season_stds = {
    'xG': df['xG_total'].std(),
    'SoT': df['SoT_total'].std(),
    'BigCh': df['BigCh_total'].std(),
    'Corners': df['Corners_total'].std(),
    'ToB': df['ToB_total'].std()
}

sls_fixed_raw = []

for idx, row in df.iterrows():
    current_stats = {
        'xG': row['xG_total'],
        'SoT': row['SoT_total'],
        'BigCh': row['BigCh_total'],
        'Corners': row['Corners_total'],
        'ToB': row['ToB_total']
    }
    
    z_scores = {}
    for feature in ['xG', 'SoT', 'BigCh', 'Corners', 'ToB']:
        if season_stds[feature] > 0:
            z_scores[feature] = (current_stats[feature] - season_means[feature]) / season_stds[feature]
        else:
            z_scores[feature] = 0
    
    sls_raw = sum(WEIGHTS[feat] * z_scores[feat] for feat in WEIGHTS.keys())
    sls_fixed_raw.append(sls_raw)

df['SLS_Fplus_fixed_raw'] = sls_fixed_raw

mean_fixed = np.mean(sls_fixed_raw)
std_fixed = np.std(sls_fixed_raw)

df['SLS_Fplus_fixed'] = df['SLS_Fplus_fixed_raw'].apply(
    lambda x: 50 + 15 * (x - mean_fixed) / std_fixed
)
df['SLS_Fplus_fixed'] = df['SLS_Fplus_fixed'].clip(0, 100)

print(f"  Computed for {len(df)} matches")

# ============================================================================
# STEP 5: XG-BASED LIVELINESS
# ============================================================================
print("\n[4/5] Computing xG-based liveliness...")

df['xG_min'] = df[['xG_home', 'xG_away']].min(axis=1)
df['Liveliness_xG'] = df['xG_total'] + df['xG_min']

print(f"  Mean: {df['Liveliness_xG'].mean():.2f}, Std: {df['Liveliness_xG'].std():.2f}")

# ============================================================================
# SAVE
# ============================================================================
print("\n[5/5] Saving to tables/all_rounds.csv...")

os.makedirs('tables', exist_ok=True)

output_cols = [
    'round', 'matchId', 'homeTeamName', 'awayTeamName', 'homeTeamId', 'awayTeamId',
    'leagueName', 'matchTimeUTC', 'matchTimeUTCDate', 'finished', 'started',
    'goals_home_count', 'goals_away_count', 'Goals_total',
    'xG_home', 'xG_away', 'sot_home', 'sot_away', 'bigch_home', 'bigch_away',
    'corners_home', 'corners_away', 'tob_home', 'tob_away', 'shots_home', 'shots_away',
    'xG_total', 'SoT_total', 'BigCh_total', 'Corners_total', 'ToB_total',
    'SLS_Fplus_rolling', 'SLS_Fplus_fixed', 'Liveliness_xG',
    'SLS_Fplus_rolling_raw', 'SLS_Fplus_fixed_raw', 'xG_min'
]

df[output_cols].to_csv('tables/all_rounds.csv', index=False)

print(f"✓ Saved {len(df)} matches")

print("\n" + "="*80)
print("COMPLETE!")
print("="*80)
print(f"Generated: tables/all_rounds.csv ({len(df)} matches)")