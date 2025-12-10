# 🚀 Footy Liveliness - Complete Deployment Guide

This guide will help you deploy your full-stack application (React + Flask) to the internet for **FREE** without needing a domain.

---

## 📋 What You'll Get

- ✅ Live website accessible from anywhere
- ✅ Free subdomain (e.g., `footy-liveliness.onrender.com`)
- ✅ Automatic HTTPS (secure connection)
- ✅ No credit card required
- ✅ Perfect for academic submissions and portfolio

---

## 🎯 Deployment Option: Render.com (Recommended)

**Why Render?**
- Free tier with no credit card
- Supports Python (Flask) + Static Sites (React)
- Easy GitHub integration
- Automatic deployments
- Free SSL certificates

---

## 📝 Step-by-Step Deployment Process

### Step 1: Create GitHub Repository

1. **Go to GitHub.com** and sign in (or create account)
2. **Click "New Repository"**
   - Name: `footy-liveliness`
   - Description: `AI-Powered Premier League Match Excitement Predictor`
   - Public or Private (your choice)
   - Don't initialize with README (we have files already)
3. **Click "Create repository"**

### Step 2: Push Your Code to GitHub

Open Terminal in your project folder and run:

```bash
# Navigate to your project
cd "/Users/muhammadrakazuhdi/Desktop/Windsurf Projects/506/Footy Liveliness/FootyLiveliness/Final_Submission/4_Web_Application/footy-liveliness-web"

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Footy Liveliness"

# Add your GitHub repository (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/footy-liveliness.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Note:** Replace `YOUR_USERNAME` with your actual GitHub username.

### Step 3: Sign Up for Render.com

1. **Go to:** https://render.com
2. **Click "Get Started"**
3. **Sign up with GitHub** (easiest option)
4. **Authorize Render** to access your repositories

### Step 4: Deploy Flask Backend

1. **In Render Dashboard**, click **"New +"** → **"Web Service"**

2. **Connect Repository:**
   - Select `footy-liveliness` repository
   - Click "Connect"

3. **Configure Web Service:**
   - **Name:** `footy-liveliness-api`
   - **Region:** Choose closest to you
   - **Branch:** `main`
   - **Root Directory:** Leave empty (or set to root)
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Instance Type:** `Free`

4. **Environment Variables** (click "Advanced"):
   - Add: `PYTHON_VERSION` = `3.9.18`
   - Add: `PORT` = `5001` (optional, Render sets this)

5. **Click "Create Web Service"**

6. **Wait for deployment** (~5-10 minutes)
   - You'll see build logs
   - Once complete, you'll get a URL like: `https://footy-liveliness-api.onrender.com`

### Step 5: Update React Frontend API URL

Before deploying frontend, update the API URL:

1. **Open:** `src/services/api.js`

2. **Find the API_BASE_URL** and update it:

```javascript
// Change from:
const API_BASE_URL = 'http://localhost:5001';

// To your Render backend URL:
const API_BASE_URL = 'https://footy-liveliness-api.onrender.com';
```

3. **Commit and push changes:**

```bash
git add src/services/api.js
git commit -m "Update API URL for production"
git push origin main
```

### Step 6: Deploy React Frontend

1. **In Render Dashboard**, click **"New +"** → **"Static Site"**

2. **Connect Repository:**
   - Select `footy-liveliness` repository
   - Click "Connect"

3. **Configure Static Site:**
   - **Name:** `footy-liveliness`
   - **Branch:** `main`
   - **Root Directory:** Leave empty
   - **Build Command:** `npm install && npm run build`
   - **Publish Directory:** `build`

4. **Click "Create Static Site"**

5. **Wait for deployment** (~3-5 minutes)
   - Once complete, you'll get a URL like: `https://footy-liveliness.onrender.com`

### Step 7: Test Your Deployed Application

1. **Visit your frontend URL:** `https://footy-liveliness.onrender.com`
2. **Check if:**
   - ✅ Page loads correctly
   - ✅ Matches are displayed
   - ✅ Week navigation works
   - ✅ Modals open (About, Getting Started, etc.)
   - ✅ No console errors

---

## 🔧 Troubleshooting

### Backend Issues

**Problem:** Backend won't start
- **Check:** Build logs in Render dashboard
- **Fix:** Ensure `requirements.txt` has all dependencies
- **Fix:** Verify `gunicorn` is installed

