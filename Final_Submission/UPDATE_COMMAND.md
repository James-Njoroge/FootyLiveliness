# 🔄 Update Command Documentation

## Overview

The `make update` command provides a one-step solution to refresh your application with the latest match data and predictions.

## What It Does

The update command performs three automated steps:

```bash
make update
```

### Step 1: Stop Application 🛑
- Gracefully stops Flask API
- Gracefully stops React frontend
- Frees ports 5001 and 3000
- Cleans up PID files

### Step 2: Re-scrape Data 🌐
- Fetches all 380 season fixtures from FotMob
- Extracts xG data for finished matches
- Updates `all_fixtures.json` with latest data
- Takes 3-5 minutes depending on network speed

### Step 3: Restart Application 🚀
- Starts Flask API (loads new data)
- Starts React frontend
- New predictions generated from updated fixtures
- Application ready with fresh data

## When to Use

### **Scenario 1: After Matches Are Played**
```bash
# New Premier League matches were played today
# You want to see the actual vs predicted comparison
make update
```

**Result:**
- New xG data fetched for finished matches
- Predictions updated
- Comparison view shows latest results

### **Scenario 2: New Fixtures Released**
```bash
# Premier League announced new fixture dates
# You want to see predictions for new matches
make update
```

**Result:**
- New upcoming fixtures added
- Predictions generated for new matches
- Week navigation shows new weeks

### **Scenario 3: Daily Refresh**
```bash
# You want the most current data
# Run update once per day
make update
```

**Result:**
- Always have latest match data
- Most accurate predictions
- Up-to-date comparison analysis

### **Scenario 4: Before Presentation**
```bash
# You're presenting to stakeholders
# Want to show real-time data
make update
```

**Result:**
- Impressive live data demonstration
- Current match predictions
- Latest accuracy metrics

## Usage Examples

### Basic Update
```bash
cd Final_Submission
make update
```

### Check Status After Update
```bash
make update
make status
```

### Update and Test
```bash
make update
make test
```

### Update and View Logs
```bash
make update
tail -f 4_Web_Application/footy-liveliness-web/api.log
```

## Output Example

```
╔════════════════════════════════════════════════════════════════╗
║              Updating Footy Liveliness Data                    ║
╚════════════════════════════════════════════════════════════════╝

📊 Step 1/3: Stopping application...
🛑 Stopping all processes...
✅ Flask API stopped
✅ React frontend stopped
✅ All processes stopped

🌐 Step 2/3: Re-scraping fixtures from FotMob...
Processing 380 matches...
  [1/380] Fetching details for Liverpool vs AFC Bournemouth...
    ✓ Got xG: 2.21 - 1.7
  [2/380] Fetching details for Chelsea vs Manchester City...
    ✓ Got xG: 1.85 - 2.35
  ...
✓ Saved 380 fixtures to ../data/current_season/all_fixtures.json
Summary:
  • Finished matches: 160 (145 with xG data)
  • Upcoming matches: 220
  • Total: 380

🚀 Step 3/3: Restarting application with new data...
✅ Flask API started on http://localhost:5001
✅ React frontend started on http://localhost:3000

╔════════════════════════════════════════════════════════════════╗
║              ✅ Update Complete!                               ║
╚════════════════════════════════════════════════════════════════╝

📱 Application running with latest data at http://localhost:3000
🔄 New predictions loaded from updated fixtures
```

## What Gets Updated

### Data Files
- ✅ `all_fixtures.json` - All 380 matches with latest xG
- ✅ Match status (finished/upcoming)
- ✅ Actual xG for newly finished matches
- ✅ Scores for completed games

### Predictions
- ✅ All 380 match predictions recalculated
- ✅ Rankings updated based on new data
- ✅ Week-by-week predictions refreshed
- ✅ Comparison view shows latest accuracy

### Application State
- ✅ Flask API reloads with new fixtures
- ✅ React frontend displays updated data
- ✅ All API endpoints return fresh predictions
- ✅ UI shows current match status

## Performance

### Timing
- **Stop:** ~1 second
- **Scrape:** ~3-5 minutes (380 matches)
- **Start:** ~10 seconds
- **Total:** ~4-6 minutes

### Network Usage
- **API Calls:** 150-160 (for finished matches)
- **Data Downloaded:** ~5-10 MB
- **Rate Limiting:** 0.5s between requests

## Comparison: Update vs Other Commands

### `make update`
- ✅ Stops, scrapes, restarts
- ✅ One command
- ✅ Ensures clean state
- ⏱️ ~4-6 minutes

### `make scrape` + `make stop` + `make start`
- ❌ Three separate commands
- ❌ Manual coordination
- ❌ Risk of forgetting steps
- ⏱️ Same time, more effort

### `make demo`
- ✅ Full setup from scratch
- ❌ Reinstalls dependencies (unnecessary)
- ❌ Slower
- ⏱️ ~10-15 minutes

## Troubleshooting

### Issue: Update Takes Too Long
**Solution:** Use faster scrape for upcoming only
```bash
make stop
cd 4_Web_Application/footy-liveliness-web
make scrape-upcoming  # Only ~5 seconds
cd ../..
make start
```

### Issue: Update Fails During Scrape
**Solution:** Check network connection and retry
```bash
make stop
make scrape  # Retry scraping
make start
```

### Issue: Application Won't Start After Update
**Solution:** Check logs and ports
```bash
make status
make kill-ports
make start
```

### Issue: Old Data Still Showing
**Solution:** Hard refresh browser
```
Press Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)
```

## Automation Ideas

### Daily Cron Job
```bash
# Update data every day at 6 AM
0 6 * * * cd /path/to/Final_Submission && make update
```

### Pre-Presentation Script
```bash
#!/bin/bash
echo "Preparing for presentation..."
make update
make test
echo "Ready to present!"
```

### CI/CD Integration
```yaml
# GitHub Actions example
- name: Update predictions
  run: make update
```

## Best Practices

### ✅ Do:
- Run update after match days
- Update before presentations
- Check status after update
- Test API after update

### ❌ Don't:
- Run update during presentations
- Update while app is in use
- Run multiple updates simultaneously
- Interrupt update mid-process

## Related Commands

```bash
make scrape           # Just scrape, don't restart
make start            # Just start, use existing data
make stop             # Just stop
make status           # Check if running
make test             # Test API endpoints
```

## Summary

The `make update` command is your **one-stop solution** for refreshing the application with the latest match data and predictions. It's perfect for:

- 📊 **Daily updates** - Keep data current
- 🎯 **Pre-presentation** - Show live data
- ✅ **After matches** - Get actual results
- 🔄 **Regular maintenance** - Stay up-to-date

**Simple, automated, reliable.** 🚀

---

**Last Updated:** December 10, 2025
