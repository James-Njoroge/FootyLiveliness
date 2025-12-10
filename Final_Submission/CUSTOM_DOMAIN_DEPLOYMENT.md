# 🌐 Deploy Footy Liveliness with Custom Domain

## Your Goal: `footyliveliness.com`

This guide will help you deploy your application with your own custom domain.

---

## 💰 Cost Breakdown

| Item | Cost | Provider |
|------|------|----------|
| Domain Name | $10-12/year | Namecheap/Cloudflare |
| Frontend Hosting | **FREE** | Vercel |
| Backend Hosting | **FREE** | Render |
| SSL Certificate | **FREE** | Automatic |
| **Total** | **$10-12/year** | |

---

## 📋 Complete Step-by-Step Guide

### Step 1: Purchase Domain (10 minutes)

#### Using Namecheap (Recommended):

1. **Go to:** https://www.namecheap.com
2. **Search:** `footyliveliness.com`
3. **Check availability:**
   - If available: Add to cart
   - If taken: Try `footyliveliness.app` or `footy-liveliness.com`
4. **Create account** and complete purchase
5. **Enable WhoisGuard** (free privacy protection)

#### Alternative: Cloudflare Registrar
- Cheapest option (~$10/year)
- Go to cloudflare.com → Registrar
- Search and purchase domain

---

### Step 2: Push Code to GitHub (5 minutes)

Open Terminal and run:

```bash
# Navigate to your project
cd "/Users/muhammadrakazuhdi/Desktop/Windsurf Projects/506/Footy Liveliness/FootyLiveliness/Final_Submission/4_Web_Application/footy-liveliness-web"

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Footy Liveliness"

# Create repository on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/footy-liveliness.git

# Push
git branch -M main
git push -u origin main
```

**To create GitHub repository:**
1. Go to github.com
2. Click "New repository"
3. Name: `footy-liveliness`
4. Click "Create repository"
5. Copy the repository URL

---

### Step 3: Deploy Backend to Render (15 minutes)

#### 3.1 Sign Up for Render

1. Go to **https://render.com**
2. Click "Get Started"
3. **Sign up with GitHub** (easiest)
4. Authorize Render to access your repositories

#### 3.2 Create Web Service for Flask API

1. **In Render Dashboard**, click **"New +"** → **"Web Service"**

2. **Connect Repository:**
   - Find and select `footy-liveliness`
   - Click "Connect"

3. **Configure Service:**
   ```
   Name: footy-liveliness-api
   Region: Oregon (US West) or closest to you
   Branch: main
   Root Directory: (leave empty)
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app --bind 0.0.0.0:$PORT
   Instance Type: Free
   ```

4. **Environment Variables** (click "Advanced"):
   - Add: `PYTHON_VERSION` = `3.9.18`

5. **Click "Create Web Service"**

6. **Wait for deployment** (~5-10 minutes)
   - Watch the build logs
   - Once complete, you'll get a URL like:
     `https://footy-liveliness-api.onrender.com`
   - **Save this URL!** You'll need it for the frontend

#### 3.3 Test Backend API

Once deployed, test it:
```bash
# In browser or terminal:
curl https://footy-liveliness-api.onrender.com/api/health
```

Should return: `{"status": "healthy"}`

---

### Step 4: Update Frontend API URL (2 minutes)

Before deploying frontend, update the API endpoint:

1. **Open:** `src/services/api.js`

2. **Find and replace:**

```javascript
// OLD (local development):
const API_BASE_URL = 'http://localhost:5001';

// NEW (production - use your actual Render URL):
const API_BASE_URL = 'https://footy-liveliness-api.onrender.com';
```

3. **Save the file**

4. **Commit and push:**
```bash
git add src/services/api.js
git commit -m "Update API URL for production"
git push origin main
```

---

### Step 5: Deploy Frontend to Vercel (10 minutes)

#### 5.1 Sign Up for Vercel

1. Go to **https://vercel.com**
2. Click "Sign Up"
3. **Sign up with GitHub** (recommended)
4. Authorize Vercel

#### 5.2 Import Project

1. **Click "Add New..."** → **"Project"**

2. **Import Git Repository:**
   - Find `footy-liveliness`
   - Click "Import"

3. **Configure Project:**
   ```
   Framework Preset: Create React App
   Root Directory: ./
   Build Command: npm run build
   Output Directory: build
   Install Command: npm install
   ```

4. **Environment Variables:** (none needed for now)

5. **Click "Deploy"**

6. **Wait for deployment** (~3-5 minutes)
   - Watch the build process
   - Once complete, you'll get a URL like:
     `https://footy-liveliness.vercel.app`

#### 5.3 Test Deployment

1. Visit your Vercel URL
2. Check if:
   - ✅ Page loads
   - ✅ Matches display
   - ✅ API calls work
   - ✅ No console errors

---

### Step 6: Connect Custom Domain (10 minutes)

#### 6.1 Add Domain to Vercel

1. **In Vercel Dashboard:**
   - Go to your project
   - Click "Settings" → "Domains"

2. **Add Domain:**
   - Enter: `footyliveliness.com`
   - Click "Add"

3. **Add www subdomain:**
   - Enter: `www.footyliveliness.com`
   - Click "Add"

4. **Vercel will show DNS records** you need to add

#### 6.2 Configure DNS at Namecheap

1. **Go to Namecheap Dashboard**
2. **Find your domain** → Click "Manage"
3. **Go to "Advanced DNS" tab**

4. **Add DNS Records:**

   **For root domain (footyliveliness.com):**
   ```
   Type: A Record
   Host: @
   Value: 76.76.21.21
   TTL: Automatic
   ```

   **For www subdomain:**
   ```
   Type: CNAME Record
   Host: www
   Value: cname.vercel-dns.com
   TTL: Automatic
   ```

