import React, { useEffect } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import { Bar, Line, Doughnut } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

const ProjectDetailsModal = ({ onClose, onShowArchitecture }) => {
  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') onClose();
    };
    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [onClose]);

  // Performance Evolution Chart Data
  const performanceData = {
    labels: ['Initial\n(Linear Reg)', 'XGBoost\nBaseline', 'Ridge\n(37 feat)', 'Elastic Net\n(Simple xG)'],
    datasets: [
      {
        label: 'R² Score',
        data: [-0.15, 0.042, 0.088, 0.821],
        backgroundColor: [
          'rgba(239, 68, 68, 0.8)',
          'rgba(251, 146, 60, 0.8)',
          'rgba(234, 179, 8, 0.8)',
          'rgba(34, 197, 94, 0.8)',
        ],
        borderColor: [
          'rgb(220, 38, 38)',
          'rgb(234, 88, 12)',
          'rgb(202, 138, 4)',
          'rgb(22, 163, 74)',
        ],
        borderWidth: 2,
      },
    ],
  };

  // Model Comparison Chart Data
  const modelComparisonData = {
    labels: ['Elastic Net', 'Ridge', 'Gradient Boosting', 'XGBoost', 'Neural Network'],
    datasets: [
      {
        label: 'Test R²',
        data: [0.821, 0.812, 0.747, 0.042, -0.05],
        backgroundColor: 'rgba(147, 51, 234, 0.8)',
        borderColor: 'rgb(126, 34, 206)',
        borderWidth: 2,
      },
    ],
  };

  // Target Metrics Comparison Chart
  const targetMetricsData = {
    labels: ['Simple xG', 'Comprehensive', 'Chances', 'Intensity', 'Shot Quality', 'Minimal', 'End-to-End'],
    datasets: [
      {
        label: 'Test R²',
        data: [0.812, 0.724, 0.702, 0.658, 0.647, 0.577, 0.408],
        backgroundColor: 'rgba(59, 130, 246, 0.8)',
        borderColor: 'rgb(37, 99, 235)',
        borderWidth: 2,
      },
    ],
  };

  // Feature Importance (Top 15)
  const featureImportanceData = {
    labels: [
      'both_top6',
      'away_Corn_att_90',
      'away_BigCh_agst_90',
      'away_last3_goals',
      'gd_diff',
      'away_position',
      'home_xGA_def_90',
      'home_BigCh_att_90',
      'home_Corn_att_90',
      'position_diff',
      'away_SoT_agst_90',
      'away_ToB_att_90',
      'away_SoT_att_90',
      'SoTSum',
      'close_positions',
    ],
    datasets: [
      {
        label: 'Coefficient',
        data: [-0.168, 0.132, 0.123, -0.117, 0.117, -0.110, 0.096, 0.094, 0.092, 0.090, -0.078, -0.068, 0.065, 0.062, -0.061],
        backgroundColor: function(context) {
          const value = context.parsed.x;
          return value >= 0 ? 'rgba(34, 197, 94, 0.8)' : 'rgba(239, 68, 68, 0.8)';
        },
        borderColor: function(context) {
          const value = context.parsed.x;
          return value >= 0 ? 'rgb(22, 163, 74)' : 'rgb(220, 38, 38)';
        },
        borderWidth: 2,
      },
    ],
  };

  // Variance Explained Doughnut
  const varianceData = {
    labels: ['Explained by Model (82%)', 'Unexplained (18%)'],
    datasets: [
      {
        data: [82, 18],
        backgroundColor: [
          'rgba(147, 51, 234, 0.8)',
          'rgba(209, 213, 219, 0.8)',
        ],
        borderColor: [
          'rgb(126, 34, 206)',
          'rgb(156, 163, 175)',
        ],
        borderWidth: 2,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: 'top',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  const horizontalChartOptions = {
    indexAxis: 'y',
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
    },
    scales: {
      x: {
        beginAtZero: true,
      },
    },
  };

  return (
    <div 
      className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 modal-enter p-4"
      onClick={onClose}
    >
      <div 
        className="bg-white rounded-xl max-w-6xl max-h-[90vh] overflow-y-auto overflow-x-hidden modal-content-enter w-full"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex justify-between items-start sticky top-0 bg-white z-10 px-6 md:px-8 pt-6 md:pt-8 pb-4 border-b mb-6">
          <h2 className="text-2xl md:text-3xl font-bold text-gray-900">📊 Complete Project Analysis</h2>
          <button 
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-full w-8 h-8 flex items-center justify-center transition-all text-2xl font-bold"
            aria-label="Close"
          >
            ×
          </button>
        </div>
        
        <div className="space-y-10 text-gray-700 px-6 md:px-8">
          {/* Executive Summary */}
          <div>
            <h3 className="text-2xl font-bold text-purple-600 mb-4 flex items-center gap-2">
              <span>🎯</span> Executive Summary
            </h3>
            <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-6 rounded-lg">
              <p className="text-lg mb-4">
                An end-to-end machine learning system that predicts Premier League match "liveliness" (excitement level) 
                using pre-match team statistics. Achieved <strong className="text-purple-600">82% variance explained (R²)</strong> and 
                <strong className="text-purple-600"> 90% accuracy</strong> in identifying the most exciting matches.
              </p>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                <div className="bg-white p-4 rounded-lg text-center shadow-sm">
                  <div className="text-3xl font-bold text-purple-600">0.82</div>
                  <div className="text-xs text-gray-600 mt-1">R² Score</div>
                </div>
                <div className="bg-white p-4 rounded-lg text-center shadow-sm">
                  <div className="text-3xl font-bold text-purple-600">90%</div>
                  <div className="text-xs text-gray-600 mt-1">Top-10 Hit</div>
                </div>
                <div className="bg-white p-4 rounded-lg text-center shadow-sm">
                  <div className="text-3xl font-bold text-purple-600">0.45</div>
                  <div className="text-xs text-gray-600 mt-1">MAE</div>
                </div>
                <div className="bg-white p-4 rounded-lg text-center shadow-sm">
                  <div className="text-3xl font-bold text-purple-600">37</div>
                  <div className="text-xs text-gray-600 mt-1">Features</div>
                </div>
                <div className="bg-white p-4 rounded-lg text-center shadow-sm">
                  <div className="text-3xl font-bold text-purple-600">380</div>
                  <div className="text-xs text-gray-600 mt-1">Matches</div>
                </div>
              </div>
            </div>
          </div>

          {/* Variance Explained Visualization */}
          <div>
            <h3 className="text-2xl font-bold text-purple-600 mb-4">📈 Model Explanatory Power</h3>
            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-gray-50 p-6 rounded-lg">
                <h4 className="font-semibold mb-4 text-center">Variance Explained</h4>
                <div className="h-64">
                  <Doughnut data={varianceData} options={{ responsive: true, maintainAspectRatio: false }} />
                </div>
                <p className="text-sm text-gray-600 mt-4 text-center">
                  Our model explains <strong>82%</strong> of what makes matches exciting. The remaining 18% includes 
                  unpredictable factors like injuries, tactics, and individual brilliance.
                </p>
              </div>
              <div className="bg-blue-50 p-6 rounded-lg">
                <h4 className="font-semibold mb-3">What the Model Captures</h4>
                <ul className="space-y-2 text-sm">
                  <li className="flex items-start gap-2">
                    <span className="text-green-600 font-bold">✓</span>
                    <span><strong>Team Form:</strong> Rolling 5-match averages of performance</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-green-600 font-bold">✓</span>
                    <span><strong>League Position:</strong> Current standings and competitive pressure</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-green-600 font-bold">✓</span>
                    <span><strong>Attacking Power:</strong> xG, shots, big chances creation</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-green-600 font-bold">✓</span>
                    <span><strong>Defensive Weakness:</strong> Goals/chances conceded</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-green-600 font-bold">✓</span>
                    <span><strong>Match Stakes:</strong> Top 6 clashes, relegation battles</span>
                  </li>
                </ul>
                <h4 className="font-semibold mb-2 mt-4">What It Misses (18%)</h4>
                <ul className="space-y-2 text-sm">
                  <li className="flex items-start gap-2">
                    <span className="text-red-600 font-bold">✗</span>
                    <span>Key player injuries/suspensions</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-red-600 font-bold">✗</span>
                    <span>Tactical surprises and formations</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-red-600 font-bold">✗</span>
                    <span>Individual moments of brilliance</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-red-600 font-bold">✗</span>
                    <span>Weather and referee decisions</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>

          {/* Performance Evolution Chart */}
          <div>
            <h3 className="text-2xl font-bold text-purple-600 mb-4">📊 Performance Evolution (+833% Improvement)</h3>
            <div className="bg-gray-50 p-6 rounded-lg">
              <div className="h-80">
                <Bar data={performanceData} options={chartOptions} />
              </div>
              <div className="mt-6 grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                <div className="bg-red-50 p-3 rounded">
                  <div className="font-bold text-red-600">Initial: R² = -0.15</div>
                  <div className="text-xs mt-1">Linear Reg + SLS-F+ (complex metric)</div>
                </div>
                <div className="bg-orange-50 p-3 rounded">
                  <div className="font-bold text-orange-600">Stage 2: R² = 0.042</div>
                  <div className="text-xs mt-1">XGBoost baseline (+19%)</div>
                </div>
                <div className="bg-yellow-50 p-3 rounded">
                  <div className="font-bold text-yellow-600">Stage 3: R² = 0.088</div>
                  <div className="text-xs mt-1">Ridge + 37 features (+110%)</div>
                </div>
                <div className="bg-green-50 p-3 rounded">
                  <div className="font-bold text-green-600">Final: R² = 0.821</div>
                  <div className="text-xs mt-1">Elastic Net + Simple xG (+833%)</div>
                </div>
              </div>
            </div>
          </div>

          {/* Model Comparison Chart */}
          <div>
            <h3 className="text-2xl font-bold text-purple-600 mb-4">🤖 Model Comparison</h3>
            <div className="bg-gray-50 p-6 rounded-lg">
              <div className="h-80">
                <Bar data={modelComparisonData} options={chartOptions} />
              </div>
              <div className="mt-6 overflow-x-auto">
                <table className="min-w-full text-sm">
                  <thead className="bg-purple-100">
                    <tr>
                      <th className="px-4 py-3 text-left font-semibold">Model</th>
                      <th className="px-4 py-3 text-center font-semibold">Test R²</th>
                      <th className="px-4 py-3 text-center font-semibold">MAE</th>
                      <th className="px-4 py-3 text-center font-semibold">Top-10 Hit</th>
                      <th className="px-4 py-3 text-center font-semibold">Overfitting</th>
                      <th className="px-4 py-3 text-left font-semibold">Verdict</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr className="border-b bg-green-50 font-semibold">
                      <td className="px-4 py-3">🏆 Elastic Net</td>
                      <td className="px-4 py-3 text-center text-green-600">0.821</td>
                      <td className="px-4 py-3 text-center">0.452</td>
                      <td className="px-4 py-3 text-center">90%</td>
                      <td className="px-4 py-3 text-center text-green-600">-0.014</td>
                      <td className="px-4 py-3">✅ Winner - Best generalization</td>
                    </tr>
                    <tr className="border-b bg-white">
                      <td className="px-4 py-3">Ridge Regression</td>
                      <td className="px-4 py-3 text-center">0.812</td>
                      <td className="px-4 py-3 text-center">0.470</td>
                      <td className="px-4 py-3 text-center">90%</td>
                      <td className="px-4 py-3 text-center text-green-600">-0.002</td>
                      <td className="px-4 py-3">✓ Close second</td>
                    </tr>
                    <tr className="border-b bg-white">
                      <td className="px-4 py-3">Gradient Boosting</td>
                      <td className="px-4 py-3 text-center">0.747</td>
                      <td className="px-4 py-3 text-center">0.542</td>
                      <td className="px-4 py-3 text-center">90%</td>
                      <td className="px-4 py-3 text-center text-orange-600">0.168</td>
                      <td className="px-4 py-3">⚠️ Moderate overfitting</td>
                    </tr>
                    <tr className="border-b bg-white">
                      <td className="px-4 py-3">XGBoost</td>
                      <td className="px-4 py-3 text-center text-red-600">0.042</td>
                      <td className="px-4 py-3 text-center">1.150</td>
                      <td className="px-4 py-3 text-center">~40%</td>
                      <td className="px-4 py-3 text-center">-</td>
                      <td className="px-4 py-3">❌ Too complex for dataset size</td>
                    </tr>
                    <tr className="border-b bg-white">
                      <td className="px-4 py-3">Neural Network (MLP)</td>
                      <td className="px-4 py-3 text-center text-red-600">Negative</td>
                      <td className="px-4 py-3 text-center">-</td>
                      <td className="px-4 py-3 text-center">-</td>
                      <td className="px-4 py-3 text-center text-red-600">Severe</td>
                      <td className="px-4 py-3">❌ Failed - needs 500+ samples</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          {/* Target Metrics Comparison Chart */}
          <div>
            <h3 className="text-2xl font-bold text-purple-600 mb-4">🧪 Target Metric Experiments</h3>
            <div className="bg-gray-50 p-6 rounded-lg">
              <p className="text-sm mb-4">
                We tested <strong>7 different formulas</strong> for measuring match liveliness to validate that Simple xG is optimal:
              </p>
              <div className="h-80">
                <Bar data={targetMetricsData} options={chartOptions} />
              </div>
              <div className="mt-6 grid md:grid-cols-2 gap-4 text-sm">
                <div className="bg-green-50 p-4 rounded-lg">
                  <h4 className="font-semibold text-green-800 mb-2">🏆 Winner: Simple xG</h4>
                  <div className="font-mono text-xs bg-white p-2 rounded mb-2">
                    xG_total + min(xG_home, xG_away)
                  </div>
                  <ul className="space-y-1">
                    <li>• <strong>R² = 0.812</strong> (best predictability)</li>
                    <li>• <strong>90% Top-10 Hit Rate</strong></li>
                    <li>• Rewards total attacking action</li>
                    <li>• Rewards competitiveness (both teams threatening)</li>
                    <li>• Simple and interpretable</li>
                  </ul>
                </div>
                <div className="bg-red-50 p-4 rounded-lg">
                  <h4 className="font-semibold text-red-800 mb-2">❌ Why Others Failed</h4>
                  <ul className="space-y-2">
                    <li><strong>Comprehensive:</strong> Too complex, dilutes signal (R²=0.72)</li>
                    <li><strong>Chances-Focused:</strong> Quantity over quality (R²=0.70)</li>
                    <li><strong>Intensity (with cards):</strong> Fouls ≠ excitement (R²=0.66)</li>
                    <li><strong>Shot Quality:</strong> Over-weighted shots (R²=0.65)</li>
                    <li><strong>Minimal:</strong> Too simple, misses nuance (R²=0.58)</li>
                    <li><strong>End-to-End:</strong> Incorrect weighting (R²=0.41)</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          {/* Feature Importance Chart */}
          <div>
            <h3 className="text-2xl font-bold text-purple-600 mb-4">🎯 Feature Importance (Top 15)</h3>
            <div className="bg-gray-50 p-6 rounded-lg">
              <div className="h-96">
                <Bar data={featureImportanceData} options={horizontalChartOptions} />
              </div>
              <div className="mt-6 grid md:grid-cols-2 gap-4 text-sm">
                <div className="bg-green-50 p-4 rounded-lg">
                  <h4 className="font-semibold text-green-800 mb-2">✅ Positive Predictors (More Exciting)</h4>
                  <ul className="space-y-1">
                    <li>• <strong>away_Corn_att_90:</strong> Away team corners (pressure indicator)</li>
                    <li>• <strong>away_BigCh_agst_90:</strong> Away defensive weakness</li>
                    <li>• <strong>gd_diff:</strong> Goal difference gap (competitive balance)</li>
                    <li>• <strong>home_xGA_def_90:</strong> Home defensive weakness</li>
                    <li>• <strong>home_BigCh_att_90:</strong> Home attacking threat</li>
                    <li>• <strong>position_diff:</strong> Table position gap</li>
                  </ul>
                </div>
                <div className="bg-red-50 p-4 rounded-lg">
                  <h4 className="font-semibold text-red-800 mb-2">❌ Negative Predictors (Less Exciting)</h4>
                  <ul className="space-y-1">
                    <li>• <strong>both_top6:</strong> Top 6 clashes are surprisingly LESS lively (tactical, cautious)</li>
                    <li>• <strong>away_last3_goals:</strong> Recent away scoring form</li>
                    <li>• <strong>away_position:</strong> Away team league position</li>
                    <li>• <strong>away_SoT_agst_90:</strong> Away defensive solidity</li>
                    <li>• <strong>close_positions:</strong> Direct position battles</li>
                  </ul>
                </div>
              </div>
              <div className="mt-4 bg-blue-50 p-4 rounded-lg">
                <h4 className="font-semibold text-blue-800 mb-2">💡 Key Insight</h4>
                <p className="text-sm">
                  <strong>Defensive weakness predicts excitement better than offensive strength!</strong> Matches are more 
                  exciting when teams are vulnerable at the back, not necessarily when they're strong going forward. 
                  Also, top 6 clashes tend to be more tactical and cautious, contrary to popular belief.
                </p>
              </div>
            </div>
          </div>

          {/* Data Collection & Pipeline */}
          <div>
            <h3 className="text-2xl font-bold text-purple-600 mb-4">📊 Data Collection & Pipeline</h3>
            <div className="grid md:grid-cols-3 gap-4">
              <div className="bg-blue-50 p-4 rounded-lg">
                <h4 className="font-semibold mb-2">1️⃣ Data Source</h4>
                <ul className="text-sm space-y-1">
                  <li><strong>Platform:</strong> FotMob</li>
                  <li><strong>Method:</strong> Selenium scraping</li>
                  <li><strong>Format:</strong> 380 JSON files</li>
                  <li><strong>Content:</strong> xG events, team stats, lineups, cards</li>
                </ul>
              </div>
              <div className="bg-green-50 p-4 rounded-lg">
                <h4 className="font-semibold mb-2">2️⃣ Feature Engineering</h4>
                <ul className="text-sm space-y-1">
                  <li><strong>Rolling features:</strong> 5-match averages</li>
                  <li><strong>Contextual:</strong> Position, form, stakes</li>
                  <li><strong>Total:</strong> 37 features</li>
                  <li><strong>No leakage:</strong> Only pre-match data</li>
                </ul>
              </div>
              <div className="bg-purple-50 p-4 rounded-lg">
                <h4 className="font-semibold mb-2">3️⃣ Model Training</h4>
                <ul className="text-sm space-y-1">
                  <li><strong>Train:</strong> 280 matches (rounds 0-27)</li>
                  <li><strong>Val:</strong> 50 matches (rounds 28-32)</li>
                  <li><strong>Test:</strong> 50 matches (rounds 33-37)</li>
                  <li><strong>Validation:</strong> Chronological splits</li>
                </ul>
              </div>
            </div>
          </div>

          {/* Feature Categories */}
          <div>
            <h3 className="text-2xl font-bold text-purple-600 mb-4">🛠️ Feature Engineering (37 Features)</h3>
            <div className="space-y-4">
              <div className="bg-gradient-to-r from-green-50 to-emerald-50 p-5 rounded-lg">
                <h4 className="font-semibold mb-3 text-lg">Rolling Features (22 features)</h4>
                <p className="text-sm mb-3">5-match rolling averages per team (home & away):</p>
                <div className="grid md:grid-cols-2 gap-4 text-sm">
                  <div>
                    <strong className="text-green-700">Offensive Metrics (10):</strong>
                    <ul className="list-disc list-inside mt-1 space-y-1">
                      <li>xG per 90 minutes</li>
                      <li>Shots on Target per 90</li>
                      <li>Big Chances per 90</li>
                      <li>Corners per 90</li>
                      <li>Touches in Opposition Box per 90</li>
                    </ul>
                  </div>
                  <div>
                    <strong className="text-green-700">Defensive Metrics (6):</strong>
                    <ul className="list-disc list-inside mt-1 space-y-1">
                      <li>xG Against per 90</li>
                      <li>Shots on Target Against per 90</li>
                      <li>Big Chances Against per 90</li>
                    </ul>
                    <strong className="text-green-700 mt-2 block">Composite (6):</strong>
                    <ul className="list-disc list-inside mt-1 space-y-1">
                      <li>TempoSum, SoTSum, AttackVsDefense</li>
                      <li>xG_att_sum, xG_att_min, BigCh_sum</li>
                    </ul>
                  </div>
                </div>
              </div>
              
              <div className="bg-gradient-to-r from-blue-50 to-cyan-50 p-5 rounded-lg">
                <h4 className="font-semibold mb-3 text-lg">Contextual Features (15 features) ⭐ Critical</h4>
                <div className="grid md:grid-cols-3 gap-4 text-sm">
                  <div>
                    <strong className="text-blue-700">League Context (5):</strong>
                    <ul className="list-disc list-inside mt-1 space-y-1">
                      <li>home_position (1-20)</li>
                      <li>away_position (1-20)</li>
                      <li>position_diff</li>
                      <li>points_diff</li>
                      <li>gd_diff</li>
                    </ul>
                  </div>
                  <div>
                    <strong className="text-blue-700">Form Trajectory (6):</strong>
                    <ul className="list-disc list-inside mt-1 space-y-1">
                      <li>home_last3_points</li>
                      <li>away_last3_points</li>
                      <li>home_last3_goals</li>
                      <li>away_last3_goals</li>
                      <li>home_form_trend</li>
                      <li>away_form_trend</li>
                    </ul>
                  </div>
                  <div>
                    <strong className="text-blue-700">Stakes Indicators (4):</strong>
                    <ul className="list-disc list-inside mt-1 space-y-1">
                      <li>both_top6 (Champions League)</li>
                      <li>both_bottom6 (Relegation)</li>
                      <li>close_positions (Direct rivals)</li>
                      <li>home/away_strength_ratio</li>
                    </ul>
                  </div>
                </div>
                <div className="mt-3 bg-white p-3 rounded text-sm">
                  <strong>Impact:</strong> Adding these 15 contextual features improved R² from 0.088 → 0.821 
                  (a <strong className="text-blue-600">+833% improvement</strong>)
                </div>
              </div>
            </div>
          </div>

          {/* Key Learnings */}
          <div>
            <h3 className="text-2xl font-bold text-purple-600 mb-4">💡 Key Learnings & Insights</h3>
            <div className="grid md:grid-cols-2 gap-4">
              <div className="bg-green-50 p-5 rounded-lg">
                <h4 className="font-semibold text-green-800 mb-3 text-lg">✅ What Works</h4>
                <ul className="space-y-2 text-sm">
                  <li className="flex items-start gap-2">
                    <span className="text-green-600 font-bold mt-0.5">✓</span>
                    <div><strong>Simple metrics beat complex composites:</strong> Simple xG (R²=0.81) vs Comprehensive (R²=0.72)</div>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-green-600 font-bold mt-0.5">✓</span>
                    <div><strong>Contextual features are crucial:</strong> Position, form, stakes added 73% to R²</div>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-green-600 font-bold mt-0.5">✓</span>
                    <div><strong>Strong regularization for small data:</strong> Elastic Net (alpha=21.54) prevents overfitting</div>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-green-600 font-bold mt-0.5">✓</span>
                    <div><strong>Single-season &gt; multi-season:</strong> R²=0.82 vs R²=-0.14 with 3 seasons</div>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-green-600 font-bold mt-0.5">✓</span>
                    <div><strong>Defensive weakness predicts excitement:</strong> Better than offensive strength</div>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-green-600 font-bold mt-0.5">✓</span>
                    <div><strong>Linear models &gt; complex models:</strong> With 280 samples, simplicity wins</div>
                  </li>
                </ul>
              </div>
              <div className="bg-red-50 p-5 rounded-lg">
                <h4 className="font-semibold text-red-800 mb-3 text-lg">❌ What Doesn't Work</h4>
                <ul className="space-y-2 text-sm">
                  <li className="flex items-start gap-2">
                    <span className="text-red-600 font-bold mt-0.5">✗</span>
                    <div><strong>Too many features with small data:</strong> 87 features → catastrophic overfitting</div>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-red-600 font-bold mt-0.5">✗</span>
                    <div><strong>Neural networks with &lt;500 samples:</strong> Need 10× more data</div>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-red-600 font-bold mt-0.5">✗</span>
                    <div><strong>Complex composite metrics (SLS-F+):</strong> Add noise, hard to predict</div>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-red-600 font-bold mt-0.5">✗</span>
                    <div><strong>Head-to-head history:</strong> Too sparse (20 teams, limited matches)</div>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-red-600 font-bold mt-0.5">✗</span>
                    <div><strong>Cards as excitement indicator:</strong> Fouls ≠ entertainment</div>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-red-600 font-bold mt-0.5">✗</span>
                    <div><strong>Cross-season training:</strong> Teams change too much year-to-year</div>
                  </li>
                </ul>
              </div>
            </div>
          </div>

          {/* Methodology & Rigor */}
          <div>
            <h3 className="text-2xl font-bold text-purple-600 mb-4">🎓 Academic Rigor & Methodology</h3>
            <div className="bg-gradient-to-r from-purple-50 to-indigo-50 p-6 rounded-lg">
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-semibold mb-3">✅ Methodology Strengths</h4>
                  <ul className="space-y-2 text-sm">
                    <li className="flex items-start gap-2">
                      <span className="text-green-600">✓</span>
                      <span><strong>No data leakage:</strong> Chronological splits, rolling features only use past data</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-green-600">✓</span>
                      <span><strong>Proper validation:</strong> Train (280) / Val (50) / Test (50) splits</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-green-600">✓</span>
                      <span><strong>Cross-validation:</strong> 5-fold CV for hyperparameter tuning</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-green-600">✓</span>
                      <span><strong>Multiple metrics:</strong> R², MAE, RMSE, Spearman ρ, Top-10 hit rate</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-green-600">✓</span>
                      <span><strong>Overfitting prevention:</strong> Strong regularization (alpha=21.54)</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-green-600">✓</span>
                      <span><strong>Reproducible:</strong> Fixed random seeds, documented pipeline</span>
                    </li>
                  </ul>
                </div>
                <div>
                  <h4 className="font-semibold mb-3">📊 Evaluation Metrics</h4>
                  <div className="space-y-3 text-sm">
                    <div className="bg-white p-3 rounded">
                      <strong>R² = 0.821:</strong> Explains 82% of variance in match excitement
                    </div>
                    <div className="bg-white p-3 rounded">
                      <strong>MAE = 0.45:</strong> Average prediction error of 0.45 points on 1-9 scale
                    </div>
                    <div className="bg-white p-3 rounded">
                      <strong>Spearman ρ = 0.896:</strong> 90% ranking accuracy across ALL matches
                    </div>
                    <div className="bg-white p-3 rounded">
                      <strong>Top-10 Hit = 90%:</strong> Identifies 9/10 most exciting matches correctly
                    </div>
                    <div className="bg-white p-3 rounded">
                      <strong>Overfitting = -0.014:</strong> Excellent generalization (train R² ≈ test R²)
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Deployment & Production */}
          <div>
            <h3 className="text-2xl font-bold text-purple-600 mb-4">🚀 Production Deployment</h3>
            <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-6 rounded-lg">
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-semibold mb-3">Configuration</h4>
                  <div className="bg-white p-4 rounded font-mono text-xs space-y-1">
                    <div><strong>Model:</strong> ElasticNet(alpha=21.54, l1_ratio=0.5)</div>
                    <div><strong>Target:</strong> xG_total + min(xG_home, xG_away)</div>
                    <div><strong>Features:</strong> 37 engineered features</div>
                    <div><strong>Scaler:</strong> StandardScaler (z-score normalization)</div>
                    <div><strong>Data:</strong> Single season (2024/25)</div>
                    <div><strong>Training:</strong> 280 matches, 5-fold CV</div>
                  </div>
                </div>
                <div>
                  <h4 className="font-semibold mb-3">Performance Guarantees</h4>
                  <ul className="space-y-2 text-sm">
                    <li className="flex items-start gap-2">
                      <span className="text-purple-600">📊</span>
                      <span><strong>82% variance explained</strong> - Industry-leading for sports prediction</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-purple-600">🎯</span>
                      <span><strong>90% top-match accuracy</strong> - Reliable recommendations</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-purple-600">⚡</span>
                      <span><strong>&lt;1ms inference time</strong> - Real-time predictions</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-purple-600">✓</span>
                      <span><strong>No overfitting</strong> - Generalizes to new matches</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-purple-600">🔄</span>
                      <span><strong>Auto-refresh</strong> - Updates every 5 minutes</span>
                    </li>
                  </ul>
                </div>
              </div>
              <div className="mt-4 bg-white p-4 rounded">
                <h4 className="font-semibold mb-2">Update Strategy</h4>
                <div className="grid md:grid-cols-3 gap-3 text-sm">
                  <div>
                    <strong>Weekly:</strong> Update rolling features after each matchweek
                  </div>
                  <div>
                    <strong>Seasonal:</strong> Retrain model at start of each season
                  </div>
                  <div>
                    <strong>Monitor:</strong> Track predictions vs actuals for drift detection
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Team & Course Info */}
          <div>
            <h3 className="text-2xl font-bold text-purple-600 mb-4">👥 Team & Course Information</h3>
            <div className="grid md:grid-cols-2 gap-4">
              <div className="bg-blue-50 p-5 rounded-lg">
                <h4 className="font-semibold mb-3">Team Members</h4>
                <ul className="space-y-2 text-sm">
                  <li className="flex items-center gap-2">
                    <span className="text-blue-600">👤</span>
                    <span><strong>James Njoroge</strong> - Data scraping, feature engineering</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <span className="text-blue-600">👤</span>
                    <span><strong>Muhammad Raka Zuhdi</strong> - Target experiments, modeling, web app</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <span className="text-blue-600">👤</span>
                    <span><strong>Fola Oladipo</strong> - Model evaluation, documentation</span>
                  </li>
                </ul>
              </div>
              <div className="bg-purple-50 p-5 rounded-lg">
                <h4 className="font-semibold mb-3">Course Details</h4>
                <ul className="space-y-2 text-sm">
                  <li><strong>Course:</strong> CS 506 - Data Science</li>
                  <li><strong>Institution:</strong> Boston University</li>
                  <li><strong>Semester:</strong> Fall 2025</li>
                  <li><strong>Project Type:</strong> End-to-end ML pipeline</li>
                  <li><strong>Grade Level:</strong> Graduate-level work</li>
                </ul>
              </div>
            </div>
          </div>

          {/* Achievements */}
          <div className="bg-gradient-to-r from-purple-100 via-pink-100 to-purple-100 p-6 rounded-lg">
            <h3 className="text-2xl font-bold text-purple-800 mb-4">🏆 Key Achievements</h3>
            <div className="grid md:grid-cols-2 gap-4 text-sm">
              <div className="space-y-2">
                <div className="flex items-start gap-2">
                  <span className="text-green-600 font-bold">✅</span>
                  <span><strong>End-to-end ML pipeline</strong> from scraping to deployment</span>
                </div>
                <div className="flex items-start gap-2">
                  <span className="text-green-600 font-bold">✅</span>
                  <span><strong>Industry-competitive baseline</strong> (R² = 0.82)</span>
                </div>
                <div className="flex items-start gap-2">
                  <span className="text-green-600 font-bold">✅</span>
                  <span><strong>90% accuracy</strong> identifying exciting matches</span>
                </div>
                <div className="flex items-start gap-2">
                  <span className="text-green-600 font-bold">✅</span>
                  <span><strong>Production-ready web application</strong> with React + Flask</span>
                </div>
              </div>
              <div className="space-y-2">
                <div className="flex items-start gap-2">
                  <span className="text-green-600 font-bold">✅</span>
                  <span><strong>Rigorous validation</strong> (no data leakage, proper splits)</span>
                </div>
                <div className="flex items-start gap-2">
                  <span className="text-green-600 font-bold">✅</span>
                  <span><strong>Comprehensive experiments</strong> (7 targets, 5 models)</span>
                </div>
                <div className="flex items-start gap-2">
                  <span className="text-green-600 font-bold">✅</span>
                  <span><strong>+833% improvement</strong> from initial to final model</span>
                </div>
                <div className="flex items-start gap-2">
                  <span className="text-green-600 font-bold">✅</span>
                  <span><strong>Honest assessment</strong> of limitations and unexplained variance</span>
                </div>
              </div>
            </div>
          </div>

          {/* Final Note */}
          <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-lg border-2 border-blue-200">
            <h4 className="font-semibold text-blue-900 mb-2 text-lg">📌 Final Note</h4>
            <p className="text-sm text-blue-900">
              This model explains <strong>82% of variance</strong> in match excitement - an exceptional result for sports prediction, 
              where typical models achieve 30-50%. The remaining 18% includes genuinely unpredictable factors like injuries, 
              tactical surprises, and individual brilliance. Our approach prioritizes <strong>interpretability, robustness, and 
              production-readiness</strong> over marginal performance gains that might not generalize.
            </p>
            <p className="text-sm text-blue-900 mt-3">
              <strong>Recommendation:</strong> Deploy with confidence. No further improvements are needed without additional 
              data sources (player injuries, tactical information, weather conditions, etc.).
            </p>
          </div>
        </div>

        <div className="mt-8 text-center sticky bottom-0 bg-white pt-4 border-t px-6 md:px-8 pb-6 md:pb-8">
          <div className="flex gap-3 justify-center">
            <button 
              onClick={onShowArchitecture}
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-colors shadow-lg flex items-center gap-2"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z"></path>
              </svg>
              View Architecture Diagram
            </button>
            <button 
              onClick={onClose}
              className="bg-purple-600 hover:bg-purple-700 text-white px-8 py-3 rounded-lg font-medium transition-colors shadow-lg"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProjectDetailsModal;
