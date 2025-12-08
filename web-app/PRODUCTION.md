# Production Deployment Guide

## Architecture

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│  React Frontend │ ───> │  Flask API       │ ───> │ Ridge Model     │
│  (Vite Build)   │      │  (Python)        │      │ (.pkl file)     │
└─────────────────┘      └──────────────────┘      └─────────────────┘
```

## Pre-Deployment Checklist

### 1. Environment Configuration

Create `.env` file:
```bash
VITE_API_URL=https://your-api-domain.com/api
```

### 2. Backend Setup

**Verify Model Files:**
- [ ] `NN/ridge_model.pkl` exists
- [ ] Model loads without errors
- [ ] All 37 features are properly named

**Test API Locally:**
```bash
cd api
python app.py

# Test endpoints
curl http://localhost:5000/api/health
curl http://localhost:5000/api/model/info
```

### 3. Frontend Build

```bash
npm run build
```

Verify `dist/` folder contains:
- `index.html`
- `assets/` folder with JS/CSS bundles

### 4. Security Hardening

**Backend (Flask):**
- [ ] Set `debug=False` in production
- [ ] Add rate limiting (Flask-Limiter)
- [ ] Enable HTTPS only
- [ ] Add API authentication (if needed)
- [ ] Configure CORS for production domain only

**Frontend:**
- [ ] Remove console.logs
- [ ] Enable CSP headers
- [ ] Minify assets (done by Vite)

## Deployment Options

### Option 1: Separate Hosting (Recommended)

**Frontend: Netlify/Vercel**
```bash
# Build
npm run build

# Deploy dist/ folder
netlify deploy --prod --dir=dist
# or
vercel deploy --prod
```

**Backend: Heroku/Railway/Render**

Create `Procfile`:
```
web: cd api && gunicorn app:app
```

Create `runtime.txt`:
```
python-3.11
```

Update `api/requirements.txt`:
```
gunicorn==21.2.0
Flask==3.0.0
flask-cors==4.0.0
numpy==1.24.3
pandas==2.0.3
scikit-learn==1.3.0
joblib==1.3.2
```

Deploy:
```bash
# Heroku
heroku create footy-liveliness-api
git subtree push --prefix api heroku main

# Railway
railway init
railway up

# Render
# Connect GitHub repo, set build command: pip install -r requirements.txt
# Set start command: gunicorn app:app
```

### Option 2: Docker (Full Stack)

**Create `Dockerfile.frontend`:**
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
FROM nginx:alpine
COPY --from=0 /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Create `Dockerfile.backend`:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY api/ .
COPY NN/ridge_model.pkl ../NN/
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

**Create `docker-compose.yml`:**
```yaml
version: '3.8'
services:
  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    environment:
      - VITE_API_URL=http://backend:5000/api

  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "5000:5000"
    volumes:
      - ./NN:/app/NN:ro
```

Deploy:
```bash
docker-compose up -d
```

### Option 3: AWS (Production-Grade)

**Frontend: S3 + CloudFront**
```bash
# Build
npm run build

# Upload to S3
aws s3 sync dist/ s3://footy-liveliness-frontend

# Create CloudFront distribution
aws cloudfront create-distribution --origin-domain-name footy-liveliness-frontend.s3.amazonaws.com
```

**Backend: AWS Lambda + API Gateway**

Convert Flask to Lambda:
```python
# api/lambda_handler.py
from app import app
import serverless_wsgi

def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)
```

Deploy with Serverless Framework:
```yaml
# serverless.yml
service: footy-liveliness-api
provider:
  name: aws
  runtime: python3.11
functions:
  api:
    handler: lambda_handler.handler
    events:
      - http: ANY /
      - http: ANY /{proxy+}
```

## Performance Optimization

### Frontend
- [x] Code splitting (Vite does this)
- [x] Asset minification
- [ ] Enable gzip compression
- [ ] Add service worker for offline support
- [ ] Implement lazy loading for images

### Backend
- [ ] Add Redis caching for predictions
- [ ] Implement request batching
- [ ] Use CDN for model file
- [ ] Add database for match data (PostgreSQL)

## Monitoring

### Frontend
- Google Analytics
- Sentry for error tracking
- Lighthouse CI for performance

### Backend
- Flask-Monitoring-Dashboard
- Prometheus + Grafana
- CloudWatch (if on AWS)

## Scaling Considerations

**Current Capacity:**
- Frontend: Static files (infinite scale with CDN)
- Backend: ~100 requests/second (single instance)

**To Scale Beyond:**
1. Add load balancer (nginx/AWS ALB)
2. Run multiple backend instances
3. Add Redis for caching
4. Use PostgreSQL for match data
5. Consider serverless (AWS Lambda) for auto-scaling

## Cost Estimates

**Small Scale (< 1000 users/month):**
- Frontend (Netlify): $0 (free tier)
- Backend (Railway): $5/month
- **Total: $5/month**

**Medium Scale (< 10,000 users/month):**
- Frontend (Vercel): $0 (free tier)
- Backend (Render): $7/month
- Database (Supabase): $0 (free tier)
- **Total: $7/month**

**Large Scale (100,000+ users/month):**
- Frontend (CloudFront): ~$10/month
- Backend (AWS Lambda): ~$20/month
- Database (RDS): ~$15/month
- **Total: ~$45/month**

## Rollback Plan

1. Keep previous deployment artifacts
2. Tag releases in git
3. Use blue-green deployment
4. Monitor error rates post-deployment
5. Have rollback script ready:

```bash
# Netlify
netlify rollback

# Heroku
heroku releases:rollback v123
```

## Post-Deployment

- [ ] Test all API endpoints
- [ ] Verify predictions are accurate
- [ ] Check error tracking
- [ ] Monitor performance metrics
- [ ] Set up alerts for downtime
- [ ] Document API for users
