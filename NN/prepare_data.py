"""
Prepare Data for Neural Network Training

Loads current baseline data (37 features, 2024/25 season) and prepares PyTorch tensors.

Input:
  - tables/all_rounds.csv
  - feature_tables/match_features_enhanced.csv

Output:
  - data_prepared_nn.pt (PyTorch tensors + metadata)
  
Train/Val/Test Split (Chronological):
  - Train: Rounds 5-28 (230 matches)
  - Val: Rounds 29-33 (50 matches)
  - Test: Rounds 34-37 (40 matches)
"""

import pandas as pd
import numpy as np
import torch
from sklearn.preprocessing import StandardScaler
from torch.utils.data import TensorDataset, DataLoader

print("="*80)
print("PREPARING DATA FOR NEURAL NETWORK")
print("="*80)

# ============================================================================
# STEP 1: LOAD DATA
# ============================================================================
print("\n[1/6] Loading labels and features...")

labels_df = pd.read_csv('../tables/all_rounds.csv')
features_df = pd.read_csv('../feature_tables/match_features_enhanced.csv')

# Merge
df = pd.merge(labels_df, features_df,
              on=['round', 'matchId', 'homeTeamName', 'awayTeamName', 
                  'homeTeamId', 'awayTeamId'],
              how='inner')

print(f"  Total matches: {len(df)}")

# ============================================================================
# STEP 2: FILTER TO VALID MATCHES
# ============================================================================
print("\n[2/6] Filtering to matches with valid features...")

# Filter to matches where we have rolling features (round >= 5)
df_model = df[df['TempoSum'].notna()].copy()

print(f"  Matches with valid features: {len(df_model)}")

# ============================================================================
# STEP 3: DEFINE TRAIN/VAL/TEST SPLITS (CHRONOLOGICAL)
# ============================================================================
print("\n[3/6] Creating chronological train/val/test splits...")

train_df = df_model[(df_model['round'] >= 5) & (df_model['round'] <= 28)].copy()
val_df = df_model[(df_model['round'] >= 29) & (df_model['round'] <= 33)].copy()
test_df = df_model[(df_model['round'] >= 34) & (df_model['round'] <= 37)].copy()

print(f"  Train: {len(train_df)} matches (rounds 5-28)")
print(f"  Val:   {len(val_df)} matches (rounds 29-33)")
print(f"  Test:  {len(test_df)} matches (rounds 34-37)")

# ============================================================================
# STEP 4: DEFINE FEATURES AND TARGET
# ============================================================================
print("\n[4/6] Selecting features and target...")

# All 37 features from enhanced baseline
feature_cols = [
    # Rolling 5-match form (home)
    'home_xG_att_90', 'home_SoT_att_90', 'home_BigCh_att_90', 
    'home_Corn_att_90', 'home_ToB_att_90', 'home_xGA_def_90', 
    'home_SoT_agst_90', 'home_BigCh_agst_90',
    
    # Rolling 5-match form (away)
    'away_xG_att_90', 'away_SoT_att_90', 'away_BigCh_att_90',
    'away_Corn_att_90', 'away_ToB_att_90', 'away_xGA_def_90',
    'away_SoT_agst_90', 'away_BigCh_agst_90',
    
    # Composite features
    'TempoSum', 'SoTSum', 'AttackVsDefense', 'xG_att_sum', 
    'xG_att_min', 'BigCh_sum',
    
    # League context
    'home_position', 'away_position', 'position_diff',
    'points_diff', 'gd_diff',
    
    # Form trajectory
    'home_last3_points', 'home_last3_goals', 'home_form_trend',
    'away_last3_points', 'away_last3_goals', 'away_form_trend',
    
    # Contextual indicators
    'home_strength_ratio', 'away_strength_ratio',
    'both_top6', 'both_bottom6', 'close_positions'
]

# Target: xG-based liveliness (best performing metric from baseline)
target = 'Liveliness_xG'

print(f"  Features: {len(feature_cols)}")
print(f"  Target: {target}")

# ============================================================================
# STEP 5: PREPARE NUMPY ARRAYS
# ============================================================================
print("\n[5/6] Extracting numpy arrays...")

