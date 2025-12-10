# Footy Liveliness - Premier League Match Excitement Predictor

**CS 506 - Data Science | Boston University | Fall 2025**

**Team Members:**
- James Njoroge
- Muhammad Raka Zuhdi
- Fola Oladipo

---

## 📋 Project Overview

An end-to-end machine learning system that predicts Premier League match "liveliness" (excitement level) using pre-match team statistics. The system helps football fans decide which matches to watch when multiple games are happening simultaneously.

### Key Achievements
- ✅ **82.1% R² Score** - Explains 82% of variance in match excitement
- ✅ **90% Top-10 Hit Rate** - Correctly identifies 9 out of 10 most exciting matches
- ✅ **0.896 Spearman ρ** - Excellent rank correlation
- ✅ **0.452 MAE** - Low prediction error
- ✅ **Production-Ready Web App** - Real-time predictions with interactive UI

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
│       ├── scrape_upcoming_fixtures.py # Live fixture scraper
│       ├── src/                       # React frontend
│       ├── model.pkl                  # Trained model
│       ├── scaler.pkl                 # Feature scaler
│       └── team_stats.pkl             # Team statistics
│
├── 5_Documentation/
│   └── (This README and additional docs)
│
└── README.md                          # This file
```

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.9+
- Node.js 14+
- pip and npm

### Installation & Running

#### 1. Install Python Dependencies
```bash
cd 4_Web_Application/footy-liveliness-web
pip3 install flask flask-cors pandas numpy scikit-learn requests
```

#### 2. Install Node Dependencies
```bash
npm install
```

#### 3. Scrape Latest Fixtures (Optional)
```bash
python3 scrape_upcoming_fixtures.py
```

#### 4. Start Flask API (Terminal 1)
```bash
python3 app.py
# Runs on http://localhost:5001
```

#### 5. Start React Frontend (Terminal 2)
```bash
npm start
# Opens http://localhost:3000
```

---

## 🔬 Methodology

### 1. Data Collection
- **Source:** FotMob public API
- **Volume:** 380 Premier League matches (2024/25 season)
- **Method:** Selenium-based web scraping
- **Data:** Match statistics, xG events, team stats, lineups

### 2. Label Generation
- **Target Metric:** Simple xG = xG_total + min(xG_home, xG_away)
- **Rationale:** Captures both total action and competitive balance
- **Alternatives Tested:** 9 different metrics (Simple xG performed best)

### 3. Feature Engineering (37 Features Total)

**Rolling Features (22):**
- 5-match rolling averages for each team
- Offensive: xG, shots on target, big chances, corners
- Defensive: xGA, shots against, corners conceded
- Composite: tempo, possession metrics

**Contextual Features (15):**
- League position (1-20)
- Form trajectory (last 3 matches)
- Points, goal difference
- Home/away splits
- Stakes indicators

### 4. Model Selection

**Models Tested:**
- ✅ **Elastic Net** (R² = 0.821) ← Selected
- Ridge Regression (R² = 0.810)
- Gradient Boosting (R² = 0.750)
- XGBoost (R² = 0.040)
- Neural Network (Failed to converge)

**Final Model:**
- Algorithm: ElasticNetCV
- Hyperparameters: α=21.54, l1_ratio=0.5
- Cross-validation: 5-fold
- Training: 280 matches (rounds 0-27)
- Validation: 50 matches (rounds 28-32)
- Test: 50 matches (rounds 33-37)

### 5. Deployment
- **Backend:** Flask API serving predictions
- **Frontend:** React 18 with TailwindCSS
- **Features:** 
  - Real-time fixture scraping
  - Week-by-week navigation
  - Top 10 analysis comparison
  - Interactive charts (Chart.js)
  - Links to FotMob match pages

---

## 📊 Model Performance

### Quantitative Metrics
| Metric | Value | Interpretation |
|--------|-------|----------------|
| R² Score | 0.821 | 82% variance explained |
| MAE | 0.452 | Average error of 0.45 liveliness points |
| Spearman ρ | 0.896 | Excellent rank correlation |
| Top-10 Hit Rate | 90% | Correctly identifies 9/10 most exciting matches |
| Overfitting | -0.014 | Minimal (train R² = 0.835, test R² = 0.821) |

### Qualitative Insights
- ✅ Excels at identifying high-profile clashes (Liverpool vs Chelsea, Arsenal vs Man City)
- ✅ Strong performance on matches with attacking teams
- ⚠️ May underestimate matches with unexpected events (red cards, late drama)
- ⚠️ Limited by pre-match data (cannot predict tactical surprises)

---

## 💻 Web Application Features

### User Features
1. **Weekly Match View**
   - Shows matches for current week (Sunday-Saturday)
   - Navigate between weeks with arrow buttons
   - Ranked by predicted liveliness

2. **Match Cards**
   - Team logos from FotMob CDN
   - Liveliness score (4 decimal places)
   - Date and time
   - Direct link to FotMob match page

3. **Top 10 Analysis**
   - Side-by-side comparison of predicted vs actual top 10
   - Visual hit/miss indicators
   - Performance metrics dashboard

4. **Documentation Modals**
   - Getting Started guide
   - Project Details with interactive charts
   - Architecture diagram
   - About section

### Technical Features
- Real-time fixture scraping from FotMob
- Auto-refresh every 5 minutes
- Responsive design (mobile-friendly)
- Component-based React architecture
- RESTful API with CORS support

---

## 🎯 Use Cases

### For Football Fans
- **Problem:** Multiple matches happening simultaneously
- **Solution:** Identifies which match will be most exciting
- **Benefit:** Never miss the best action

### For Broadcasters
- **Problem:** Deciding which matches to feature
- **Solution:** Data-driven match selection
- **Benefit:** Higher viewer engagement

### For Betting
- **Problem:** Predicting match entertainment value
- **Solution:** Quantitative liveliness scores
- **Benefit:** Informed betting decisions

---

## 📈 Key Findings

### 1. Feature Importance
Top 5 most important features:
1. Home team rolling xG (offensive strength)
2. Away team rolling xG (offensive strength)
3. Home team rolling xGA (defensive weakness)
4. League position difference (stakes)
5. Recent form trajectory (momentum)

### 2. Target Metric Selection
- Tested 9 different liveliness metrics
- Simple xG outperformed complex alternatives
- Rolling metrics failed due to data leakage
- Balance between total action and competitiveness is key

### 3. Model Selection
- Linear models (Elastic Net, Ridge) outperformed tree-based models
- Neural networks failed to converge (insufficient data)
- Regularization crucial to prevent overfitting
- 37 features optimal (more features = overfitting)

---

## 🔮 Future Enhancements

### Data Enhancements
- [ ] Player-level data (injuries, suspensions)
- [ ] Tactical information (formations, pressing intensity)
- [ ] Weather conditions
- [ ] Historical head-to-head records
- [ ] Referee statistics

### Model Improvements
- [ ] Ensemble methods (stacking multiple models)
- [ ] Time-series modeling (LSTM for form trends)
- [ ] Multi-output prediction (goals, cards, corners)
- [ ] Uncertainty quantification (confidence intervals)

### Application Features
- [ ] Multi-league support (La Liga, Serie A, Bundesliga)
- [ ] Push notifications for top matches
- [ ] Historical match archive
- [ ] User preferences and favorites
- [ ] Social sharing features

---

## 📚 Technical Stack

### Data Science
- **Python 3.9+**
- pandas, numpy (data manipulation)
- scikit-learn (machine learning)
- Selenium, BeautifulSoup (web scraping)

### Backend
- **Flask** (API server)
- Flask-CORS (cross-origin requests)
- pickle (model serialization)

### Frontend
- **React 18** (UI framework)
- TailwindCSS (styling)
- Chart.js + react-chartjs-2 (visualizations)
- Axios (HTTP client)

---

## 🎓 Learning Outcomes

This project demonstrates:
- ✅ End-to-end ML pipeline (data → model → deployment)
- ✅ Feature engineering for sports analytics
- ✅ Model selection and hyperparameter tuning
- ✅ Web scraping and API integration
- ✅ Full-stack web development
- ✅ Production deployment best practices

---

## 📝 Citations & References

### Data Source
- **FotMob:** https://www.fotmob.com
- Public API endpoints for Premier League data
- Team logos from FotMob CDN

### Methodology
- Elastic Net: Zou & Hastie (2005)
- xG Methodology: StatsBomb, Opta
- Feature Engineering: Inspired by football analytics literature

---

## 📧 Contact

For questions or feedback:
- **Course:** CS 506 - Data Science
- **Institution:** Boston University
- **Semester:** Fall 2025

---

## 📄 License

This project is for educational purposes as part of CS 506 coursework.

---

**Last Updated:** December 10, 2025
