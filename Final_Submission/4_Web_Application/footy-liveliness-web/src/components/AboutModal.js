import React, { useEffect } from 'react';

const AboutModal = ({ onClose }) => {
  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') onClose();
    };
    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [onClose]);

  return (
    <div 
      className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 modal-enter"
      onClick={onClose}
    >
      <div 
        className="bg-white rounded-xl max-w-4xl max-h-[90vh] overflow-y-auto p-8 m-4 modal-content-enter"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex justify-between items-start mb-6">
          <h2 className="text-3xl font-bold text-gray-900">About Footy Liveliness</h2>
          <button 
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 text-2xl leading-none"
          >
            &times;
          </button>
        </div>
        
        <div className="space-y-6 text-gray-700">
          <div>
            <h3 className="text-xl font-semibold text-gray-900 mb-3">🎯 What is Footy Liveliness?</h3>
            <p className="mb-3">An AI-powered Premier League match excitement predictor that helps football fans make informed decisions about which matches to watch when multiple games are happening simultaneously.</p>
            <div className="bg-gradient-to-r from-yellow-50 to-blue-50 p-4 rounded-lg">
              <p className="text-sm"><strong>The Problem:</strong> With 10 Premier League matches every weekend, fans face a dilemma - which game should they watch? Traditional factors like team popularity or league position don't always predict the most exciting matches.</p>
              <p className="text-sm mt-2"><strong>Our Solution:</strong> We use machine learning to predict match "liveliness" (excitement level) based on pre-match statistics, helping fans choose the most entertaining games.</p>
            </div>
          </div>

          <div>
            <h3 className="text-xl font-semibold text-gray-900 mb-3">🎬 What This Website Does</h3>
            <div className="space-y-3">
              <div className="flex items-start gap-3">
                <div className="bg-orange-600 text-white rounded-full w-8 h-8 flex items-center justify-center flex-shrink-0 font-bold">1</div>
                <div>
                  <h4 className="font-semibold text-gray-900">Predicts Match Excitement</h4>
                  <p className="text-sm">Uses an Elastic Net regression model to predict the "liveliness" score (0-8 scale) for every Premier League match based on 27 pre-match features.</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="bg-orange-600 text-white rounded-full w-8 h-8 flex items-center justify-center flex-shrink-0 font-bold">2</div>
                <div>
                  <h4 className="font-semibold text-gray-900">Ranks All Matches</h4>
                  <p className="text-sm">Sorts all 380 season matches by predicted excitement level, showing you the most entertaining fixtures first. Navigate by week to see rankings for specific gameweeks.</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="bg-orange-600 text-white rounded-full w-8 h-8 flex items-center justify-center flex-shrink-0 font-bold">3</div>
                <div>
                  <h4 className="font-semibold text-gray-900">Shows Predicted vs Actual</h4>
                  <p className="text-sm">For finished matches, displays actual liveliness scores alongside predictions, with accuracy percentages. Toggle to Comparison View to see side-by-side rankings.</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="bg-orange-600 text-white rounded-full w-8 h-8 flex items-center justify-center flex-shrink-0 font-bold">4</div>
                <div>
                  <h4 className="font-semibold text-gray-900">Validates Model Performance</h4>
                  <p className="text-sm">Demonstrates 82% average accuracy across 150+ finished matches, proving the model's effectiveness in predicting match excitement.</p>
                </div>
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-xl font-semibold text-gray-900 mb-3">🤖 The Machine Learning Model</h3>
            <div className="bg-gray-50 p-4 rounded-lg space-y-3">
              <div>
                <h4 className="font-semibold text-gray-900 mb-1">Algorithm: Elastic Net Regression</h4>
                <p className="text-sm">A linear regression model with L1 and L2 regularization that balances feature selection and coefficient shrinkage. Chosen for its interpretability and performance on our dataset.</p>
              </div>
              <div>
                <h4 className="font-semibold text-gray-900 mb-1">Target Variable: Simple xG</h4>
                <p className="text-sm">Formula: <code className="bg-white px-2 py-1 rounded">xG_home + xG_away + min(xG_home, xG_away)</code></p>
                <p className="text-sm mt-1">This metric captures both total attacking output and match competitiveness. A close match (similar xG values) scores higher than a one-sided game.</p>
              </div>
              <div>
                <h4 className="font-semibold text-gray-900 mb-1">27 Input Features</h4>
                <div className="grid md:grid-cols-2 gap-2 text-sm">
                  <div>
                    <strong>Attacking Features:</strong>
                    <ul className="list-disc list-inside ml-2 text-xs">
                      <li>xG per 90 minutes</li>
                      <li>Shots on target per 90</li>
                      <li>Big chances created per 90</li>
                      <li>Corners per 90</li>
                      <li>Touches in box per 90</li>
                    </ul>
                  </div>
                  <div>
                    <strong>Defensive Features:</strong>
                    <ul className="list-disc list-inside ml-2 text-xs">
                      <li>xG allowed per 90</li>
                      <li>Shots on target against per 90</li>
                      <li>Big chances allowed per 90</li>
                    </ul>
                  </div>
                  <div>
                    <strong>Form Features:</strong>
                    <ul className="list-disc list-inside ml-2 text-xs">
                      <li>Attack vs Defense ratio</li>
                      <li>Days rest</li>
                      <li>Rest difference</li>
                    </ul>
                  </div>
                  <div>
                    <strong>Context Features:</strong>
                    <ul className="list-disc list-inside ml-2 text-xs">
                      <li>Home advantage flag</li>
                      <li>League average xG</li>
                      <li>League average corners</li>
                    </ul>
                  </div>
                </div>
              </div>
              <div>
                <h4 className="font-semibold text-gray-900 mb-1">Training Data</h4>
                <p className="text-sm">Trained on 380 matches from the 2024/25 Premier League season. All features are rolling 5-match averages to capture recent form while smoothing out anomalies.</p>
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">📊 Performance</h3>
            <div className="grid grid-cols-2 gap-4 bg-yellow-50 p-4 rounded-lg">
              <div>
                <div className="text-2xl font-bold text-orange-600">82%</div>
                <div className="text-sm text-gray-600">R² Score (Variance Explained)</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-orange-600">90%</div>
                <div className="text-sm text-gray-600">Top-10 Hit Rate</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-orange-600">0.45</div>
                <div className="text-sm text-gray-600">Mean Absolute Error</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-orange-600">0.90</div>
                <div className="text-sm text-gray-600">Spearman ρ (Ranking)</div>
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">🎓 Project Info</h3>
            <ul className="list-disc list-inside space-y-1">
              <li><strong>Course:</strong> CS 506 - Data Science</li>
              <li><strong>Institution:</strong> Boston University</li>
              <li><strong>Team:</strong> James Njoroge, Muhammad Raka Zuhdi, Fola Oladipo</li>
              <li><strong>Semester:</strong> Fall 2025</li>
            </ul>
          </div>

          <div>
            <h3 className="text-xl font-semibold text-gray-900 mb-3">💡 How It Works (Technical Pipeline)</h3>
            <div className="space-y-3">
              <div className="flex items-start gap-3">
                <div className="bg-blue-600 text-white rounded-full w-8 h-8 flex items-center justify-center flex-shrink-0 text-sm font-bold">1</div>
                <div>
                  <h4 className="font-semibold text-gray-900">Data Collection</h4>
                  <p className="text-sm">Scrapes match fixtures and statistics from FotMob API. For finished matches, extracts actual xG data from shot-by-shot events. For upcoming matches, uses pre-computed team statistics.</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="bg-blue-600 text-white rounded-full w-8 h-8 flex items-center justify-center flex-shrink-0 text-sm font-bold">2</div>
                <div>
                  <h4 className="font-semibold text-gray-900">Feature Engineering</h4>
                  <p className="text-sm">For each match, creates a 27-feature vector using team statistics (from <code className="bg-white px-1 rounded text-xs">team_stats.pkl</code>). Features include home/away attacking stats, defensive stats, rest days, and league averages.</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="bg-blue-600 text-white rounded-full w-8 h-8 flex items-center justify-center flex-shrink-0 text-sm font-bold">3</div>
                <div>
                  <h4 className="font-semibold text-gray-900">Feature Scaling</h4>
                  <p className="text-sm">Applies StandardScaler (from <code className="bg-white px-1 rounded text-xs">scaler.pkl</code>) to normalize features. This ensures features with larger ranges don't dominate the model.</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="bg-blue-600 text-white rounded-full w-8 h-8 flex items-center justify-center flex-shrink-0 text-sm font-bold">4</div>
                <div>
                  <h4 className="font-semibold text-gray-900">Prediction</h4>
                  <p className="text-sm">Feeds scaled features into the Elastic Net model (from <code className="bg-white px-1 rounded text-xs">model.pkl</code>) to generate liveliness score (0-8 scale).</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="bg-blue-600 text-white rounded-full w-8 h-8 flex items-center justify-center flex-shrink-0 text-sm font-bold">5</div>
                <div>
                  <h4 className="font-semibold text-gray-900">Ranking & Display</h4>
                  <p className="text-sm">Sorts all 380 matches by predicted liveliness (descending) and assigns global ranks. Frontend displays matches with team logos, scores, and accuracy metrics.</p>
                </div>
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-xl font-semibold text-gray-900 mb-3">🎯 Use Cases</h3>
            <div className="grid md:grid-cols-2 gap-4">
              <div className="bg-green-50 p-4 rounded-lg">
                <h4 className="font-semibold text-green-800 mb-2">👥 For Fans</h4>
                <ul className="text-sm space-y-1 text-green-900">
                  <li>✓ Decide which match to watch on busy weekends</li>
                  <li>✓ Discover exciting matches between mid-table teams</li>
                  <li>✓ Plan viewing schedule for the week</li>
                  <li>✓ Avoid boring one-sided games</li>
                </ul>
              </div>
              <div className="bg-blue-50 p-4 rounded-lg">
                <h4 className="font-semibold text-blue-800 mb-2">📺 For Broadcasters</h4>
                <ul className="text-sm space-y-1 text-blue-900">
                  <li>✓ Select matches for prime-time slots</li>
                  <li>✓ Optimize scheduling for viewer engagement</li>
                  <li>✓ Predict viewership potential</li>
                  <li>✓ Market matches more effectively</li>
                </ul>
              </div>
              <div className="bg-yellow-50 p-4 rounded-lg">
                <h4 className="font-semibold text-orange-800 mb-2">📊 For Analysts</h4>
                <ul className="text-sm space-y-1 text-purple-900">
                  <li>✓ Quantify match entertainment value</li>
                  <li>✓ Identify factors driving excitement</li>
                  <li>✓ Compare predicted vs actual outcomes</li>
                  <li>✓ Validate model performance</li>
                </ul>
              </div>
              <div className="bg-orange-50 p-4 rounded-lg">
                <h4 className="font-semibold text-orange-800 mb-2">🎰 For Betting</h4>
                <ul className="text-sm space-y-1 text-orange-900">
                  <li>✓ Predict over/under goals markets</li>
                  <li>✓ Identify high-scoring games</li>
                  <li>✓ Find value in entertainment bets</li>
                  <li>✓ Assess match competitiveness</li>
                </ul>
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-xl font-semibold text-gray-900 mb-3">🔬 Key Features of This Website</h3>
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <span className="text-green-600">✓</span>
                <span className="text-sm"><strong>Real-time Data:</strong> Scrapes 380 matches with actual xG for 150+ finished games</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-green-600">✓</span>
                <span className="text-sm"><strong>Week Navigation:</strong> Browse past and future weeks to see predictions and results</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-green-600">✓</span>
                <span className="text-sm"><strong>Comparison View:</strong> Side-by-side predicted vs actual rankings for finished matches</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-green-600">✓</span>
                <span className="text-sm"><strong>Accuracy Metrics:</strong> Color-coded accuracy badges (green 90%+, blue 75%+, yellow 60%+)</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-green-600">✓</span>
                <span className="text-sm"><strong>Live Updates:</strong> Run <code className="bg-white px-1 rounded text-xs">make update</code> to refresh data after matches</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-green-600">✓</span>
                <span className="text-sm"><strong>Automated Setup:</strong> One-command installation with Makefile automation</span>
              </div>
            </div>
          </div>

          <div className="bg-gradient-to-r from-blue-50 to-yellow-50 p-4 rounded-lg border-l-4 border-blue-500">
            <p className="text-sm text-gray-900 mb-2">
              <strong>📈 Model Limitations:</strong> This model explains 82% of variance in match excitement. The remaining 18% includes unpredictable factors:
            </p>
            <ul className="text-xs text-gray-700 ml-4 space-y-1">
              <li>• Last-minute injuries or lineup changes</li>
              <li>• Tactical surprises or formation changes</li>
              <li>• Individual moments of brilliance</li>
              <li>• Weather conditions and pitch quality</li>
              <li>• Referee decisions and VAR controversies</li>
              <li>• Team motivation and psychological factors</li>
            </ul>
          </div>
        </div>

        <div className="mt-8 text-center">
          <button 
            onClick={onClose}
            className="bg-orange-600 hover:bg-orange-700 text-white px-6 py-2 rounded-lg font-medium transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default AboutModal;
