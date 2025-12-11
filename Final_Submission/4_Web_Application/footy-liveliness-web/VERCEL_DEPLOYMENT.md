# 🚀 Vercel Auto-Deployment Setup

## Quick Setup (5 Minutes)

### Step 1: Import Project to Vercel

1. Go to: https://vercel.com/new
2. Click **"Import Git Repository"**
3. Select: `James-Njoroge/FootyLiveliness`
4. Click **"Import"**

### Step 2: Configure Build Settings

```
Framework Preset:     Create React App
Root Directory:       Final_Submission/4_Web_Application/footy-liveliness-web
Build Command:        npm run build
Output Directory:     build
Install Command:      npm install
Node.js Version:      18.x (default)
```

### Step 3: Configure Git Settings

**IMPORTANT:** Change the production branch!

```
Production Branch:    raka-ridge  ← Change from 'main'
```

### Step 4: Deploy

Click **"Deploy"** and wait ~2 minutes.

---

## ✅ Auto-Deploy is Now Active!

Every time you push to `raka-ridge`:

```bash
git add .
git commit -m "Update frontend"
git push origin raka-ridge
```

Vercel will **automatically**:
1. ✅ Detect the push
2. ✅ Build your React app
3. ✅ Deploy to production
4. ✅ Update your live URL

---

## 🔧 Vercel Dashboard Settings

After initial deployment, verify these settings:

### Settings → Git

```
✅ Production Branch: raka-ridge
✅ Deploy Hooks: Enabled
✅ Auto-deploy: Enabled
✅ Preview Deployments: Enabled (optional)
```

### Settings → Environment Variables (Optional)

Add if you want to override the backend URL:

```
Name:  REACT_APP_API_URL
Value: https://footyliveliness.onrender.com
```

---

## 📊 Deployment Status

### Check Deployment Status:

1. Go to: https://vercel.com/dashboard
2. Click your project
3. View **"Deployments"** tab

### Deployment States:

- 🟡 **Building** - Vercel is building your app
- ✅ **Ready** - Deployed successfully
- ❌ **Error** - Build failed (check logs)

---

## 🌐 Your URLs

After deployment, you'll get:

### Production URL:
```
https://footy-liveliness.vercel.app
```

### Preview URLs (for each commit):
```
https://footy-liveliness-git-raka-ridge-yourname.vercel.app
```

---

## 🔄 How Auto-Deploy Works

```
┌─────────────────────────────────────────────────────────┐
│ 1. You Push Code                                        │
│    git push origin raka-ridge                           │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 2. GitHub Webhook Triggers Vercel                       │
│    GitHub → Vercel: "New commit detected!"              │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 3. Vercel Clones & Builds                               │
│    - Clone repo                                         │
│    - Run: npm install                                   │
│    - Run: npm run build                                 │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 4. Vercel Deploys to CDN                                │
│    - Upload build/ to global CDN                        │
│    - Update DNS                                         │
│    - Live in ~30 seconds                                │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 5. You Get Notification                                 │
│    ✅ Deployment successful!                            │
│    🌐 https://footy-liveliness.vercel.app               │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Test Auto-Deploy

### Make a Small Change:

```bash
# Edit a file
echo "// Test auto-deploy" >> src/App.js

# Commit and push
git add .
git commit -m "Test auto-deploy"
git push origin raka-ridge
```

### Watch Vercel:

1. Go to: https://vercel.com/dashboard
2. You'll see a new deployment start immediately
3. Wait ~2 minutes
4. Visit your URL to see the change

---

## 🐛 Troubleshooting

### Build Fails

**Check logs:**
1. Vercel Dashboard → Your Project → Deployments
2. Click the failed deployment
3. View **"Build Logs"**

**Common issues:**
- Missing dependencies: `npm install` failed
- Build errors: Check `npm run build` locally first
- Wrong Node version: Set to 18.x in settings

### Auto-Deploy Not Working

**Check:**
1. ✅ GitHub integration is connected
2. ✅ Production branch is set to `raka-ridge`
3. ✅ Webhooks are enabled (Settings → Git)

**Re-connect GitHub:**
1. Settings → Git → Disconnect
2. Re-import project from Vercel dashboard

### Wrong Branch Deploying

**Fix:**
1. Settings → Git
2. Change **"Production Branch"** to `raka-ridge`
3. Save changes

---

## 📝 Configuration Files

Your project includes:

### `vercel.json`
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "build",
  "framework": "create-react-app",
  "git": {
    "deploymentEnabled": {
      "raka-ridge": true
    }
  }
}
```

This tells Vercel:
- ✅ Build with `npm run build`
- ✅ Deploy from `build/` folder
- ✅ Use Create React App framework
- ✅ Auto-deploy from `raka-ridge` branch

---

## 🎉 You're All Set!

Now every push to `raka-ridge` will automatically deploy to Vercel!

### Next Steps:

1. ✅ Push code → Auto-deploys
2. ✅ Share your URL: `https://footy-liveliness.vercel.app`
3. ✅ Monitor deployments in Vercel dashboard

---

## 📚 Resources

- Vercel Docs: https://vercel.com/docs
- Deployment Guide: https://vercel.com/docs/deployments/overview
- GitHub Integration: https://vercel.com/docs/git/vercel-for-github
