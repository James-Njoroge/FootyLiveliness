import React from 'react';
import { X, Brain, TrendingUp, Target, Award, AlertCircle } from 'lucide-react';

const ModelInfo = ({ onClose, apiStatus }) => {
  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl max-w-3xl w-full max-h-[90vh] overflow-y-auto shadow-2xl">
        <div className="sticky top-0 bg-gradient-to-r from-green-600 to-emerald-600 text-white p-6 rounded-t-2xl">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Brain className="w-8 h-8" />
              <h2 className="text-2xl font-bold">How It Works</h2>
            </div>
            <button
              onClick={onClose}
              className="p-2 hover:bg-white/20 rounded-lg transition-colors"
            >
              <X className="w-6 h-6" />
            </button>
          </div>
        </div>

        <div className="p-6 space-y-6">
          {/* Overview */}
          <section>
            <h3 className="text-xl font-bold text-gray-800 mb-3 flex items-center gap-2">
              <Target className="w-5 h-5 text-purple-600" />
              What is Liveliness?
            </h3>
            <p className="text-gray-700 leading-relaxed">
              Liveliness is a viewer-centric metric that combines attacking action and competitiveness. 
              We use the formula: <code className="bg-gray-100 px-2 py-1 rounded">xG_total + min(xG_home, xG_away)</code>
            </p>
            <p className="text-gray-600 text-sm mt-2">
              This rewards both total attacking threat AND competitive matches where both teams are dangerous.
            </p>
          </section>

          {/* Model Details */}
          <section className="bg-gradient-to-r from-green-50 to-yellow-50 p-4 rounded-xl">
            <h3 className="text-xl font-bold text-gray-800 mb-3 flex items-center gap-2">
              <Brain className="w-5 h-5 text-purple-600" />
              The Model
            </h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-gray-600 font-semibold">Algorithm</p>
                <p className="text-gray-800">Ridge Regression</p>
              </div>
              <div>
                <p className="text-sm text-gray-600 font-semibold">Features</p>
                <p className="text-gray-800">37 contextual features</p>
              </div>
              <div>
                <p className="text-sm text-gray-600 font-semibold">R² Score</p>
                <p className="text-gray-800">0.088 (8.8% variance explained)</p>
              </div>
              <div>
                <p className="text-sm text-gray-600 font-semibold">Training Data</p>
                <p className="text-gray-800">240 PL matches (2024/25)</p>
              </div>
              <div className="col-span-2">
                <p className="text-sm text-gray-600 font-semibold">API Status</p>
                <p className={`text-gray-800 flex items-center gap-2 ${
                  apiStatus === 'connected' ? 'text-green-600' : 'text-yellow-600'
                }`}>
                  <span className={`w-2 h-2 rounded-full ${
                    apiStatus === 'connected' ? 'bg-green-500' : 'bg-yellow-500'
                  }`}></span>
                  {apiStatus === 'connected' ? 'Backend Connected (Full Model)' : 'Demo Mode (Simplified Model)'}
                </p>
              </div>
            </div>
          </section>

          {/* Performance */}
          <section>
            <h3 className="text-xl font-bold text-gray-800 mb-3 flex items-center gap-2">
              <Award className="w-5 h-5 text-purple-600" />
              Performance Metrics
            </h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                <span className="text-gray-700 font-medium">Top-3 Recommendation Accuracy</span>
                <span className="text-green-700 font-bold">67%</span>
              </div>
              <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                <span className="text-gray-700 font-medium">Precision@5 (Finding Lively Matches)</span>
                <span className="text-blue-700 font-bold">60%</span>
              </div>
              <div className="flex items-center justify-between p-3 bg-purple-50 rounded-lg">
                <span className="text-gray-700 font-medium">Mean Absolute Error</span>
                <span className="text-purple-700 font-bold">±1.04 points</span>
              </div>
            </div>
          </section>

          {/* Features Used */}
          <section>
            <h3 className="text-xl font-bold text-gray-800 mb-3 flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-purple-600" />
              Key Features Analyzed
            </h3>
            <div className="grid grid-cols-2 gap-3">
              <div className="bg-gray-50 p-3 rounded-lg">
                <p className="font-semibold text-gray-800 text-sm">Rolling Form</p>
                <p className="text-xs text-gray-600">Last 5 matches (xG, shots, corners)</p>
              </div>
              <div className="bg-gray-50 p-3 rounded-lg">
                <p className="font-semibold text-gray-800 text-sm">League Position</p>
                <p className="text-xs text-gray-600">Current standings & points</p>
              </div>
              <div className="bg-gray-50 p-3 rounded-lg">
                <p className="font-semibold text-gray-800 text-sm">Form Trajectory</p>
                <p className="text-xs text-gray-600">Recent 3 vs previous 5 matches</p>
              </div>
              <div className="bg-gray-50 p-3 rounded-lg">
                <p className="font-semibold text-gray-800 text-sm">High Stakes</p>
                <p className="text-xs text-gray-600">Top 6 battles, relegation fights</p>
              </div>
            </div>
          </section>

          {/* Limitations */}
          <section className="bg-yellow-50 p-4 rounded-xl border border-yellow-200">
            <h3 className="text-lg font-bold text-gray-800 mb-2 flex items-center gap-2">
              <AlertCircle className="w-5 h-5 text-yellow-600" />
              What the Model Can't Predict
            </h3>
            <ul className="text-sm text-gray-700 space-y-1 list-disc list-inside">
              <li>Player injuries and suspensions</li>
              <li>Tactical surprises and in-game adjustments</li>
              <li>Individual moments of brilliance</li>
              <li>Weather conditions and referee decisions</li>
              <li>Psychological factors (rivalry intensity, pressure)</li>
            </ul>
          </section>

          {/* Data Source */}
          <section className="text-center text-sm text-gray-600 pt-4 border-t">
            <p>
              Data sourced from <span className="font-semibold">FotMob</span> | 
              Model trained on 2024/25 Premier League season
            </p>
            <p className="mt-1">
              CS 506 - Data Science | Boston University | Fall 2025
            </p>
          </section>
        </div>
      </div>
    </div>
  );
};

export default ModelInfo;
