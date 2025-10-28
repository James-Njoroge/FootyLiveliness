# Predicting Liveliness for 2024/25 Premier League Matches using FotMob Statistics

[![Watch the video](https://img.youtube.com/vi/vWeHg9z0MsM/0.jpg)](https://www.youtube.com/watch?v=vWeHg9z0MsM)


**Description:** This project aims to build a model to predict a match’s Liveliness Score—a viewer-centric composite of danger and pace—before kickoff, using historical FotMob team and league statistics from the 2024/25 Premier League.

This can be a tool that helps football fans decide the most interesting matches to watch when there are too many appealing options.

## Goals
1. Develop a testable metric that defines liveliness during a match between two teams.
2. Train a model to predict this testable metric based on historical match data between teams from the English Premier League.

## Data
 
- Purpose: Season dataset for the 2024–25 Premier League used by the project, containing full match data scraped from FotMob. See the detailed dataset docs: [data/README_data.md](data/README_data.md).
- Structure: Located at `data/24-25_PL_Data_raw/` with an `index.json` manifest and 38 round folders (`round_0`–`round_37`) each holding 10 per-match JSON files.
- Contents: Each match JSON includes metadata, score/timing, xG shot events, lineups with player ratings/subs, and team stats by period.

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

# FootyLiveliness (SLS-F+) — 2024/25 Premier League  
**Project Update Report — October 2025**

End-to-end pipeline to scrape match data from FotMob, compute a *Spectator Liveliness Score (SLS-F+)*, engineer leakage-safe pre-match features, perform exploratory data analysis, and prepare models to predict and rank upcoming match liveliness.

---

## Overview of Progress (10/27/2025)

This update summarizes progress since the initial proposal.  
The project now includes the full data science workflow:
1. **Data collection and scraping** from FotMob  
2. **Feature computation** using leakage-safe pre-match statistics  
3. **Exploratory data analysis (EDA)** with R  
4. **Model preparation** for predicting and ranking match liveliness

---

## 1. Data Acquisition and Structure

- Implemented **Selenium Wire scraping pipeline** (`data/fotmob_scraping.ipynb`) to collect all 2024/25 Premier League `matchDetails` JSON payloads from FotMob.
- Each round’s data is saved under: data/24-25_PL_Data_raw/round_<k>/<matchId>matchDetails<Home>-vs-<Away>.json

- The global `index.json` file maps all matches and rounds.
- Dataset schema and field definitions are documented in [`data/README_data.md`](data/README_data.md).

**Notes:**
- Polite scraping rules and delays are enforced.
- ChromeDriver path and season constants (`SEASON_LABEL`, `LEAGUE_ID`) are configurable.
- All 38 rounds (380 matches) have been successfully collected.

---

## 2. Feature Engineering and Label Creation

Feature and label computation is performed in `data/data_manipulation.ipynb`.

### Key Computations
- **Aggregate match totals**: xG, Shots on Target, Big Chances, Corners, Touches in Opposition Box  
- **Per-minute normalization**: divides totals by minutes played  
- **Season-wide standardization**: z-scores computed per feature  
- **Spectator Liveliness Score (SLS-F+)**:
- Weighted blend of offensive z-scores:
  ```
  xG: 0.50 | SoT: 0.20 | BigCh: 0.10 | Corners: 0.10 | ToB: 0.10
  ```
- Attendance occupancy adds a capped ±0.30 boost
- Final score scaled to mean = 50, std = 15, clipped [0, 100]

**Outputs:**
- `tables/all_rounds.csv` — full season table with features + SLS-F+ label  
- `tables/round_<k>.csv` — per-round outputs for verification

---

## 3. Leakage-Safe Pre-Match Features

To ensure valid prediction, all model inputs use **only pre-match information**.  
Each feature is computed as a **5-match rolling average** per team.

### Engineered Features
**Offensive Form**
- `xG_att_90`, `SoT_att_90`, `BigCh_att_90`, `Corn_att_90`, `ToB_att_90`

**Defensive Concessions**
- `xGA_def_90`, `SoT_agst_90`, `BigCh_agst_90`

**Contextual Features**
- `DaysRestDiff` — rest differential between teams  
- `Home_occ_prior` — previous occupancy ratio  
- `LeagueAvg_xG_perMatch_sofar`, `LeagueAvg_Corners_perMatch_sofar`

**Composite Predictors**
- `AttackVsDefense` — offensive form vs opponent defensive weakness  
- `TempoSum` — combined attacking tempo  
- `SoTSum` — combined pre-match shots-on-target rate  

All features are saved to: feature_tables/match_features_wide.csv


---

## 4. Exploratory Data Analysis (EDA)

EDA was conducted in R (`feature_visualizations.Rnw` → `feature_visualizations.pdf`).

### Objectives
- Assess the relationship between pre-match features and `SLS_Fplus`
- Check for data leakage, multicollinearity, and feature importance trends
- Validate that “lively” matches correspond to higher offensive tempo and shot activity

### Findings
- Positive correlation between **TempoSum**, **SoTSum**, and **SLS_Fplus**
- Early rounds show weak trends (league priors), later rounds strengthen as form stabilizes
- Moderate correlations between related tempo features (expected)
- Occupancy ratio (`Home_occ_prior`) mildly boosts liveliness

### Generated Visuals
| File | Description |
|-------|-------------|
| `pairwise-global-1.pdf` | Pairwise scatterplot matrix |
| `cor-heatmap-1.pdf` | Feature correlation heatmap |
| `scatter-tempo-1.pdf` | Tempo vs liveliness |
| `scatter-sot-1.pdf` | SoTSum vs liveliness |
| `facet-round-1.pdf` | Tempo vs liveliness by round |
| `sls-vs-occupancy.pdf` | Occupancy vs liveliness |

---

## 5. Modeling Preparation

### Modeling Objective
Predict `SLS_Fplus` using pre-match rolling form features and contextual metrics.

### Train/Validation/Test Split
- Train: Rounds 1–28  
- Validation: Rounds 29–33  
- Test: Rounds 34–38  
(Chronological split to preserve time order)

### Planned Models
| Stage | Model | Purpose |
|--------|--------|----------|
| **Baseline** | Linear Regression | Benchmark interpretability |
| **Final** | XGBoost / Gradient Boosting Regressor | Nonlinear performance model |
| **Experimental** | Neural Network (MLP) | Capture deeper nonlinear relationships |

### Evaluation Metrics
- **MAE** — Mean Absolute Error  
- **RMSE** — Root Mean Squared Error  
- **R²** — Coefficient of Determination  
- **Spearman ρ** — Rank correlation (for liveliness ranking)

---

## Attribution

- Data sourced from FotMob public endpoints for educational purposes.  
- Not affiliated with or endorsed by FotMob.  
- Project Team: **James Njoroge, Muhammad Raka Zuhdi, Fola Oladipo**  
- Boston University — CS 506 Data Science Project, Fall 2025
