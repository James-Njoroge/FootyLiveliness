# 🚀 Quick Start on a New Computer

## One-Command Setup

```bash
git clone https://github.com/James-Njoroge/FootyLiveliness.git && \
cd FootyLiveliness/Final_Submission/4_Web_Application/footy-liveliness-web && \
./setup.sh && \
make start
```

That's it! The app will automatically:
1. ✅ Clone the repository
2. ✅ Install Python dependencies
3. ✅ Install Node.js dependencies
4. ✅ Start both backend and frontend
5. ✅ Open in your browser at http://localhost:3000

---

## Prerequisites (Must Have Installed)

Before running the command above, install:

1. **Python 3.9+**
   - Mac: `brew install python3`
   - Windows: Download from https://python.org
   - Linux: `sudo apt install python3 python3-pip`

2. **Node.js 14+**
   - Mac: `brew install node`
   - Windows/Linux: Download from https://nodejs.org

3. **Git**
   - Mac: `brew install git`
   - Windows: Download from https://git-scm.com
   - Linux: `sudo apt install git`

---

## Manual Setup (If One-Command Fails)

### Step 1: Clone Repository
```bash
git clone https://github.com/James-Njoroge/FootyLiveliness.git
cd FootyLiveliness/Final_Submission/4_Web_Application/footy-liveliness-web
```

### Step 2: Install Dependencies
```bash
# Python dependencies
pip3 install -r requirements.txt

# Node.js dependencies
npm install
```

### Step 3: Start Application
```bash
# Option A: Using Makefile (recommended)
make start

# Option B: Manual (two terminals)
# Terminal 1:
python3 app.py

# Terminal 2:
npm start
```

---

## Verify Installation

### Check Backend (Flask API)
```bash
curl http://localhost:5001/api/health
```

Expected response:
```json
{"status": "healthy", "model": "Elastic Net", "features": 27}
```

### Check Frontend (React)
Open browser: http://localhost:3000

You should see the Footy Liveliness dashboard with ranked fixtures.

---

## Troubleshooting

### Port Already in Use
```bash
# Kill processes on ports 5001 and 3000
make stop

# Or manually:
lsof -ti:5001 | xargs kill -9
lsof -ti:3000 | xargs kill -9
```

### Module Not Found
```bash
# Reinstall Python dependencies
pip3 install -r requirements.txt

# Reinstall Node dependencies
rm -rf node_modules package-lock.json
npm install
```

### Python Version Issues
```bash
# Check Python version (must be 3.9+)
python3 --version

# If too old, install newer version
brew install python@3.11  # Mac
```

---

## Available Commands

| Command | Description |
|---------|-------------|
| `make start` | Start both backend and frontend |
| `make stop` | Stop all processes |
| `make restart` | Restart everything |
| `make api` | Start only Flask backend |
| `make web` | Start only React frontend |
| `make logs` | View application logs |
| `make clean` | Clean build artifacts |

---

## Project Structure

```
footy-liveliness-web/
├── app.py                  # Flask API backend
├── model.pkl               # Trained ML model
├── scaler.pkl              # Feature scaler
├── feature_names.pkl       # Feature names
├── team_stats.pkl          # Team statistics
├── requirements.txt        # Python dependencies
├── package.json            # Node.js dependencies
├── src/                    # React frontend source
│   ├── App.js
│   ├── components/
│   └── services/
└── public/                 # Static assets
```

---

## Next Steps

1. **View Predictions**: Open http://localhost:3000
2. **Test API**: `curl http://localhost:5001/api/upcoming`
3. **Scrape Live Data**: `python3 scrape_upcoming_fixtures.py`
4. **Read Documentation**: Check `README.md` for full details

---

## Production Deployment

- **Frontend**: Deployed on Vercel
- **Backend**: Deployed on Render at https://footyliveliness.onrender.com

See `README.md` for deployment instructions.

---

## Support

For issues or questions:
- Check `TROUBLESHOOTING.md`
- Review logs: `make logs`
- Restart: `make restart`
