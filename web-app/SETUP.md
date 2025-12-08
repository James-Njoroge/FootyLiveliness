# Setup Instructions

## Prerequisites Not Found

Your system needs Node.js and npm to run the React frontend.

## Quick Setup

### 1. Install Node.js

**Option A: Using Homebrew (Recommended for Mac)**
```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Node.js
brew install node

# Verify installation
node --version
npm --version
```

**Option B: Download from nodejs.org**
1. Visit https://nodejs.org/
2. Download the LTS version (recommended)
3. Run the installer
4. Restart your terminal

### 2. Install Dependencies

Once Node.js is installed:

```bash
# Navigate to web-app directory
cd "/Users/muhammadrakazuhdi/Desktop/Windsurf Projects/506/Footy Liveliness/FootyLiveliness/web-app"

# Install frontend dependencies
npm install

# Install backend dependencies
cd api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..
```

### 3. Run the Application

**Full Stack (Frontend + Backend):**
```bash
npm run dev:full
```

**Or run separately:**

Terminal 1 - Frontend:
```bash
npm run dev
```

Terminal 2 - Backend:
```bash
cd api
source venv/bin/activate
python app.py
```

## Alternative: Backend Only (Python)

If you want to test just the backend API without the frontend:

```bash
cd api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then visit: http://localhost:5000/api/health

## Troubleshooting

**"npm: command not found"**
- Node.js is not installed or not in PATH
- Follow installation steps above

**"python: command not found"**
- Use `python3` instead of `python`

**"Module not found" errors**
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again

**Port already in use**
- Frontend (3000): Change in `vite.config.js`
- Backend (5000): Change in `api/app.py`
