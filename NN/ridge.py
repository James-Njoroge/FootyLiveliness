"""
Train Ridge Regression for Match Liveliness Prediction

Ridge Regression = Linear Regression + L2 Regularization
Perfect for small datasets (230 training samples)

Architecture:
  - Linear model with regularization (no hidden layers)
  - Alpha (regularization strength) tuned via cross-validation
  - Much more stable than neural networks for small data

Compares against XGBoost baseline (R²=0.042, rho=0.302)
"""

import torch
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge, RidgeCV
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from scipy.stats import spearmanr
import time

print("="*80)
print("TRAINING RIDGE REGRESSION")
print("="*80)

# ============================================================================
# STEP 1: LOAD PREPARED DATA
# ============================================================================
print("\n[1/6] Loading prepared data...")

data = torch.load('data_prepared_nn.pt', weights_only=False)

# Convert to numpy
X_train = data['X_train'].numpy()
y_train = data['y_train'].numpy().flatten()
X_val = data['X_val'].numpy()
y_val = data['y_val'].numpy().flatten()
X_test = data['X_test'].numpy()
y_test = data['y_test'].numpy().flatten()

feature_cols = data['feature_cols']

print(f"  Train samples: {len(X_train)}")
print(f"  Val samples: {len(X_val)}")
print(f"  Test samples: {len(X_test)}")
print(f"  Features: {X_train.shape[1]}")

# ============================================================================
# STEP 2: TUNE ALPHA WITH CROSS-VALIDATION
# ============================================================================
print("\n[2/6] Tuning regularization strength (alpha) with cross-validation...")

# Test different alpha values
alphas = [0.001, 0.01, 0.1, 0.5, 1.0, 5.0, 10.0, 50.0, 100.0]

# Use RidgeCV for automatic cross-validation
ridge_cv = RidgeCV(alphas=alphas, cv=5, scoring='r2')
ridge_cv.fit(X_train, y_train)

best_alpha = ridge_cv.alpha_

print(f"  Tested alphas: {alphas}")
print(f"  Best alpha: {best_alpha}")
print(f"  CV R² with best alpha: {ridge_cv.best_score_:.4f}")

# ============================================================================
# STEP 3: TRAIN FINAL MODEL WITH BEST ALPHA
# ============================================================================
print("\n[3/6] Training final Ridge model with best alpha...")

start_time = time.time()

model = Ridge(alpha=best_alpha)
model.fit(X_train, y_train)

training_time = time.time() - start_time

print(f"  ✓ Training completed in {training_time:.3f} seconds")

# ============================================================================
# STEP 4: EVALUATE ON ALL SPLITS
# ============================================================================
print("\n[4/6] Evaluating on train/val/test sets...")

# Predictions
y_pred_train = model.predict(X_train)
y_pred_val = model.predict(X_val)
y_pred_test = model.predict(X_test)

# Metrics - Train
r2_train = r2_score(y_train, y_pred_train)
mae_train = mean_absolute_error(y_train, y_pred_train)
rmse_train = np.sqrt(mean_squared_error(y_train, y_pred_train))
spearman_train = spearmanr(y_train, y_pred_train)[0]

# Metrics - Validation
r2_val = r2_score(y_val, y_pred_val)
mae_val = mean_absolute_error(y_val, y_pred_val)
rmse_val = np.sqrt(mean_squared_error(y_val, y_pred_val))
spearman_val = spearmanr(y_val, y_pred_val)[0]

# Metrics - Test
r2_test = r2_score(y_test, y_pred_test)
mae_test = mean_absolute_error(y_test, y_pred_test)
rmse_test = np.sqrt(mean_squared_error(y_test, y_pred_test))
spearman_test = spearmanr(y_test, y_pred_test)[0]

print(f"\n  Train - R²: {r2_train:.4f}, MAE: {mae_train:.4f}, RMSE: {rmse_train:.4f}, rho: {spearman_train:.4f}")
print(f"  Val   - R²: {r2_val:.4f}, MAE: {mae_val:.4f}, RMSE: {rmse_val:.4f}, rho: {spearman_val:.4f}")
print(f"  Test  - R²: {r2_test:.4f}, MAE: {mae_test:.4f}, RMSE: {rmse_test:.4f}, rho: {spearman_test:.4f}")

# Overfitting check
if r2_train - r2_test > 0.15:
    print(f"\n  ⚠ WARNING: Possible overfitting (train R² - test R² = {r2_train - r2_test:.4f})")
else:
    print(f"\n  ✓ No significant overfitting (train R² - test R² = {r2_train - r2_test:.4f})")

# ============================================================================
# STEP 5: FEATURE IMPORTANCE ANALYSIS
# ============================================================================
print("\n[5/6] Analyzing feature importance...")

