import React, { useEffect } from 'react';

const GettingStartedModal = ({ onClose }) => {
  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') onClose();
    };
    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [onClose]);

  return (
    <div 
      className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 modal-enter p-4"
      onClick={onClose}
    >
      <div 
        className="bg-white rounded-xl max-w-4xl max-h-[90vh] overflow-y-auto overflow-x-hidden modal-content-enter w-full"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex justify-between items-start sticky top-0 bg-white z-10 px-6 md:px-8 pt-6 md:pt-8 pb-4 border-b mb-6">
          <h2 className="text-2xl md:text-3xl font-bold text-gray-900">🚀 Getting Started</h2>
          <button 
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-full w-8 h-8 flex items-center justify-center transition-all text-2xl font-bold"
            aria-label="Close"
          >
            ×
          </button>
        </div>
        
        <div className="space-y-8 text-gray-700 px-6 md:px-8">
          {/* Quick Start */}
          <div>
            <h3 className="text-xl font-bold text-orange-600 mb-4">⚡ Quick Start (First Time Setup)</h3>
            <div className="bg-gradient-to-r from-yellow-50 to-blue-50 p-6 rounded-lg">
              <p className="mb-4 font-semibold">🎯 First time running? Just 2 simple steps:</p>
              <div className="space-y-4">
                <div className="bg-white p-4 rounded-lg shadow-sm border-2 border-lime-300">
                  <div className="flex items-center gap-3 mb-2">
                    <div className="bg-orange-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold">1</div>
                    <h4 className="font-semibold text-lg">Open Terminal in Final_Submission Folder</h4>
                  </div>
                  <div className="ml-11">
                    <p className="text-sm text-gray-600 mb-2">Navigate to the Final_Submission directory</p>
                    <div className="bg-gray-900 text-green-400 p-3 rounded font-mono text-sm overflow-x-auto">
                      <div>cd /path/to/Final_Submission</div>
                    </div>
                    <p className="text-xs text-gray-500 mt-2">💡 Tip: You can drag the folder into Terminal to get the path</p>
                  </div>
                </div>

                <div className="bg-white p-4 rounded-lg shadow-sm border-2 border-green-300">
                  <div className="flex items-center gap-3 mb-2">
                    <div className="bg-green-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold">2</div>
                    <h4 className="font-semibold text-lg">Run Setup Command</h4>
                  </div>
                  <div className="ml-11">
                    <p className="text-sm text-gray-600 mb-2">This installs all dependencies and starts the app</p>
                    <div className="bg-gray-900 text-green-400 p-3 rounded font-mono text-sm overflow-x-auto">
                      <div>make install && make start</div>
                    </div>
                    <p className="text-sm text-gray-600 mt-2">⏱️ Takes ~30 seconds</p>
                  </div>
                </div>
              </div>
              <div className="mt-4 bg-green-50 border-l-4 border-green-500 p-4 rounded">
                <p className="text-sm text-green-800">
                  <strong>✨ Done!</strong> The app will automatically open at http://localhost:3000
                </p>
              </div>
              <div className="mt-4 bg-yellow-50 border-l-4 border-yellow-500 p-4 rounded">
                <p className="text-sm text-yellow-800 mb-2">
                  <strong>⚠️ First time running?</strong> The app uses pre-loaded sample data to get you started immediately.
                </p>
                <p className="text-xs text-yellow-700 mt-1">
                  To fetch live data with 380 real matches, run <code className="bg-white px-1 rounded">make demo</code> instead (~5 min)
                </p>
              </div>
            </div>
          </div>

          {/* Prerequisites */}
          <div>
            <h3 className="text-xl font-bold text-orange-600 mb-4">📋 Prerequisites</h3>
            <div className="grid md:grid-cols-2 gap-4">
              <div className="bg-blue-50 p-4 rounded-lg">
                <h4 className="font-semibold text-blue-800 mb-3">Required Software</h4>
                <ul className="space-y-2 text-sm">
                  <li className="flex items-start gap-2">
                    <span className="text-blue-600">✓</span>
                    <div>
                      <strong>Node.js 14+</strong>
                      <div className="text-gray-600">Check: <code className="bg-white px-1 rounded">node --version</code></div>
                    </div>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-blue-600">✓</span>
                    <div>
                      <strong>Python 3.9+</strong>
                      <div className="text-gray-600">Check: <code className="bg-white px-1 rounded">python3 --version</code></div>
                    </div>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-blue-600">✓</span>
                    <div>
                      <strong>npm or yarn</strong>
                      <div className="text-gray-600">Check: <code className="bg-white px-1 rounded">npm --version</code></div>
                    </div>
                  </li>
                </ul>
              </div>
              <div className="bg-yellow-50 p-4 rounded-lg">
                <h4 className="font-semibold text-orange-800 mb-3">Python Packages</h4>
                <div className="text-sm space-y-2">
                  <p>Install required packages:</p>
                  <div className="bg-gray-900 text-green-400 p-2 rounded font-mono text-xs">
                    pip3 install flask flask-cors pandas numpy scikit-learn
                  </div>
                  <p className="text-gray-600 mt-2">Or use requirements.txt:</p>
                  <div className="bg-gray-900 text-green-400 p-2 rounded font-mono text-xs">
                    pip3 install -r requirements.txt
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Detailed Setup */}
          <div>
            <h3 className="text-xl font-bold text-orange-600 mb-4">🔧 Detailed Setup Guide (Manual Method)</h3>
            <p className="text-sm text-gray-600 mb-4">
              If you prefer to run commands manually instead of using the Makefile:
            </p>
            
            {/* Step 1: Navigate */}
            <div className="mb-6">
              <div className="bg-gradient-to-r from-gray-500 to-gray-600 text-white px-4 py-2 rounded-t-lg font-semibold">
                Step 1: Navigate to Web App Directory
              </div>
              <div className="bg-gray-50 p-4 rounded-b-lg border border-t-0">
                <div className="bg-gray-900 text-green-400 p-3 rounded font-mono text-sm mb-3">
                  <div># Navigate to web app directory</div>
                  <div>cd Final_Submission/4_Web_Application/footy-liveliness-web</div>
                </div>
                <p className="text-sm text-gray-600">Make sure you're in the <code className="bg-white px-1 rounded">footy-liveliness-web</code> directory.</p>
              </div>
            </div>

            {/* Step 2: Install Python */}
            <div className="mb-6">
              <div className="bg-gradient-to-r from-blue-500 to-blue-600 text-white px-4 py-2 rounded-t-lg font-semibold">
                Step 2: Install Python Dependencies
              </div>
              <div className="bg-gray-50 p-4 rounded-b-lg border border-t-0">
                <div className="bg-gray-900 text-green-400 p-3 rounded font-mono text-sm mb-3">
                  <div>pip3 install flask flask-cors pandas numpy scikit-learn requests</div>
                </div>
                <p className="text-sm text-gray-600">This installs all required Python packages for the Flask API.</p>
              </div>
            </div>

            {/* Step 3: Install Node Dependencies */}
            <div className="mb-6">
              <div className="bg-gradient-to-r from-green-500 to-green-600 text-white px-4 py-2 rounded-t-lg font-semibold">
                Step 3: Install Node.js Dependencies
              </div>
              <div className="bg-gray-50 p-4 rounded-b-lg border border-t-0">
                <div className="bg-gray-900 text-green-400 p-3 rounded font-mono text-sm mb-3">
                  <div>npm install</div>
                  <div className="text-gray-500"># or</div>
                  <div>yarn install</div>
                </div>
                <div className="space-y-2 text-sm">
                  <p className="text-gray-600">This installs:</p>
                  <ul className="list-disc list-inside text-gray-600 ml-4">
                    <li>React 18</li>
                    <li>Chart.js & react-chartjs-2</li>
                    <li>Axios (HTTP client)</li>
                    <li>TailwindCSS (via CDN)</li>
                  </ul>
                  <div className="bg-yellow-50 border-l-4 border-yellow-500 p-3 rounded mt-3">
                    <p className="text-sm text-yellow-800">
                      <strong>⚠️ Note:</strong> You might see some deprecation warnings - these are safe to ignore.
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Step 4: Start Backend */}
            <div className="mb-6">
              <div className="bg-gradient-to-r from-yellow-500 to-orange-600 text-white px-4 py-2 rounded-t-lg font-semibold">
                Step 4: Start Flask Backend (Terminal 1)
              </div>
              <div className="bg-gray-50 p-4 rounded-b-lg border border-t-0">
                <div className="bg-gray-900 text-green-400 p-3 rounded font-mono text-sm mb-3">
                  <div>python3 app.py</div>
                </div>
                <div className="space-y-2 text-sm">
                  <p className="text-gray-600">You should see:</p>
                  <div className="bg-white p-3 rounded border text-xs font-mono">
                    <div className="text-green-600">Loading model artifacts...</div>
                    <div className="text-green-600">✓ Model loaded (27 features)</div>
                    <div className="text-blue-600">FOOTY LIVELINESS API</div>
                    <div className="text-gray-600">Starting server on http://localhost:5001</div>
                    <div className="text-gray-600">* Running on http://127.0.0.1:5001</div>
                  </div>
                  <div className="bg-blue-50 border-l-4 border-blue-500 p-3 rounded mt-3">
                    <p className="text-sm text-blue-800">
                      <strong>✅ Success!</strong> Keep this terminal running. The API is now serving predictions.
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Step 5: Start Frontend */}
            <div className="mb-6">
              <div className="bg-gradient-to-r from-pink-500 to-pink-600 text-white px-4 py-2 rounded-t-lg font-semibold">
                Step 5: Start React Frontend (Terminal 2)
              </div>
              <div className="bg-gray-50 p-4 rounded-b-lg border border-t-0">
                <div className="bg-gray-900 text-green-400 p-3 rounded font-mono text-sm mb-3">
                  <div>npm start</div>
                </div>
                <div className="space-y-2 text-sm">
                  <p className="text-gray-600">You should see:</p>
                  <div className="bg-white p-3 rounded border text-xs font-mono">
                    <div className="text-green-600">Compiled successfully!</div>
                    <div className="text-blue-600">Local: http://localhost:3000</div>
                    <div className="text-gray-600">webpack compiled successfully</div>
                  </div>
                  <div className="bg-green-50 border-l-4 border-green-500 p-3 rounded mt-3">
                    <p className="text-sm text-green-800">
                      <strong>🎉 Done!</strong> The app will automatically open in your browser at http://localhost:3000
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Troubleshooting */}
          <div>
            <h3 className="text-xl font-bold text-orange-600 mb-4">🔍 Troubleshooting</h3>
            <div className="space-y-4">
              <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded">
                <h4 className="font-semibold text-red-800 mb-2">❌ Port 5001 already in use</h4>
                <p className="text-sm text-red-700 mb-2">Another process is using port 5001.</p>
                <div className="bg-gray-900 text-green-400 p-2 rounded font-mono text-xs">
                  <div># Find and kill the process</div>
                  <div>lsof -ti:5001 | xargs kill -9</div>
                </div>
              </div>

              <div className="bg-orange-50 border-l-4 border-orange-500 p-4 rounded">
                <h4 className="font-semibold text-orange-800 mb-2">⚠️ Module not found errors</h4>
                <p className="text-sm text-orange-700 mb-2">Missing Python or Node packages.</p>
                <div className="bg-gray-900 text-green-400 p-2 rounded font-mono text-xs space-y-1">
                  <div># For Python:</div>
                  <div>pip3 install -r requirements.txt</div>
                  <div className="mt-2"># For Node:</div>
                  <div>rm -rf node_modules package-lock.json</div>
                  <div>npm install</div>
                </div>
              </div>

              <div className="bg-yellow-50 border-l-4 border-yellow-500 p-4 rounded">
                <h4 className="font-semibold text-yellow-800 mb-2">⚠️ API connection failed</h4>
                <p className="text-sm text-yellow-700 mb-2">Frontend can't reach backend.</p>
                <ul className="text-sm text-yellow-700 space-y-1 ml-4 list-disc">
                  <li>Make sure Flask is running on port 5001</li>
                  <li>Check that both terminals are in the same directory</li>
                  <li>Verify CORS is enabled in app.py</li>
                </ul>
              </div>

              <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
                <h4 className="font-semibold text-blue-800 mb-2">💡 Browser doesn't auto-open</h4>
                <p className="text-sm text-blue-700 mb-2">Manually navigate to:</p>
                <div className="bg-white p-2 rounded font-mono text-sm text-blue-600">
                  http://localhost:3000
                </div>
              </div>
            </div>
          </div>

          {/* Project Structure */}
          <div>
            <h3 className="text-xl font-bold text-orange-600 mb-4">📁 Project Structure</h3>
            <div className="bg-gray-900 text-gray-300 p-4 rounded font-mono text-xs overflow-x-auto">
              <pre>{`footy-liveliness-web/
├── public/
│   └── index.html              # HTML template
├── src/
│   ├── components/             # React components
│   │   ├── Header.js
│   │   ├── MatchCard.js
│   │   ├── AboutModal.js
│   │   ├── ProjectDetailsModal.js
│   │   └── ArchitectureDiagram.js
│   ├── services/
│   │   └── api.js              # API calls
│   ├── utils/
│   │   └── teamLogos.js        # Team logo mappings
│   ├── App.js                  # Main app
│   └── index.js                # Entry point
├── app.py                      # Flask API ⚡
├── model.pkl                   # Trained model
├── scaler.pkl                  # Feature scaler
├── team_stats.pkl              # Team statistics
├── package.json                # Node dependencies
└── requirements.txt            # Python dependencies`}</pre>
            </div>
          </div>

          {/* Useful Commands */}
          <div>
            <h3 className="text-xl font-bold text-orange-600 mb-4">⌨️ Makefile Commands</h3>
            <div className="grid md:grid-cols-2 gap-4">
              <div className="bg-gray-50 p-4 rounded-lg border">
                <h4 className="font-semibold mb-3 text-orange-600">🚀 Main Commands</h4>
                <div className="space-y-2 text-sm">
                  <div>
                    <code className="bg-gray-900 text-green-400 px-2 py-1 rounded text-xs">make install</code>
                    <p className="text-gray-600 mt-1">Install all dependencies</p>
                  </div>
                  <div>
                    <code className="bg-gray-900 text-green-400 px-2 py-1 rounded text-xs">make start</code>
                    <p className="text-gray-600 mt-1">Start Flask API + React</p>
                  </div>
                  <div>
                    <code className="bg-gray-900 text-green-400 px-2 py-1 rounded text-xs">make stop</code>
                    <p className="text-gray-600 mt-1">Stop all processes</p>
                  </div>
                  <div>
                    <code className="bg-gray-900 text-green-400 px-2 py-1 rounded text-xs">make status</code>
                    <p className="text-gray-600 mt-1">Check if running</p>
                  </div>
                </div>
              </div>
              <div className="bg-gray-50 p-4 rounded-lg border">
                <h4 className="font-semibold mb-3 text-blue-600">🔄 Data Commands</h4>
                <div className="space-y-2 text-sm">
                  <div>
                    <code className="bg-gray-900 text-green-400 px-2 py-1 rounded text-xs">make scrape</code>
                    <p className="text-gray-600 mt-1">Scrape 380 matches (~5 min)</p>
                  </div>
                  <div>
                    <code className="bg-gray-900 text-green-400 px-2 py-1 rounded text-xs">make update</code>
                    <p className="text-gray-600 mt-1">Re-scrape & restart</p>
                  </div>
                  <div>
                    <code className="bg-gray-900 text-green-400 px-2 py-1 rounded text-xs">make test</code>
                    <p className="text-gray-600 mt-1">Test API endpoints</p>
                  </div>
                  <div>
                    <code className="bg-gray-900 text-green-400 px-2 py-1 rounded text-xs">make clean</code>
                    <p className="text-gray-600 mt-1">Remove temp files</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Live Data Scraping */}
          <div>
            <h3 className="text-xl font-bold text-orange-600 mb-4">🌐 Live Data & Predictions</h3>
            <div className="bg-gradient-to-r from-green-50 to-blue-50 p-6 rounded-lg">
              <p className="mb-4 font-semibold">Get real match data with actual xG for finished matches:</p>
              <div className="bg-white p-4 rounded-lg shadow-sm mb-4">
                <div className="bg-gray-900 text-green-400 p-3 rounded font-mono text-sm">
                  <div>make scrape</div>
                </div>
                <p className="text-sm text-gray-600 mt-2">⏱️ Takes ~5 minutes | Fetches all 380 season matches</p>
              </div>
              <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded mb-4">
                <p className="text-sm text-blue-800">
                  <strong>📊 What you get:</strong>
                </p>
                <ul className="list-disc list-inside text-blue-700 ml-4 space-y-1 mt-2 text-sm">
                  <li>150 finished matches with actual xG data</li>
                  <li>230 upcoming matches with predictions</li>
                  <li>Predicted vs Actual comparison view</li>
                  <li>Navigate through past weeks to see accuracy</li>
                </ul>
              </div>
              <div className="bg-green-50 border-l-4 border-green-500 p-4 rounded">
                <p className="text-sm text-green-800 mb-2">
                  <strong>🔄 Update Data:</strong> Run after matches are played
                </p>
                <div className="bg-gray-900 text-green-400 p-2 rounded font-mono text-xs">
                  make update
                </div>
                <p className="text-xs text-green-600 mt-2">Stops app → Re-scrapes → Restarts with new data</p>
              </div>
            </div>
          </div>

          {/* Next Steps */}
          <div className="bg-gradient-to-r from-yellow-100 to-pink-100 p-6 rounded-lg">
            <h3 className="text-xl font-bold text-orange-800 mb-4">🎯 Next Steps</h3>
            <div className="space-y-3 text-sm">
              <div className="flex items-start gap-3">
                <span className="text-2xl">1️⃣</span>
                <div>
                  <strong>Explore Predictions:</strong> See ranked match predictions with liveliness scores and team logos
                </div>
              </div>
              <div className="flex items-start gap-3">
                <span className="text-2xl">2️⃣</span>
                <div>
                  <strong>Navigate Weeks:</strong> Use ← Previous / Next → buttons to explore past and future weeks
                </div>
              </div>
              <div className="flex items-start gap-3">
                <span className="text-2xl">3️⃣</span>
                <div>
                  <strong>Comparison View:</strong> For past weeks, toggle to ⚖️ Comparison View to see predicted vs actual rankings
                </div>
              </div>
              <div className="flex items-start gap-3">
                <span className="text-2xl">4️⃣</span>
                <div>
                  <strong>Update Data:</strong> Run <code className="bg-white px-1 rounded">make update</code> after matches to get latest results
                </div>
              </div>
              <div className="flex items-start gap-3">
                <span className="text-2xl">5️⃣</span>
                <div>
                  <strong>View Details:</strong> Click "Project Details" for comprehensive analysis with charts and metrics
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-8 text-center sticky bottom-0 bg-white pt-4 border-t px-6 md:px-8 pb-6 md:pb-8">
          <button 
            onClick={onClose}
            className="bg-orange-600 hover:bg-orange-700 text-white px-8 py-3 rounded-lg font-medium transition-colors shadow-lg"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default GettingStartedModal;
