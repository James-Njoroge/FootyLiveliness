#!/bin/bash

# Target Metric Experiments - Run All Scripts
# This script runs the complete pipeline to find the best target metric

echo "================================================================================"
echo "TARGET METRIC EXPERIMENTS - COMPLETE PIPELINE"
echo "================================================================================"
echo ""
echo "This will run 3 scripts in sequence:"
echo "  1. Create alternative target metrics (~30 sec)"
echo "  2. Compare target metrics with Ridge Regression (~1-2 min)"
echo "  3. Train multiple models on best target (~2-3 min)"
echo ""
echo "Total estimated time: ~5 minutes"
echo ""
echo "================================================================================"
echo ""

# Check if we're in the right directory
if [ ! -f "01_create_alternative_targets.py" ]; then
    echo "Error: Please run this script from the target_metric_experiments folder"
    exit 1
fi

# Step 1: Create alternative targets
echo "STEP 1/3: Creating alternative target metrics..."
echo "--------------------------------------------------------------------------------"
python3 01_create_alternative_targets.py
if [ $? -ne 0 ]; then
    echo "Error in Step 1. Exiting."
    exit 1
fi
echo ""
echo "✓ Step 1 complete!"
echo ""

# Step 2: Compare target metrics
echo "STEP 2/3: Comparing target metrics..."
echo "--------------------------------------------------------------------------------"
python3 02_compare_target_metrics.py
if [ $? -ne 0 ]; then
    echo "Error in Step 2. Exiting."
    exit 1
fi
echo ""
echo "✓ Step 2 complete!"
echo ""

# Step 3: Train multiple models on best target
echo "STEP 3/3: Training multiple models on best target..."
echo "--------------------------------------------------------------------------------"
python3 03_train_best_target.py
if [ $? -ne 0 ]; then
    echo "Error in Step 3. Exiting."
    exit 1
fi
echo ""
echo "✓ Step 3 complete!"
echo ""

# Summary
echo "================================================================================"
echo "ALL EXPERIMENTS COMPLETE!"
echo "================================================================================"
echo ""
echo "Generated files:"
echo "  📊 targets_comparison.csv"
echo "  📊 targets_summary_stats.csv"
echo "  📊 target_metrics_comparison_results.csv"
echo "  📄 target_metrics_comparison_report.txt ⭐ READ THIS FIRST"
echo "  📈 target_metrics_comparison.png"
echo "  📊 best_target_models_comparison.csv"
echo "  📄 best_target_models_report.txt ⭐ READ THIS SECOND"
echo "  📈 best_target_models_comparison.png"
echo ""
echo "Next steps:"
echo "  1. Read: target_metrics_comparison_report.txt"
echo "  2. Read: best_target_models_report.txt"
echo "  3. Decide: Keep current target or switch to new one?"
echo ""
echo "================================================================================"
