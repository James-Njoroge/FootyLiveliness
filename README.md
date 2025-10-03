# Predicting Liveliness for 2024/25 Premier League Matches using FotMob Statistics

**Description:** This project aims to build a model to predict a match’s Liveliness Score—a viewer-centric composite of danger and pace—before kickoff, using historical FotMob team and league statistics from the 2024/25 Premier League.

This can be a tool that helps football fans decide the most interesting matches to watch when there are too many appealing options.

## Goals
1. Develop a testable metric that defines liveliness during a match between two teams.
2. Train a model to predict this testable metric based on historical match data between teams from the English Premier League.

## Data to Collect
### Match Data:
1. **Label (match-wise, post-match)**:
    - Goals
    - Fouls
    - Expected Goals (xG)
    - Big chances
    - Total Shots
    - Shots on Target
    - Shots Inside Box
    - Corners
    - Touches in opposition box
    - Stadium attendance vs. Stadium Capacity (*Factor in the fan demand since they play a hand in influencing player behavior.*)
2. **Features (team-wise, pre-match)**:
    - xG/90
    - shots on target/90
    - corners/90
    - xG conceded/90
    - Home advantage
3. **Collection Method**:
    - Use selenium Python web-scraping to query [FotMob’s](https://www.fotmob.com) public endpoints and collect the data needed above. 


## Modeling plan

We think that this is a simple supervised regression problem for a continuous label so we will lead with that and then explore other modeling techniques like:
- Gradient Boosted Trees (LightGBM/XGBoost/CatBoost) for accuracy.

## Visualization plan

- Predicted vs Actual Liveliness Score scatter plot.

- Weekend Top-5 predicted “lively” matches list with component breakdowns.

- Team timelines of predicted vs observed Liveliness Score over the season.

- Plots/HeatMaps of matches with high liveliness (to see what teams play most lively matches). 

## Test plan

**Chronological split**: 
- Train on matchweeks (MW) 1–28, validate on MW 29–33, test on MW 34–38. Additional testing will be conducted in a subjective manner (personal knowledge/experience), and current season upcoming matches will be used for testing (predict liveliness before the match, and compare to actual liveliness during/after the match). 

- Metrics: MAE, RMSE, R², Spearman ρ, and Top-K hit rate for ranking utility.

- Robustness: performance by home/away

