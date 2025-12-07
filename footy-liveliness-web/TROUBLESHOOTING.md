# 🔧 Troubleshooting Guide

## Issue: Predictions Not Loading

### Problem
The web app shows "Failed to load predictions" error.

### Cause
Port 5000 is used by macOS AirPlay/AirTunes service by default.

### Solution ✅
**We've already fixed this!** The app now uses port **5001** instead.

---

## Quick Fixes

### 1. Restart Everything

```bash
# Kill all servers
lsof -ti:5001 | xargs kill -9 2>/dev/null
lsof -ti:8000 | xargs kill -9 2>/dev/null

# Restart
./run.sh
```

### 2. Check if API is Running

```bash
curl http://localhost:5001/api/upcoming
```

Should return JSON with match predictions.

### 3. Check if Web Server is Running

Visit: http://localhost:8000

Should show the web app.

### 4. View Logs

```bash
# API logs
tail -f api.log

# Web server logs
tail -f web.log
```

---

## Common Issues

### "Port already in use"

```bash
# Find what's using the port
lsof -i :5001
lsof -i :8000

# Kill it
lsof -ti:5001 | xargs kill -9
lsof -ti:8000 | xargs kill -9
```

### "Module not found"

```bash
pip3 install -r requirements.txt
```

### "Model file not found"

```bash
python3 train_and_save_model.py
```

### CORS Errors in Browser

Make sure you're accessing via `http://localhost:8000` (not `file://`)

---

## Verify Everything is Working

### Test API Health

```bash
curl http://localhost:5001/api/health
```

Expected output:
```json
{
  "status": "healthy",
  "model": "Elastic Net",
  "features": 27
}
```

### Test Predictions

```bash
curl http://localhost:5001/api/upcoming | python3 -m json.tool
```

Should show ranked fixtures.

### Test Web App

1. Open http://localhost:8000
2. Should see match rankings
3. Check browser console (F12) for errors

---

## Still Not Working?

### Complete Reset

```bash
# 1. Kill everything
pkill -f "python3 app.py"
pkill -f "python3 -m http.server"

# 2. Clean up
rm -f api.log web.log .api.pid .web.pid

# 3. Restart
./run.sh
```

### Manual Start (Debug Mode)

Terminal 1 - API:
```bash
python3 app.py
```

Terminal 2 - Web:
```bash
python3 -m http.server 8000
```

Watch for errors in both terminals.

---

## macOS Specific: Disable AirPlay on Port 5000

If you want to use port 5000:

1. System Settings → General → AirDrop & Handoff
2. Turn off "AirPlay Receiver"

Then change back to port 5000 in:
- `app.py` (line 165)
- `index.html` (line 117)
- `run.sh` (line 17, 22, 45)

---

## Success Checklist

- [ ] API running on http://localhost:5001
- [ ] Web server running on http://localhost:8000
- [ ] `curl http://localhost:5001/api/upcoming` returns JSON
- [ ] Browser shows match rankings
- [ ] No CORS errors in browser console

---

## Need Help?

Check the logs:
```bash
tail -f api.log
tail -f web.log
```

Or run manually to see errors in real-time.
