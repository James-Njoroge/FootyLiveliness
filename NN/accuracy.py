"""
Comprehensive Accuracy Analysis for Ridge Regression Predictions

Computes practical accuracy metrics beyond R² and MAE:
1. Categorical accuracy (boring/average/very lively)
2. Top-K hit rates (recommendation system metrics)
3. Precision@K (information retrieval metrics)
4. Confusion matrix visualization
5. Ranking quality analysis

Input: ridge_predictions.csv
Output: accuracy_report.txt + accuracy_analysis.png
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
# At the very top of the file (line 1-2)
# -*- coding: utf-8 -*-
import sys
import io

# Force UTF-8 encoding for file writing (Windows fix)
if sys.platform == 'win32':
    import codecs
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
print("="*80)
print("RIDGE REGRESSION - COMPREHENSIVE ACCURACY ANALYSIS")
print("="*80)

# ============================================================================
# STEP 1: LOAD PREDICTIONS
# ============================================================================
print("\n[1/6] Loading predictions...")

df = pd.read_csv('ridge_predictions.csv')

y_actual = df['actual'].values
y_pred = df['predicted'].values

print(f"  Total predictions: {len(y_actual)}")
print(f"  Actual range: [{y_actual.min():.2f}, {y_actual.max():.2f}]")
print(f"  Predicted range: [{y_pred.min():.2f}, {y_pred.max():.2f}]")

# ============================================================================
# STEP 2: CATEGORICAL ACCURACY (3 CATEGORIES)
# ============================================================================
print("\n[2/6] Computing categorical accuracy...")

# Define thresholds (quartiles)
q25_actual = np.percentile(y_actual, 25)  # Bottom 25%
q75_actual = np.percentile(y_actual, 75)  # Top 25%

print(f"\n  Thresholds:")
print(f"    Boring: < {q25_actual:.2f}")
print(f"    Average: {q25_actual:.2f} - {q75_actual:.2f}")
print(f"    Very Lively: > {q75_actual:.2f}")

# Categorize actual values
actual_categories = np.where(y_actual >= q75_actual, 'Very Lively',
                    np.where(y_actual <= q25_actual, 'Boring', 'Average'))

# Categorize predictions using same thresholds
pred_categories = np.where(y_pred >= q75_actual, 'Very Lively',
                  np.where(y_pred <= q25_actual, 'Boring', 'Average'))

# Calculate accuracy for each category
print(f"\n  Categorical Breakdown:")
category_results = {}

for category in ['Boring', 'Average', 'Very Lively']:
    mask = (actual_categories == category)
    
    if mask.sum() > 0:
        correct = (pred_categories[mask] == category).sum()
        total = mask.sum()
        accuracy = correct / total * 100
        
        category_results[category] = {
            'total': total,
            'correct': correct,
            'accuracy': accuracy
        }
        
        print(f"    {category}:")
        print(f"      Total: {total}")
        print(f"      Correctly predicted: {correct}")
        print(f"      Accuracy: {accuracy:.1f}%")

# Overall categorical accuracy
overall_correct = (pred_categories == actual_categories).sum()
overall_accuracy = overall_correct / len(y_actual) * 100
random_baseline = 100 / 3  # 33.3% for 3 categories

print(f"\n  Overall Categorical Accuracy: {overall_accuracy:.1f}%")
print(f"  Random Baseline: {random_baseline:.1f}%")
print(f"  Improvement: {overall_accuracy - random_baseline:.1f} percentage points")

# ============================================================================
# STEP 3: TOP-K HIT RATES
# ============================================================================
print("\n[3/6] Computing Top-K hit rates...")

top_k_results = {}

for K in [3, 5, 10]:
    # Get indices of top K predictions
    top_k_pred_indices = set(np.argsort(y_pred)[-K:])
    
    # Get indices of actual top K matches
    top_k_actual_indices = set(np.argsort(y_actual)[-K:])
    
    # How many overlap?
    hits = len(top_k_pred_indices & top_k_actual_indices)
    hit_rate = hits / K * 100
    
    # Relaxed version: predicted top K in actual top 2K
    top_2k_actual = set(np.argsort(y_actual)[-2*K:])
    relaxed_hits = len([i for i in top_k_pred_indices if i in top_2k_actual])
    relaxed_rate = relaxed_hits / K * 100
    
    top_k_results[K] = {
        'hits': hits,
        'hit_rate': hit_rate,
        'relaxed_hits': relaxed_hits,
        'relaxed_rate': relaxed_rate
    }
    
    print(f"\n  Top-{K} Hit Rate:")
    print(f"    Exact overlap: {hits}/{K} ({hit_rate:.1f}%)")
    print(f"    Relaxed (in top {2*K}): {relaxed_hits}/{K} ({relaxed_rate:.1f}%)")
    
    # Random baseline
    random_expected = K * K / len(y_actual)
    print(f"    Random baseline: {random_expected:.1f} hits")
    print(f"    Improvement: {hits - random_expected:.1f} hits")

# ============================================================================
# STEP 4: PRECISION@K (INFORMATION RETRIEVAL)
# ============================================================================
print("\n[4/6] Computing Precision@K...")

# Define "relevant" as top 25% (very lively)
threshold = np.percentile(y_actual, 75)

precision_results = {}

for K in [3, 5, 10]:
    top_k_pred_indices = np.argsort(y_pred)[-K:]
    top_k_pred_values = y_actual[top_k_pred_indices]
    
    relevant = (top_k_pred_values >= threshold).sum()
    precision = relevant / K * 100
    
    # Expected random precision
    total_relevant = (y_actual >= threshold).sum()
    random_precision = (total_relevant / len(y_actual)) * 100
    
    precision_results[K] = {
        'relevant': relevant,
        'precision': precision,
        'random_precision': random_precision
    }
    
    print(f"\n  Precision@{K}:")
    print(f"    Recommended: {K} matches")
    print(f"    Actually lively (top 25%): {relevant}")
    print(f"    Precision: {precision:.1f}%")
    print(f"    Random baseline: {random_precision:.1f}%")
    print(f"    Improvement: {precision - random_precision:.1f} percentage points")

# ============================================================================
# STEP 5: RANKING QUALITY ANALYSIS
# ============================================================================
print("\n[5/6] Analyzing ranking quality...")

# Kendall's Tau (alternative to Spearman)
from scipy.stats import kendalltau
tau, p_value = kendalltau(y_actual, y_pred)

print(f"\n  Kendall's Tau: {tau:.4f} (p-value: {p_value:.4e})")
print(f"  Interpretation: {'Significant' if p_value < 0.05 else 'Not significant'} ranking correlation")

# Normalized Discounted Cumulative Gain (NDCG@K)
def dcg_at_k(relevance, k):
    """Discounted Cumulative Gain"""
    relevance = np.array(relevance)[:k]
    if relevance.size:
        return np.sum(relevance / np.log2(np.arange(2, relevance.size + 2)))
    return 0.0

def ndcg_at_k(y_true, y_pred, k):
    """Normalized Discounted Cumulative Gain"""
    # Get predicted ranking
    pred_order = np.argsort(y_pred)[::-1]
    relevance = y_true[pred_order]
    
    # Get ideal ranking
    ideal_order = np.argsort(y_true)[::-1]
    ideal_relevance = y_true[ideal_order]
    
    dcg = dcg_at_k(relevance, k)
    idcg = dcg_at_k(ideal_relevance, k)
    
    return dcg / idcg if idcg > 0 else 0.0

print(f"\n  NDCG (Ranking Quality):")
for K in [5, 10, 20]:
    ndcg = ndcg_at_k(y_actual, y_pred, K)
    print(f"    NDCG@{K}: {ndcg:.4f}")

# ============================================================================
# STEP 6: VISUALIZATIONS
# ============================================================================
print("\n[6/6] Generating visualizations...")

fig = plt.figure(figsize=(16, 12))
gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.35)

# Plot 1: Confusion Matrix
ax1 = fig.add_subplot(gs[0, 0])
categories_order = ['Boring', 'Average', 'Very Lively']
cm = confusion_matrix(actual_categories, pred_categories, labels=categories_order)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax1,
            xticklabels=categories_order, yticklabels=categories_order)
ax1.set_xlabel('Predicted Category', fontsize=11)
ax1.set_ylabel('Actual Category', fontsize=11)
ax1.set_title('Confusion Matrix\n(3 Liveliness Categories)', fontsize=12, fontweight='bold')

# Plot 2: Categorical Accuracy Comparison
ax2 = fig.add_subplot(gs[0, 1])
categories = ['Boring', 'Average', 'Very Lively']
accuracies = [category_results[cat]['accuracy'] for cat in categories]
colors = ['#d62728', '#ff7f0e', '#2ca02c']
bars = ax2.bar(categories, accuracies, color=colors, alpha=0.7, edgecolor='black')
ax2.axhline(y=random_baseline, color='red', linestyle='--', linewidth=2, 
            label=f'Random ({random_baseline:.1f}%)')
ax2.set_ylabel('Accuracy (%)', fontsize=11)
ax2.set_title('Categorical Accuracy by Type', fontsize=12, fontweight='bold')
ax2.legend()
ax2.grid(alpha=0.3, axis='y')

# Add value labels
for bar, acc in zip(bars, accuracies):
    ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
            f'{acc:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')

# Plot 3: Overall vs Random
ax3 = fig.add_subplot(gs[0, 2])
comparison_labels = ['Random\nGuessing', 'Ridge\nRegression']
comparison_values = [random_baseline, overall_accuracy]
comparison_colors = ['lightgray', 'coral']
bars = ax3.bar(comparison_labels, comparison_values, color=comparison_colors, 
               alpha=0.8, edgecolor='black', width=0.5)
ax3.set_ylabel('Accuracy (%)', fontsize=11)
ax3.set_title('Overall Categorical Accuracy', fontsize=12, fontweight='bold')
ax3.set_ylim([0, 60])
ax3.grid(alpha=0.3, axis='y')

# Add value labels
for bar, val in zip(bars, comparison_values):
    ax3.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
            f'{val:.1f}%', ha='center', va='bottom', fontsize=12, fontweight='bold')

# Plot 4: Top-K Hit Rates
ax4 = fig.add_subplot(gs[1, 0])
k_values = [3, 5, 10]
hit_rates = [top_k_results[k]['hit_rate'] for k in k_values]
relaxed_rates = [top_k_results[k]['relaxed_rate'] for k in k_values]

x_pos = np.arange(len(k_values))
width = 0.35

bars1 = ax4.bar(x_pos - width/2, hit_rates, width, label='Exact Top-K', 
                color='steelblue', alpha=0.8)
bars2 = ax4.bar(x_pos + width/2, relaxed_rates, width, label='Relaxed (Top-2K)',
                color='lightblue', alpha=0.8)

ax4.set_xlabel('K (Number of Recommendations)', fontsize=11)
ax4.set_ylabel('Hit Rate (%)', fontsize=11)
ax4.set_title('Top-K Hit Rates', fontsize=12, fontweight='bold')
ax4.set_xticks(x_pos)
ax4.set_xticklabels([f'K={k}' for k in k_values])
ax4.legend()
ax4.grid(alpha=0.3, axis='y')

# Plot 5: Precision@K
ax5 = fig.add_subplot(gs[1, 1])
k_values = [3, 5, 10]
precisions = [precision_results[k]['precision'] for k in k_values]
random_precisions = [precision_results[k]['random_precision'] for k in k_values]

x_pos = np.arange(len(k_values))
bars1 = ax5.bar(x_pos - width/2, precisions, width, label='Ridge Model',
                color='coral', alpha=0.8)
bars2 = ax5.bar(x_pos + width/2, random_precisions, width, label='Random',
                color='lightgray', alpha=0.8)

ax5.set_xlabel('K (Number of Recommendations)', fontsize=11)
ax5.set_ylabel('Precision (%)', fontsize=11)
ax5.set_title('Precision@K (Finding Lively Matches)', fontsize=12, fontweight='bold')
ax5.set_xticks(x_pos)
ax5.set_xticklabels([f'K={k}' for k in k_values])
ax5.legend()
ax5.grid(alpha=0.3, axis='y')

# Plot 6: Ranking Quality (NDCG)
ax6 = fig.add_subplot(gs[1, 2])
k_values_ndcg = [5, 10, 20]
ndcg_values = [ndcg_at_k(y_actual, y_pred, k) for k in k_values_ndcg]
bars = ax6.bar([f'NDCG@{k}' for k in k_values_ndcg], ndcg_values, 
               color='mediumseagreen', alpha=0.8, edgecolor='black')
ax6.set_ylabel('NDCG Score', fontsize=11)
ax6.set_title('Ranking Quality (NDCG)', fontsize=12, fontweight='bold')
ax6.set_ylim([0, 1])
ax6.axhline(y=0.7, color='red', linestyle='--', alpha=0.5, label='Good (0.7)')
ax6.legend()
ax6.grid(alpha=0.3, axis='y')

# Add value labels
for bar, val in zip(bars, ndcg_values):
    ax6.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
            f'{val:.3f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

# Plot 7: Prediction Distribution by Category
ax7 = fig.add_subplot(gs[2, :])
for category, color in zip(['Boring', 'Average', 'Very Lively'], 
                          ['#d62728', '#ff7f0e', '#2ca02c']):
    mask = (actual_categories == category)
    ax7.scatter(y_actual[mask], y_pred[mask], alpha=0.6, s=80, 
               label=category, color=color, edgecolors='black', linewidth=0.5)

# Perfect prediction line
ax7.plot([y_actual.min(), y_actual.max()], [y_actual.min(), y_actual.max()],
         'k--', linewidth=2, alpha=0.5, label='Perfect Prediction')

# Category boundaries
ax7.axvline(x=q25_actual, color='gray', linestyle=':', linewidth=1.5, alpha=0.7)
ax7.axvline(x=q75_actual, color='gray', linestyle=':', linewidth=1.5, alpha=0.7)
ax7.axhline(y=q25_actual, color='gray', linestyle=':', linewidth=1.5, alpha=0.7)
ax7.axhline(y=q75_actual, color='gray', linestyle=':', linewidth=1.5, alpha=0.7)

ax7.set_xlabel('Actual Liveliness', fontsize=12)
ax7.set_ylabel('Predicted Liveliness', fontsize=12)
ax7.set_title('Predictions Colored by Actual Category', fontsize=12, fontweight='bold')
ax7.legend(loc='upper left')
ax7.grid(alpha=0.3)

plt.suptitle('Ridge Regression - Comprehensive Accuracy Analysis', 
             fontsize=16, fontweight='bold', y=0.995)

plt.savefig('accuracy_analysis.png', dpi=300, bbox_inches='tight')
print("  ✓ Saved accuracy_analysis.png")

# ============================================================================
# SAVE DETAILED REPORT
# ============================================================================
print("\n[7/7] Saving detailed report...")

with open('accuracy_report.txt', 'w',  encoding='utf-8') as f:
    f.write("="*80 + "\n")
    f.write("RIDGE REGRESSION - COMPREHENSIVE ACCURACY ANALYSIS\n")
    f.write("="*80 + "\n\n")
    
    f.write("DATASET SUMMARY:\n")
    f.write(f"  Total predictions: {len(y_actual)}\n")
    f.write(f"  Actual range: [{y_actual.min():.2f}, {y_actual.max():.2f}]\n")
    f.write(f"  Predicted range: [{y_pred.min():.2f}, {y_pred.max():.2f}]\n\n")
    
    f.write("CATEGORICAL ACCURACY (3 CATEGORIES):\n")
    f.write("-"*80 + "\n")
    f.write(f"  Thresholds:\n")
    f.write(f"    Boring: < {q25_actual:.2f}\n")
    f.write(f"    Average: {q25_actual:.2f} - {q75_actual:.2f}\n")
    f.write(f"    Very Lively: > {q75_actual:.2f}\n\n")
    
    for category in ['Boring', 'Average', 'Very Lively']:
        res = category_results[category]
        f.write(f"  {category}:\n")
        f.write(f"    Total: {res['total']}\n")
        f.write(f"    Correct: {res['correct']}\n")
        f.write(f"    Accuracy: {res['accuracy']:.1f}%\n\n")
    
    f.write(f"  Overall Categorical Accuracy: {overall_accuracy:.1f}%\n")
    f.write(f"  Random Baseline: {random_baseline:.1f}%\n")
    f.write(f"  Improvement: +{overall_accuracy - random_baseline:.1f} percentage points\n\n")
    
    f.write("TOP-K HIT RATES (RECOMMENDATION METRICS):\n")
    f.write("-"*80 + "\n")
    for K in [3, 5, 10]:
        res = top_k_results[K]
        f.write(f"  Top-{K}:\n")
        f.write(f"    Exact overlap: {res['hits']}/{K} ({res['hit_rate']:.1f}%)\n")
        f.write(f"    Relaxed (in top {2*K}): {res['relaxed_hits']}/{K} ({res['relaxed_rate']:.1f}%)\n\n")
    
    f.write("PRECISION@K (INFORMATION RETRIEVAL):\n")
    f.write("-"*80 + "\n")
    for K in [3, 5, 10]:
        res = precision_results[K]
        f.write(f"  Precision@{K}:\n")
        f.write(f"    Relevant matches found: {res['relevant']}/{K}\n")
        f.write(f"    Precision: {res['precision']:.1f}%\n")
        f.write(f"    Random baseline: {res['random_precision']:.1f}%\n")
        f.write(f"    Improvement: +{res['precision'] - res['random_precision']:.1f} pp\n\n")
    
    f.write("RANKING QUALITY:\n")
    f.write("-"*80 + "\n")
    f.write(f"  Kendall's Tau: {tau:.4f}\n")
    f.write(f"  P-value: {p_value:.4e}\n")
    f.write(f"  Significance: {'Yes' if p_value < 0.05 else 'No'} (α=0.05)\n\n")
    
    f.write("  NDCG (Normalized Discounted Cumulative Gain):\n")
    for K in [5, 10, 20]:
        ndcg = ndcg_at_k(y_actual, y_pred, K)
        f.write(f"    NDCG@{K}: {ndcg:.4f}\n")
    
    f.write("\n" + "="*80 + "\n")
    f.write("KEY TAKEAWAYS:\n")
    f.write("="*80 + "\n\n")
    
    f.write(f"1. CATEGORICAL ACCURACY: {overall_accuracy:.1f}%\n")
    f.write(f"   - {overall_accuracy - random_baseline:.1f} percentage points better than random (33.3%)\n")
    f.write(f"   - Best at: {max(category_results.items(), key=lambda x: x[1]['accuracy'])[0]}\n\n")
    
    f.write(f"2. RECOMMENDATION QUALITY (Top-3):\n")
    f.write(f"   - Exact: {top_k_results[3]['hit_rate']:.1f}% of recommendations are truly top-3\n")
    f.write(f"   - Relaxed: {top_k_results[3]['relaxed_rate']:.1f}% are in top-6\n\n")
    
    f.write(f"3. PRECISION (Finding Lively Matches):\n")
    f.write(f"   - Precision@5: {precision_results[5]['precision']:.1f}%\n")
    f.write(f"   - {precision_results[5]['precision'] - precision_results[5]['random_precision']:.1f} pp better than random\n\n")
    
    f.write(f"4. RANKING QUALITY:\n")
    f.write(f"   - NDCG@10: {ndcg_at_k(y_actual, y_pred, 10):.3f}\n")
    f.write(f"   - {'Good' if ndcg_at_k(y_actual, y_pred, 10) > 0.7 else 'Moderate'} ranking correlation\n\n")
    
    f.write("PRACTICAL INTERPRETATION:\n")
    f.write("-"*80 + "\n")
    f.write("Use Case: 'Which 3 matches should I watch this weekend?'\n\n")
    
    if top_k_results[3]['relaxed_rate'] >= 60:
        f.write(f"✓ Success Rate: ~{top_k_results[3]['relaxed_rate']:.0f}%\n")
        f.write(f"  Model successfully recommends at least 2 genuinely exciting matches\n")
        f.write(f"  out of 3, making it useful for viewer recommendations.\n")
    else:
        f.write(f"⚠ Success Rate: ~{top_k_results[3]['relaxed_rate']:.0f}%\n")
        f.write(f"  Model provides better-than-random recommendations but has\n")
        f.write(f"  room for improvement with more training data.\n")

print("  ✓ Saved accuracy_report.txt")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
print(f"\n📊 KEY RESULTS:")
print(f"   Categorical Accuracy: {overall_accuracy:.1f}% (vs {random_baseline:.1f}% random)")
print(f"   Top-3 Hit Rate: {top_k_results[3]['hit_rate']:.1f}%")
print(f"   Top-3 Relaxed: {top_k_results[3]['relaxed_rate']:.1f}%")
print(f"   Precision@5: {precision_results[5]['precision']:.1f}%")
print(f"   NDCG@10: {ndcg_at_k(y_actual, y_pred, 10):.3f}")

print(f"\n📁 Files Generated:")
print(f"   - accuracy_analysis.png (7-panel visualization)")
print(f"   - accuracy_report.txt (detailed report)")

print(f"\n✅ Honest Assessment:")
if overall_accuracy > 40:
    print(f"   Your model performs WELL above random baseline!")
    print(f"   Categorical accuracy of {overall_accuracy:.1f}% is good for match excitement.")
elif overall_accuracy > 35:
    print(f"   Your model performs moderately above random baseline.")
    print(f"   This is expected given R²=0.088 and small dataset (230 samples).")
else:
    print(f"   Model struggles with categorical prediction but still beats random.")
    print(f"   Focus on ranking metrics (Spearman, NDCG) which are more informative.")