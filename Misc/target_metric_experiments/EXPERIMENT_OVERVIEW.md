# 🎯 Target Metric Experiments - Overview

## What Your Friend Suggested

> "I would say keep it going with just xG and then let's get the best model from that. Maybe Muhammad Raka Zuhdi could try and find a target metric for liveliness that captures:
> - Shot volume and quality (No. Of shots, xG)
> - End-to-end attacking
> - Lots of chances (so low xG, but many opportunities)
> - Transitions (intense with low quality)
> - Cards
>
> I would lowkey take a subset of the data and then just take the score that we have right now, make multiple versions of the target with each being less complex and see what model performs best."

## What We Built

A systematic experiment framework to test **7 different target metrics** and find the optimal one.

---

## 📋 The 7 Target Metrics

### 1️⃣ Simple xG (Current Baseline)
```
xG_total + min(xG_home, xG_away)
```
- **Focus:** Pure attacking threat + competitiveness
- **Complexity:** Low
- **Current R²:** 0.088

### 2️⃣ Shot Quality
```
0.5 × xG_total + 0.3 × shots_total + 0.2 × sot_total
```
- **Focus:** Quality (xG) + Volume (shots) + Accuracy (SoT)
- **Complexity:** Low-Medium
- **Captures:** Shot volume and quality ✓

### 3️⃣ Chances-Focused
```
0.4 × shots_total + 0.3 × bigch_total + 0.3 × xG_total
```
- **Focus:** Many opportunities (even if low quality)
- **Complexity:** Low-Medium
- **Captures:** Lots of chances ✓

### 4️⃣ End-to-End Attacking
```
xG_total + 2 × min(xG_home, xG_away) + min(shots_home, shots_away)
```
- **Focus:** Competitive matches with both teams attacking
- **Complexity:** Medium
- **Captures:** End-to-end attacking ✓

### 5️⃣ Intensity (Transitions + Cards)
```
0.3 × xG + 0.2 × shots + 0.2 × corners + 0.15 × cards + 0.15 × bigch
```
- **Focus:** Fast-paced, intense matches
- **Complexity:** Medium-High
- **Captures:** Transitions + Cards ✓

### 6️⃣ Comprehensive (All Factors)
```
0.25 × xG + 0.20 × shots + 0.15 × sot + 0.15 × bigch + 0.15 × corners + 0.10 × cards
```
- **Focus:** Everything combined
- **Complexity:** High
- **Captures:** All factors ✓✓✓

### 7️⃣ Minimal
```
0.6 × xG_total + 0.4 × shots_total
```
- **Focus:** Simplest possible (just xG + shots)
- **Complexity:** Very Low
- **Captures:** Basic shot volume and quality ✓

---

## 🔬 Experiment Design

### Data Split (Chronological)
- **Train:** Rounds 0-27 (280 matches)
- **Val:** Rounds 28-32 (50 matches)
- **Test:** Rounds 33-37 (50 matches)

### Features Used
- Same 37 features as current best model
- No data leakage (chronological split)

### Evaluation Metrics
1. **R²** - How much variance explained?
2. **MAE** - Average prediction error
3. **Spearman ρ** - Ranking quality
4. **Top-10 Hit Rate** - Can we identify exciting matches?

### Models Tested
- **Phase 1:** Ridge Regression (for fair comparison)
- **Phase 2:** Ridge, Elastic Net, XGBoost, Gradient Boosting (on best target)

---

## 🚀 How to Run

### Option 1: Run Everything at Once (Recommended)
```bash
cd target_metric_experiments
./run_all.sh
```
**Time:** ~5 minutes

### Option 2: Step by Step
```bash
# Step 1: Create targets
python 01_create_alternative_targets.py

# Step 2: Compare targets
python 02_compare_target_metrics.py

# Step 3: Train best target
python 03_train_best_target.py
```

---

## 📊 What You'll Get

### Immediate Answers:
1. ✅ Which target metric is most predictable?
2. ✅ Does adding cards/corners help?
3. ✅ Should we use a simple or complex formula?
4. ✅ Which model works best for the winning target?

### Files Generated:
```
📄 target_metrics_comparison_report.txt  ⭐ Main findings
📈 target_metrics_comparison.png         📊 Visual comparison
📄 best_target_models_report.txt         ⭐ Best model recommendation
📈 best_target_models_comparison.png     📊 Model comparison
📊 targets_comparison.csv                 Raw data
📊 target_metrics_comparison_results.csv  Detailed metrics
```

---

## 🎯 Expected Outcomes

### Scenario A: New Target Wins 🎉
- **R² improves to 0.12-0.15** (40% better)
- **Top-10 hit rate → 50-60%**
- **Action:** Update main pipeline to use new target

### Scenario B: Simple xG Still Best 🤷
- **Current baseline holds**
- **Action:** Focus on getting more data (2022/23, 2023/24 seasons)
- **Insight:** Target metric isn't the bottleneck

### Scenario C: Close Call 🤔
- **Multiple targets perform similarly**
- **Action:** Choose based on interpretability or use case
- **Option:** Ensemble different targets

---

## 💡 Key Insights You'll Gain

1. **Complexity vs Performance Trade-off**
   - Does a complex formula actually help?
   - Or is simple xG already optimal?

2. **Feature Importance**
   - Which match characteristics matter most?
   - Cards? Corners? Shot volume?

3. **Model Selection**
   - Is Ridge still best?
   - Or does XGBoost/Gradient Boosting work better with new target?

4. **Practical Utility**
   - Can we better identify exciting matches?
   - Does Top-10 hit rate improve?

---

## 📝 Notes

- All experiments use **same features** (fair comparison)
- **No data leakage** (chronological splits)
- **Reproducible** (fixed random seeds)
- **Fast** (~5 minutes total)

---

## 🎓 For Your Friend

This addresses all their suggestions:
- ✅ Multiple target versions (7 variants)
- ✅ Varying complexity (simple → comprehensive)
- ✅ Captures all desired factors (shots, xG, chances, transitions, cards)
- ✅ Uses subset approach (train/val/test splits)
- ✅ Tests best model for each target
- ✅ Data-driven recommendation

---

## 🚦 Ready to Start?

```bash
cd target_metric_experiments
./run_all.sh
```

Then read the two report files for your answer! 📄⭐
