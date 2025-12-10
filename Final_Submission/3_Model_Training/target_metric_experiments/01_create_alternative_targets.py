"""
Create Alternative Target Metrics for Liveliness Prediction

Generates 7 different target metrics with varying complexity:
1. Simple xG (current baseline)
2. Shot Volume + Quality
3. Chances-Focused (many opportunities)
4. End-to-End Attacking (competitiveness)
5. Transitions + Intensity (cards + tempo)
6. Comprehensive (all factors)
7. Minimal (just shots and xG)

Reads from: data/24-25_PL_Data_raw/
Creates: target_metric_experiments/targets_comparison.csv
"""

import json
import pandas as pd
import numpy as np
import os
import glob

print("="*80)
print("CREATING ALTERNATIVE TARGET METRICS")
print("="*80)

# ============================================================================
# STEP 1: LOAD EXISTING LABELS
# ============================================================================
print("\n[1/4] Loading existing labels...")

labels_df = pd.read_csv('../data/tables/all_rounds.csv')

# Rename columns to match expected format
labels_df = labels_df.rename(columns={
    'Round': 'round',
    'HomeTeam': 'homeTeamName',
    'AwayTeam': 'awayTeamName',
    'xG_home': 'xG_home',
    'xG_away': 'xG_away',
    'Shots_home': 'shots_home',
    'Shots_away': 'shots_away',
    'ShotsOnTarget_home': 'sot_home',
    'ShotsOnTarget_away': 'sot_away',
    'BigChances_home': 'bigch_home',
    'BigChances_away': 'bigch_away',
    'Corners_home': 'corners_home',
    'Corners_away': 'corners_away'
})

# Create matchId from round and teams
labels_df['matchId'] = labels_df['round'].astype(str) + '_' + labels_df['homeTeamName'] + '_vs_' + labels_df['awayTeamName']

print(f"Loaded {len(labels_df)} matches")
print(f"Columns: {labels_df.columns.tolist()}")

# ============================================================================
# STEP 2: EXTRACT CARDS DATA FROM JSON
# ============================================================================
print("\n[2/4] Extracting cards data from raw JSON files...")

data_dir = '../data/24-25_PL_Data_raw'
cards_data = []

for round_num in range(38):
    round_dir = os.path.join(data_dir, f'round_{round_num}')
    
    if not os.path.exists(round_dir):
        print(f"  Warning: {round_dir} not found, skipping...")
        continue
    
    json_files = glob.glob(os.path.join(round_dir, '*_matchDetails_*.json'))
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                match_data = json.load(f)
            
            match_id = match_data['general']['matchId']
            
            # Extract cards from header.events
            home_yellow = 0
            home_red = 0
            away_yellow = 0
            away_red = 0
            
            if 'events' in match_data['header']:
                # Home team cards
                if 'homeTeam' in match_data['header']['events']:
                    for event in match_data['header']['events']['homeTeam']:
                        if event.get('type') == 'Card':
                            if event.get('card') == 'Yellow':
                                home_yellow += 1
                            elif event.get('card') == 'Red':
                                home_red += 1
                
                # Away team cards
                if 'awayTeam' in match_data['header']['events']:
                    for event in match_data['header']['events']['awayTeam']:
                        if event.get('type') == 'Card':
                            if event.get('card') == 'Yellow':
                                away_yellow += 1
                            elif event.get('card') == 'Red':
                                away_red += 1
            
            cards_data.append({
                'matchId': match_id,
                'yellow_cards_home': home_yellow,
                'yellow_cards_away': away_yellow,
                'red_cards_home': home_red,
                'red_cards_away': away_red,
                'total_cards': home_yellow + away_yellow + home_red + away_red,
                'total_yellow': home_yellow + away_yellow,
                'total_red': home_red + away_red
            })
            
        except Exception as e:
            print(f"  Error processing {json_file}: {e}")
            continue

cards_df = pd.DataFrame(cards_data)
print(f"  Extracted cards for {len(cards_df)} matches")
print(f"  Average cards per match: {cards_df['total_cards'].mean():.2f}")

# Merge cards data
df = pd.merge(labels_df, cards_df, on='matchId', how='left')

# Fill missing card values with 0
card_cols = ['yellow_cards_home', 'yellow_cards_away', 'red_cards_home', 'red_cards_away', 'total_cards']
for col in card_cols:
    if col in df.columns:
        df[col] = df[col].fillna(0)
df['total_cards'] = df['total_cards'].fillna(0)
df['total_yellow'] = df['total_yellow'].fillna(0)
df['total_red'] = df['total_red'].fillna(0)

# ============================================================================
# STEP 3: CREATE ALTERNATIVE TARGET METRICS
# ============================================================================
print("\n[3/4] Creating alternative target metrics...")