**Problem:** API returns 500 errors
- **Check:** Application logs in Render
- **Fix:** Ensure `model.pkl`, `scaler.pkl`, `team_stats.pkl` are in repository
- **Fix:** Check file paths in `app.py`

### Frontend Issues

**Problem:** "Cannot connect to API"
- **Check:** API URL in `src/services/api.js`
- **Fix:** Ensure it matches your Render backend URL
- **Fix:** Check CORS is enabled in Flask (`flask-cors`)

**Problem:** Build fails
- **Check:** Build logs in Render
- **Fix:** Ensure `package.json` has all dependencies
- **Fix:** Run `npm install` locally to verify

### CORS Issues

If you see CORS errors in browser console:

1. **Update `app.py`:**

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

2. **Commit and push:**

```bash
git add app.py
git commit -m "Fix CORS for production"
git push origin main
```

---

## 💰 Cost Breakdown

### Render Free Tier Limits:
- ✅ **Backend (Web Service):** 750 hours/month (enough for 24/7)
- ✅ **Frontend (Static Site):** Unlimited
- ⚠️ **Limitation:** Backend sleeps after 15 min of inactivity
  - First request after sleep takes ~30 seconds to wake up
  - Subsequent requests are instant

### To Keep Backend Always Active (Optional):
- Upgrade to paid plan ($7/month)
- Or use a free service like UptimeRobot to ping every 10 minutes

---

## 🌐 Alternative Deployment Options

### Option 2: Netlify (Frontend) + Render (Backend)

**Frontend on Netlify:**
1. Go to netlify.com
2. Drag and drop your `build` folder
3. Get instant deployment

**Backend on Render:**
- Same as Step 4 above

### Option 3: Heroku (Full-Stack)

**Note:** Heroku removed free tier in 2022, now requires credit card.

1. Install Heroku CLI
2. Create `Procfile`:
   ```
   web: gunicorn app:app
   ```
3. Deploy:
   ```bash
   heroku create footy-liveliness
   heroku buildpacks:add heroku/python
   heroku buildpacks:add heroku/nodejs
   git push heroku main
   ```

### Option 4: Railway.app

Similar to Render but with different interface:
1. Sign up at railway.app
2. Connect GitHub repository
3. Deploy with one click

---

## 📊 Post-Deployment Checklist

After successful deployment:

- [ ] Test all features on live site
- [ ] Update README.md with live URL
- [ ] Add live URL to PROJECT_DOCUMENTATION.md
- [ ] Test on mobile devices
- [ ] Share link with professor/classmates
- [ ] Take screenshots for documentation
- [ ] Record demo video (optional)

---

## 🎓 For Academic Submission

Include in your submission:

1. **Live URL:** `https://footy-liveliness.onrender.com`
2. **GitHub Repository:** `https://github.com/YOUR_USERNAME/footy-liveliness`
3. **Demo Video:** (optional but impressive)
4. **Screenshots:** Show key features
5. **This Deployment Guide:** Proves you can deploy

---

## 🆘 Need Help?

If you encounter issues:

1. **Check Render Logs:**
   - Dashboard → Your Service → Logs tab
   - Look for error messages

2. **Check Browser Console:**
   - Right-click → Inspect → Console tab
   - Look for API errors

3. **Common Fixes:**
   - Clear browser cache
   - Rebuild and redeploy
   - Check environment variables
   - Verify API URL is correct

---

## 🎉 Success!

Once deployed, you'll have:
- ✅ Live website accessible from anywhere
- ✅ Professional portfolio piece
- ✅ Shareable link for your resume
- ✅ Proof of full-stack deployment skills

**Your live URLs:**
- Frontend: `https://footy-liveliness.onrender.com`
- Backend API: `https://footy-liveliness-api.onrender.com`

---

## 📝 Quick Reference Commands

```bash
# Check git status
git status

# Add all changes
git add .

# Commit changes
git commit -m "Your message"

# Push to GitHub
git push origin main

# View git remote
git remote -v

# Build React locally
npm run build

# Test Flask locally
python3 app.py
```

---

**Last Updated:** December 10, 2025  
**Deployment Platform:** Render.com (Free Tier)  
**Estimated Time:** 30-45 minutes for first deployment
