# 🚀 Quick Start Guide - Footy Liveliness

## For the Professor: Running the Application

### Option 1: Quick Demo (5 minutes)

The easiest way to see the project in action:

```bash
# 1. Navigate to the web application
cd Final_Submission/4_Web_Application/footy-liveliness-web

# 2. Install Python dependencies (if not already installed)
pip3 install flask flask-cors pandas numpy scikit-learn

# 3. Install Node dependencies
npm install

# 4. Start the Flask API (Terminal 1)
python3 app.py
# Wait for "Running on http://127.0.0.1:5001"

# 5. Start the React frontend (Terminal 2 - open new terminal)
npm start
# App will open at http://localhost:3000
```

**What you'll see:**
- Ranked list of upcoming Premier League matches
- Predicted liveliness scores for each match
- Week-by-week navigation
- Links to FotMob for match details
- Interactive modals with project documentation

---

### Option 2: Full Experience (10 minutes)

To see the complete pipeline including live data scraping:

```bash
# Follow Option 1 steps 1-3, then:

# 4. Scrape latest fixtures from FotMob
python3 scrape_upcoming_fixtures.py
# Takes ~2 seconds, fetches real upcoming matches

# 5. Start Flask API (Terminal 1)
python3 app.py

# 6. Start React frontend (Terminal 2)
npm start
```

---

## What to Explore

### 1. Main Page
- **This Week's Fixtures**: Matches ranked by predicted excitement
- **Navigation**: Use ← Previous / Next → buttons to browse weeks
- **Match Cards**: Click "Details" to see match info on FotMob

### 2. Header Buttons (Top Right)
- **Getting Started**: Complete setup instructions
- **Top 10 Analysis**: Predicted vs actual top 10 comparison (90% hit rate!)
- **About**: Project overview
- **Project Details**: Comprehensive analysis with interactive charts

### 3. Key Features to Demo
- Week navigation (shows only relevant matches)
- Liveliness scores (4 decimal precision)
- Top 10 comparison modal (shows model accuracy)
- Architecture diagram (system design)

---

## Project Structure for Review

```
Final_Submission/
├── 1_Data_Collection/          # Web scraping notebook
├── 2_Feature_Engineering/      # Feature creation scripts
├── 3_Model_Training/           # Model experiments & training
├── 4_Web_Application/          # Full-stack app (START HERE)
└── 5_Documentation/            # Additional docs
```

---

## Key Files to Review

### Code Quality
1. `4_Web_Application/footy-liveliness-web/app.py` - Flask API
2. `4_Web_Application/footy-liveliness-web/src/App.js` - React main app
3. `2_Feature_Engineering/extra_features.py` - Feature engineering
4. `3_Model_Training/target_metric_experiments/03_train_best_target.py` - Final model

### Documentation
1. `README.md` - Comprehensive project overview
2. `4_Web_Application/footy-liveliness-web/README_REACT.md` - React app guide
3. `4_Web_Application/footy-liveliness-web/README_SCRAPER.md` - Scraper docs

### Model Artifacts
1. `4_Web_Application/footy-liveliness-web/model.pkl` - Trained Elastic Net
2. `4_Web_Application/footy-liveliness-web/scaler.pkl` - Feature scaler
3. `4_Web_Application/footy-liveliness-web/team_stats.pkl` - Team statistics

---

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 5001
lsof -ti:5001 | xargs kill -9

# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

### Missing Dependencies
```bash
# Python
pip3 install flask flask-cors pandas numpy scikit-learn requests

# Node
cd 4_Web_Application/footy-liveliness-web
rm -rf node_modules package-lock.json
npm install
```

### API Not Loading
- Make sure Flask is running (Terminal 1)
- Check http://localhost:5001/api/health
- Restart both Flask and React

---

## Performance Metrics

The web app displays these key metrics:

| Metric | Value | Meaning |
|--------|-------|---------|
| **R² Score** | 82.1% | Explains 82% of variance in match excitement |
| **Top-10 Hit Rate** | 90% | Correctly identifies 9/10 most exciting matches |
| **MAE** | 0.452 | Average prediction error of 0.45 points |
| **Spearman ρ** | 0.896 | Excellent rank correlation |

---

## Demo Script (For Presentation)

### 1. Show Main Page (30 seconds)
- "This is the main interface showing this week's Premier League matches"
- "Matches are ranked by predicted liveliness from our Elastic Net model"
- "Notice the top 3 have special badges (🔥⭐✨)"

### 2. Navigate Weeks (15 seconds)
- "Click Next → to see next week's fixtures"
- "The model predicts excitement for 230+ upcoming matches"

### 3. Show Top 10 Analysis (45 seconds)
- "Click 'Top 10 Analysis' button"
- "Left side: Our model's predicted top 10"
- "Right side: Actual top 10 from last season"
- "Green highlights show correct predictions - 90% hit rate!"

### 4. Show Project Details (30 seconds)
- "Click 'Project Details' for comprehensive analysis"
- "Interactive charts show model performance"
- "5 different visualizations of our results"

### 5. Show Architecture (20 seconds)
- "Click 'View Architecture Diagram'"
- "Shows our end-to-end ML pipeline"
- "From data collection to production deployment"

**Total Demo Time: ~2.5 minutes**

---

## Questions to Anticipate

**Q: How does the model work?**
A: Uses 37 pre-match features (team form, xG, league position) with Elastic Net regression to predict match excitement.

**Q: What makes a match "exciting"?**
A: We use Simple xG metric: total xG + minimum xG between teams. Captures both action and competitiveness.

**Q: How accurate is it?**
A: 82% R² score and 90% top-10 hit rate. Better than random by a large margin.

**Q: Can it predict upsets?**
A: Not designed for that - predicts excitement level, not match outcome.

**Q: What data do you use?**
A: Trained on 380 matches from 2024/25 Premier League season, scraped from FotMob.

---

## Contact & Support

For any issues running the application:
1. Check the main README.md
2. Review troubleshooting section above
3. Ensure all dependencies are installed
4. Verify both Flask and React are running

---

**Estimated Review Time:**
- Quick run: 5 minutes
- Full exploration: 15-20 minutes
- Code review: 30-45 minutes
- Complete analysis: 1-2 hours
