import React, { useEffect } from 'react';

const ArchitectureDiagram = ({ onClose }) => {
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
        className="bg-white rounded-xl max-w-7xl max-h-[95vh] overflow-y-auto p-6 md:p-8 modal-content-enter w-full"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex justify-between items-start mb-6 sticky top-0 bg-white z-10 pb-4 border-b">
          <h2 className="text-2xl md:text-3xl font-bold text-gray-900">🏗️ System Architecture</h2>
          <button 
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-full w-8 h-8 flex items-center justify-center transition-all text-2xl font-bold"
            aria-label="Close"
          >
            ×
          </button>
        </div>

        <div className="space-y-8">
          {/* Architecture Diagram */}
          <div className="bg-gradient-to-br from-purple-50 to-blue-50 p-8 rounded-xl">
            <h3 className="text-xl font-bold text-purple-800 mb-6 text-center">End-to-End ML Pipeline</h3>
            
            {/* Data Collection Layer */}
            <div className="mb-8">
              <div className="bg-blue-600 text-white px-4 py-2 rounded-lg font-semibold text-center mb-4">
                1️⃣ DATA COLLECTION
              </div>
              <div className="grid md:grid-cols-3 gap-4">
                <div className="bg-white p-4 rounded-lg shadow-md border-2 border-blue-200">
                  <div className="font-semibold text-blue-800 mb-2">📡 Web Scraping</div>
                  <div className="text-sm text-gray-700">
                    <div className="font-mono text-xs bg-gray-100 p-2 rounded mb-2">Selenium + BeautifulSoup</div>
                    <ul className="text-xs space-y-1">
                      <li>• FotMob public endpoints</li>
                      <li>• 380 JSON files (38 rounds)</li>
                      <li>• xG events, stats, lineups</li>
                    </ul>
                  </div>
                </div>
                <div className="bg-white p-4 rounded-lg shadow-md border-2 border-blue-200">
                  <div className="font-semibold text-blue-800 mb-2">💾 Raw Data</div>
                  <div className="text-sm text-gray-700">
                    <div className="font-mono text-xs bg-gray-100 p-2 rounded mb-2">data/24-25_PL_Data_raw/</div>
                    <ul className="text-xs space-y-1">
                      <li>• Match metadata</li>
                      <li>• Team statistics</li>
                      <li>• Event data (shots, cards)</li>
                    </ul>
                  </div>
                </div>
                <div className="bg-white p-4 rounded-lg shadow-md border-2 border-blue-200">
                  <div className="font-semibold text-blue-800 mb-2">📊 Schema</div>
                  <div className="text-sm text-gray-700">
                    <div className="font-mono text-xs bg-gray-100 p-2 rounded mb-2">JSON Format</div>
                    <ul className="text-xs space-y-1">
                      <li>• general: teams, scores</li>
                      <li>• shotmap: xG events</li>
                      <li>• stats: team metrics</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>

            {/* Arrow Down */}
            <div className="flex justify-center mb-8">
              <svg className="w-8 h-8 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 3a1 1 0 011 1v10.586l3.293-3.293a1 1 0 111.414 1.414l-5 5a1 1 0 01-1.414 0l-5-5a1 1 0 111.414-1.414L9 14.586V4a1 1 0 011-1z" clipRule="evenodd" />
              </svg>
            </div>

            {/* Label Generation Layer */}
            <div className="mb-8">
              <div className="bg-green-600 text-white px-4 py-2 rounded-lg font-semibold text-center mb-4">
                2️⃣ LABEL GENERATION
              </div>
              <div className="grid md:grid-cols-2 gap-4">
                <div className="bg-white p-4 rounded-lg shadow-md border-2 border-green-200">
                  <div className="font-semibold text-green-800 mb-2">🎯 create_labels.py</div>
                  <div className="text-sm text-gray-700">
                    <div className="font-mono text-xs bg-gray-100 p-2 rounded mb-2">
                      Simple xG = xG_total + min(xG_home, xG_away)
                    </div>
                    <ul className="text-xs space-y-1">
                      <li>• Extract xG from shot events</li>
                      <li>• Calculate 3 liveliness metrics</li>
                      <li>• Extract cards from JSON</li>
                      <li>• Output: tables/all_rounds.csv</li>
                    </ul>
                  </div>
                </div>
                <div className="bg-white p-4 rounded-lg shadow-md border-2 border-green-200">
                  <div className="font-semibold text-green-800 mb-2">📈 Target Metrics Tested</div>
                  <div className="text-sm text-gray-700">
                    <ul className="text-xs space-y-1">
                      <li>✅ <strong>Simple xG</strong> (R²=0.81)</li>
                      <li>• SLS-F+ Rolling (R²=-0.15)</li>
                      <li>• SLS-F+ Fixed (data leakage)</li>
                      <li>• 6 other alternatives tested</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>

            {/* Arrow Down */}
            <div className="flex justify-center mb-8">
              <svg className="w-8 h-8 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 3a1 1 0 011 1v10.586l3.293-3.293a1 1 0 111.414 1.414l-5 5a1 1 0 01-1.414 0l-5-5a1 1 0 111.414-1.414L9 14.586V4a1 1 0 011-1z" clipRule="evenodd" />
              </svg>
            </div>

            {/* Feature Engineering Layer */}
            <div className="mb-8">
              <div className="bg-yellow-600 text-white px-4 py-2 rounded-lg font-semibold text-center mb-4">
                3️⃣ FEATURE ENGINEERING
              </div>
              <div className="grid md:grid-cols-3 gap-4">
                <div className="bg-white p-4 rounded-lg shadow-md border-2 border-yellow-200">
                  <div className="font-semibold text-yellow-800 mb-2">🔄 create_features.py</div>
                  <div className="text-sm text-gray-700">
                    <div className="font-mono text-xs bg-gray-100 p-2 rounded mb-2">22 Rolling Features</div>
                    <ul className="text-xs space-y-1">
                      <li>• 5-match rolling averages</li>
                      <li>• Offensive: xG, SoT, BigCh</li>
                      <li>• Defensive: xGA, SoT_agst</li>
                      <li>• Composite: TempoSum, etc.</li>
                    </ul>
                  </div>
                </div>
                <div className="bg-white p-4 rounded-lg shadow-md border-2 border-yellow-200">
                  <div className="font-semibold text-yellow-800 mb-2">⭐ extra_features.py</div>
                  <div className="text-sm text-gray-700">
                    <div className="font-mono text-xs bg-gray-100 p-2 rounded mb-2">+15 Contextual Features</div>
                    <ul className="text-xs space-y-1">
                      <li>• League position (1-20)</li>
                      <li>• Form trajectory (last 3)</li>
                      <li>• Stakes indicators</li>
                      <li>• <strong>R² boost: +73%</strong></li>
                    </ul>
                  </div>
                </div>
                <div className="bg-white p-4 rounded-lg shadow-md border-2 border-yellow-200">
                  <div className="font-semibold text-yellow-800 mb-2">📁 Output</div>
                  <div className="text-sm text-gray-700">
                    <div className="font-mono text-xs bg-gray-100 p-2 rounded mb-2">feature_tables/</div>
                    <ul className="text-xs space-y-1">
                      <li>• match_features_wide.csv</li>
                      <li>• match_features_enhanced.csv</li>
                      <li>• <strong>37 total features</strong></li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>

            {/* Arrow Down */}
            <div className="flex justify-center mb-8">
              <svg className="w-8 h-8 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 3a1 1 0 011 1v10.586l3.293-3.293a1 1 0 111.414 1.414l-5 5a1 1 0 01-1.414 0l-5-5a1 1 0 111.414-1.414L9 14.586V4a1 1 0 011-1z" clipRule="evenodd" />
              </svg>
            </div>

            {/* Model Training Layer */}
            <div className="mb-8">
              <div className="bg-purple-600 text-white px-4 py-2 rounded-lg font-semibold text-center mb-4">
                4️⃣ MODEL TRAINING & EVALUATION
              </div>
              <div className="grid md:grid-cols-4 gap-4">
                <div className="bg-white p-4 rounded-lg shadow-md border-2 border-purple-200">
                  <div className="font-semibold text-purple-800 mb-2">📊 Data Split</div>
                  <div className="text-sm text-gray-700">
                    <ul className="text-xs space-y-1">
                      <li>• Train: 280 (rounds 0-27)</li>
                      <li>• Val: 50 (rounds 28-32)</li>
                      <li>• Test: 50 (rounds 33-37)</li>
                      <li>• Chronological (no leakage)</li>
                    </ul>
                  </div>
                </div>
                <div className="bg-white p-4 rounded-lg shadow-md border-2 border-purple-200">
                  <div className="font-semibold text-purple-800 mb-2">🤖 Models Tested</div>
                  <div className="text-sm text-gray-700">
                    <ul className="text-xs space-y-1">
                      <li>✅ <strong>Elastic Net</strong> (0.82)</li>
                      <li>• Ridge (0.81)</li>
                      <li>• Gradient Boosting (0.75)</li>
                      <li>• XGBoost (0.04)</li>
                      <li>• Neural Network (failed)</li>
                    </ul>
                  </div>
                </div>
                <div className="bg-white p-4 rounded-lg shadow-md border-2 border-purple-200">
                  <div className="font-semibold text-purple-800 mb-2">🎯 Hyperparameters</div>
                  <div className="text-sm text-gray-700">
                    <div className="font-mono text-xs bg-gray-100 p-2 rounded mb-2">
                      ElasticNetCV
                    </div>
                    <ul className="text-xs space-y-1">
                      <li>• alpha: 21.54</li>
                      <li>• l1_ratio: 0.5</li>
                      <li>• cv: 5-fold</li>
                      <li>• max_iter: 10000</li>
                    </ul>
                  </div>
                </div>
                <div className="bg-white p-4 rounded-lg shadow-md border-2 border-purple-200">
                  <div className="font-semibold text-purple-800 mb-2">📈 Metrics</div>
                  <div className="text-sm text-gray-700">
                    <ul className="text-xs space-y-1">
                      <li>• R²: 0.821</li>
                      <li>• MAE: 0.452</li>
                      <li>• Spearman ρ: 0.896</li>
                      <li>• Top-10 Hit: 90%</li>
                      <li>• Overfitting: -0.014</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>

            {/* Arrow Down */}
            <div className="flex justify-center mb-8">
              <svg className="w-8 h-8 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 3a1 1 0 011 1v10.586l3.293-3.293a1 1 0 111.414 1.414l-5 5a1 1 0 01-1.414 0l-5-5a1 1 0 111.414-1.414L9 14.586V4a1 1 0 011-1z" clipRule="evenodd" />
              </svg>
            </div>

            {/* Deployment Layer */}
            <div>
              <div className="bg-red-600 text-white px-4 py-2 rounded-lg font-semibold text-center mb-4">
                5️⃣ PRODUCTION DEPLOYMENT
              </div>
              <div className="grid md:grid-cols-2 gap-4">
                <div className="bg-white p-4 rounded-lg shadow-md border-2 border-red-200">
                  <div className="font-semibold text-red-800 mb-2">🔧 Backend (Flask API)</div>
                  <div className="text-sm text-gray-700">
                    <div className="font-mono text-xs bg-gray-100 p-2 rounded mb-2">app.py - Port 5001</div>
                    <ul className="text-xs space-y-1">
                      <li>• Load model.pkl, scaler.pkl</li>
                      <li>• GET /api/upcoming (ranked fixtures)</li>
                      <li>• POST /api/predict (single match)</li>
                      <li>• GET /api/stats (model info)</li>
                      <li>• CORS enabled for local dev</li>
                    </ul>
                  </div>
                </div>
                <div className="bg-white p-4 rounded-lg shadow-md border-2 border-red-200">
                  <div className="font-semibold text-red-800 mb-2">💻 Frontend (React)</div>
                  <div className="text-sm text-gray-700">
                    <div className="font-mono text-xs bg-gray-100 p-2 rounded mb-2">React 18 + TailwindCSS</div>
                    <ul className="text-xs space-y-1">
                      <li>• Component-based architecture</li>
                      <li>• Axios for API calls</li>
                      <li>• Chart.js for visualizations</li>
                      <li>• Auto-refresh every 5 min</li>
                      <li>• Responsive design</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Tech Stack */}
          <div>
            <h3 className="text-xl font-bold text-purple-800 mb-4">🛠️ Technology Stack</h3>
            <div className="grid md:grid-cols-3 gap-4">
              <div className="bg-blue-50 p-4 rounded-lg">
                <h4 className="font-semibold text-blue-800 mb-2">Data & ML</h4>
                <ul className="text-sm space-y-1">
                  <li>• Python 3.9+</li>
                  <li>• pandas, numpy</li>
                  <li>• scikit-learn</li>
                  <li>• Selenium, BeautifulSoup</li>
                  <li>• pickle (model serialization)</li>
                </ul>
              </div>
              <div className="bg-purple-50 p-4 rounded-lg">
                <h4 className="font-semibold text-purple-800 mb-2">Backend</h4>
                <ul className="text-sm space-y-1">
                  <li>• Flask (API server)</li>
                  <li>• Flask-CORS</li>
                  <li>• Axios (HTTP client)</li>
                  <li>• JSON data format</li>
                </ul>
              </div>
              <div className="bg-pink-50 p-4 rounded-lg">
                <h4 className="font-semibold text-pink-800 mb-2">Frontend</h4>
                <ul className="text-sm space-y-1">
                  <li>• React 18</li>
                  <li>• TailwindCSS</li>
                  <li>• Chart.js + react-chartjs-2</li>
                  <li>• React Hooks (useState, useEffect)</li>
                </ul>
              </div>
            </div>
          </div>

          {/* File Structure */}
          <div>
            <h3 className="text-xl font-bold text-purple-800 mb-4">📁 Project Structure</h3>
            <div className="bg-gray-50 p-6 rounded-lg font-mono text-xs overflow-x-auto">
              <pre className="text-gray-800">
{`FootyLiveliness/
├── data/
│   └── 24-25_PL_Data_raw/          # 380 JSON files
├── tables/
│   └── all_rounds.csv              # Labels (3 metrics)
├── feature_tables/
│   ├── match_features_wide.csv     # 22 features
│   └── match_features_enhanced.csv # 37 features ✅
├── Scripts:
│   ├── create_labels.py            # Generate targets
│   ├── create_features.py          # Rolling features
│   └── extra_features.py           # Contextual features
├── target_metric_experiments/
│   ├── 01_create_alternative_targets.py
│   ├── 02_compare_target_metrics.py
│   └── 03_train_best_target.py     # Final model
└── footy-liveliness-web/
    ├── app.py                      # Flask API
    ├── model.pkl                   # Trained Elastic Net
    ├── scaler.pkl                  # StandardScaler
    ├── src/
    │   ├── App.js                  # Main React app
    │   ├── components/             # React components
    │   └── services/api.js         # API calls
    └── public/index.html           # HTML template`}
              </pre>
            </div>
          </div>

          {/* Data Flow */}
          <div>
            <h3 className="text-xl font-bold text-purple-800 mb-4">🔄 Data Flow</h3>
            <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-6 rounded-lg">
              <div className="space-y-3 text-sm">
                <div className="flex items-center gap-3">
                  <div className="bg-blue-600 text-white px-3 py-1 rounded font-semibold min-w-[100px] text-center">Input</div>
                  <div className="flex-1">User opens web app → React fetches from Flask API</div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="bg-green-600 text-white px-3 py-1 rounded font-semibold min-w-[100px] text-center">API Call</div>
                  <div className="flex-1">GET /api/upcoming → Flask loads model.pkl & team_stats.pkl</div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="bg-yellow-600 text-white px-3 py-1 rounded font-semibold min-w-[100px] text-center">Features</div>
                  <div className="flex-1">Create 37-feature vector for each match from team stats</div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="bg-purple-600 text-white px-3 py-1 rounded font-semibold min-w-[100px] text-center">Prediction</div>
                  <div className="flex-1">Elastic Net predicts liveliness score (1-9 scale)</div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="bg-pink-600 text-white px-3 py-1 rounded font-semibold min-w-[100px] text-center">Ranking</div>
                  <div className="flex-1">Sort matches by predicted liveliness (descending)</div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="bg-red-600 text-white px-3 py-1 rounded font-semibold min-w-[100px] text-center">Output</div>
                  <div className="flex-1">React displays ranked list with team logos, scores, badges</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-8 text-center sticky bottom-0 bg-white pt-4 border-t">
          <button 
            onClick={onClose}
            className="bg-purple-600 hover:bg-purple-700 text-white px-8 py-3 rounded-lg font-medium transition-colors shadow-lg"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default ArchitectureDiagram;
