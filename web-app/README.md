# Footy Liveliness Web App

AI-powered Premier League match excitement predictor using Ridge Regression ML model.

## Features

- 🔥 Real-time match liveliness predictions
- 📊 Interactive match rankings
- 🎯 67% recommendation accuracy (Top-3 matches)
- 📈 Detailed model performance metrics
- 🎨 Modern, responsive UI with Tailwind CSS

## Tech Stack

- **Frontend**: React 18 + Vite
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **ML Model**: Ridge Regression (R² = 0.088)

## Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.8+ (for backend API)

### Installation

```bash
# Install frontend dependencies
npm install

# Install backend dependencies
cd api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cd ..
```

### Running the App

**Option 1: Full Stack (Frontend + Backend)**
```bash
npm run dev:full
```
This runs both the React frontend (port 3000) and Flask backend (port 5000).

**Option 2: Frontend Only (Demo Mode)**
```bash
npm run dev
```
Uses client-side predictions with simplified model.

**Option 3: Separate Processes**
```bash
# Terminal 1 - Frontend
npm run dev

# Terminal 2 - Backend
npm run api
```

### Production Build

```bash
# Build frontend
npm run build

# Preview production build
npm run preview
```

The app will open at `http://localhost:3000`

## Model Details

- **Algorithm**: Ridge Regression with L2 regularization
- **Features**: 37 contextual features including:
  - Rolling 5-match form (xG, shots, corners)
  - League position & points differential
  - Form trajectory (last 3 vs previous 5)
  - High-stakes indicators
- **Training Data**: 240 Premier League matches (2024/25 season)
- **Performance**:
  - R² = 0.088 (8.8% variance explained)
  - MAE = ±1.04 points
  - Top-3 accuracy = 67%
  - Precision@5 = 60%

## How It Works

1. **Data Collection**: Match statistics scraped from FotMob
2. **Feature Engineering**: 37 pre-match features computed from rolling averages and league context
3. **Prediction**: Ridge Regression model predicts liveliness score (1-8 scale)
4. **Ranking**: Matches sorted by predicted excitement level

## Liveliness Metric

```
Liveliness = xG_total + min(xG_home, xG_away)
```

This formula rewards:
- Total attacking action (xG_total)
- Competitive matches where both teams are dangerous

## Project Structure

```
web-app/
├── src/
│   ├── components/
│   │   ├── MatchCard.jsx      # Individual match display
│   │   └── ModelInfo.jsx      # Model information modal
│   ├── utils/
│   │   └── predictor.js       # ML prediction logic
│   ├── App.jsx                # Main application
│   ├── main.jsx               # React entry point
│   └── index.css              # Global styles
├── public/                    # Static assets
├── index.html                 # HTML template
└── package.json               # Dependencies
```

## Customization

### Adding Real Match Data

Replace the sample data in `src/utils/predictor.js` with real API calls:

```javascript
// Example: Fetch from your backend
export async function fetchUpcomingMatches() {
  const response = await fetch('/api/matches/upcoming');
  return response.json();
}
```

### Updating Model Coefficients

Update coefficients in `src/utils/predictor.js` with your trained model:

```javascript
const modelCoefficients = {
  'both_top6': -0.168447,
  'away_Corn_att_90': 0.132473,
  // ... all 37 features
};
```

## Deployment

### Netlify

```bash
npm run build
# Deploy dist/ folder to Netlify
```

### Vercel

```bash
npm run build
vercel deploy
```

## Known Limitations

The model cannot predict:
- Player injuries and suspensions
- Tactical surprises
- Individual moments of brilliance
- Weather conditions
- Psychological factors (rivalry intensity)

## Credits

- **Data Source**: FotMob
- **Course**: CS 506 - Data Science, Boston University
- **Team**: James Njoroge, Muhammad Raka Zuhdi, Fola Oladipo

## License

MIT License - Educational purposes only
