# Footy Liveliness - Executive Summary

**CS 506 - Data Science | Boston University | Fall 2025**

---

## 🎯 Problem Statement

Football fans face a common dilemma: when multiple Premier League matches are happening simultaneously, which one should they watch? Traditional methods rely on subjective opinions or team popularity, lacking data-driven insights.

---

## 💡 Our Solution

An AI-powered system that predicts match "liveliness" (excitement level) using pre-match team statistics, helping fans make informed viewing decisions.

---

## 📊 Key Results

### Model Performance
- **82.1% R² Score** - Explains 82% of variance in match excitement
- **90% Top-10 Hit Rate** - Correctly identifies 9 out of 10 most exciting matches
- **0.896 Spearman ρ** - Excellent rank correlation between predicted and actual rankings
- **0.452 MAE** - Low average prediction error

### Production Deployment
- ✅ Full-stack web application (React + Flask)
- ✅ Real-time fixture scraping from FotMob
- ✅ Interactive visualizations and analytics
- ✅ Mobile-responsive design

---

## 🔬 Methodology Overview

### 1. Data Collection
- **Source:** FotMob public API
- **Volume:** 380 Premier League matches (2024/25 season)
- **Method:** Selenium-based web scraping
- **Output:** JSON files with match statistics, xG events, team stats

### 2. Target Metric Selection
**Tested 9 different metrics, selected:**
- **Simple xG** = xG_total + min(xG_home, xG_away)
- Captures both total action AND competitive balance
- Outperformed complex alternatives

### 3. Feature Engineering
**37 features total:**
- **22 Rolling Features:** 5-match averages (xG, shots, corners, etc.)
- **15 Contextual Features:** League position, form, stakes

### 4. Model Selection
**Tested 5 models, selected:**
- **Elastic Net Regression** (α=21.54, l1_ratio=0.5)
- Outperformed Ridge, Gradient Boosting, XGBoost, Neural Networks
- Optimal balance between bias and variance

### 5. Deployment
- Flask API backend serving predictions
- React frontend with interactive UI
- Real-time scraping for upcoming fixtures

---

## 💻 Technical Implementation

### Data Pipeline
```
FotMob → Selenium Scraper → JSON Files → Feature Engineering → Model Training → Predictions → Web App
```

### Model Pipeline
```
Raw Stats → Rolling Averages → Contextual Features → Scaling → Elastic Net → Liveliness Score
```

### Web Application
```
User Request → Flask API → Load Model → Create Features → Predict → Rank → Display
```

---

## 📈 Business Value

### For Fans
- **Problem:** Don't know which match to watch
- **Solution:** Data-driven recommendations
- **Impact:** Never miss the best action

### For Broadcasters
- **Problem:** Deciding which matches to feature
- **Solution:** Quantitative excitement scores
- **Impact:** Higher viewer engagement

### For Betting
- **Problem:** Predicting entertainment value
- **Solution:** Accurate liveliness predictions
- **Impact:** Informed betting decisions

---

## 🎓 Key Learnings

### What Worked
✅ Simple xG metric outperformed complex alternatives
✅ Rolling features captured team form effectively
✅ Elastic Net prevented overfitting better than tree models
✅ Contextual features (league position, form) added significant value
✅ 5-match window optimal for rolling statistics

### What Didn't Work
❌ Neural networks failed to converge (insufficient data)
❌ XGBoost severely overfit (R² = 0.04 on test set)
❌ Rolling target metrics caused data leakage
❌ Too many features (>50) led to overfitting
❌ Fixed-window features performed worse than rolling

### Challenges Overcome
- Data leakage in rolling metrics (solved by proper train/test split)
- Overfitting with tree-based models (solved with linear models)
- Web scraping reliability (solved with retry logic and fallbacks)
- Feature scaling importance (solved with StandardScaler)

---

## 🔮 Future Enhancements

### Short-term (Next Semester)
- [ ] Add player-level data (injuries, suspensions)
- [ ] Include weather conditions
- [ ] Multi-league support (La Liga, Serie A)
- [ ] Confidence intervals for predictions

### Long-term (Production)
- [ ] Mobile app (iOS/Android)
- [ ] Push notifications for top matches
- [ ] User preferences and favorites
- [ ] Social sharing features
- [ ] Historical match archive

---

## 📚 Technical Stack

**Data Science:**
- Python 3.9+, pandas, numpy, scikit-learn
- Selenium, BeautifulSoup (web scraping)

**Backend:**
- Flask (API), Flask-CORS
- pickle (model serialization)

**Frontend:**
- React 18, TailwindCSS
- Chart.js (visualizations)
- Axios (HTTP client)

---

## 🏆 Project Achievements

### Technical Excellence
✅ End-to-end ML pipeline from data to deployment
✅ Production-ready web application
✅ Comprehensive documentation
✅ Clean, modular code architecture
✅ Automated testing and validation

### Academic Rigor
✅ Systematic model selection (5 algorithms tested)
✅ Proper train/validation/test split
✅ Cross-validation for hyperparameter tuning
✅ Multiple evaluation metrics
✅ Thorough error analysis

### Innovation
✅ Novel target metric (Simple xG)
✅ Real-time fixture scraping
✅ Interactive web interface
✅ Week-by-week navigation
✅ Top 10 comparison analysis

---

## 📊 Model Comparison

| Model | R² (Test) | MAE | Training Time | Complexity |
|-------|-----------|-----|---------------|------------|
| **Elastic Net** | **0.821** | **0.452** | 2s | Low |
| Ridge | 0.810 | 0.465 | 1s | Low |
| Gradient Boosting | 0.750 | 0.520 | 45s | High |
| XGBoost | 0.040 | 1.250 | 30s | High |
| Neural Network | Failed | N/A | N/A | High |

**Winner: Elastic Net** - Best performance with lowest complexity

---

## 🎯 Impact Metrics

### Accuracy
- 90% of predicted top 10 matches were actually in top 10
- 82% of variance in excitement explained
- Average error of only 0.45 liveliness points

### Usability
- 230+ upcoming matches ranked
- Real-time updates every 5 minutes
- Mobile-responsive design
- <2 second prediction time

### Scalability
- Can handle full season (380 matches)
- Easily extensible to other leagues
- Modular architecture for future features

---

## 📝 Deliverables

### Code
✅ Data collection scripts
✅ Feature engineering pipeline
✅ Model training notebooks
✅ Web application (frontend + backend)
✅ Deployment scripts

### Documentation
✅ Comprehensive README
✅ Quick start guide
✅ API documentation
✅ Architecture diagrams
✅ Code comments

### Presentation Materials
✅ Interactive web demo
✅ Performance visualizations
✅ Top 10 comparison analysis
✅ Architecture overview

---

## 👥 Team Contributions

**James Njoroge:**
- Data collection and web scraping
- FotMob API integration
- Data pipeline development

**Muhammad Raka Zuhdi:**
- Feature engineering
- Model training and selection
- Web application development

**Fola Oladipo:**
- Target metric experimentation
- Model evaluation
- Documentation

---

## 📧 Contact

**Course:** CS 506 - Data Science
**Institution:** Boston University
**Semester:** Fall 2025

---

**Project Completion Date:** December 10, 2025
