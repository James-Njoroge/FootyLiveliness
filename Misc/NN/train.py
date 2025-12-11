"""
Train Multi-Layer Perceptron (MLP) for Match Liveliness Prediction

Loads prepared data and trains a neural network to predict match liveliness.

Architecture:
  - Input: 37 features
  - Hidden layers: 64 → 32 → 16 neurons
  - Dropout + Batch Normalization for regularization
  - Output: 1 (liveliness score)

Compares against XGBoost baseline (R²=0.042, ρ=0.302)
"""

import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from scipy.stats import spearmanr
import matplotlib.pyplot as plt
import numpy as np
import time

print("="*80)
print("TRAINING MULTI-LAYER PERCEPTRON (MLP)")
print("="*80)

# ============================================================================
# STEP 1: LOAD PREPARED DATA
# ============================================================================
print("\n[1/7] Loading prepared data...")

data = torch.load('data_prepared_nn.pt', weights_only=False)
train_loader = data['train_loader']
val_loader = data['val_loader']
X_test = data['X_test']
y_test = data['y_test']
X_train = data['X_train']
y_train = data['y_train']
X_val = data['X_val']
y_val = data['y_val']
feature_cols = data['feature_cols']

input_dim = X_test.shape[1]

print(f"  Input dimension: {input_dim} features")
print(f"  Train samples: {len(X_train)}")
print(f"  Val samples: {len(X_val)}")
print(f"  Test samples: {len(X_test)}")

# ============================================================================
# STEP 2: DEFINE MLP ARCHITECTURE
# ============================================================================
print("\n[2/7] Defining MLP architecture...")

class LivelinessPredictor(nn.Module):
    def __init__(self, input_dim=37):
        super().__init__()
        self.network = nn.Sequential(
            # Layer 1: Input → 64
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.BatchNorm1d(64),
            nn.Dropout(0.3),
            
            # Layer 2: 64 → 32
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.BatchNorm1d(32),
            nn.Dropout(0.3),
            
            # Layer 3: 32 → 16
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Dropout(0.2),
            
            # Output layer: 16 → 1
            nn.Linear(16, 1)
        )
    
    def forward(self, x):
        return self.network(x)

model = LivelinessPredictor(input_dim=input_dim)

# Count parameters
total_params = sum(p.numel() for p in model.parameters())
trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)

print(f"  Architecture: {input_dim} → 64 → 32 → 16 → 1")
print(f"  Total parameters: {total_params:,}")
print(f"  Trainable parameters: {trainable_params:,}")

# ============================================================================
# STEP 3: TRAINING CONFIGURATION
# ============================================================================
print("\n[3/7] Setting up training configuration...")

criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training hyperparameters
epochs = 200
patience = 20
best_val_loss = float('inf')
patience_counter = 0
train_losses = []
val_losses = []

print(f"  Loss function: MSE")
print(f"  Optimizer: Adam (lr=0.001)")
print(f"  Max epochs: {epochs}")
print(f"  Early stopping patience: {patience}")

# ============================================================================
# STEP 4: TRAINING LOOP
# ============================================================================
print("\n[4/7] Training model...")
print("  " + "-"*60)

start_time = time.time()

for epoch in range(epochs):
    # ========== TRAINING ==========
    model.train()
    train_loss = 0
    for X_batch, y_batch in train_loader:
        optimizer.zero_grad()
        y_pred = model(X_batch)
        loss = criterion(y_pred, y_batch)
        loss.backward()
        optimizer.step()
        train_loss += loss.item()
    
    train_loss /= len(train_loader)
    train_losses.append(train_loss)
    
    # ========== VALIDATION ==========
    model.eval()
    val_loss = 0
    with torch.no_grad():
        for X_batch, y_batch in val_loader:
            y_pred = model(X_batch)
            loss = criterion(y_pred, y_batch)
            val_loss += loss.item()
    
    val_loss /= len(val_loader)
    val_losses.append(val_loss)
    
    # ========== EARLY STOPPING ==========
    if val_loss < best_val_loss:
        best_val_loss = val_loss
        patience_counter = 0
        torch.save(model.state_dict(), 'best_mlp_model.pt')
    else:
        patience_counter += 1
    
    # Print progress every 20 epochs
    if (epoch + 1) % 20 == 0:
        print(f"  Epoch {epoch+1:3d}/{epochs} | Train Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f} | Patience: {patience_counter}/{patience}")
    
    # Early stopping
    if patience_counter >= patience:
        print(f"\n  ✓ Early stopping at epoch {epoch+1}")
        break

training_time = time.time() - start_time
print(f"  ✓ Training completed in {training_time:.1f} seconds ({training_time/60:.1f} minutes)")

# ============================================================================
# STEP 5: LOAD BEST MODEL AND EVALUATE
# ============================================================================
print("\n[5/7] Loading best model and evaluating...")

model.load_state_dict(torch.load('best_mlp_model.pt'))
model.eval()

# Test evaluation
with torch.no_grad():
    y_pred_test = model(X_test).numpy()
    y_true_test = y_test.numpy()
    
    # Also evaluate on train and val for comparison
    y_pred_train = model(X_train).numpy()
    y_true_train = y_train.numpy()
    
    y_pred_val = model(X_val).numpy()
    y_true_val = y_val.numpy()