X_train = train_df[feature_cols].values
y_train = train_df[target].values

X_val = val_df[feature_cols].values
y_val = val_df[target].values

X_test = test_df[feature_cols].values
y_test = test_df[target].values

print(f"  Train shape: X={X_train.shape}, y={y_train.shape}")
print(f"  Val shape:   X={X_val.shape}, y={y_val.shape}")
print(f"  Test shape:  X={X_test.shape}, y={y_test.shape}")

# Check for NaN values
if np.isnan(X_train).any() or np.isnan(y_train).any():
    print("\n  ⚠ WARNING: Training data contains NaN values!")
    print(f"    NaN in X_train: {np.isnan(X_train).sum()}")
    print(f"    NaN in y_train: {np.isnan(y_train).sum()}")
    raise ValueError("Cannot proceed with NaN values in training data")

# ============================================================================
# STEP 6: STANDARDIZE FEATURES (CRITICAL FOR NEURAL NETWORKS)
# ============================================================================
print("\n[6/6] Standardizing features...")

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

print(f"  Feature means (after scaling): {X_train_scaled.mean(axis=0)[:3]} ... (showing first 3)")
print(f"  Feature stds (after scaling):  {X_train_scaled.std(axis=0)[:3]} ... (should be ~1.0)")

# ============================================================================
# CONVERT TO PYTORCH TENSORS
# ============================================================================
print("\n[7/7] Converting to PyTorch tensors...")

X_train_t = torch.FloatTensor(X_train_scaled)
y_train_t = torch.FloatTensor(y_train).reshape(-1, 1)

X_val_t = torch.FloatTensor(X_val_scaled)
y_val_t = torch.FloatTensor(y_val).reshape(-1, 1)

X_test_t = torch.FloatTensor(X_test_scaled)
y_test_t = torch.FloatTensor(y_test).reshape(-1, 1)

# Create DataLoaders
batch_size = 16
train_dataset = TensorDataset(X_train_t, y_train_t)
val_dataset = TensorDataset(X_val_t, y_val_t)
test_dataset = TensorDataset(X_test_t, y_test_t)

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

print(f"  Batch size: {batch_size}")
print(f"  Train batches: {len(train_loader)}")
print(f"  Val batches: {len(val_loader)}")
print(f"  Test batches: {len(test_loader)}")

# ============================================================================
# SAVE FOR LATER USE
# ============================================================================
print("\n[8/8] Saving prepared data...")

torch.save({
    'train_loader': train_loader,
    'val_loader': val_loader,
    'test_loader': test_loader,
    'X_test': X_test_t,
    'y_test': y_test_t,
    'X_train': X_train_t,
    'y_train': y_train_t,
    'X_val': X_val_t,
    'y_val': y_val_t,
    'scaler': scaler,
    'feature_cols': feature_cols,
    'target': target,
    'batch_size': batch_size
}, 'data_prepared_nn.pt')

print("  ✓ Saved to data_prepared_nn.pt")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*80)
print("DATA PREPARATION COMPLETE")
print("="*80)
print(f"\n📊 Dataset Summary:")
print(f"   Training samples:   {len(X_train)}")
print(f"   Validation samples: {len(X_val)}")
print(f"   Test samples:       {len(X_test)}")
print(f"   Features:           {len(feature_cols)}")
print(f"   Target:             {target}")
print(f"\n📈 Target Statistics:")
print(f"   Train - Mean: {y_train.mean():.2f}, Std: {y_train.std():.2f}, Range: [{y_train.min():.2f}, {y_train.max():.2f}]")
print(f"   Val   - Mean: {y_val.mean():.2f}, Std: {y_val.std():.2f}, Range: [{y_val.min():.2f}, {y_val.max():.2f}]")
print(f"   Test  - Mean: {y_test.mean():.2f}, Std: {y_test.std():.2f}, Range: [{y_test.min():.2f}, {y_test.max():.2f}]")
print(f"\n✅ Ready for neural network training!")
print(f"   Run: python train_mlp.py")