5. **Save changes**

#### 6.3 Wait for DNS Propagation

- **Time:** 5 minutes to 48 hours (usually ~30 minutes)
- **Check status:** In Vercel dashboard, domain status will change to "Valid"
- **Test:** Try visiting `https://footyliveliness.com`

---

### Step 7: Enable HTTPS (Automatic)

Vercel automatically provisions SSL certificates:
- ✅ Happens automatically after DNS propagates
- ✅ Usually takes 5-10 minutes
- ✅ Your site will be accessible via `https://footyliveliness.com`

---

## 🎉 Success! Your Site is Live

Once DNS propagates, your application will be accessible at:
- ✅ **https://footyliveliness.com**
- ✅ **https://www.footyliveliness.com**

Backend API:
- ✅ **https://footy-liveliness-api.onrender.com**

---

## 🔧 Troubleshooting

### Domain Not Working

**Problem:** Domain shows "DNS_PROBE_FINISHED_NXDOMAIN"
- **Cause:** DNS not propagated yet
- **Solution:** Wait 30 minutes to 24 hours
- **Check:** Use https://dnschecker.org to check propagation

**Problem:** "Invalid Configuration"
- **Cause:** Wrong DNS records
- **Solution:** Double-check A and CNAME records match Vercel's instructions

### API Not Connecting

**Problem:** Frontend can't reach backend
- **Check:** API URL in `src/services/api.js`
- **Check:** CORS enabled in Flask (already done ✅)
- **Check:** Backend is running on Render

**Problem:** CORS errors in browser console
- **Solution:** Ensure `flask-cors` is installed and configured
- **Check:** `app.py` has `CORS(app)` line

### Build Failures

**Frontend build fails:**
- Check build logs in Vercel
- Ensure all dependencies in `package.json`
- Try building locally: `npm run build`

**Backend build fails:**
- Check build logs in Render
- Ensure all dependencies in `requirements.txt`
- Verify Python version compatibility

---

## 📊 Post-Deployment Checklist

After successful deployment:

- [ ] Visit `https://footyliveliness.com`
- [ ] Test all features:
  - [ ] Matches load correctly
  - [ ] Week navigation works
  - [ ] Comparison view displays
  - [ ] All modals open
  - [ ] Info button works
- [ ] Test on mobile device
- [ ] Check browser console for errors
- [ ] Test API endpoints directly
- [ ] Share link with friends/professor
- [ ] Update README.md with live URL
- [ ] Take screenshots for documentation

---

## 🔄 Making Updates

After initial deployment, updates are automatic:

```bash
# Make your changes
git add .
git commit -m "Description of changes"
git push origin main
```

- **Vercel:** Auto-deploys on every push (2-3 minutes)
- **Render:** Auto-deploys on every push (5-10 minutes)

---

## 💡 Pro Tips

### 1. Custom Subdomain for API
Instead of `footy-liveliness-api.onrender.com`, use `api.footyliveliness.com`:

**In Namecheap DNS:**
```
Type: CNAME
Host: api
Value: footy-liveliness-api.onrender.com
TTL: Automatic
```

**Update frontend:**
```javascript
const API_BASE_URL = 'https://api.footyliveliness.com';
```

### 2. Add Google Analytics
Track visitors by adding Google Analytics to your React app.

### 3. Set Up Monitoring
Use UptimeRobot (free) to:
- Keep backend awake (ping every 10 minutes)
- Get alerts if site goes down

### 4. Add Favicon
Create a custom favicon for your site:
- Use favicon.io to generate
- Replace `public/favicon.ico`

---

## 📈 Performance Optimization

### Enable Caching
Vercel automatically caches static assets.

### Optimize Images
If you add images later, use WebP format.

### Monitor Performance
- Use Vercel Analytics (free)
- Check Lighthouse scores in Chrome DevTools

---

## 🆘 Need Help?

### Vercel Support
- Documentation: vercel.com/docs
- Community: github.com/vercel/vercel/discussions

### Render Support
- Documentation: render.com/docs
- Community: community.render.com

### Domain Issues
- Namecheap Support: namecheap.com/support
- DNS Checker: dnschecker.org

---

## 📝 Quick Reference

### Important URLs
- **Your Site:** https://footyliveliness.com
- **Vercel Dashboard:** vercel.com/dashboard
- **Render Dashboard:** dashboard.render.com
- **GitHub Repo:** github.com/YOUR_USERNAME/footy-liveliness
- **Namecheap:** namecheap.com/myaccount

### DNS Records (Namecheap)
```
Type: A Record
Host: @
Value: 76.76.21.21

Type: CNAME
Host: www
Value: cname.vercel-dns.com
```

### Deployment Commands
```bash
# Push updates
git add .
git commit -m "Update message"
git push origin main

# Build locally
npm run build

# Test API locally
python3 app.py
```

---

## 🎓 For Your Submission

Include in your project submission:

1. **Live URL:** https://footyliveliness.com
2. **GitHub Repository:** https://github.com/YOUR_USERNAME/footy-liveliness
3. **API Endpoint:** https://footy-liveliness-api.onrender.com
4. **Screenshots:** Show key features
5. **This Guide:** Proves deployment capability

---

## 🎉 Congratulations!

You now have:
- ✅ Professional custom domain
- ✅ Live, accessible website
- ✅ Production-ready application
- ✅ Portfolio-worthy project
- ✅ Automatic deployments
- ✅ Free HTTPS/SSL

**Your application is live at:** https://footyliveliness.com 🚀

---

**Estimated Total Time:** 1-2 hours (including domain purchase and DNS propagation)  
**Total Cost:** $10-12/year (domain only, hosting is free)  
**Last Updated:** December 10, 2025
