"""
FootyLiveliness - Enhanced Model Comparison with Contextual Features

Tests all 3 liveliness metrics WITH the new contextual features:
- League position, points, form trajectory, home/away splits

Goal: See if contextual features improve R²
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from scipy.stats import spearmanr
import xgboost as xgb
import warnings
warnings.filterwarnings('ignore')

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)

print("="*80)
print("ENHANCED MODEL COMPARISON - WITH CONTEXTUAL FEATURES")
print("="*80)

# ============================================================================
# LOAD DATA
# ============================================================================
print("\n[1/6] Loading labels + enhanced features...")

labels_df = pd.read_csv('tables/all_rounds.csv')
features_enhanced = pd.read_csv('feature_tables/match_features_enhanced.csv')

# Merge
df = pd.merge(labels_df, features_enhanced,
              on=['round', 'matchId', 'homeTeamName', 'awayTeamName', 'homeTeamId', 'awayTeamId'],
              how='inner')

print(f"Merged dataset: {len(df)} matches")

# ============================================================================
# PREPARE SPLITS
# ============================================================================
print("\n[2/6] Preparing train/val/test splits...")

df_model = df[df['TempoSum'].notna()].copy()

train_df = df_model[(df_model['round'] >= 5) & (df_model['round'] <= 28)]
val_df = df_model[(df_model['round'] >= 29) & (df_model['round'] <= 33)]
test_df = df_model[(df_model['round'] >= 34) & (df_model['round'] <= 37)]

print(f"Train: {len(train_df)} | Val: {len(val_df)} | Test: {len(test_df)}")

# Define ALL features (original + new contextual)
feature_cols = [
    # Original rolling features
    'home_xG_att_90', 'home_SoT_att_90', 'home_BigCh_att_90', 'home_Corn_att_90', 'home_ToB_att_90',
    'home_xGA_def_90', 'home_SoT_agst_90', 'home_BigCh_agst_90',
    'away_xG_att_90', 'away_SoT_att_90', 'away_BigCh_att_90', 'away_Corn_att_90', 'away_ToB_att_90',
    'away_xGA_def_90', 'away_SoT_agst_90', 'away_BigCh_agst_90',
    'TempoSum', 'SoTSum', 'AttackVsDefense', 'xG_att_sum', 'xG_att_min', 'BigCh_sum',
    
    # NEW contextual features
    'home_position', 'away_position', 'position_diff',
    'points_diff', 'gd_diff',
    'home_last3_points', 'home_last3_goals', 'home_form_trend',
    'away_last3_points', 'away_last3_goals', 'away_form_trend',
    'home_strength_ratio', 'away_strength_ratio',
    'both_top6', 'both_bottom6', 'close_positions'
]

print(f"Total features: {len(feature_cols)} (22 original + {len(feature_cols) - 22} new)")

# ============================================================================
# TRAIN ALL MODELS
# ============================================================================
print("\n[3/6] Training models with enhanced features...")

metrics_to_test = {
    'SLS_Fplus_rolling': 'SLS-F+ (Rolling Z-Scores)',
    'SLS_Fplus_fixed': 'SLS-F+ (Fixed Z-Scores)',
    'Liveliness_xG': 'xG-Based Liveliness'
}

results = {}

for metric_name, metric_label in metrics_to_test.items():
    print(f"\n  Testing: {metric_label}")
    
    train_valid = train_df[train_df[metric_name].notna()].copy()
    val_valid = val_df[val_df[metric_name].notna()].copy()
    test_valid = test_df[test_df[metric_name].notna()].copy()
    
    # Drop rows with NaN in features
    train_valid = train_valid.dropna(subset=feature_cols)
    val_valid = val_valid.dropna(subset=feature_cols)
    test_valid = test_valid.dropna(subset=feature_cols)
    
    if len(train_valid) == 0 or len(test_valid) == 0:
        print(f"    Skipping - insufficient data")
        continue
    
    X_train = train_valid[feature_cols]
    y_train = train_valid[metric_name]
    
    X_val = val_valid[feature_cols]
    y_val = val_valid[metric_name]
    
    X_test = test_valid[feature_cols]
    y_test = test_valid[metric_name]
    
    print(f"    Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")
    
    # Linear Regression
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    lr_test_pred = lr.predict(X_test)
    
    lr_metrics = {
        'MAE': mean_absolute_error(y_test, lr_test_pred),
        'RMSE': np.sqrt(mean_squared_error(y_test, lr_test_pred)),
        'R2': r2_score(y_test, lr_test_pred),
        'Spearman': spearmanr(y_test, lr_test_pred)[0]
    }
    
    print(f"    Linear Reg - R²: {lr_metrics['R2']:.3f}, MAE: {lr_metrics['MAE']:.3f}")
    
    # XGBoost
    xgb_model = xgb.XGBRegressor(
        objective='reg:squarederror',
        max_depth=4,
        learning_rate=0.05,
        n_estimators=150,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42
    )
    
    xgb_model.fit(X_train, y_train,
                  eval_set=[(X_val, y_val)],
                  verbose=False)
    
    xgb_test_pred = xgb_model.predict(X_test)
    
    xgb_metrics = {
        'MAE': mean_absolute_error(y_test, xgb_test_pred),
        'RMSE': np.sqrt(mean_squared_error(y_test, xgb_test_pred)),
        'R2': r2_score(y_test, xgb_test_pred),
        'Spearman': spearmanr(y_test, xgb_test_pred)[0]
    }
    
    print(f"    XGBoost    - R²: {xgb_metrics['R2']:.3f}, MAE: {xgb_metrics['MAE']:.3f}")
    
    results[metric_name] = {
        'label': metric_label,
        'lr_metrics': lr_metrics,
        'xgb_metrics': xgb_metrics,
        'y_test': y_test,
        'lr_pred': lr_test_pred,
        'xgb_pred': xgb_test_pred,
        'lr_model': lr,
        'xgb_model': xgb_model
    }

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*80)
print("ENHANCED RESULTS - TEST SET PERFORMANCE")
print("="*80)

summary_data = []
for metric_name, res in results.items():
    summary_data.append({
        'Metric': res['label'],
        'Model': 'Linear Reg',
        'R²': res['lr_metrics']['R2'],
        'MAE': res['lr_metrics']['MAE'],
        'RMSE': res['lr_metrics']['RMSE'],
        'Spearman ρ': res['lr_metrics']['Spearman']
    })
    summary_data.append({
        'Metric': res['label'],
        'Model': 'XGBoost',
        'R²': res['xgb_metrics']['R2'],
        'MAE': res['xgb_metrics']['MAE'],
        'RMSE': res['xgb_metrics']['RMSE'],
        'Spearman ρ': res['xgb_metrics']['Spearman']
    })

summary_df = pd.DataFrame(summary_data)
print(summary_df.to_string(index=False))

best_r2 = summary_df.loc[summary_df['R²'].idxmax()]
best_spearman = summary_df.loc[summary_df['Spearman ρ'].idxmax()]

print("\n" + "="*80)
print("BEST PERFORMERS")
print("="*80)
print(f"Best R²: {best_r2['Metric']} with {best_r2['Model']} (R²={best_r2['R²']:.3f})")
print(f"Best Ranking: {best_spearman['Metric']} with {best_spearman['Model']} (ρ={best_spearman['Spearman ρ']:.3f})")

# ============================================================================
# COMPARISON WITH BASELINE (from previous run)
# ============================================================================
print("\n" + "="*80)
print("IMPROVEMENT OVER BASELINE (Without Contextual Features)")
print("="*80)

baseline_results = {
    'SLS_Fplus_rolling': {'LR': -0.128, 'XGB': -0.051},
    'SLS_Fplus_fixed': {'LR': -0.135, 'XGB': 0.085},
    'Liveliness_xG': {'LR': -0.078, 'XGB': 0.008}
}

for metric_name, res in results.items():
    print(f"\n{res['label']}:")
    
    lr_baseline = baseline_results[metric_name]['LR']
    lr_enhanced = res['lr_metrics']['R2']
    lr_improvement = lr_enhanced - lr_baseline
    
    xgb_baseline = baseline_results[metric_name]['XGB']
    xgb_enhanced = res['xgb_metrics']['R2']
    xgb_improvement = xgb_enhanced - xgb_baseline
    
    print(f"  Linear Reg: {lr_baseline:.3f} → {lr_enhanced:.3f} (Δ {lr_improvement:+.3f})")
    print(f"  XGBoost:    {xgb_baseline:.3f} → {xgb_enhanced:.3f} (Δ {xgb_improvement:+.3f})")

# ============================================================================
# VISUALIZATIONS
# ============================================================================
print("\n[4/6] Generating visualizations...")

import os
os.makedirs('results_enhanced', exist_ok=True)

# 1. Comparison bars
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

for idx, metric in enumerate(['R²', 'MAE', 'RMSE', 'Spearman ρ']):
    ax = axes[idx // 2, idx % 2]
    pivot = summary_df.pivot(index='Metric', columns='Model', values=metric)
    pivot.plot(kind='bar', ax=ax, alpha=0.8, edgecolor='black', width=0.7)
    ax.set_title(f'{metric} - Enhanced Features', fontsize=14, fontweight='bold')
    ax.set_xlabel('Liveliness Metric', fontsize=12)
    ax.set_ylabel(metric, fontsize=12)
    ax.legend(title='Model')
    ax.grid(True, alpha=0.3, axis='y')
    if metric == 'R²':
        ax.axhline(y=0, color='red', linestyle='--', linewidth=2)
    ax.tick_params(axis='x', rotation=15)

plt.tight_layout()
plt.savefig('results_enhanced/comparison_enhanced.png', dpi=300, bbox_inches='tight')
print("  ✓ Saved: comparison_enhanced.png")
plt.close()

# 2. Feature importance (best model)
best_metric_name = best_r2['Metric']
for metric_name, res in results.items():
    if res['label'] == best_metric_name:
        best_res = res
        break

fig, axes = plt.subplots(1, 2, figsize=(18, 10))

# XGBoost importance
xgb_imp = pd.DataFrame({
    'feature': feature_cols,
    'importance': best_res['xgb_model'].feature_importances_
}).sort_values('importance', ascending=False).head(20)

axes[0].barh(range(len(xgb_imp)), xgb_imp['importance'],
             color='forestgreen', alpha=0.7, edgecolor='black')
axes[0].set_yticks(range(len(xgb_imp)))
axes[0].set_yticklabels(xgb_imp['feature'], fontsize=9)
axes[0].set_xlabel('Importance (Gain)', fontsize=11, fontweight='bold')
axes[0].set_title(f'Top 20 Features - XGBoost\n({best_metric_name})',
                  fontsize=12, fontweight='bold')
axes[0].grid(True, alpha=0.3, axis='x')

# Linear Regression coefficients
lr_coef = pd.DataFrame({
    'feature': feature_cols,
    'coefficient': best_res['lr_model'].coef_
}).sort_values('coefficient', key=abs, ascending=False).head(20)

colors = ['green' if x > 0 else 'red' for x in lr_coef['coefficient']]
axes[1].barh(range(len(lr_coef)), lr_coef['coefficient'],
             color=colors, alpha=0.7, edgecolor='black')
axes[1].set_yticks(range(len(lr_coef)))
axes[1].set_yticklabels(lr_coef['feature'], fontsize=9)
axes[1].set_xlabel('Coefficient', fontsize=11, fontweight='bold')
axes[1].set_title(f'Top 20 Features - Linear Regression\n({best_metric_name})',
                  fontsize=12, fontweight='bold')
axes[1].axvline(x=0, color='black', linestyle='-', linewidth=1)
axes[1].grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig('results_enhanced/feature_importance_enhanced.png', dpi=300, bbox_inches='tight')
print("  ✓ Saved: feature_importance_enhanced.png")
plt.close()

# 3. Predicted vs Actual
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for idx, (metric_name, res) in enumerate(results.items()):
    ax = axes[idx]
    
    if res['xgb_metrics']['R2'] > res['lr_metrics']['R2']:
        y_pred = res['xgb_pred']
        model_name = 'XGBoost'
        r2 = res['xgb_metrics']['R2']
    else:
        y_pred = res['lr_pred']
        model_name = 'Linear Reg'
        r2 = res['lr_metrics']['R2']
    
    y_test = res['y_test']
    
    ax.scatter(y_test, y_pred, alpha=0.6, s=50, edgecolors='black', linewidth=0.5)
    ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()],
            'r--', lw=2, label='Perfect')
    ax.set_xlabel('Actual', fontsize=11, fontweight='bold')
    ax.set_ylabel('Predicted', fontsize=11, fontweight='bold')
    ax.set_title(f'{res["label"]}\n({model_name}, R²={r2:.3f})',
                 fontsize=12, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('results_enhanced/predicted_vs_actual_enhanced.png', dpi=300, bbox_inches='tight')
print("  ✓ Saved: predicted_vs_actual_enhanced.png")
plt.close()

# ============================================================================
# SAVE REPORT
# ============================================================================
print("\n[5/6] Saving report...")

with open('results_enhanced/enhanced_report.txt', 'w', encoding='utf-8') as f:
    f.write("FOOTYLIVELINESS - ENHANCED MODEL WITH CONTEXTUAL FEATURES\n")
    f.write("="*80 + "\n\n")
    
    f.write("ENHANCEMENTS:\n")
    f.write("  Added 15+ contextual features:\n")
    f.write("  - League position & points\n")
    f.write("  - Form trajectory (last 3 vs previous 5)\n")
    f.write("  - Home/away strength ratios\n")
    f.write("  - High-stakes indicators\n\n")
    
    f.write("RESULTS:\n")
    f.write(summary_df.to_string(index=False))
    f.write("\n\n")
    
    f.write("BEST PERFORMERS:\n")
    f.write(f"  Best R²: {best_r2['Metric']} with {best_r2['Model']} (R²={best_r2['R²']:.3f})\n")
    f.write(f"  Best Ranking: {best_spearman['Metric']} with {best_spearman['Model']} (ρ={best_spearman['Spearman ρ']:.3f})\n\n")
    
    f.write("IMPROVEMENT vs BASELINE:\n")
    for metric_name, res in results.items():
        lr_improvement = res['lr_metrics']['R2'] - baseline_results[metric_name]['LR']
        xgb_improvement = res['xgb_metrics']['R2'] - baseline_results[metric_name]['XGB']
        f.write(f"  {res['label']}:\n")
        f.write(f"    Linear Reg: Δ {lr_improvement:+.3f}\n")
        f.write(f"    XGBoost:    Δ {xgb_improvement:+.3f}\n")

print("  ✓ Saved: enhanced_report.txt")

print("\n" + "="*80)
print("COMPLETE!")
print("="*80)
print(f"\n🏆 BEST MODEL: {best_r2['Metric']} with {best_r2['Model']}")
print(f"   R² = {best_r2['R²']:.3f}")
print(f"   Spearman ρ = {best_spearman['Spearman ρ']:.3f}")

if best_r2['R²'] > 0.15:
    print("\n✓ STRONG improvement! Contextual features are working!")
elif best_r2['R²'] > 0.05:
    print("\n⚠ Moderate improvement. Some signal captured.")
else:
    print("\n✗ Weak results. May need more features or different approach.")