# Calculate totals for convenience
df['xG_total'] = df['xG_home'] + df['xG_away']
df['xG_min'] = df[['xG_home', 'xG_away']].min(axis=1)
df['shots_total'] = df['shots_home'] + df['shots_away']
df['shots_min'] = df[['shots_home', 'shots_away']].min(axis=1)
df['sot_total'] = df['sot_home'] + df['sot_away']
df['bigch_total'] = df['bigch_home'] + df['bigch_away']
df['corners_total'] = df['corners_home'] + df['corners_away']

# ============================================================================
# TARGET METRIC 1: Simple xG (Current Baseline)
# ============================================================================
df['target_1_simple_xg'] = df['xG_total'] + df['xG_min']

# ============================================================================
# TARGET METRIC 2: Shot Volume + Quality
# ============================================================================
df['target_2_shot_quality'] = (
    0.5 * df['xG_total'] + 
    0.3 * df['shots_total'] + 
    0.2 * df['sot_total']
)

# ============================================================================
# TARGET METRIC 3: Chances-Focused (Low xG but many opportunities)
# ============================================================================
df['target_3_chances'] = (
    0.4 * df['shots_total'] + 
    0.3 * df['bigch_total'] + 
    0.3 * df['xG_total']
)

# ============================================================================
# TARGET METRIC 4: End-to-End Attacking (Competitiveness)
# ============================================================================
df['target_4_end_to_end'] = (
    df['xG_total'] + 
    2 * df['xG_min'] + 
    df['shots_min']
)

# ============================================================================
# TARGET METRIC 5: Transitions + Intensity (Cards + Tempo)
# ============================================================================
df['target_5_intensity'] = (
    0.3 * df['xG_total'] + 
    0.2 * df['shots_total'] + 
    0.2 * df['corners_total'] + 
    0.15 * df['total_cards'] + 
    0.15 * df['bigch_total']
)

# ============================================================================
# TARGET METRIC 6: Comprehensive (All factors)
# ============================================================================
df['target_6_comprehensive'] = (
    0.25 * df['xG_total'] + 
    0.20 * df['shots_total'] + 
    0.15 * df['sot_total'] + 
    0.15 * df['bigch_total'] + 
    0.15 * df['corners_total'] + 
    0.10 * df['total_cards']
)

# ============================================================================
# TARGET METRIC 7: Minimal (Just shots and xG)
# ============================================================================
df['target_7_minimal'] = (
    0.6 * df['xG_total'] + 
    0.4 * df['shots_total']
)

# ============================================================================
# STEP 4: SAVE RESULTS
# ============================================================================
print("\n[4/4] Saving results...")

# Select relevant columns (only those that exist)
output_cols = [
    'round', 'matchId', 'homeTeamName', 'awayTeamName',
    'xG_home', 'xG_away', 'xG_total', 'xG_min',
    'shots_home', 'shots_away', 'shots_total',
    'sot_home', 'sot_away', 'sot_total',
    'bigch_home', 'bigch_away', 'bigch_total',
    'corners_home', 'corners_away', 'corners_total',
    'yellow_cards_home', 'yellow_cards_away', 
    'red_cards_home', 'red_cards_away', 'total_cards',
    'target_1_simple_xg',
    'target_2_shot_quality',
    'target_3_chances',
    'target_4_end_to_end',
    'target_5_intensity',
    'target_6_comprehensive',
    'target_7_minimal'
]

# Only include columns that actually exist in the dataframe
output_cols = [col for col in output_cols if col in df.columns]
output_df = df[output_cols].copy()
output_path = 'targets_comparison.csv'
output_df.to_csv(output_path, index=False)

print(f"✓ Saved to: {output_path}")
print(f"  Total matches: {len(output_df)}")
print(f"  Target metrics created: 7")

# ============================================================================
# SUMMARY STATISTICS
# ============================================================================
print("\n" + "="*80)
print("SUMMARY STATISTICS FOR EACH TARGET METRIC")
print("="*80)

target_cols = [col for col in output_df.columns if col.startswith('target_')]

summary_stats = []
for target in target_cols:
    stats = {
        'Metric': target.replace('target_', '').replace('_', ' ').title(),
        'Mean': output_df[target].mean(),
        'Std': output_df[target].std(),
        'Min': output_df[target].min(),
        'Max': output_df[target].max(),
        'Range': output_df[target].max() - output_df[target].min(),
        'CV': output_df[target].std() / output_df[target].mean()  # Coefficient of variation
    }
    summary_stats.append(stats)

summary_df = pd.DataFrame(summary_stats)
print(summary_df.to_string(index=False))

# Save summary
summary_df.to_csv('targets_summary_stats.csv', index=False)
print(f"\n✓ Summary statistics saved to: targets_summary_stats.csv")

print("\n" + "="*80)
print("DONE! Ready for model comparison.")
print("="*80)
