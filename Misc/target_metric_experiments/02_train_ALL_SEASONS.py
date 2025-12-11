"""
Train Models on All Seasons Data

Uses Simple xG target (winner from single-season experiments)
Tests Elastic Net (winner from single-season experiments)
Compares to single-season baseline
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import Ridge, RidgeCV, ElasticNet, ElasticNetCV
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from scipy.stats import spearmanr
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("TRAINING MODELS ON ALL SEASONS DATA")
print("="*80)

# ============================================================================
# STEP 1: LOAD DATA
# ============================================================================
print("\n[1/6] Loading all-seasons data...")

df = pd.read_csv('all_seasons_features.csv')

print(f"Loaded {len(df)} matches")
print(f"Seasons: {df['season'].unique().tolist()}")

# ============================================================================
# STEP 2: PREPARE SPLITS (CHRONOLOGICAL BY SEASON)
# ============================================================================
print("\n[2/6] Preparing chronological train/val/test splits...")

# Split by season (chronological)
# Train: 2022/23 + first half of 2023/24
# Val: Second half of 2023/24
# Test: 2024/25

train_mask = (
    (df['season'] == '2022-23') |
    ((df['season'] == '2023-24') & (df['round'] <= 18))
)
val_mask = (df['season'] == '2023-24') & (df['round'] > 18)
test_mask = df['season'] == '2024-25'

train_df = df[train_mask].copy()
val_df = df[val_mask].copy()
test_df = df[test_mask].copy()

print(f"Train: {len(train_df)} matches (2022/23 + half of 2023/24)")
print(f"Val:   {len(val_df)} matches (second half of 2023/24)")
print(f"Test:  {len(test_df)} matches (2024/25)")

# ============================================================================
# STEP 3: PREPARE FEATURES
# ============================================================================
print("\n[3/6] Preparing features...")

# Feature columns
feature_cols = [
    'season_encoded',
    'round',
    'xG_combined',
    'shots_combined',
    'sot_combined',
    'bigch_combined',
    'corners_combined',
    'xG_diff',
    'shots_diff',
    'xG_home_rolling_home',
    'xG_away_rolling_away',
    'shots_home_rolling_home',
    'shots_away_rolling_away',
    'sot_home_rolling_home',
    'sot_away_rolling_away',
    'bigch_home_rolling_home',
    'bigch_away_rolling_away',
    'corners_home_rolling_home',
    'corners_away_rolling_away'
]

print(f"Using {len(feature_cols)} features")

# Target
target_col = 'target_simple_xg'

# Prepare data
X_train = train_df[feature_cols].values
y_train = train_df[target_col].values

X_val = val_df[feature_cols].values
y_val = val_df[target_col].values

X_test = test_df[feature_cols].values
y_test = test_df[target_col].values

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

# ============================================================================
# STEP 4: EVALUATION FUNCTION
# ============================================================================
def evaluate_model(split_name, y_true, y_pred):
    """Calculate all evaluation metrics"""
    mae = mean_absolute_error(y_true, y_pred)
    rmse = mean_squared_error(y_true, y_pred, squared=False)
    r2 = r2_score(y_true, y_pred)
    rho, _ = spearmanr(y_true, y_pred)
    
    k = min(10, len(y_true))
    pred_top_idx = np.argsort(y_pred)[-k:]
    true_top_idx = np.argsort(y_true)[-k:]
    hit = len(set(pred_top_idx).intersection(set(true_top_idx)))
    top_k_hit_rate = (hit / k) * 100 if k > 0 else 0.0
    
    return {
        'split': split_name,
        'r2': r2,
        'mae': mae,
        'rmse': rmse,
        'spearman': rho,
        'top10_hit': top_k_hit_rate
    }

# ============================================================================
# STEP 5: TRAIN MODELS
# ============================================================================
print("\n[4/6] Training models...")

all_results = []

# MODEL 1: Ridge Regression
print("\n--- Ridge Regression ---")
alphas = np.logspace(-2, 3, 20)
ridge_cv = RidgeCV(alphas=alphas, cv=5)
ridge_cv.fit(X_train_scaled, y_train)

print(f"Best alpha: {ridge_cv.alpha_:.2f}")

y_train_pred_ridge = ridge_cv.predict(X_train_scaled)
y_val_pred_ridge = ridge_cv.predict(X_val_scaled)
y_test_pred_ridge = ridge_cv.predict(X_test_scaled)

ridge_train = evaluate_model("Train", y_train, y_train_pred_ridge)
ridge_val = evaluate_model("Val", y_val, y_val_pred_ridge)
ridge_test = evaluate_model("Test", y_test, y_test_pred_ridge)

ridge_train['model'] = 'Ridge'
ridge_val['model'] = 'Ridge'
ridge_test['model'] = 'Ridge'

all_results.extend([ridge_train, ridge_val, ridge_test])

print(f"\n  Train: R²={ridge_train['r2']:.4f}, MAE={ridge_train['mae']:.3f}, Top-10={ridge_train['top10_hit']:.1f}%")
print(f"  Val:   R²={ridge_val['r2']:.4f}, MAE={ridge_val['mae']:.3f}, Top-10={ridge_val['top10_hit']:.1f}%")
print(f"  Test:  R²={ridge_test['r2']:.4f}, MAE={ridge_test['mae']:.3f}, Top-10={ridge_test['top10_hit']:.1f}%")

# MODEL 2: Elastic Net (Winner from single-season)
print("\n--- Elastic Net ---")
alphas = np.logspace(-3, 1, 20)
l1_ratios = [0.1, 0.3, 0.5, 0.7, 0.9, 0.95, 0.99]
en_cv = ElasticNetCV(alphas=alphas, l1_ratio=l1_ratios, cv=5, max_iter=10000)
en_cv.fit(X_train_scaled, y_train)

print(f"Best alpha: {en_cv.alpha_:.2f}, Best l1_ratio: {en_cv.l1_ratio_:.2f}")

y_train_pred_en = en_cv.predict(X_train_scaled)
y_val_pred_en = en_cv.predict(X_val_scaled)
y_test_pred_en = en_cv.predict(X_test_scaled)

en_train = evaluate_model("Train", y_train, y_train_pred_en)
en_val = evaluate_model("Val", y_val, y_val_pred_en)
en_test = evaluate_model("Test", y_test, y_test_pred_en)

en_train['model'] = 'ElasticNet'
en_val['model'] = 'ElasticNet'
en_test['model'] = 'ElasticNet'

all_results.extend([en_train, en_val, en_test])

print(f"\n  Train: R²={en_train['r2']:.4f}, MAE={en_train['mae']:.3f}, Top-10={en_train['top10_hit']:.1f}%")
print(f"  Val:   R²={en_val['r2']:.4f}, MAE={en_val['mae']:.3f}, Top-10={en_val['top10_hit']:.1f}%")
print(f"  Test:  R²={en_test['r2']:.4f}, MAE={en_test['mae']:.3f}, Top-10={en_test['top10_hit']:.1f}%")

# MODEL 3: Gradient Boosting
print("\n--- Gradient Boosting ---")
gb_model = GradientBoostingRegressor(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=2,
    min_samples_leaf=5,
    random_state=42
)
gb_model.fit(X_train_scaled, y_train)

y_train_pred_gb = gb_model.predict(X_train_scaled)
y_val_pred_gb = gb_model.predict(X_val_scaled)
y_test_pred_gb = gb_model.predict(X_test_scaled)

gb_train = evaluate_model("Train", y_train, y_train_pred_gb)
gb_val = evaluate_model("Val", y_val, y_val_pred_gb)
gb_test = evaluate_model("Test", y_test, y_test_pred_gb)

gb_train['model'] = 'GradientBoosting'
gb_val['model'] = 'GradientBoosting'
gb_test['model'] = 'GradientBoosting'

all_results.extend([gb_train, gb_val, gb_test])

print(f"\n  Train: R²={gb_train['r2']:.4f}, MAE={gb_train['mae']:.3f}, Top-10={gb_train['top10_hit']:.1f}%")
print(f"  Val:   R²={gb_val['r2']:.4f}, MAE={gb_val['mae']:.3f}, Top-10={gb_val['top10_hit']:.1f}%")
print(f"  Test:  R²={gb_test['r2']:.4f}, MAE={gb_test['mae']:.3f}, Top-10={gb_test['top10_hit']:.1f}%")

# ============================================================================
# STEP 6: GENERATE REPORT
# ============================================================================
print("\n[5/6] Generating comparison report...")

results_df = pd.DataFrame(all_results)
results_df.to_csv('all_seasons_results.csv', index=False)

# Get best model
test_results = results_df[results_df['split'] == 'Test'].sort_values('r2', ascending=False)
best_model = test_results.iloc[0]

report_path = 'all_seasons_report.txt'
with open(report_path, 'w') as f:
    f.write("="*80 + "\n")
    f.write("ALL-SEASONS MODEL COMPARISON\n")
    f.write("="*80 + "\n\n")
    
    f.write("DATASET:\n")
    f.write(f"  Total matches: {len(df)}\n")
    f.write(f"  Seasons: 2022/23, 2023/24, 2024/25\n")
    f.write(f"  Train: {len(train_df)} matches\n")
    f.write(f"  Val:   {len(val_df)} matches\n")
    f.write(f"  Test:  {len(test_df)} matches\n\n")
    
    f.write("TARGET METRIC: Simple xG (winner from single-season experiments)\n")
    f.write(f"FEATURES: {len(feature_cols)} rolling and aggregate features\n\n")
    
    f.write("="*80 + "\n")
    f.write("RESULTS BY MODEL\n")
    f.write("="*80 + "\n\n")
    
    for model_name in results_df['model'].unique():
        model_results = results_df[results_df['model'] == model_name]
        f.write(f"{model_name}\n")
        f.write("-" * 80 + "\n")
        
        for _, row in model_results.iterrows():
            f.write(f"  {row['split']}:\n")
            f.write(f"    R²:          {row['r2']:6.4f}\n")
            f.write(f"    MAE:         {row['mae']:6.3f}\n")
            f.write(f"    RMSE:        {row['rmse']:6.3f}\n")
            f.write(f"    Spearman ρ:  {row['spearman']:6.3f}\n")
            f.write(f"    Top-10 Hit:  {row['top10_hit']:5.1f}%\n")
        f.write("\n")
    
    f.write("="*80 + "\n")
    f.write("BEST MODEL (BY TEST R²)\n")
    f.write("="*80 + "\n\n")
    
    f.write(f"Model: {best_model['model']}\n")
    f.write(f"  Test R²:        {best_model['r2']:.4f}\n")
    f.write(f"  Test MAE:       {best_model['mae']:.3f}\n")
    f.write(f"  Top-10 Hit:     {best_model['top10_hit']:.1f}%\n\n")
    
    f.write("="*80 + "\n")
    f.write("COMPARISON TO SINGLE-SEASON BASELINE\n")
    f.write("="*80 + "\n\n")
    
    f.write("Single-Season (2024/25 only):\n")
    f.write("  Model: Elastic Net\n")
    f.write("  Test R²: 0.8205\n")
    f.write("  Test MAE: 0.452\n")
    f.write("  Top-10 Hit: 90.0%\n")
    f.write("  Training samples: 280\n\n")
    
    f.write("All-Seasons (2022/23, 2023/24, 2024/25):\n")
    f.write(f"  Model: {best_model['model']}\n")
    f.write(f"  Test R²: {best_model['r2']:.4f}\n")
    f.write(f"  Test MAE: {best_model['mae']:.3f}\n")
    f.write(f"  Top-10 Hit: {best_model['top10_hit']:.1f}%\n")
    f.write(f"  Training samples: {len(train_df)}\n\n")
    
    improvement_r2 = ((best_model['r2'] - 0.8205) / 0.8205 * 100)
    f.write(f"R² Change: {improvement_r2:+.1f}%\n")
    
    if best_model['r2'] > 0.8205:
        f.write("\n✓ All-seasons approach IMPROVES performance!\n")
    else:
        f.write("\n✗ All-seasons approach DECREASES performance.\n")
        f.write("  Recommendation: Stick with single-season model.\n")

print(f"✓ Saved report to: {report_path}")

# ============================================================================
# VISUALIZATION
# ============================================================================
print("\n[6/6] Creating visualizations...")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('All-Seasons vs Single-Season Comparison', fontsize=14, fontweight='bold')

# Plot 1: Test R² comparison
ax = axes[0]
test_r2 = results_df[results_df['split'] == 'Test'].sort_values('r2', ascending=False)
models = test_r2['model'].tolist() + ['Single-Season\n(Elastic Net)']
r2_values = test_r2['r2'].tolist() + [0.8205]
colors = ['#3498db'] * len(test_r2) + ['#2ecc71']

ax.barh(range(len(models)), r2_values, color=colors)
ax.set_yticks(range(len(models)))
ax.set_yticklabels(models)
ax.set_xlabel('Test R²', fontweight='bold')
ax.set_title('Test R² Comparison', fontweight='bold')
ax.axvline(x=0.8205, color='red', linestyle='--', alpha=0.5, label='Single-season baseline')
ax.legend()
ax.grid(axis='x', alpha=0.3)

# Plot 2: Top-10 Hit Rate comparison
ax = axes[1]
test_top10 = results_df[results_df['split'] == 'Test'].sort_values('top10_hit', ascending=False)
models = test_top10['model'].tolist() + ['Single-Season\n(Elastic Net)']
top10_values = test_top10['top10_hit'].tolist() + [90.0]
colors = ['#3498db'] * len(test_top10) + ['#2ecc71']

ax.barh(range(len(models)), top10_values, color=colors)
ax.set_yticks(range(len(models)))
ax.set_yticklabels(models)
ax.set_xlabel('Top-10 Hit Rate (%)', fontweight='bold')
ax.set_title('Top-10 Hit Rate Comparison', fontweight='bold')
ax.axvline(x=90.0, color='red', linestyle='--', alpha=0.5, label='Single-season baseline')
ax.legend()
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig('all_seasons_comparison.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved visualization to: all_seasons_comparison.png")

plt.close()

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*80)
print("ALL-SEASONS TRAINING COMPLETE!")
print("="*80)

print(f"\nBest All-Seasons Model: {best_model['model']}")
print(f"  Test R²: {best_model['r2']:.4f}")
print(f"  Test MAE: {best_model['mae']:.3f}")
print(f"  Top-10 Hit: {best_model['top10_hit']:.1f}%")

print(f"\nComparison to Single-Season:")
print(f"  Single-season R²: 0.8205")
print(f"  All-seasons R²:   {best_model['r2']:.4f}")
print(f"  Change:           {improvement_r2:+.1f}%")

if best_model['r2'] > 0.8205:
    print("\n✓ All-seasons is BETTER! Use this approach.")
else:
    print("\n✗ Single-season is BETTER! Stick with current model.")

print("\nGenerated files:")
print("  1. all_seasons_features.csv")
print("  2. all_seasons_results.csv")
print("  3. all_seasons_report.txt ⭐")
print("  4. all_seasons_comparison.png")

print("\n" + "="*80)
