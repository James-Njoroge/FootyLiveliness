"""
Compare Alternative Target Metrics

Tests each target metric with Ridge Regression using existing 37 features.
Evaluates:
- R² (variance explained)
- MAE (prediction accuracy)
- Spearman ρ (ranking quality)
- Top-10 hit rate (practical utility)
- Distribution characteristics

Outputs:
- Comprehensive comparison report
- Visualization plots
- Recommendation for best target metric
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import Ridge, RidgeCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from scipy.stats import spearmanr
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("COMPARING TARGET METRICS WITH RIDGE REGRESSION")
print("="*80)

# ============================================================================
# STEP 1: LOAD DATA
# ============================================================================
print("\n[1/5] Loading data...")

targets_df = pd.read_csv('targets_comparison.csv')
features_df = pd.read_csv('../data/feature_tables/match_features_wide.csv')

# Rename feature columns to match
features_df = features_df.rename(columns={
    'Round': 'round',
    'HomeTeam': 'homeTeamName',
    'AwayTeam': 'awayTeamName'
})

# Merge on round and team names
df = pd.merge(targets_df, features_df,
              on=['round', 'homeTeamName', 'awayTeamName'],
              how='inner')

print(f"Merged dataset: {len(df)} matches")

# ============================================================================
# STEP 2: PREPARE SPLITS
# ============================================================================
print("\n[2/5] Preparing train/val/test splits...")

# Chronological split
train_df = df[df['round'] <= 27].copy()
val_df = df[(df['round'] >= 28) & (df['round'] <= 32)].copy()
test_df = df[df['round'] >= 33].copy()

print(f"Train: {len(train_df)} | Val: {len(val_df)} | Test: {len(test_df)}")

# Define features (same as current best model)
drop_cols = [
    'HomeTeam', 'AwayTeam',
    'Home_AttackVsDefense', 'Away_AttackVsDefense',
    'TempoSum', 'SoTSum'
]

# Get all target columns
target_cols = [col for col in df.columns if col.startswith('target_')]

# Get feature columns (exclude targets and metadata)
metadata_cols = ['round', 'matchId', 'homeTeamName', 'awayTeamName', 
                 'homeTeamId', 'awayTeamId', 'goals_home_count', 'goals_away_count',
                 'xG_home', 'xG_away', 'xG_total', 'xG_min',
                 'shots_home', 'shots_away', 'shots_total',
                 'sot_home', 'sot_away', 'sot_total',
                 'bigch_home', 'bigch_away', 'bigch_total',
                 'corners_home', 'corners_away', 'corners_total',
                 'yellow_cards_home', 'yellow_cards_away',
                 'red_cards_home', 'red_cards_away', 'total_cards']

feature_cols = [c for c in df.columns 
                if c not in target_cols 
                and c not in metadata_cols 
                and c not in drop_cols]

print(f"Using {len(feature_cols)} features")

# ============================================================================
# STEP 3: TRAIN AND EVALUATE EACH TARGET METRIC
# ============================================================================
print("\n[3/5] Training Ridge Regression for each target metric...")

results = []

for target_col in target_cols:
    target_name = target_col.replace('target_', '').replace('_', ' ').title()
    print(f"\n  Training: {target_name}")
    
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
    
    # Tune alpha with cross-validation
    alphas = np.logspace(-2, 3, 10)
    ridge_cv = RidgeCV(alphas=alphas, cv=5)
    ridge_cv.fit(X_train_scaled, y_train)
    
    best_alpha = ridge_cv.alpha_
    
    # Predict on all splits
    y_train_pred = ridge_cv.predict(X_train_scaled)
    y_val_pred = ridge_cv.predict(X_val_scaled)
    y_test_pred = ridge_cv.predict(X_test_scaled)
    
    # Calculate metrics for each split
    def calc_metrics(y_true, y_pred, split_name):
        mae = mean_absolute_error(y_true, y_pred)
        rmse = mean_squared_error(y_true, y_pred, squared=False)
        r2 = r2_score(y_true, y_pred)
        rho, rho_p = spearmanr(y_true, y_pred)
        
        # Top-10 hit rate
        k = min(10, len(y_true))
        pred_top_idx = np.argsort(y_pred)[-k:]
        true_top_idx = np.argsort(y_true)[-k:]
        hit = len(set(pred_top_idx).intersection(set(true_top_idx)))
        top_k_hit_rate = hit / k if k > 0 else 0.0
        
        return {
            f'{split_name}_mae': mae,
            f'{split_name}_rmse': rmse,
            f'{split_name}_r2': r2,
            f'{split_name}_rho': rho,
            f'{split_name}_top10_hit': top_k_hit_rate * 100
        }
    
    train_metrics = calc_metrics(y_train, y_train_pred, 'train')
    val_metrics = calc_metrics(y_val, y_val_pred, 'val')
    test_metrics = calc_metrics(y_test, y_test_pred, 'test')
    
    # Combine results
    result = {
        'target': target_name,
        'target_col': target_col,
        'best_alpha': best_alpha,
        'target_mean': train_df[target_col].mean(),
        'target_std': train_df[target_col].std(),
        'target_range': train_df[target_col].max() - train_df[target_col].min(),
        **train_metrics,
        **val_metrics,
        **test_metrics
    }
    
    results.append(result)
    
    print(f"    Test R²: {test_metrics['test_r2']:.4f} | MAE: {test_metrics['test_mae']:.3f} | Top-10: {test_metrics['test_top10_hit']:.1f}%")

results_df = pd.DataFrame(results)

# ============================================================================
# STEP 4: GENERATE COMPARISON REPORT
# ============================================================================
print("\n[4/5] Generating comparison report...")

# Sort by test R²
results_df = results_df.sort_values('test_r2', ascending=False)

# Save full results
results_df.to_csv('target_metrics_comparison_results.csv', index=False)
print(f"✓ Saved detailed results to: target_metrics_comparison_results.csv")

# Create summary report
report_path = 'target_metrics_comparison_report.txt'
with open(report_path, 'w') as f:
    f.write("="*80 + "\n")
    f.write("TARGET METRICS COMPARISON REPORT\n")
    f.write("="*80 + "\n\n")
    
    f.write("MODEL: Ridge Regression with 37 features\n")
    f.write(f"SPLITS: Train ({len(train_df)}) | Val ({len(val_df)}) | Test ({len(test_df)})\n\n")
    
    f.write("="*80 + "\n")
    f.write("RANKING BY TEST R² (Best to Worst)\n")
    f.write("="*80 + "\n\n")
    
    for idx, row in results_df.iterrows():
        f.write(f"{row['target']}\n")
        f.write("-" * 80 + "\n")
        f.write(f"  Test R²:        {row['test_r2']:6.4f}\n")
        f.write(f"  Test MAE:       {row['test_mae']:6.3f}\n")
        f.write(f"  Test RMSE:      {row['test_rmse']:6.3f}\n")
        f.write(f"  Test Spearman:  {row['test_rho']:6.3f}\n")
        f.write(f"  Test Top-10:    {row['test_top10_hit']:5.1f}%\n")
        f.write(f"  Train R²:       {row['train_r2']:6.4f}\n")
        f.write(f"  Overfitting:    {row['train_r2'] - row['test_r2']:6.4f}\n")
        f.write(f"  Best Alpha:     {row['best_alpha']:6.2f}\n")
        f.write(f"  Target Range:   [{row['target_mean'] - row['target_std']:.2f}, {row['target_mean'] + row['target_std']:.2f}]\n")
        f.write("\n")
    
    f.write("="*80 + "\n")
    f.write("RECOMMENDATION\n")
    f.write("="*80 + "\n\n")
    
    best_target = results_df.iloc[0]
    f.write(f"Best Target Metric: {best_target['target']}\n")
    f.write(f"  - Test R²: {best_target['test_r2']:.4f}\n")
    f.write(f"  - Test MAE: {best_target['test_mae']:.3f}\n")
    f.write(f"  - Top-10 Hit Rate: {best_target['test_top10_hit']:.1f}%\n")
    f.write(f"  - Overfitting: {best_target['train_r2'] - best_target['test_r2']:.4f}\n\n")
    
    # Compare to baseline (target_1_simple_xg)
    baseline = results_df[results_df['target_col'] == 'target_1_simple_xg'].iloc[0]
    if best_target['target_col'] != 'target_1_simple_xg':
        improvement_r2 = ((best_target['test_r2'] - baseline['test_r2']) / abs(baseline['test_r2'])) * 100
        improvement_mae = ((baseline['test_mae'] - best_target['test_mae']) / baseline['test_mae']) * 100
        
        f.write(f"Improvement over Simple xG baseline:\n")
        f.write(f"  - R² improvement: {improvement_r2:+.1f}%\n")
        f.write(f"  - MAE improvement: {improvement_mae:+.1f}%\n")
    else:
        f.write("Current baseline (Simple xG) is already the best performer.\n")

print(f"✓ Saved report to: {report_path}")

# ============================================================================
# STEP 5: CREATE VISUALIZATIONS
# ============================================================================
print("\n[5/5] Creating visualizations...")

fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle('Target Metrics Comparison', fontsize=16, fontweight='bold')

# Plot 1: Test R² comparison
ax = axes[0, 0]
results_plot = results_df.sort_values('test_r2')
colors = ['#2ecc71' if x == results_plot['test_r2'].max() else '#3498db' for x in results_plot['test_r2']]
ax.barh(range(len(results_plot)), results_plot['test_r2'], color=colors)
ax.set_yticks(range(len(results_plot)))
ax.set_yticklabels(results_plot['target'], fontsize=9)
ax.set_xlabel('Test R²', fontweight='bold')
ax.set_title('Test R² by Target Metric', fontweight='bold')
ax.axvline(x=0, color='red', linestyle='--', alpha=0.5)
ax.grid(axis='x', alpha=0.3)

# Plot 2: Test MAE comparison
ax = axes[0, 1]
results_plot = results_df.sort_values('test_mae')
colors = ['#2ecc71' if x == results_plot['test_mae'].min() else '#3498db' for x in results_plot['test_mae']]
ax.barh(range(len(results_plot)), results_plot['test_mae'], color=colors)
ax.set_yticks(range(len(results_plot)))
ax.set_yticklabels(results_plot['target'], fontsize=9)
ax.set_xlabel('Test MAE (lower is better)', fontweight='bold')
ax.set_title('Test MAE by Target Metric', fontweight='bold')
ax.grid(axis='x', alpha=0.3)

# Plot 3: Top-10 Hit Rate
ax = axes[0, 2]
results_plot = results_df.sort_values('test_top10_hit')
colors = ['#2ecc71' if x == results_plot['test_top10_hit'].max() else '#3498db' for x in results_plot['test_top10_hit']]
ax.barh(range(len(results_plot)), results_plot['test_top10_hit'], color=colors)
ax.set_yticks(range(len(results_plot)))
ax.set_yticklabels(results_plot['target'], fontsize=9)
ax.set_xlabel('Top-10 Hit Rate (%)', fontweight='bold')
ax.set_title('Top-10 Hit Rate by Target Metric', fontweight='bold')
ax.grid(axis='x', alpha=0.3)

# Plot 4: Overfitting check (Train R² vs Test R²)
ax = axes[1, 0]
ax.scatter(results_df['train_r2'], results_df['test_r2'], s=100, alpha=0.6)
for idx, row in results_df.iterrows():
    ax.annotate(row['target'].split()[0], 
                (row['train_r2'], row['test_r2']),
                fontsize=8, ha='right')
ax.plot([results_df['train_r2'].min(), results_df['train_r2'].max()],
        [results_df['train_r2'].min(), results_df['train_r2'].max()],
        'r--', alpha=0.5, label='Perfect fit')
ax.set_xlabel('Train R²', fontweight='bold')
ax.set_ylabel('Test R²', fontweight='bold')
ax.set_title('Overfitting Check', fontweight='bold')
ax.legend()
ax.grid(alpha=0.3)

# Plot 5: Spearman correlation comparison
ax = axes[1, 1]
results_plot = results_df.sort_values('test_rho')
colors = ['#2ecc71' if x == results_plot['test_rho'].max() else '#3498db' for x in results_plot['test_rho']]
ax.barh(range(len(results_plot)), results_plot['test_rho'], color=colors)
ax.set_yticks(range(len(results_plot)))
ax.set_yticklabels(results_plot['target'], fontsize=9)
ax.set_xlabel('Spearman ρ (ranking quality)', fontweight='bold')
ax.set_title('Ranking Quality by Target Metric', fontweight='bold')
ax.grid(axis='x', alpha=0.3)

# Plot 6: Multi-metric radar chart for top 3
ax = axes[1, 2]
top3 = results_df.head(3)

# Normalize metrics to 0-1 scale for comparison
metrics_to_plot = ['test_r2', 'test_rho', 'test_top10_hit']
metric_labels = ['R²', 'Spearman ρ', 'Top-10 Hit %']

# Create table instead of radar
table_data = []
for idx, row in top3.iterrows():
    table_data.append([
        row['target'],
        f"{row['test_r2']:.3f}",
        f"{row['test_rho']:.3f}",
        f"{row['test_top10_hit']:.1f}%"
    ])

ax.axis('tight')
ax.axis('off')
table = ax.table(cellText=table_data,
                colLabels=['Target', 'R²', 'Spearman ρ', 'Top-10 Hit'],
                cellLoc='center',
                loc='center',
                colWidths=[0.4, 0.2, 0.2, 0.2])
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 2)
ax.set_title('Top 3 Performers', fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('target_metrics_comparison.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved visualization to: target_metrics_comparison.png")

plt.close()

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*80)
print("COMPARISON COMPLETE!")
print("="*80)
print(f"\nBest Target Metric: {best_target['target']}")
print(f"  Test R²: {best_target['test_r2']:.4f}")
print(f"  Test MAE: {best_target['test_mae']:.3f}")
print(f"  Top-10 Hit Rate: {best_target['test_top10_hit']:.1f}%")

print("\nGenerated files:")
print("  1. targets_comparison.csv (from previous script)")
print("  2. target_metrics_comparison_results.csv")
print("  3. target_metrics_comparison_report.txt")
print("  4. target_metrics_comparison.png")

print("\nNext step: Run 03_train_best_target.py with the winning metric!")
print("="*80)