# Get coefficients
coefficients = model.coef_

# Create feature importance dataframe
feature_importance = pd.DataFrame({
    'feature': feature_cols,
    'coefficient': coefficients,
    'abs_coefficient': np.abs(coefficients)
}).sort_values('abs_coefficient', ascending=False)

print("\n  Top 10 Most Important Features:")
print("  " + "-"*60)
for idx, row in feature_importance.head(10).iterrows():
    print(f"  {row['feature']:<30} {row['coefficient']:>10.4f}")

# ============================================================================
# STEP 6: COMPARISON WITH BASELINE
# ============================================================================
print("\n[6/6] Comparing with XGBoost baseline...")

baseline_r2 = 0.042
baseline_spearman = 0.302
baseline_mae = 1.15

r2_improvement = r2_test - baseline_r2
spearman_improvement = spearman_test - baseline_spearman
mae_improvement = baseline_mae - mae_test

print("\n  " + "="*60)
print("  RESULTS COMPARISON")
print("  " + "="*60)
print(f"  {'Metric':<20} {'XGBoost':>12} {'Ridge':>12} {'Improvement':>15}")
print("  " + "-"*60)
print(f"  {'R²':<20} {baseline_r2:>12.4f} {r2_test:>12.4f} {r2_improvement:>+15.4f}")
print(f"  {'Spearman rho':<20} {baseline_spearman:>12.4f} {spearman_test:>12.4f} {spearman_improvement:>+15.4f}")
print(f"  {'MAE':<20} {baseline_mae:>12.4f} {mae_test:>12.4f} {mae_improvement:>+15.4f}")
print("  " + "="*60)

if r2_test > baseline_r2:
    print(f"\n  🎉 SUCCESS! Ridge outperforms XGBoost baseline by {r2_improvement:.4f} R²")
elif r2_test > 0:
    print(f"\n  ✓ POSITIVE R²! Ridge explains {r2_test*100:.1f}% of variance")
else:
    print(f"\n  ⚠ Negative R². Data or features may have issues.")

# ============================================================================
# VISUALIZATIONS
# ============================================================================
print("\n[7/7] Generating visualizations...")

fig = plt.figure(figsize=(16, 10))

# Create grid for subplots
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# Plot 1: Predicted vs Actual (Test Set)
ax1 = fig.add_subplot(gs[0, 0])
ax1.scatter(y_test, y_pred_test, alpha=0.6, s=60, edgecolors='black', linewidth=0.5)
ax1.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 
         'r--', linewidth=2, label='Perfect Prediction')
ax1.set_xlabel('Actual Liveliness', fontsize=11)
ax1.set_ylabel('Predicted Liveliness', fontsize=11)
ax1.set_title(f'Ridge Predictions (Test Set)\nR²={r2_test:.3f}, rho={spearman_test:.3f}', 
              fontsize=12, fontweight='bold')
ax1.legend()
ax1.grid(alpha=0.3)

# Plot 2: Residuals
ax2 = fig.add_subplot(gs[0, 1])
residuals = y_test - y_pred_test
ax2.scatter(y_pred_test, residuals, alpha=0.6, s=60, edgecolors='black', linewidth=0.5)
ax2.axhline(y=0, color='r', linestyle='--', linewidth=2)
ax2.set_xlabel('Predicted Liveliness', fontsize=11)
ax2.set_ylabel('Residuals (Actual - Predicted)', fontsize=11)
ax2.set_title('Residual Plot', fontsize=12, fontweight='bold')
ax2.grid(alpha=0.3)

# Plot 3: Performance Comparison
ax3 = fig.add_subplot(gs[0, 2])
metrics_names = ['R²', 'Spearman rho']
xgb_scores = [baseline_r2, baseline_spearman]
ridge_scores = [r2_test, spearman_test]

x_pos = np.arange(len(metrics_names))
width = 0.35

bars1 = ax3.bar(x_pos - width/2, xgb_scores, width, label='XGBoost', alpha=0.8, color='steelblue')
bars2 = ax3.bar(x_pos + width/2, ridge_scores, width, label='Ridge', alpha=0.8, color='coral')

ax3.set_ylabel('Score', fontsize=11)
ax3.set_title('Ridge vs XGBoost Comparison', fontsize=12, fontweight='bold')
ax3.set_xticks(x_pos)
ax3.set_xticklabels(metrics_names)
ax3.legend()
ax3.grid(alpha=0.3, axis='y')
ax3.axhline(y=0, color='black', linewidth=0.5)

# Add value labels on bars
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}', ha='center', va='bottom', fontsize=9)

