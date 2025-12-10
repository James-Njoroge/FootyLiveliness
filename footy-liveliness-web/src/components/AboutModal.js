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
        className="bg-white rounded-xl max-w-2xl max-h-[80vh] overflow-y-auto p-8 m-4 modal-content-enter"
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
            <h3 className="text-xl font-semibold text-gray-900 mb-2">🎯 What is this?</h3>
            <p>An AI-powered system that predicts Premier League match "liveliness" (excitement level) to help football fans decide which matches to watch when multiple games are happening simultaneously.</p>
          </div>

          <div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">🤖 The Model</h3>
            <ul className="list-disc list-inside space-y-1">
              <li><strong>Algorithm:</strong> Elastic Net Regression</li>
              <li><strong>Target Metric:</strong> Simple xG (xG_total + min(xG_home, xG_away))</li>
              <li><strong>Features:</strong> 37 engineered features including team form, attacking strength, defensive stats, league position, and recent performance</li>
              <li><strong>Training Data:</strong> Trained on 2024/25 Premier League season (380 matches)</li>
            </ul>
          </div>

          <div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">📊 Performance</h3>
            <div className="grid grid-cols-2 gap-4 bg-purple-50 p-4 rounded-lg">
              <div>
                <div className="text-2xl font-bold text-purple-600">82%</div>
                <div className="text-sm text-gray-600">R² Score (Variance Explained)</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-purple-600">90%</div>
                <div className="text-sm text-gray-600">Top-10 Hit Rate</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-purple-600">0.45</div>
                <div className="text-sm text-gray-600">Mean Absolute Error</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-purple-600">0.90</div>
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
            <h3 className="text-xl font-semibold text-gray-900 mb-2">💡 How It Works</h3>
            <ol className="list-decimal list-inside space-y-2">
              <li>Collects pre-match statistics for both teams (rolling 5-match averages)</li>
              <li>Analyzes 37 features including offensive power, defensive weakness, form, and league position</li>
              <li>Predicts match liveliness using the trained Elastic Net model</li>
              <li>Ranks all upcoming fixtures by predicted excitement level</li>
            </ol>
          </div>

          <div className="bg-blue-50 p-4 rounded-lg">
            <p className="text-sm text-blue-900">
              <strong>Note:</strong> This model explains 82% of variance in match excitement. The remaining 18% includes unpredictable factors like injuries, tactics, individual brilliance, and luck.
            </p>
          </div>
        </div>

        <div className="mt-8 text-center">
          <button 
            onClick={onClose}
            className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-2 rounded-lg font-medium transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default AboutModal;
