#!/bin/bash

# All-Seasons Experiments - Proper Implementation
# Uses rolling features across all 3 seasons

echo "================================================================================"
echo "ALL-SEASONS EXPERIMENTS (2022/23, 2023/24, 2024/25)"
echo "================================================================================"
echo ""
echo "This will:"
echo "  1. Generate features for all 3 seasons (~2 min)"
echo "  2. Train models on combined data (~2 min)"
echo "  3. Compare to single-season baseline"
echo ""
echo "Total estimated time: ~4 minutes"
echo ""
echo "Data: 1,140 matches across 3 seasons"
echo "Target: Simple xG (winner from single-season)"
echo "Models: Ridge, Elastic Net, Gradient Boosting"
echo ""
echo "================================================================================"
echo ""

# Check if we're in the right directory
if [ ! -f "01_create_features_ALL_SEASONS.py" ]; then
    echo "Error: Please run this script from the target_metric_experiments folder"
    exit 1
fi

# Step 1: Generate features
echo "STEP 1/2: Generating features for all seasons..."
echo "--------------------------------------------------------------------------------"
python3 01_create_features_ALL_SEASONS.py
if [ $? -ne 0 ]; then
    echo "Error in Step 1. Exiting."
    exit 1
fi
echo ""
echo "✓ Step 1 complete!"
echo ""

# Step 2: Train models
echo "STEP 2/2: Training models on all-seasons data..."
echo "--------------------------------------------------------------------------------"
python3 02_train_ALL_SEASONS.py
if [ $? -ne 0 ]; then
    echo "Error in Step 2. Exiting."
    exit 1
fi
echo ""
echo "✓ Step 2 complete!"
echo ""

# Summary
echo "================================================================================"
echo "ALL-SEASONS EXPERIMENTS COMPLETE!"
echo "================================================================================"
echo ""
echo "Generated files:"
echo "  📊 all_seasons_features.csv"
echo "  📊 all_seasons_results.csv"
echo "  📄 all_seasons_report.txt ⭐ READ THIS"
echo "  📈 all_seasons_comparison.png"
echo ""
echo "Key question answered:"
echo "  Does using 3× more data improve performance?"
echo ""
echo "Next steps:"
echo "  1. Read: all_seasons_report.txt"
echo "  2. Compare to single-season results (R² = 0.8205)"
echo "  3. Decide which approach to use"
echo ""
echo "================================================================================"
