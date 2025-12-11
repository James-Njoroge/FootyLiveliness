"""
Train Multiple Models on Best Target Metric

After identifying the best target metric from comparison,
this script trains multiple models to find the optimal predictor:
- Ridge Regression
- XGBoost
- Gradient Boosting
- Elastic Net

Generates comprehensive evaluation and recommendations.
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

# Try to import XGBoost (optional)
try:
    import xgboost as xgb
    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False
    print("Warning: XGBoost not available. Install with: brew install libomp && pip3 install xgboost")

print("="*80)
print("TRAINING MULTIPLE MODELS ON BEST TARGET METRIC")
print("="*80)

# ============================================================================
# STEP 1: LOAD BEST TARGET METRIC
# ============================================================================
print("\n[1/6] Loading data and identifying best target...")

# Load comparison results
comparison_df = pd.read_csv('target_metrics_comparison_results.csv')
best_target_row = comparison_df.sort_values('test_r2', ascending=False).iloc[0]
best_target_col = best_target_row['target_col']
best_target_name = best_target_row['target']

print(f"Best target metric: {best_target_name}")
print(f"  Column: {best_target_col}")
print(f"  Baseline R²: {best_target_row['test_r2']:.4f}")

# Load data
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

print(f"Loaded {len(df)} matches")

# ============================================================================
# STEP 2: PREPARE DATA
# ============================================================================
print("\n[2/6] Preparing train/val/test splits...")

train_df = df[df['round'] <= 27].copy()
val_df = df[(df['round'] >= 28) & (df['round'] <= 32)].copy()
test_df = df[df['round'] >= 33].copy()

print(f"Train: {len(train_df)} | Val: {len(val_df)} | Test: {len(test_df)}")

# Define features
drop_cols = [
    'HomeTeam', 'AwayTeam',
    'Home_AttackVsDefense', 'Away_AttackVsDefense',
    'TempoSum', 'SoTSum'
]

target_cols = [col for col in df.columns if col.startswith('target_')]
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

# Prepare arrays
X_train = train_df[feature_cols].values
y_train = train_df[best_target_col].values

X_val = val_df[feature_cols].values
y_val = val_df[best_target_col].values

X_test = test_df[feature_cols].values
y_test = test_df[best_target_col].values

# Scale features (for linear models)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

# ============================================================================
# STEP 3: EVALUATION FUNCTION
# ============================================================================
def evaluate_model(name, y_true, y_pred):
    """Calculate all evaluation metrics"""
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
    
    print(f"\n  {name}:")
    print(f"    R²:          {r2:6.4f}")
    print(f"    MAE:         {mae:6.3f}")
    print(f"    RMSE:        {rmse:6.3f}")
    print(f"    Spearman ρ:  {rho:6.3f}")
    print(f"    Top-10 Hit:  {top_k_hit_rate*100:5.1f}%")
    
    return {
        'split': name,
        'mae': mae,
        'rmse': rmse,
        'r2': r2,
        'rho': rho,
        'top10_hit': top_k_hit_rate * 100
    }

# ============================================================================
# STEP 4: TRAIN MODELS
# ============================================================================
print("\n[3/6] Training models...")

all_results = []

# ============================================================================
# MODEL 1: Ridge Regression
# ============================================================================
print("\n--- Ridge Regression ---")
alphas = np.logspace(-2, 3, 10)
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

# ============================================================================
# MODEL 2: Elastic Net
# ============================================================================
print("\n--- Elastic Net ---")
elasticnet_cv = ElasticNetCV(alphas=alphas, l1_ratio=[0.1, 0.5, 0.7, 0.9, 0.95, 0.99], cv=5, max_iter=10000)
elasticnet_cv.fit(X_train_scaled, y_train)

print(f"Best alpha: {elasticnet_cv.alpha_:.2f}, Best l1_ratio: {elasticnet_cv.l1_ratio_:.2f}")

y_train_pred_en = elasticnet_cv.predict(X_train_scaled)
y_val_pred_en = elasticnet_cv.predict(X_val_scaled)
y_test_pred_en = elasticnet_cv.predict(X_test_scaled)

en_train = evaluate_model("Train", y_train, y_train_pred_en)
en_val = evaluate_model("Val", y_val, y_val_pred_en)
en_test = evaluate_model("Test", y_test, y_test_pred_en)

en_train['model'] = 'ElasticNet'
en_val['model'] = 'ElasticNet'
en_test['model'] = 'ElasticNet'

all_results.extend([en_train, en_val, en_test])

# ============================================================================
# MODEL 3: XGBoost (Optional)
# ============================================================================
if HAS_XGBOOST:
    print("\n--- XGBoost ---")
    xgb_model = xgb.XGBRegressor(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=3,
        min_child_weight=5,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        verbosity=0
    )
    xgb_model.fit(X_train, y_train)

    y_train_pred_xgb = xgb_model.predict(X_train)
    y_val_pred_xgb = xgb_model.predict(X_val)
    y_test_pred_xgb = xgb_model.predict(X_test)

    xgb_train = evaluate_model("Train", y_train, y_train_pred_xgb)
    xgb_val = evaluate_model("Val", y_val, y_val_pred_xgb)
    xgb_test = evaluate_model("Test", y_test, y_test_pred_xgb)

    xgb_train['model'] = 'XGBoost'
    xgb_val['model'] = 'XGBoost'
    xgb_test['model'] = 'XGBoost'

    all_results.extend([xgb_train, xgb_val, xgb_test])
else:
    print("\n--- XGBoost --- SKIPPED (not installed)")

# ============================================================================
# MODEL 4: Gradient Boosting
# ============================================================================
print("\n--- Gradient Boosting ---")
gb_model = GradientBoostingRegressor(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=2,
    min_samples_leaf=5,
    random_state=42
)
gb_model.fit(X_train, y_train)

y_train_pred_gb = gb_model.predict(X_train)
y_val_pred_gb = gb_model.predict(X_val)
y_test_pred_gb = gb_model.predict(X_test)

gb_train = evaluate_model("Train", y_train, y_train_pred_gb)
gb_val = evaluate_model("Val", y_val, y_val_pred_gb)
gb_test = evaluate_model("Test", y_test, y_test_pred_gb)

gb_train['model'] = 'GradientBoosting'
gb_val['model'] = 'GradientBoosting'
gb_test['model'] = 'GradientBoosting'

all_results.extend([gb_train, gb_val, gb_test])

# ============================================================================
# STEP 5: GENERATE REPORT
# ============================================================================
print("\n[4/6] Generating comparison report...")

results_df = pd.DataFrame(all_results)
results_df.to_csv('best_target_models_comparison.csv', index=False)

# Get test results only
test_results = results_df[results_df['split'] == 'Test'].sort_values('r2', ascending=False)

report_path = 'best_target_models_report.txt'
with open(report_path, 'w') as f:
    f.write("="*80 + "\n")
    f.write("BEST TARGET METRIC - MODELS COMPARISON REPORT\n")
    f.write("="*80 + "\n\n")
    
    f.write(f"Target Metric: {best_target_name}\n")
    f.write(f"Target Column: {best_target_col}\n\n")
    
    f.write(f"Dataset Splits:\n")
    f.write(f"  Train: {len(train_df)} matches\n")
    f.write(f"  Val:   {len(val_df)} matches\n")
    f.write(f"  Test:  {len(test_df)} matches\n\n")
    
    f.write("="*80 + "\n")
    f.write("TEST SET RESULTS (Ranked by R²)\n")
    f.write("="*80 + "\n\n")
    
    for idx, row in test_results.iterrows():
        f.write(f"{row['model']}\n")
        f.write("-" * 80 + "\n")
        f.write(f"  R²:          {row['r2']:6.4f}\n")
        f.write(f"  MAE:         {row['mae']:6.3f}\n")
        f.write(f"  RMSE:        {row['rmse']:6.3f}\n")
        f.write(f"  Spearman ρ:  {row['rho']:6.3f}\n")
        f.write(f"  Top-10 Hit:  {row['top10_hit']:5.1f}%\n\n")
    
    f.write("="*80 + "\n")
    f.write("OVERFITTING CHECK\n")
    f.write("="*80 + "\n\n")
    
    for model_name in results_df['model'].unique():
        model_results = results_df[results_df['model'] == model_name]
        train_r2 = model_results[model_results['split'] == 'Train']['r2'].values[0]
        test_r2 = model_results[model_results['split'] == 'Test']['r2'].values[0]
        gap = train_r2 - test_r2
        
        status = "✓ Good" if gap < 0.1 else "⚠ Moderate" if gap < 0.2 else "✗ High"
        f.write(f"{model_name}:\n")
        f.write(f"  Train R²: {train_r2:.4f}\n")
        f.write(f"  Test R²:  {test_r2:.4f}\n")
        f.write(f"  Gap:      {gap:.4f} ({status})\n\n")
    
    f.write("="*80 + "\n")
    f.write("RECOMMENDATION\n")
    f.write("="*80 + "\n\n")
    
    best_model = test_results.iloc[0]
    f.write(f"Best Model: {best_model['model']}\n")
    f.write(f"  Test R²:        {best_model['r2']:.4f}\n")
    f.write(f"  Test MAE:       {best_model['mae']:.3f}\n")
    f.write(f"  Top-10 Hit:     {best_model['top10_hit']:.1f}%\n")
    f.write(f"  Spearman ρ:     {best_model['rho']:.3f}\n\n")
    
    # Compare to baseline Ridge from comparison
    f.write(f"Improvement over baseline Ridge:\n")
    f.write(f"  R² change:      {best_model['r2'] - best_target_row['test_r2']:+.4f}\n")
    f.write(f"  MAE change:     {best_model['mae'] - best_target_row['test_mae']:+.3f}\n")

print(f"✓ Saved report to: {report_path}")

# ============================================================================
# STEP 6: VISUALIZATIONS
# ============================================================================
print("\n[5/6] Creating visualizations...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle(f'Model Comparison - {best_target_name}', fontsize=14, fontweight='bold')

# Plot 1: Test R² comparison
ax = axes[0, 0]
test_plot = test_results.sort_values('r2')
colors = ['#2ecc71' if x == test_plot['r2'].max() else '#3498db' for x in test_plot['r2']]
ax.barh(range(len(test_plot)), test_plot['r2'], color=colors)
ax.set_yticks(range(len(test_plot)))
ax.set_yticklabels(test_plot['model'])
ax.set_xlabel('Test R²', fontweight='bold')
ax.set_title('Test R² by Model', fontweight='bold')
ax.grid(axis='x', alpha=0.3)

# Plot 2: Test MAE comparison
ax = axes[0, 1]
test_plot = test_results.sort_values('mae')
colors = ['#2ecc71' if x == test_plot['mae'].min() else '#3498db' for x in test_plot['mae']]
ax.barh(range(len(test_plot)), test_plot['mae'], color=colors)
ax.set_yticks(range(len(test_plot)))
ax.set_yticklabels(test_plot['model'])
ax.set_xlabel('Test MAE (lower is better)', fontweight='bold')
ax.set_title('Test MAE by Model', fontweight='bold')
ax.grid(axis='x', alpha=0.3)

# Plot 3: Overfitting check
ax = axes[1, 0]
for model_name in results_df['model'].unique():
    model_results = results_df[results_df['model'] == model_name]
    train_r2 = model_results[model_results['split'] == 'Train']['r2'].values[0]
    test_r2 = model_results[model_results['split'] == 'Test']['r2'].values[0]
    ax.scatter(train_r2, test_r2, s=100, label=model_name)

ax.plot([0, results_df['r2'].max()], [0, results_df['r2'].max()], 
        'r--', alpha=0.5, label='Perfect fit')
ax.set_xlabel('Train R²', fontweight='bold')
ax.set_ylabel('Test R²', fontweight='bold')
ax.set_title('Overfitting Check', fontweight='bold')
ax.legend()
ax.grid(alpha=0.3)

# Plot 4: Top-10 Hit Rate
ax = axes[1, 1]
test_plot = test_results.sort_values('top10_hit')
colors = ['#2ecc71' if x == test_plot['top10_hit'].max() else '#3498db' for x in test_plot['top10_hit']]
ax.barh(range(len(test_plot)), test_plot['top10_hit'], color=colors)
ax.set_yticks(range(len(test_plot)))
ax.set_yticklabels(test_plot['model'])
ax.set_xlabel('Top-10 Hit Rate (%)', fontweight='bold')
ax.set_title('Top-10 Hit Rate by Model', fontweight='bold')
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig('best_target_models_comparison.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved visualization to: best_target_models_comparison.png")

plt.close()

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*80)
print("MODEL COMPARISON COMPLETE!")
print("="*80)
print(f"\nBest Model: {best_model['model']}")
print(f"  Test R²: {best_model['r2']:.4f}")
print(f"  Test MAE: {best_model['mae']:.3f}")
print(f"  Top-10 Hit Rate: {best_model['top10_hit']:.1f}%")

print("\nGenerated files:")
print("  1. best_target_models_comparison.csv")
print("  2. best_target_models_report.txt")
print("  3. best_target_models_comparison.png")

print("\n" + "="*80)