# Metrics
r2_test = r2_score(y_true_test, y_pred_test)
mae_test = mean_absolute_error(y_true_test, y_pred_test)
rmse_test = np.sqrt(mean_squared_error(y_true_test, y_pred_test))
spearman_test = spearmanr(y_true_test, y_pred_test)[0]

r2_train = r2_score(y_true_train, y_pred_train)
r2_val = r2_score(y_true_val, y_pred_val)

print(f"  Test  - R²: {r2_test:.4f}, MAE: {mae_test:.4f}, RMSE: {rmse_test:.4f}, Spearman ρ: {spearman_test:.4f}")
print(f"  Train - R²: {r2_train:.4f}")
print(f"  Val   - R²: {r2_val:.4f}")

# ============================================================================
# STEP 6: COMPARISON WITH BASELINE
# ============================================================================
print("\n[6/7] Comparing with XGBoost baseline...")

baseline_r2 = 0.042
baseline_spearman = 0.302
baseline_mae = 1.15

r2_improvement = r2_test - baseline_r2
spearman_improvement = spearman_test - baseline_spearman
mae_improvement = baseline_mae - mae_test

print("\n  " + "="*60)
print("  RESULTS COMPARISON")
print("  " + "="*60)
print(f"  {'Metric':<20} {'XGBoost':>12} {'MLP':>12} {'Improvement':>15}")
print("  " + "-"*60)
print(f"  {'R²':<20} {baseline_r2:>12.4f} {r2_test:>12.4f} {r2_improvement:>+15.4f}")
print(f"  {'Spearman ρ':<20} {baseline_spearman:>12.4f} {spearman_test:>12.4f} {spearman_improvement:>+15.4f}")
print(f"  {'MAE':<20} {baseline_mae:>12.4f} {mae_test:>12.4f} {mae_improvement:>+15.4f}")
print("  " + "="*60)

if r2_test > baseline_r2:
    print(f"\n  🎉 SUCCESS! MLP outperforms XGBoost baseline by {r2_improvement:.4f} R²")
elif r2_test > 0:
    print(f"\n  ✓ POSITIVE R²! MLP explains {r2_test*100:.1f}% of variance")
else:
    print(f"\n  ⚠ Negative R². Model needs tuning (try lower dropout, more epochs, or simpler architecture)")