# Plot 4: Feature Importance (Top 15)
ax4 = fig.add_subplot(gs[1, :])
top_features = feature_importance.head(15)
colors = ['green' if c > 0 else 'red' for c in top_features['coefficient']]
ax4.barh(range(len(top_features)), top_features['coefficient'], color=colors, alpha=0.7)
ax4.set_yticks(range(len(top_features)))
ax4.set_yticklabels(top_features['feature'], fontsize=9)
ax4.set_xlabel('Coefficient Value', fontsize=11)
ax4.set_title('Top 15 Most Important Features (by absolute coefficient)', 
              fontsize=12, fontweight='bold')
ax4.axvline(x=0, color='black', linewidth=0.8)
ax4.grid(alpha=0.3, axis='x')
ax4.invert_yaxis()

# Plot 5: R² across splits
ax5 = fig.add_subplot(gs[2, 0])
splits = ['Train', 'Val', 'Test']
r2_scores = [r2_train, r2_val, r2_test]
colors_splits = ['lightgreen', 'lightblue', 'lightcoral']
bars = ax5.bar(splits, r2_scores, color=colors_splits, alpha=0.8, edgecolor='black')
ax5.set_ylabel('R² Score', fontsize=11)
ax5.set_title('R² Across Train/Val/Test', fontsize=12, fontweight='bold')
ax5.axhline(y=0, color='black', linewidth=0.8)
ax5.grid(alpha=0.3, axis='y')
for bar, score in zip(bars, r2_scores):
    ax5.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
            f'{score:.3f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

# Plot 6: MAE comparison
ax6 = fig.add_subplot(gs[2, 1])
mae_names = ['XGBoost', 'Ridge']
mae_values = [baseline_mae, mae_test]
colors_mae = ['steelblue', 'coral']
bars = ax6.bar(mae_names, mae_values, color=colors_mae, alpha=0.8, edgecolor='black')
ax6.set_ylabel('MAE (Lower is Better)', fontsize=11)
ax6.set_title('MAE Comparison', fontsize=12, fontweight='bold')
ax6.grid(alpha=0.3, axis='y')
for bar, mae in zip(bars, mae_values):
    ax6.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
            f'{mae:.3f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

# Plot 7: Alpha tuning visualization
ax7 = fig.add_subplot(gs[2, 2])
# Manually evaluate each alpha for visualization
alpha_scores = []
for alpha in alphas:
    temp_model = Ridge(alpha=alpha)
    temp_model.fit(X_train, y_train)
    val_pred = temp_model.predict(X_val)
    alpha_scores.append(r2_score(y_val, val_pred))

ax7.plot(alphas, alpha_scores, marker='o', linewidth=2, markersize=8, color='purple')
ax7.axvline(x=best_alpha, color='red', linestyle='--', linewidth=2, 
            label=f'Best α={best_alpha}')
ax7.set_xscale('log')
ax7.set_xlabel('Alpha (Regularization Strength)', fontsize=11)
ax7.set_ylabel('Validation R²', fontsize=11)
ax7.set_title('Alpha Tuning Curve', fontsize=12, fontweight='bold')
ax7.legend()
ax7.grid(alpha=0.3)

plt.suptitle('Ridge Regression - Complete Analysis', fontsize=16, fontweight='bold', y=0.995)

plt.savefig('ridge_results.png', dpi=300, bbox_inches='tight')
print("  ✓ Saved ridge_results.png")

# ============================================================================
# SAVE RESULTS
# ============================================================================
print("\n[8/8] Saving results...")

# Save predictions
predictions_df = pd.DataFrame({
    'actual': y_test,
    'predicted': y_pred_test,
    'residual': residuals
})
predictions_df.to_csv('ridge_predictions.csv', index=False)
print("  ✓ Saved ridge_predictions.csv")

# Save feature importance
feature_importance.to_csv('ridge_feature_importance.csv', index=False)
print("  ✓ Saved ridge_feature_importance.csv")

# Save model (using joblib for sklearn models)
import joblib
joblib.dump(model, 'ridge_model.pkl')
print("  ✓ Saved ridge_model.pkl")

