# Footy Liveliness API

Flask backend API for serving Ridge Regression predictions.

## Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
python app.py
```

Server runs on `http://localhost:5000`

## API Endpoints

### Health Check
```bash
GET /api/health
```

### Single Match Prediction
```bash
POST /api/predict
Content-Type: application/json

{
  "homeTeam": "Liverpool",
  "awayTeam": "Manchester City",
  "features": {
    "home_xG_att_90": 2.3,
    "away_xG_att_90": 2.1,
    "home_position": 1,
    "away_position": 2,
    ...
  }
}
```

### Batch Predictions
```bash
POST /api/predict/batch
Content-Type: application/json

{
  "matches": [
    {
      "id": 1,
      "homeTeam": "Liverpool",
      "awayTeam": "Manchester City",
      "features": {...}
    }
  ]
}
```

### Model Info
```bash
GET /api/model/info
```

## Required Features (37 total)

**Rolling Form (16 features):**
- `home_xG_att_90`, `home_SoT_att_90`, `home_BigCh_att_90`, `home_Corn_att_90`, `home_ToB_att_90`
- `home_xGA_def_90`, `home_SoT_agst_90`, `home_BigCh_agst_90`
- Same for away team (8 features)

**League Context (5 features):**
- `home_position`, `away_position`, `points_diff`, `gd_diff`

**Form Trajectory (6 features):**
- `home_last3_points`, `home_last3_goals`, `home_form_trend`
- `away_last3_points`, `away_last3_goals`, `away_form_trend`

**Contextual (2 features):**
- `home_strength_ratio`, `away_strength_ratio`

**Composite features are auto-calculated:**
- `TempoSum`, `SoTSum`, `AttackVsDefense`, `xG_att_sum`, `xG_att_min`, `BigCh_sum`
- `position_diff`, `both_top6`, `both_bottom6`, `close_positions`