# ============================================================================
# STEP 7: VISUALIZATIONS
# ============================================================================
print("\n[7/7] Generating visualizations...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: Training curves
axes[0, 0].plot(train_losses, label='Train Loss', alpha=0.7)
axes[0, 0].plot(val_losses, label='Val Loss', alpha=0.7)
axes[0, 0].axhline(y=best_val_loss, color='r', linestyle='--', alpha=0.5, label=f'Best Val Loss ({best_val_loss:.4f})')
axes[0, 0].set_xlabel('Epoch')
axes[0, 0].set_ylabel('Loss (MSE)')
axes[0, 0].set_title('Training and Validation Loss')
axes[0, 0].legend()
axes[0, 0].grid(alpha=0.3)

# Plot 2: Predicted vs Actual (Test Set)
axes[0, 1].scatter(y_true_test, y_pred_test, alpha=0.6, s=50)
axes[0, 1].plot([y_true_test.min(), y_true_test.max()], 
                [y_true_test.min(), y_true_test.max()], 
                'r--', linewidth=2, label='Perfect Prediction')
axes[0, 1].set_xlabel('Actual Liveliness')
axes[0, 1].set_ylabel('Predicted Liveliness')
axes[0, 1].set_title(f'MLP Predictions (Test Set)\nR²={r2_test:.3f}, ρ={spearman_test:.3f}')
axes[0, 1].legend()
axes[0, 1].grid(alpha=0.3)

# Plot 3: Residuals
residuals = y_true_test.flatten() - y_pred_test.flatten()
axes[1, 0].scatter(y_pred_test, residuals, alpha=0.6, s=50)
axes[1, 0].axhline(y=0, color='r', linestyle='--', linewidth=2)
axes[1, 0].set_xlabel('Predicted Liveliness')
axes[1, 0].set_ylabel('Residuals (Actual - Predicted)')
axes[1, 0].set_title('Residual Plot')
axes[1, 0].grid(alpha=0.3)

# Plot 4: Performance comparison
metrics_names = ['R²', 'Spearman ρ', 'MAE\n(lower is better)']
xgb_scores = [baseline_r2, baseline_spearman, -baseline_mae]  # Negative MAE for visualization
mlp_scores = [r2_test, spearman_test, -mae_test]

x_pos = np.arange(len(metrics_names))
width = 0.35

bars1 = axes[1, 1].bar(x_pos - width/2, xgb_scores, width, label='XGBoost', alpha=0.8)
bars2 = axes[1, 1].bar(x_pos + width/2, mlp_scores, width, label='MLP', alpha=0.8)

axes[1, 1].set_xlabel('Metric')
axes[1, 1].set_ylabel('Score')
axes[1, 1].set_title('MLP vs XGBoost Baseline Comparison')
axes[1, 1].set_xticks(x_pos)
axes[1, 1].set_xticklabels(metrics_names)
axes[1, 1].legend()
axes[1, 1].grid(alpha=0.3, axis='y')
axes[1, 1].axhline(y=0, color='black', linewidth=0.5)

plt.tight_layout()
plt.savefig('mlp_results.png', dpi=300, bbox_inches='tight')
print("  ✓ Saved mlp_results.png")

# ============================================================================
# SAVE RESULTS
# ============================================================================
print("\n[8/8] Saving results...")

# Save predictions
results_df = {
    'actual': y_true_test.flatten(),
    'predicted': y_pred_test.flatten(),
    'residual': residuals
}
import pandas as pd
pd.DataFrame(results_df).to_csv('mlp_predictions.csv', index=False)
print("  ✓ Saved mlp_predictions.csv")

# Save summary report
with open('mlp_report.txt', 'w') as f:
    f.write("="*80 + "\n")
    f.write("MLP TRAINING REPORT - MATCH LIVELINESS PREDICTION\n")
    f.write("="*80 + "\n\n")
    
    f.write("DATASET:\n")
    f.write(f"  Training samples:   {len(X_train)}\n")
    f.write(f"  Validation samples: {len(X_val)}\n")
    f.write(f"  Test samples:       {len(X_test)}\n")
    f.write(f"  Features:           {input_dim}\n\n")
    
    f.write("ARCHITECTURE:\n")
    f.write(f"  Layers: {input_dim} → 64 → 32 → 16 → 1\n")
    f.write(f"  Total parameters: {total_params:,}\n")
    f.write(f"  Dropout: 0.3 (layers 1-2), 0.2 (layer 3)\n")
    f.write(f"  Activation: ReLU\n")
    f.write(f"  Normalization: Batch Normalization\n\n")
    
    f.write("TRAINING:\n")
    f.write(f"  Optimizer: Adam (lr=0.001)\n")
    f.write(f"  Loss: MSE\n")
    f.write(f"  Epochs trained: {epoch+1}\n")
    f.write(f"  Best val loss: {best_val_loss:.4f}\n")
    f.write(f"  Training time: {training_time:.1f}s\n\n")
    
    f.write("RESULTS (Test Set):\n")
    f.write(f"  R²:          {r2_test:.4f}\n")
    f.write(f"  MAE:         {mae_test:.4f}\n")
    f.write(f"  RMSE:        {rmse_test:.4f}\n")
    f.write(f"  Spearman ρ:  {spearman_test:.4f}\n\n")
    
    f.write("OVERFITTING CHECK:\n")
    f.write(f"  Train R²: {r2_train:.4f}\n")
    f.write(f"  Val R²:   {r2_val:.4f}\n")
    f.write(f"  Test R²:  {r2_test:.4f}\n")
    if r2_train - r2_test > 0.15:
        f.write("  ⚠ WARNING: Possible overfitting (train R² >> test R²)\n\n")
    else:
        f.write("  ✓ No significant overfitting detected\n\n")
    
    f.write("COMPARISON WITH BASELINE:\n")
    f.write(f"  {'Metric':<15} {'XGBoost':>12} {'MLP':>12} {'Improvement':>15}\n")
    f.write("  " + "-"*55 + "\n")
    f.write(f"  {'R²':<15} {baseline_r2:>12.4f} {r2_test:>12.4f} {r2_improvement:>+15.4f}\n")
    f.write(f"  {'Spearman ρ':<15} {baseline_spearman:>12.4f} {spearman_test:>12.4f} {spearman_improvement:>+15.4f}\n")
    f.write(f"  {'MAE':<15} {baseline_mae:>12.4f} {mae_test:>12.4f} {mae_improvement:>+15.4f}\n\n")

print("  ✓ Saved mlp_report.txt")

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "="*80)
print("MLP TRAINING COMPLETE")
print("="*80)
print(f"\n🎯 FINAL RESULTS:")
print(f"   R²: {r2_test:.4f} (baseline: {baseline_r2:.4f})")
print(f"   Spearman ρ: {spearman_test:.4f} (baseline: {baseline_spearman:.4f})")
print(f"   MAE: {mae_test:.4f} (baseline: {baseline_mae:.4f})")

if r2_test > baseline_r2 and spearman_test > baseline_spearman:
    print(f"\n🏆 SUCCESS! MLP beats baseline on both R² and Spearman ρ!")
elif r2_test > baseline_r2:
    print(f"\n✓ IMPROVEMENT! MLP beats baseline on R²")
elif r2_test > 0:
    print(f"\n✓ POSITIVE! MLP achieves positive R²")
else:
    print(f"\n⚠ Model needs tuning. Try adjusting hyperparameters.")

print(f"\n📁 Files Generated:")
print(f"   - best_mlp_model.pt (model weights)")
print(f"   - mlp_results.png (visualizations)")
print(f"   - mlp_predictions.csv (test predictions)")
print(f"   - mlp_report.txt (detailed report)")
print(f"\n✅ Ready to compare with baseline or try advanced architectures!")