# Save detailed report
with open('ridge_report.txt', 'w', encoding='utf-8') as f:
    f.write("="*80 + "\n")
    f.write("RIDGE REGRESSION REPORT - MATCH LIVELINESS PREDICTION\n")
    f.write("="*80 + "\n\n")
    
    f.write("DATASET:\n")
    f.write(f"  Training samples:   {len(X_train)}\n")
    f.write(f"  Validation samples: {len(X_val)}\n")
    f.write(f"  Test samples:       {len(X_test)}\n")
    f.write(f"  Features:           {X_train.shape[1]}\n\n")
    
    f.write("MODEL:\n")
    f.write(f"  Algorithm: Ridge Regression (L2 regularization)\n")
    f.write(f"  Best alpha: {best_alpha}\n")
    f.write(f"  Alpha tuning: Cross-validation (5 folds)\n")
    f.write(f"  Alphas tested: {alphas}\n")
    f.write(f"  Training time: {training_time:.3f}s\n\n")
    
    f.write("RESULTS:\n")
    f.write(f"  Train - R²: {r2_train:.4f}, MAE: {mae_train:.4f}, RMSE: {rmse_train:.4f}, rho: {spearman_train:.4f}\n")
    f.write(f"  Val   - R²: {r2_val:.4f}, MAE: {mae_val:.4f}, RMSE: {rmse_val:.4f}, rho: {spearman_val:.4f}\n")
    f.write(f"  Test  - R²: {r2_test:.4f}, MAE: {mae_test:.4f}, RMSE: {rmse_test:.4f}, rho: {spearman_test:.4f}\n\n")
    
    f.write("OVERFITTING CHECK:\n")
    f.write(f"  Train - Test R² difference: {r2_train - r2_test:.4f}\n")
    if r2_train - r2_test > 0.15:
        f.write("  Status: ⚠ WARNING - Possible overfitting\n\n")
    else:
        f.write("  Status: ✓ No significant overfitting\n\n")
    
    f.write("COMPARISON WITH BASELINE:\n")
    f.write(f"  {'Metric':<15} {'XGBoost':>12} {'Ridge':>12} {'Improvement':>15}\n")
    f.write("  " + "-"*55 + "\n")
    f.write(f"  {'R²':<15} {baseline_r2:>12.4f} {r2_test:>12.4f} {r2_improvement:>+15.4f}\n")
    f.write(f"  {'Spearman rho':<15} {baseline_spearman:>12.4f} {spearman_test:>12.4f} {spearman_improvement:>+15.4f}\n")
    f.write(f"  {'MAE':<15} {baseline_mae:>12.4f} {mae_test:>12.4f} {mae_improvement:>+15.4f}\n\n")
    
    f.write("TOP 15 MOST IMPORTANT FEATURES:\n")
    f.write("-"*80 + "\n")
    f.write(f"{'Rank':<6} {'Feature':<35} {'Coefficient':>15}\n")
    f.write("-"*80 + "\n")
    for idx, (_, row) in enumerate(feature_importance.head(15).iterrows(), 1):
        f.write(f"{idx:<6} {row['feature']:<35} {row['coefficient']:>15.6f}\n")

print("  ✓ Saved ridge_report.txt")

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "="*80)
print("RIDGE REGRESSION COMPLETE")
print("="*80)
print(f"\n🎯 FINAL RESULTS:")
print(f"   R²: {r2_test:.4f} (baseline: {baseline_r2:.4f}, improvement: {r2_improvement:+.4f})")
print(f"   Spearman rho: {spearman_test:.4f} (baseline: {baseline_spearman:.4f}, improvement: {spearman_improvement:+.4f})")
print(f"   MAE: {mae_test:.4f} (baseline: {baseline_mae:.4f}, improvement: {mae_improvement:+.4f})")

if r2_test > baseline_r2 and spearman_test > baseline_spearman:
    print(f"\n🏆 SUCCESS! Ridge beats baseline on both R² and Spearman rho!")
elif r2_test > baseline_r2:
    print(f"\n✓ IMPROVEMENT! Ridge beats baseline on R²")
elif r2_test > 0:
    print(f"\n✓ POSITIVE! Ridge achieves positive R² ({r2_test*100:.1f}% variance explained)")
else:
    print(f"\n⚠ Negative R². Check data quality and feature engineering.")

print(f"\n📊 Overfitting Status:")
if r2_train - r2_test < 0.05:
    print(f"   ✓ Excellent generalization (train-test gap: {r2_train - r2_test:.4f})")
elif r2_train - r2_test < 0.15:
    print(f"   ✓ Good generalization (train-test gap: {r2_train - r2_test:.4f})")
else:
    print(f"   ⚠ Some overfitting (train-test gap: {r2_train - r2_test:.4f})")

print(f"\n📁 Files Generated:")
print(f"   - ridge_model.pkl (trained model)")
print(f"   - ridge_results.png (7-panel visualization)")
print(f"   - ridge_predictions.csv (test predictions)")
print(f"   - ridge_feature_importance.csv (feature coefficients)")
print(f"   - ridge_report.txt (detailed report)")

print(f"\n✅ Ridge Regression is your new baseline!")
print(f"   Use this model until you get more data (2023/24, 2022/23 seasons)")