# 🎯 Running with Live Data

## ✅ **Automatic Live Data Fetching**

Your app now automatically fetches upcoming Premier League matches when started!

### **Quick Start:**

```bash
cd web-app

# Option 1: Use the startup script (Recommended)
./start-with-live-data.sh

# Option 2: Use npm command
npm run start:live

# Option 3: Manual steps
npm run fetch-live  # Fetch live matches
npm run dev:full    # Start both servers
```

## 🔄 **How It Works:**

1. **Scraper runs** (`data/scrape_upcoming.py`)
   - Connects to FotMob fixtures page
   - Extracts upcoming matches
   - Calculates features from historical data
   - Saves to `src/utils/live_matches.json`

2. **Frontend loads data** (`src/utils/predictor.js`)
   - Tries to load `live_matches.json`
   - Falls back to sample data if not available
   - Displays matches in the UI

3. **Backend serves predictions**
   - Uses your trained Ridge model
   - Ranks matches by liveliness
   - Returns sorted results

## 📊 **Data Flow:**

```
┌─────────────────────┐
│  FotMob Website     │
│  (Fixtures Page)    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  scrape_upcoming.py │ (Selenium)
│  - Fetch fixtures   │
│  - Extract details  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Historical Data    │
│  tables/*.csv       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Feature Calculation│
│  (38 features)      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  live_matches.json  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  React Frontend     │
│  (Display matches)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Flask Backend      │
│  (Ridge predictions)│
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Ranked Matches     │
│  (By liveliness)    │
└─────────────────────┘
```

## 🛠️ **Configuration:**

### **Update Scraper Settings:**

Edit `data/scrape_upcoming.py`:

```python
# Chrome driver path
CHROMEDRIVER_PATH = "/opt/homebrew/bin/chromedriver"

# Run in background (no browser window)
HEADLESS = True

# Output file
OUTPUT_FILE = "../web-app/src/utils/live_matches.json"
```

### **Update Historical Data Paths:**

```python
HISTORICAL_DATA_PATH = "../tables/all_rounds.csv"
FEATURES_DATA_PATH = "../feature_tables/match_features_enhanced.csv"
```

## 📅 **Refresh Schedule:**

### **Manual Refresh:**
```bash
npm run fetch-live
```

### **Automatic Refresh (Recommended):**

**Option 1: Run before each session**
```bash
./start-with-live-data.sh
```

**Option 2: Set up cron job (Weekly)**
```bash
# Edit crontab
crontab -e

# Add this line (runs every Saturday at 6 AM)
0 6 * * 6 cd /path/to/FootyLiveliness/data && python3 scrape_upcoming.py
```

**Option 3: GitHub Actions (Automated)**
Create `.github/workflows/update-fixtures.yml`:
```yaml
name: Update Fixtures
on:
  schedule:
    - cron: '0 6 * * 6'  # Saturday 6 AM
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: |
          cd data
          python3 scrape_upcoming.py
          git add ../web-app/src/utils/live_matches.json
          git commit -m "Update fixtures"
          git push
```

## 🔧 **Troubleshooting:**

### **"No matches found"**
- Check if FotMob website structure changed
- Verify chromedriver is working: `chromedriver --version`
- Run with `HEADLESS = False` to see what's happening

### **"selenium-wire not found"**
```bash
pip3 install selenium-wire brotli
```

### **"Permission denied: chromedriver"**
```bash
chmod +x /opt/homebrew/bin/chromedriver
xattr -d com.apple.quarantine /opt/homebrew/bin/chromedriver
```

### **"Features not calculating correctly"**
- Verify historical data paths are correct
- Check that `tables/all_rounds.csv` exists
- Ensure team names match exactly

## 📈 **Improving Feature Calculation:**

The current scraper uses simplified feature calculation. To improve:

1. **Load your feature calculation logic:**
```python
# Import from your existing scripts
from create_features import calculate_rolling_features

def calculate_team_features(team_name, historical_df):
    return calculate_rolling_features(team_name, historical_df)
```

2. **Add league table data:**
```python
# Get current standings
standings = get_league_table()
match['homePosition'] = standings[home_team]['position']
```

3. **Calculate form indicators:**
```python
# Last 5 matches form
form = get_team_form(team_name, last_n=5)
match['homeForm'] = form  # e.g., "WWDLW"
```

## ✅ **Verification:**

After running, check:

1. **File created:**
```bash
ls -lh web-app/src/utils/live_matches.json
```

2. **Valid JSON:**
```bash
cat web-app/src/utils/live_matches.json | python3 -m json.tool | head -20
```

3. **Matches loaded in app:**
- Open http://localhost:3000
- Check browser console for "Live matches" or "Sample data" message
- Verify match names look real

## 🎉 **Success Indicators:**

✅ Scraper runs without errors
✅ `live_matches.json` file created
✅ File contains upcoming fixtures
✅ Features calculated for each match
✅ Frontend loads live data
✅ Backend serves predictions
✅ Matches ranked by liveliness

---

**Your app now uses live data! 🚀**

Run `./start-with-live-data.sh` and watch it fetch real upcoming matches!
