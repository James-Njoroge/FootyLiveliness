# FotMob Upcoming Fixtures Scraper

## Overview

This scraper fetches upcoming Premier League fixtures from FotMob's public API and prepares them for prediction by the Elastic Net model.

## Features

- ✅ Fetches real-time upcoming Premier League fixtures from FotMob
- ✅ Extracts match details (teams, date, time, match ID)
- ✅ Filters out finished/ongoing matches
- ✅ Saves fixtures in JSON format for the Flask API
- ✅ Automatic fallback to alternative endpoints
- ✅ No authentication required (uses public API)

## Requirements

```bash
pip3 install requests
```

## Usage

### 1. Run the Scraper

```bash
cd footy-liveliness-web
python3 scrape_upcoming_fixtures.py
```

### 2. Output

The scraper will:
- Fetch upcoming fixtures from FotMob
- Display found fixtures in the terminal
- Save them to `../data/current_season/upcoming_fixtures.json`

Example output:
```
================================================================================
FOTMOB UPCOMING FIXTURES SCRAPER
================================================================================

Fetching league data from FotMob...
✓ Successfully fetched league data
✓ Found 10 upcoming fixtures

================================================================================
FOUND 10 UPCOMING FIXTURES
================================================================================

 1. Arsenal                    vs Manchester City            | 2025-01-15 20:00
 2. Liverpool                  vs Chelsea                    | 2025-01-15 17:30
 3. Manchester United          vs Tottenham Hotspur          | 2025-01-16 16:30
 ...

✓ Saved 10 fixtures to ../data/current_season/upcoming_fixtures.json

================================================================================
✓ SCRAPING COMPLETE
================================================================================

Next steps:
1. Run the Flask API: python3 app.py
2. The API will use these fixtures for predictions
3. View predictions at http://localhost:3000
```

### 3. Use with Flask API

The Flask API automatically loads fixtures from the JSON file:

```bash
# Start the API (it will auto-load the scraped fixtures)
python3 app.py
```

To manually refresh fixtures while the API is running:
```bash
curl -X POST http://localhost:5001/api/refresh-fixtures
```

## How It Works

### 1. Data Source
- **FotMob API**: `https://www.fotmob.com/api/leagues?id=47`
- **League ID**: 47 (Premier League)
- **Public endpoint**: No authentication required

### 2. Scraping Process

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Fetch League Data                                        │
│    GET /api/leagues?id=47                                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. Extract Upcoming Matches                                 │
│    - Filter: status.started = false                         │
│    - Filter: status.finished = false                        │
│    - Extract: home, away, date, time, matchId               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. Save to JSON                                             │
│    ../data/current_season/upcoming_fixtures.json            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. Flask API Loads Fixtures                                 │
│    - Creates features from team stats                       │
│    - Runs Elastic Net predictions                           │
│    - Ranks by predicted liveliness                          │
└─────────────────────────────────────────────────────────────┘
```

### 3. Data Format

The scraper saves fixtures in this format:

```json
[
  {
    "matchId": 4506263,
    "home": "Arsenal",
    "away": "Manchester City",
    "date": "2025-01-15",
    "time": "20:00",
    "timestamp": "2025-01-15T20:00:00Z"
  },
  ...
]
```

## Integration with Model

### Feature Creation Pipeline

```python
# 1. Scraper provides fixtures
fixtures = load_upcoming_fixtures()

# 2. API creates features for each match
for fixture in fixtures:
    X = create_features_for_match(fixture['home'], fixture['away'])
    
    # Features include:
    # - Home team rolling stats (xG, shots, corners, etc.)
    # - Away team rolling stats
    # - Contextual features (league position, form, etc.)
    
# 3. Model predicts liveliness
    X_scaled = scaler.transform(X)
    prediction = model.predict(X_scaled)[0]
    
# 4. Fixtures ranked by predicted excitement
    predictions.sort(key=lambda x: x['predicted_liveliness'], reverse=True)
```

## Scheduling (Optional)

To automatically scrape fixtures daily:

### Using cron (Mac/Linux)

```bash
# Edit crontab
crontab -e

# Add this line to run daily at 6 AM
0 6 * * * cd /path/to/footy-liveliness-web && python3 scrape_upcoming_fixtures.py
```

### Using Python scheduler

```python
import schedule
import time

def job():
    os.system('python3 scrape_upcoming_fixtures.py')

schedule.every().day.at("06:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## Troubleshooting

### No fixtures found

**Possible causes:**
- No upcoming matches scheduled (check FotMob manually)
- FotMob API structure changed
- Network/connection issues

**Solutions:**
1. Check https://www.fotmob.com/leagues/47/fixtures/premier-league
2. Verify internet connection
3. Check if FotMob is accessible

### API returns mock data

**Cause:** Fixtures file is empty or missing

**Solution:**
```bash
# Run the scraper
python3 scrape_upcoming_fixtures.py

# Verify file was created
cat ../data/current_season/upcoming_fixtures.json

# Restart Flask API
python3 app.py
```

### Predictions seem off

**Possible causes:**
- Team stats are outdated
- Team names don't match between scraper and model

**Solutions:**
1. Check team name consistency in `team_stats.pkl`
2. Update team stats with latest season data
3. Verify feature engineering pipeline

## API Endpoints

After scraping, these endpoints use the fixtures:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/upcoming` | GET | Get ranked upcoming fixtures with predictions |
| `/api/refresh-fixtures` | POST | Reload fixtures from JSON file |
| `/api/predict` | POST | Predict single match liveliness |
| `/api/stats` | GET | Model performance statistics |

## Comparison: Scraper vs Original Notebook

| Feature | Original Notebook | This Scraper |
|---------|------------------|--------------|
| Purpose | Scrape historical match data | Scrape upcoming fixtures |
| Selenium | ✅ Required | ❌ Not needed |
| ChromeDriver | ✅ Required | ❌ Not needed |
| Network Interception | ✅ selenium-wire | ❌ Direct API calls |
| Data Volume | 380 matches (full season) | 10-20 matches (upcoming) |
| Speed | ~5-10 minutes | ~2 seconds |
| Complexity | High (browser automation) | Low (simple HTTP requests) |
| Dependencies | selenium, selenium-wire, brotli | requests only |

## Future Enhancements

- [ ] Add retry logic with exponential backoff
- [ ] Support multiple leagues (La Liga, Serie A, etc.)
- [ ] Scrape team form/injuries for better predictions
- [ ] Add webhook notifications when new fixtures are found
- [ ] Cache results to reduce API calls
- [ ] Add logging to file for debugging

## Credits

Based on the original FotMob scraping methodology by James Njoroge.
Simplified for upcoming fixtures only (no Selenium required).

## License

Part of the Footy Liveliness project - CS 506, Boston University, Fall 2025
