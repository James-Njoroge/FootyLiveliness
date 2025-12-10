# 🚀 START HERE - Target Metric Experiments

## Quick Start (5 minutes)

### Step 1: Open Terminal
```bash
cd "/Users/muhammadrakazuhdi/Desktop/Windsurf Projects/506/Footy Liveliness/FootyLiveliness/target_metric_experiments"
```

### Step 2: Run Experiments
```bash
python3 run_all.py
```

### Step 3: Read Results
1. Open `target_metrics_comparison_report.txt` ⭐
2. Open `best_target_models_report.txt` ⭐

**That's it!** 🎉

---

## What This Does

Tests **7 different target metrics** to find which one best captures match liveliness:

1. **Simple xG** (your current baseline)
2. **Shot Quality** (xG + shots + shots on target)
3. **Chances-Focused** (many opportunities)
4. **End-to-End** (competitive matches)
5. **Intensity** (transitions + cards)
6. **Comprehensive** (everything)
7. **Minimal** (just xG + shots)

Then trains **4 different models** on the winner:
- Ridge Regression
- Elastic Net
- XGBoost
- Gradient Boosting

---

## Expected Output

```
✓ targets_comparison.csv
✓ target_metrics_comparison_report.txt  ⭐ READ THIS
✓ target_metrics_comparison.png
✓ best_target_models_report.txt         ⭐ READ THIS
✓ best_target_models_comparison.png
```

---

## What You'll Learn

1. **Which target metric is most predictable?**
   - Does adding cards/corners help?
   - Is simple better than complex?

2. **Which model works best?**
   - Ridge? XGBoost? Gradient Boosting?

3. **Should you switch from current baseline?**
   - Data-driven recommendation

---

## Time Required

- Script runtime: **~5 minutes**
- Reading reports: **~5 minutes**
- **Total: 10 minutes**

---

## Need More Info?

- Read `EXPERIMENT_OVERVIEW.md` for detailed explanation
- Read `README.md` for step-by-step guide

---

## Ready? Let's Go! 🚀

```bash
./run_all.sh
```
