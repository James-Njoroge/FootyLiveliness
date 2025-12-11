# Footy Liveliness - React Frontend

Modern React.js frontend for the Footy Liveliness match prediction system.

## 🚀 Quick Start

### Install Dependencies
```bash
npm install
```

### Start Development Server
```bash
npm start
```

The app will open at http://localhost:3000

### Build for Production
```bash
npm run build
```

## 📁 Project Structure

```
src/
├── components/
│   ├── Header.js           # Header with About button
│   ├── StatsBar.js         # Model statistics bar
│   ├── MatchList.js        # List of matches
│   ├── MatchCard.js        # Individual match card
│   ├── AboutModal.js       # About modal dialog
│   └── Footer.js           # Footer section
├── services/
│   └── api.js              # API service layer
├── utils/
│   └── teamLogos.js        # Team logo mappings
├── App.js                  # Main app component
├── index.js                # Entry point
└── index.css               # Global styles
```

## 🔧 Configuration

### API URL
Set the API URL via environment variable:

```bash
# .env.local
REACT_APP_API_URL=http://localhost:5001
```

Or it defaults to `http://localhost:5001`

## 🎨 Features

- ✅ **Modern React Architecture** - Component-based, hooks, functional components
- ✅ **Responsive Design** - Works on desktop, tablet, and mobile
- ✅ **Real-time Updates** - Auto-refreshes every 5 minutes
- ✅ **Team Logos** - Official Premier League team logos
- ✅ **About Modal** - Comprehensive project information
- ✅ **Loading States** - Smooth loading and error handling
- ✅ **Hover Effects** - Interactive card animations
- ✅ **TailwindCSS** - Utility-first CSS framework

## 📦 Dependencies

- **react** (^18.2.0) - UI library
- **react-dom** (^18.2.0) - React DOM rendering
- **axios** (^1.6.0) - HTTP client
- **react-scripts** (5.0.1) - Create React App scripts

## 🔌 API Integration

The app connects to the Flask backend API:

- `GET /api/upcoming` - Fetch ranked upcoming fixtures
- `POST /api/predict` - Predict single match
- `GET /api/stats` - Get model statistics
- `GET /api/health` - Health check

## 🎯 Components Overview

### Header
- Gradient background
- About button (top-right)
- Project title and tagline

### StatsBar
- 4-column grid showing model metrics
- R² score, Top-10 hit rate, Model type, Season

### MatchList
- Container for all match cards
- Title and description

### MatchCard
- Compact horizontal layout
- Rank badge (🔥, ⭐, ✨ for top 3)
- Team names with logos
- Liveliness score with progress bar
- Date and time

### AboutModal
- Full project information
- Model details and performance
- Team information
- How it works explanation
- Close on ESC key or click outside

### Footer
- Model description
- Key metrics

## 🚀 Deployment

### Development
```bash
npm start
```

### Production Build
```bash
npm run build
```

The build folder will contain optimized production files.

### Serve Production Build
```bash
npm install -g serve
serve -s build -p 3000
```

## 🔄 Migration from Vanilla HTML

The React version maintains all features from the original HTML version:
- ✅ Same visual design
- ✅ Same functionality
- ✅ Better code organization
- ✅ Easier to maintain and extend
- ✅ Component reusability
- ✅ Better state management

## 📝 Notes

- The Flask backend must be running on port 5001
- CORS is enabled on the backend for local development
- Team logos are fetched from FotMob CDN
- Auto-refresh interval is set to 5 minutes

## 🛠️ Development Tips

### Add New Component
```javascript
// src/components/NewComponent.js
import React from 'react';

const NewComponent = ({ prop1, prop2 }) => {
  return (
    <div>
      {/* Component JSX */}
    </div>
  );
};

export default NewComponent;
```

### Add New API Endpoint
```javascript
// src/services/api.js
export const newEndpoint = async (params) => {
  const response = await axios.get(`${API_URL}/api/new-endpoint`, { params });
  return response.data;
};
```

### Styling with TailwindCSS
Use utility classes directly in JSX:
```javascript
<div className="bg-purple-600 text-white p-4 rounded-lg hover:bg-purple-700">
  Content
</div>
```

## 🎓 Learning Resources

- [React Documentation](https://react.dev)
- [TailwindCSS Documentation](https://tailwindcss.com)
- [Axios Documentation](https://axios-http.com)

---

**Built with React 18 + TailwindCSS**
