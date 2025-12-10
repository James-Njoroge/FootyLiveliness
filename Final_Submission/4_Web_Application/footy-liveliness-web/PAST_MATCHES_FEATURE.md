# Past Matches Feature - Predicted vs Actual Comparison

## Overview

The application now supports viewing past matches and comparing predicted liveliness scores with actual results!

## What's New

### 1. **All-Season Scraper**
- New script: `scrape_all_season_fixtures.py`
- Fetches **all matches** from the current season (past + future)
- For finished matches, retrieves actual xG data from FotMob
- Calculates actual "Simple xG" liveliness score

### 2. **Past Week Navigation**
- Navigate back to previous weeks using the ← button
- View matches that have already been played
- See how well the model predicted each match

### 3. **Predicted vs Actual Comparison**
For finished matches, each card now shows:
- **Predicted Score** (purple bar) - What the model predicted
- **Actual Score** (green bar) - What actually happened
- **Accuracy Percentage** - How close the prediction was
  - 🟢 Green (90%+) - Excellent prediction
  - 🔵 Blue (75-90%) - Good prediction
  - 🟡 Yellow (60-75%) - Fair prediction
  - 🔴 Red (<60%) - Poor prediction

## How to Use

### Step 1: Scrape All Season Data
```bash
# This will fetch all matches including past ones with actual xG
make scrape

# Or manually:
python3 scrape_all_season_fixtures.py
```

**Note:** This may take 2-5 minutes as it fetches detailed match data for each finished game.

### Step 2: Start the Application
```bash
make start
```

### Step 3: Navigate to Past Weeks
1. Open http://localhost:3000
2. Click the **← Previous** button to go back in time
3. View past weeks to see predicted vs actual comparison
4. Green bars show actual results, purple bars show predictions

## Technical Details

### Data Structure

**Finished Match Example:**
```json
{
  "matchId": 4193490,
  "home": "Liverpool",
  "away": "Chelsea",
  "date": "2025-12-15",
  "time": "17:30",
  "status": "finished",
  "actualScore": {
    "home": 2,
    "away": 1
  },
  "actualXG": {
    "home": 2.3,
    "away": 1.5,
    "total": 3.8,
    "simple_xg": 5.3
  }
}
```

### Accuracy Calculation

```javascript
accuracy = 100 - (|predicted - actual| / actual) * 100
```

Example:
- Predicted: 5.5
- Actual: 5.3
- Difference: 0.2
- Accuracy: 100 - (0.2 / 5.3) * 100 = 96.2% ✅

### API Changes

The `/api/upcoming` endpoint now returns:
- All matches (past and future)
- `status` field: "finished", "ongoing", or "upcoming"
- `actualXG` and `actualScore` for finished matches

## Benefits

### For Users
- **Validate model accuracy** on real historical data
- **Build confidence** in predictions for upcoming matches
- **Learn patterns** - which types of matches the model predicts well

### For Evaluation
- **Transparent performance** - see every prediction vs reality
- **Week-by-week analysis** - track model performance over time
- **Visual comparison** - easy to spot good and bad predictions

## Example Use Cases

### 1. Check Last Week's Predictions
```
Navigate to last week → See all matches
Green bars show actual excitement levels
Compare with purple predicted bars
```

### 2. Find Model Strengths
```
Look for matches with 90%+ accuracy
These show match types the model predicts well
Example: Top-6 clashes, high-scoring games
```

### 3. Find Model Weaknesses
```
Look for matches with <60% accuracy
These show where the model struggles
Example: Unexpected upsets, defensive games
```

## Performance Expectations

Based on test data, the model achieves:
- **82% R² Score** - Overall variance explained
- **90% Top-10 Hit Rate** - Correctly identifies most exciting matches
- **~75-85% accuracy** on individual match predictions

## Scraper Details

### What Gets Scraped

**For All Matches:**
- Match ID, teams, date, time
- Match status (finished/ongoing/upcoming)

**For Finished Matches (additional):**
- Actual xG (home and away)
- Actual score
- Simple xG calculation

### Rate Limiting

The scraper includes:
- 0.5 second delay between match detail requests
- Graceful error handling
- Progress indicators

### Estimated Time

- **Upcoming matches only:** ~5 seconds
- **All season (with past matches):** 2-5 minutes
  - Depends on number of finished matches
  - ~0.5 seconds per finished match

## Troubleshooting

### No Past Matches Showing

**Problem:** Only seeing upcoming matches

**Solution:**
```bash
# Make sure you ran the all-season scraper
python3 scrape_all_season_fixtures.py

# Check the output file
cat ../data/current_season/all_fixtures.json | grep "finished"
```

### Actual Data Missing

**Problem:** Past matches don't show actual scores

**Possible causes:**
1. FotMob hasn't published xG data yet (takes ~1 hour after match)
2. Match details API failed
3. xG data not available for that match

**Solution:** Re-run scraper after a few hours

### Scraper Taking Too Long

**Problem:** Scraper seems stuck

**Solution:**
```bash
# Use the faster upcoming-only scraper instead
python3 scrape_upcoming_fixtures.py

# Or check progress - scraper prints status for each match
```

## Future Enhancements

Potential improvements:
- [ ] Cache scraped data to avoid re-fetching
- [ ] Incremental updates (only fetch new matches)
- [ ] Aggregate statistics (average accuracy per week)
- [ ] Filter by accuracy threshold
- [ ] Export comparison data to CSV

## Commands Summary

```bash
# Scrape all season data (past + future)
make scrape

# Scrape only upcoming (faster)
make scrape-upcoming

# Start application
make start

# Check status
make status

# Stop application
make stop
```

---

**Last Updated:** December 10, 2025
