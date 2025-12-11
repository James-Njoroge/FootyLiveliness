# Target Metric Experiments

This folder contains scripts to explore alternative target metrics for match liveliness prediction, as suggested by your friend.

## Objective

Find the best target metric that captures:
- ✅ Shot volume and quality (No. of shots, xG)
- ✅ End-to-end attacking
- ✅ Lots of chances (low xG but many opportunities)
- ✅ Transitions (intense with low quality)
- ✅ Cards

## Workflow

### Step 1: Create Alternative Target Metrics
```bash
cd target_metric_experiments
python3 01_create_alternative_targets.py
```

**What it does:**
- Extracts cards data from raw JSON files
- Creates 7 different target metrics with varying complexity
- Outputs: `targets_comparison.csv` and `targets_summary_stats.csv`

**Target Metrics Created:**
1. **Simple xG** (current baseline) - `xG_total + min(xG_home, xG_away)`
2. **Shot Quality** - Weighted: xG (50%), shots (30%), SoT (20%)
3. **Chances-Focused** - Emphasizes opportunities: shots (40%), big chances (30%), xG (30%)
4. **End-to-End** - Rewards competitiveness: `xG_total + 2*min(xG) + min(shots)`
5. **Intensity** - Includes cards: xG (30%), shots (20%), corners (20%), cards (15%), big chances (15%)
6. **Comprehensive** - All factors: xG (25%), shots (20%), SoT (15%), big chances (15%), corners (15%), cards (10%)
7. **Minimal** - Just basics: xG (60%), shots (40%)

**Runtime:** ~30 seconds

---

### Step 2: Compare Target Metrics
```bash
python3 02_compare_target_metrics.py
```

**What it does:**
- Trains Ridge Regression on each target metric
- Uses your existing 37 features
- Evaluates on train/val/test splits
- Compares R², MAE, Spearman ρ, Top-10 hit rate

**Outputs:**
- `target_metrics_comparison_results.csv` - Detailed metrics for all targets
- `target_metrics_comparison_report.txt` - Human-readable report with recommendation
- `target_metrics_comparison.png` - Visualization comparing all metrics

**Runtime:** ~1-2 minutes

---

### Step 3: Train Multiple Models on Best Target
```bash
python3 03_train_best_target.py
```

**What it does:**
- Takes the winning target metric from Step 2
- Trains 4 different models: Ridge, Elastic Net, XGBoost, Gradient Boosting
- Comprehensive evaluation and comparison
- Identifies the best model + target combination

**Outputs:**
- `best_target_models_comparison.csv` - Results for all models
- `best_target_models_report.txt` - Detailed report with recommendation
- `best_target_models_comparison.png` - Model comparison visualizations

**Runtime:** ~2-3 minutes

---

## Expected Results

### Best Case Scenario:
- Find a target metric with **R² = 0.12-0.15** (40% improvement over current 0.088)
- Better practical utility (Top-10 hit rate → 50-60%)
- More interpretable formula

### Realistic Scenario:
- Identify 2-3 competitive metrics (R² = 0.09-0.12)
- Understand trade-offs between simplicity and performance
- Choose based on use case (ranking vs exact prediction)

---

## Quick Start

Run all three scripts in sequence:

```bash
cd target_metric_experiments

# Step 1: Create targets (~30 sec)
python3 01_create_alternative_targets.py

# Step 2: Compare targets (~1-2 min)
python3 02_compare_target_metrics.py

# Step 3: Train best target (~2-3 min)
python3 03_train_best_target.py
```

**Total time:** ~5 minutes

---

## Files Generated

After running all scripts, you'll have:

```
target_metric_experiments/
├── README.md (this file)
├── 01_create_alternative_targets.py
├── 02_compare_target_metrics.py
├── 03_train_best_target.py
├── targets_comparison.csv
├── targets_summary_stats.csv
├── target_metrics_comparison_results.csv
├── target_metrics_comparison_report.txt ⭐ READ THIS
├── target_metrics_comparison.png
├── best_target_models_comparison.csv
├── best_target_models_report.txt ⭐ READ THIS
└── best_target_models_comparison.png
```

---

## Key Questions Answered

1. **Which target metric is most predictable?**
   - See `target_metrics_comparison_report.txt`

2. **Does adding cards/corners/complexity help?**
   - Compare R² across different formulas

3. **Which model works best for the winning target?**
   - See `best_target_models_report.txt`

4. **Should we stick with simple xG or switch?**
   - Data-driven recommendation in both reports

---

## Next Steps After Experiments

Based on results, you can:

1. **If new target is better:** Update main pipeline to use it
2. **If simple xG wins:** Stick with current approach, focus on more data
3. **If close call:** Consider ensemble or use case-specific choice

---

## Notes

- All scripts use chronological train/val/test splits (no data leakage)
- Same 37 features as your current best model
- Ridge Regression used for fair comparison (your current winner)
- All metrics normalized for comparison

---

## Questions?

Check the generated `.txt` reports first - they contain detailed explanations and recommendations!
