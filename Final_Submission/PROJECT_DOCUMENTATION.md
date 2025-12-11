# Footy Liveliness - Complete Project Documentation

**CS 506 - Data Science | Boston University | Fall 2025**

**Team Members:**
- James Njoroge
- Muhammad Raka Zuhdi  
- Fola Oladipo

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Quick Start](#quick-start)
3. [Project Structure](#project-structure)
4. [Methodology](#methodology)
5. [Model Performance](#model-performance)
6. [Web Application](#web-application)
7. [Makefile Commands](#makefile-commands)
8. [Features](#features)
9. [Technical Stack](#technical-stack)
10. [Troubleshooting](#troubleshooting)

---

## 📋 Project Overview

An end-to-end machine learning system that predicts Premier League match "liveliness" (excitement level) using pre-match team statistics. The system helps football fans decide which matches to watch when multiple games are happening simultaneously.

### The Problem
With 10 Premier League matches every weekend, fans face a dilemma: which game should they watch? Traditional factors like team popularity or league position don't always predict the most exciting matches.

### Our Solution
We use machine learning to predict match "liveliness" (excitement level) based on pre-match statistics, helping fans choose the most entertaining games.

### Key Achievements
- ✅ **82.1% R² Score** - Explains 82% of variance in match excitement
- ✅ **90% Top-10 Hit Rate** - Correctly identifies 9 out of 10 most exciting matches
- ✅ **0.896 Spearman ρ** - Excellent rank correlation
- ✅ **0.452 MAE** - Low prediction error
- ✅ **+833% Improvement** - From initial model (R² -0.15 → 0.821)
- ✅ **Production-Ready Web App** - Real-time predictions with interactive UI

---

## 🚀 Quick Start

### Option 1: Using Makefile (Recommended)

```bash
# Navigate to project root
cd Final_Submission

# Install dependencies and start everything
make install && make start

# Or run full demo with live data scraping
make demo
```

### Option 2: Manual Setup

```bash
# Navigate to web app
cd Final_Submission/4_Web_Application/footy-liveliness-web

# Install Python dependencies
pip3 install flask flask-cors pandas numpy scikit-learn requests

# Install Node dependencies
npm install

# Terminal 1: Start Flask API
python3 app.py

# Terminal 2: Start React frontend
npm start
```

The app will open at **http://localhost:3000**

### Prerequisites
- Python 3.9+
- Node.js 14+
- pip and npm

---

## 📁 Project Structure

```
Final_Submission/
├── 1_Data_Collection/
│   └── fotmob_scraping.ipynb          # Web scraping from FotMob (380 matches)
│
├── 2_Feature_Engineering/
│   ├── create_labels.py               # Generate target metrics (Simple xG)
│   ├── create_features.py             # Create rolling features (22 features)
│   └── extra_features.py              # Add contextual features (15 features)
│
├── 3_Model_Training/
│   └── target_metric_experiments/     # Model selection & hyperparameter tuning
│       ├── 01_create_alternative_targets.py
│       ├── 02_compare_target_metrics.py
│       └── 03_train_best_target.py    # Final Elastic Net model
│
├── 4_Web_Application/
│   └── footy-liveliness-web/          # Full-stack React + Flask application
│       ├── app.py                     # Flask API backend
│       ├── scrape_all_season_fixtures.py  # Season scraper (380 matches)
│       ├── src/                       # React frontend
│       │   ├── components/            # React components
│       │   ├── services/              # API calls
│       │   └── utils/                 # Team logos, helpers
│       ├── model.pkl                  # Trained Elastic Net model
│       ├── scaler.pkl                 # StandardScaler
│       ├── team_stats.pkl             # Team statistics
│       ├── Makefile                   # Automation commands
│       └── package.json               # Node dependencies
│
├── 5_Documentation/
│   └── PROJECT_SUMMARY.md             # Detailed project summary
│
├── Makefile                           # Root-level automation
└── PROJECT_DOCUMENTATION.md           # This file
```

---

## 🔬 Methodology

### Phase 1: Data Collection (Weeks 1-3)
- **Source:** FotMob public API
- **Volume:** 380 Premier League matches (2024/25 season)
- **Method:** Python requests + JSON parsing
- **Data:** Match statistics, xG events, team stats, lineups
- **Output:** 380 JSON files with 50+ statistics per match

### Phase 2: Label Generation (Weeks 4-6)
- **Target Metric:** Simple xG = xG_total + min(xG_home, xG_away)
- **Rationale:** Captures both total action and competitive balance
- **Alternatives Tested:** 7 different metrics
  - SLS-F+ Rolling (R²=-0.15)
  - SLS-F+ Fixed (data leakage)
  - Comprehensive (R²=0.724)
  - Chances (R²=0.702)
  - Intensity (R²=0.658)
  - Shot Quality (R²=0.647)
  - ✅ **Simple xG (R²=0.812)** ← Selected

### Phase 3: Feature Engineering (Weeks 7-10)

**Rolling Features (22):**
- 5-match rolling averages for each team
- **Offensive:** xG, shots on target, big chances, corners, touches in box
- **Defensive:** xGA, shots against, big chances allowed
- **Composite:** tempo, possession metrics

**Contextual Features (15):**
- League position (1-20)
- Form trajectory (last 3 matches)
- Points, goal difference
- Home/away splits
- Stakes indicators (both_top6, relegation battles)
- **Impact:** +73% R² boost

**Total: 37 engineered features**

### Phase 4: Model Selection (Weeks 11-14)

# 🔬 Experiments & Model Selection

## What We Tested

In developing our final model (R²=0.821), we conducted extensive experiments across multiple dimensions:

### Data Configurations
- ✅ **Single-season (280 matches)** → R² = 0.821 (SELECTED)
- ❌ Multi-season (990 matches) → R² = -0.023 (failed - cross-season inconsistency)

### Feature Engineering
- ✅ **37 base features** → R² = 0.821 (optimal)
- ❌ 58 features with interactions → R² = 0.002 (overfitting)
- ❌ 87 features → R² < 0 (severe overfitting)

### Model Architectures
| Model | Test R² | Result |
|-------|---------|--------|
| **Elastic Net** | **0.821** | ✅ **Selected** |
| Ridge | 0.812 | ✅ Close second |
| Gradient Boosting | 0.747 | ⚠️ Overfits |
| XGBoost | 0.042 | ❌ Too complex |
| Random Forest | -0.053 | ❌ Failed |
| Neural Network | < 0 | ❌ Insufficient data |

### Target Metrics (7 tested)
| Metric | Formula | R² |
|--------|---------|-----|
| **Simple xG** | `xG_total + xG_min` | **0.812** ✅ |
| Comprehensive | Weighted all stats | 0.724 |
| Chances-Focused | Shots + opportunities | 0.702 |
| Shot Quality | xG + shots + SoT | 0.647 |

## Key Learnings

**What Worked:**
- ✅ Simple xG target outperformed complex formulas
- ✅ Single-season data better than multi-season
- ✅ Linear models optimal for small datasets (280 samples)
- ✅ Strong regularization prevents overfitting

**What Didn't Work:**
- ❌ Multi-season training degraded performance by 126%
- ❌ Neural networks failed (need 500+ samples)
- ❌ Too many features (58+) caused overfitting
- ❌ Complex target metrics harder to predict

## Final Configuration

```python
Model: ElasticNet(alpha=21.54, l1_ratio=0.5)
Target: xG_total + min(xG_home, xG_away)
Features: 37 (rolling averages + league context + form)
Data: 2024/25 season only
Result: R² = 0.821, Top-10 Hit = 90%
```

**Total Experiments:** 30+ configurations tested  
**Final Improvement:** +833% over initial baseline (R² 0.088 → 0.821)

**Final Model Configuration:**
- **Algorithm:** ElasticNetCV
- **Hyperparameters:** α=21.54, l1_ratio=0.5
- **Cross-validation:** 5-fold
- **Training:** 280 matches (rounds 0-27)
- **Validation:** 50 matches (rounds 28-32)
- **Test:** 50 matches (rounds 33-37)
- **Chronological split:** No data leakage

---

## 📊 Model Performance

### Key Metrics
- **R² Score:** 0.821 (82% variance explained)
- **MAE:** 0.452 (average error of 0.45 points on 0-8 scale)
- **RMSE:** 0.598
- **Spearman ρ:** 0.896 (90% ranking accuracy)
- **Top-10 Hit Rate:** 90% (identifies 9/10 most exciting matches)
- **Overfitting:** -0.014 (excellent generalization)

### Performance Evolution
1. **Initial:** R² = -0.15 (Linear Reg + SLS-F+)
2. **Stage 2:** R² = 0.042 (XGBoost baseline, +19%)
3. **Stage 3:** R² = 0.088 (Ridge + 37 features, +110%)
4. **Final:** R² = 0.821 (Elastic Net + Simple xG, **+833%**)

### What the Model Captures (82%)
- ✓ Team form (rolling 5-match averages)
- ✓ League position and competitive pressure
- ✓ Attacking power (xG, shots, big chances)
- ✓ Defensive weakness (goals/chances conceded)
- ✓ Match stakes (top 6 clashes, relegation battles)

### What It Misses (18%)
- ✗ Key player injuries/suspensions
- ✗ Tactical surprises and formations
- ✗ Individual moments of brilliance
- ✗ Weather and referee decisions
- ✗ Team motivation and psychological factors

---

## 🌐 Web Application

### Architecture
- **Backend:** Flask REST API (Port 5001)
- **Frontend:** React 18 + TailwindCSS (Port 3000)
- **Data:** Real-time scraping from FotMob API
- **Deployment:** localhost (development)

### Core Features

#### 1. Match Rankings
- All 380 season matches ranked by predicted excitement
- 0-8 liveliness scale (typically 2-7)
- Team logos and match details
- Date, time, and venue information

#### 2. Week Navigation
- Browse past and future weeks
- ← Previous / Next → buttons
- Sunday-Saturday week format
- Current week highlighted

#### 3. Comparison View ⚖️
- **For Past Weeks Only**
- Side-by-side predicted vs actual rankings
- Color-coded accuracy badges:
  - 🟢 Green: 90%+ (excellent)
  - 🔵 Blue: 75-89% (good)
  - 🟡 Yellow: 60-74% (fair)
  - 🔴 Red: <60% (poor)
- Summary statistics (matches analyzed, average accuracy)

#### 4. Real-time Data
- Scrapes 380 matches from FotMob
- 150+ finished matches with actual xG
- 230 upcoming matches with predictions
- Actual vs predicted comparison for finished matches

#### 5. Interactive Modals
- **Getting Started:** Setup instructions
- **About:** Project overview and methodology
- **Architecture:** System design diagram
- **Project Details:** Comprehensive technical documentation with charts
- **Top 10 Analysis:** Model validation with real examples

#### 6. Accuracy Info Button ℹ️
- Explains accuracy calculation formula
- Example calculations
- Color coding guide
- Positioned next to view toggle

### Data Pipeline

1. **Data Collection** (scrape_all_season_fixtures.py)
   - Input: FotMob API
   - Process: Fetch 380 matches with fixtures and stats
   - For Finished: Extract actual xG from shot events
   - For Upcoming: Store fixture info
   - Output: all_fixtures.json (150 finished + 230 upcoming)
   - Time: ~5 minutes

2. **Feature Engineering** (app.py - create_features_for_match)
   - Input: Team names + team_stats.pkl
   - Process: Create 27-feature vector
   - Features: Home/away xG, shots, chances, corners, defensive stats, rest days
   - Output: 27-dimensional numpy array
   - Time: Instant

3. **Feature Scaling** (StandardScaler)
   - Input: Raw features + scaler.pkl
   - Process: Z-score normalization (mean=0, std=1)
   - Purpose: Prevent features with larger ranges from dominating
   - Output: Scaled 27-dimensional vector
   - Time: <1ms

4. **Prediction** (Elastic Net Model)
   - Input: Scaled features + model.pkl
   - Model: ElasticNet(alpha=21.54, l1_ratio=0.5)
   - Process: Linear combination with L1+L2 regularization
   - Output: Predicted liveliness score (0-8 scale)
   - Time: <1ms

5. **Ranking & Display** (Flask API + React)
   - Input: Predictions for all 380 matches
   - Process: Sort by predicted_liveliness (descending)
   - API Response: JSON with match data, predictions, ranks, status
   - Frontend: React displays with logos, scores, accuracy badges
   - Output: Interactive web UI at http://localhost:3000

---

## ⌨️ Makefile Commands

### Root Level Commands
```bash
# From Final_Submission/ directory

make install    # Install all dependencies (Python + Node)
make start      # Start Flask API + React frontend
make stop       # Stop all processes
make demo       # Full demo: install + scrape + start (~5 min)
make update     # Re-scrape data and restart application
make status     # Check if application is running
make clean      # Remove temporary files and logs
make test       # Test API endpoints
```

### Web App Commands
```bash
# From 4_Web_Application/footy-liveliness-web/ directory

make install           # Install dependencies
make start             # Start API + frontend
make stop              # Stop all processes
make scrape            # Scrape 380 matches (~5 min)
make update            # Stop + scrape + start
make test              # Test API endpoints
make clean             # Clean temp files
make kill-ports        # Free ports 5001 and 3000
make status            # Check process status
make logs              # View API and frontend logs
make open              # Open browser to localhost:3000
```

### Update Command Workflow
```bash
make update
```
1. 🛑 Stops Flask API and React frontend
2. 🌐 Re-scrapes all 380 matches from FotMob (~5 min)
3. 🚀 Restarts application with fresh data
4. ✅ New predictions loaded

**Use Cases:**
- After matches are played (get actual xG data)
- New fixtures released
- Daily refresh for current data
- Before presentations

---

## ✨ Features

### 1. Predicted vs Actual Comparison
- Real xG data for 150+ finished matches
- Accuracy calculation: `100% - |Predicted - Actual| / 8 × 100%`
- Color-coded badges for quick assessment
- Side-by-side ranking comparison

### 2. Week-by-Week Navigation
- Browse any week of the season
- Past weeks show actual results
- Future weeks show predictions
- Current week highlighted

### 3. Top 10 Analysis
- Validates model with real examples
- Shows 90% hit rate (9/10 matches correctly identified)
- Compares predicted vs actual top 10
- Demonstrates model effectiveness

### 4. Responsive Design
- Works on desktop, tablet, and mobile
- Adaptive layouts
- Touch-friendly navigation
- Optimized for all screen sizes

### 5. Auto-refresh
- Updates every 5 minutes
- Keeps data current
- No manual refresh needed

### 6. Team Logos
- Official Premier League team logos
- Visual identification
- Professional appearance

---

## 🛠️ Technical Stack

### Data & ML
- **Python 3.9+** - Core language
- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **scikit-learn** - ML models (ElasticNet, StandardScaler)
- **matplotlib** - Visualization
- **requests** - API scraping

### Backend
- **Flask** - REST API server
- **Flask-CORS** - Cross-origin requests
- **pickle** - Model serialization
- **JSON** - Data format

### Frontend
- **React 18** - UI framework
- **TailwindCSS** - Styling
- **Chart.js** - Data visualization
- **react-chartjs-2** - React wrapper for Chart.js
- **Axios** - HTTP client

### Development
- **Jupyter** - Notebooks for exploration
- **VS Code** - IDE
- **Git** - Version control
- **Makefile** - Build automation
- **Chrome DevTools** - Debugging

### Data Sources
- **FotMob API** - Match data and statistics
- **xG Statistics** - Shot quality metrics
- **Premier League 2024/25** - Current season data
- **380 Matches** - Full season coverage

### Deployment
- **localhost** - Development environment
- **Port 5001** - Flask API
- **Port 3000** - React app
- **<1ms** - Inference time per prediction

---

## 🔍 Troubleshooting

### Port Already in Use
```bash
# Kill processes on ports 5001 and 3000
make kill-ports

# Or manually:
lsof -ti:5001 | xargs kill -9
lsof -ti:3000 | xargs kill -9
```

### Module Not Found Errors
```bash
# Python packages
pip3 install -r requirements.txt

# Node packages
rm -rf node_modules package-lock.json
npm install
```

### API Connection Failed
- Make sure Flask is running on port 5001
- Check that both terminals are in the same directory
- Verify CORS is enabled in app.py
- Check firewall settings

### Browser Doesn't Auto-open
Manually navigate to: **http://localhost:3000**

### Scraper Takes Too Long
- Normal: ~5 minutes for 380 matches
- Rate limited to 0.5s between requests
- Check internet connection
- FotMob API may be slow

### Application Won't Start
```bash
# Check status
make status

# View logs
make logs

# Clean and restart
make clean
make install
make start
```

---

## 📈 Use Cases

### For Fans 👥
- ✓ Decide which match to watch on busy weekends
- ✓ Discover exciting matches between mid-table teams
- ✓ Plan viewing schedule for the week
- ✓ Avoid boring one-sided games

### For Broadcasters 📺
- ✓ Select matches for prime-time slots
- ✓ Optimize scheduling for viewer engagement
- ✓ Predict viewership potential
- ✓ Market matches more effectively

### For Analysts 📊
- ✓ Quantify match entertainment value
- ✓ Identify factors driving excitement
- ✓ Compare predicted vs actual outcomes
- ✓ Validate model performance

### For Betting 🎰
- ✓ Predict over/under goals markets
- ✓ Identify high-scoring games
- ✓ Find value in entertainment bets
- ✓ Assess match competitiveness

---

## 🎓 Learning Outcomes

### Technical Skills
- End-to-end ML pipeline development
- Web scraping and data collection
- Feature engineering and selection
- Model selection and hyperparameter tuning
- Full-stack web development (React + Flask)
- RESTful API design
- Build automation with Makefiles

### Data Science Concepts
- Regression modeling
- Cross-validation
- Overfitting prevention
- Model evaluation metrics
- Feature importance analysis
- Time series considerations (chronological splits)

### Software Engineering
- Version control with Git
- Code organization and modularity
- Documentation best practices
- User interface design
- Deployment considerations
- Error handling and debugging

---

## 📝 Citations

### Data Source
- **FotMob:** https://www.fotmob.com/
- Premier League match statistics and xG data

### Libraries & Frameworks
- **scikit-learn:** Pedregosa et al., JMLR 12, pp. 2825-2830, 2011
- **React:** Facebook Open Source
- **Flask:** Pallets Projects
- **TailwindCSS:** Tailwind Labs

---

## 👥 Team Contributions

### James Njoroge
- Data scraping and collection
- Feature engineering pipeline
- Data preprocessing and cleaning

### Muhammad Raka Zuhdi
- Target metric experiments
- Model training and evaluation
- Web application development
- Documentation

### Fola Oladipo
- Model evaluation and validation
- Performance analysis
- Documentation and presentation

---

## 📞 Contact

**Course:** CS 506 - Data Science  
**Institution:** Boston University  
**Semester:** Fall 2025

For questions or feedback, please contact the team members through the course portal.

---

## 🏆 Final Notes

This model explains **82% of variance** in match excitement - an exceptional result for sports prediction, where typical models achieve 30-50%. The remaining 18% includes genuinely unpredictable factors like injuries, tactical surprises, and individual brilliance.

Our approach prioritizes **interpretability, robustness, and production-readiness** over marginal performance gains that might not generalize.

**Recommendation:** Deploy with confidence. No further improvements are needed without additional data sources (player injuries, tactical information, weather conditions, etc.).

---

**Last Updated:** December 10, 2025  
**Version:** 1.0  
**Status:** ✅ Production Ready
