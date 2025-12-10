# 🚀 Deployment Quick Start

## ✅ Your Application is Ready to Deploy!

All necessary files are configured:
- ✅ `requirements.txt` - Python dependencies (including gunicorn)
- ✅ `package.json` - Node dependencies
- ✅ `app.py` - Flask API with CORS enabled
- ✅ Model files - `model.pkl`, `scaler.pkl`, `team_stats.pkl`

---

## 🎯 Recommended Path: Render.com (Free)

**Time Required:** 30-45 minutes  
**Cost:** $0 (Free tier)  
**Domain:** Free subdomain (e.g., `footy-liveliness.onrender.com`)

---

## 📋 Quick Steps

### 1. Push to GitHub (5 minutes)
```bash
cd "/Users/muhammadrakazuhdi/Desktop/Windsurf Projects/506/Footy Liveliness/FootyLiveliness/Final_Submission/4_Web_Application/footy-liveliness-web"

git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/footy-liveliness.git
git push -u origin main
```

### 2. Deploy Backend to Render (10 minutes)
1. Go to render.com → Sign up with GitHub
2. New Web Service → Connect repository
3. Configure:
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app --bind 0.0.0.0:$PORT`
4. Deploy!

### 3. Update Frontend API URL (2 minutes)
Edit `src/services/api.js`:
```javascript
const API_BASE_URL = 'https://YOUR-API-URL.onrender.com';
```

### 4. Deploy Frontend to Render (10 minutes)
1. New Static Site → Connect repository
2. Configure:
   - Build: `npm install && npm run build`
   - Publish: `build`
3. Deploy!

---

## 📖 Full Guide

See **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** for:
- Detailed step-by-step instructions
- Screenshots and examples
- Troubleshooting tips
- Alternative deployment options
- Post-deployment checklist

---

## 🆘 Quick Help

**Problem:** Don't have GitHub account?
- **Solution:** Create one at github.com (free, 2 minutes)

**Problem:** Git not installed?
- **Solution:** Download from git-scm.com

**Problem:** Want to test locally first?
- **Solution:** Run `make start` - already working!

---

## 🎓 For Your Submission

Once deployed, you'll have:
- ✅ Live URL to share with professor
- ✅ Professional portfolio piece
- ✅ Proof of deployment skills
- ✅ Accessible from anywhere

**Example URLs:**
- Frontend: `https://footy-liveliness.onrender.com`
- API: `https://footy-liveliness-api.onrender.com`

---

## 💡 Pro Tips

1. **Deploy backend first** - Frontend needs backend URL
2. **Test locally** - Make sure `make start` works
3. **Check logs** - Render shows build/runtime logs
4. **Be patient** - First deployment takes 5-10 minutes
5. **Free tier sleeps** - First request after 15min takes ~30s

---

**Ready to deploy?** Follow [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)!
