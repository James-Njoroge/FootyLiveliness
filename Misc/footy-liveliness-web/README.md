# ⚽ Footy Liveliness Web App

AI-powered web application that ranks upcoming Premier League matches by predicted liveliness.

## Features

- 🔥 **Live Rankings** - See which matches will be most exciting
- 📊 **AI Predictions** - Uses Elastic Net model (R² = 0.82)
- 🎯 **Top-10 Hit Rate: 90%** - Highly accurate predictions
- 💫 **Beautiful UI** - Modern, responsive design with TailwindCSS

## Quick Start

### One-Command Startup (Recommended)

```bash
cd footy-liveliness-web
./run.sh
```

This will:
1. Train the model (if not already trained)
2. Start the API server on `http://localhost:5000`
3. Start the web server on `http://localhost:8000`
4. Open the app in your browser automatically

**That's it!** The app will open automatically.

### Manual Setup (Alternative)

#### 1. Install Dependencies

```bash
pip3 install -r requirements.txt
```

#### 2. Train the Model

```bash
python3 train_and_save_model.py
```

#### 3. Start Both Servers

Terminal 1 (API):
```bash
python3 app.py
```

Terminal 2 (Web):
```bash
python3 -m http.server 8000
```

#### 4. Open Browser

Visit `http://localhost:8000`

## API Endpoints

### GET /api/health
Health check

**Response:**
```json
{
  "status": "healthy",
  "model": "Elastic Net",
  "features": 24
}
```

### GET /api/upcoming
Get ranked upcoming fixtures

**Response:**
```json
[
  {
    "rank": 1,
    "home": "Arsenal",
    "away": "Manchester City",
    "date": "2025-01-15",
    "time": "20:00",
    "predicted_liveliness": 5.87
  },
  ...
]
```

### POST /api/predict
Predict single match

**Request:**
```json
{
  "home": "Liverpool",
  "away": "Chelsea"
}
```

**Response:**
```json
{
  "home": "Liverpool",
  "away": "Chelsea",
  "predicted_liveliness": 5.42
}
```

### GET /api/stats
Get model statistics

**Response:**
```json
{
  "model": "Elastic Net",
  "target": "Simple xG",
  "performance": {
    "r2": 0.8205,
    "mae": 0.452,
    "top10_hit_rate": 90.0
  }
}
```

## How It Works

### The Model

- **Algorithm:** Elastic Net Regression
- **Target Metric:** Simple xG (`xG_total + min(xG_home, xG_away)`)
- **Features:** 24 pre-match features including:
  - Team attacking strength (xG/90, shots/90)
  - Team defensive strength (xG conceded/90)
  - Recent form (5-match rolling averages)
  - League position and context

### Performance

- **R²:** 0.8205 (explains 82% of variance)
- **MAE:** 0.452 (average error)
- **Top-10 Hit Rate:** 90% (identifies 9/10 most exciting matches)

### Training Data

- **Season:** 2024/25 Premier League
- **Matches:** 380 matches
- **Features:** 24 engineered pre-match features

## Project Structure

```
footy-liveliness-web/
├── train_and_save_model.py  # Train and save model
├── app.py                    # Flask API server
├── index.html                # Web frontend
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── model.pkl                 # Trained model (generated)
├── scaler.pkl                # Feature scaler (generated)
├── feature_names.pkl         # Feature list (generated)
└── team_stats.pkl            # Team stats (generated)
```

## Customization

### Update Fixtures

Edit `UPCOMING_FIXTURES` in `app.py`:

```python
UPCOMING_FIXTURES = [
    {"home": "Arsenal", "away": "Man City", "date": "2025-01-15", "time": "20:00"},
    # Add more fixtures...
]
```

### Fetch Live Fixtures

Replace the mock data with a real API (e.g., FotMob, The Football Data API):

```python
import requests

def fetch_upcoming_fixtures():
    response = requests.get('https://api.football-data.org/v4/competitions/PL/matches')
    return response.json()['matches']
```

## Deployment

### Deploy to Heroku

1. Create `Procfile`:
```
web: python app.py
```

2. Deploy:
```bash
heroku create footy-liveliness
git push heroku main
```

### Deploy Frontend to Netlify

1. Drag and drop `index.html` to Netlify
2. Update `API_URL` in `index.html` to your Heroku URL

## Future Enhancements

- [ ] Fetch live fixtures from API
- [ ] Add historical predictions vs actual results
- [ ] User accounts and favorite teams
- [ ] Email/SMS notifications for top matches
- [ ] Mobile app (React Native)
- [ ] Betting odds integration
- [ ] Live match updates

## License

MIT

## Credits

Built using:
- **Model:** Elastic Net (scikit-learn)
- **Backend:** Flask
- **Frontend:** HTML + TailwindCSS
- **Data:** FotMob Premier League statistics
