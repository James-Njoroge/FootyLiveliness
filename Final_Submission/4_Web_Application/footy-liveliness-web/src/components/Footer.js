import React from 'react';

const Footer = () => {
  return (
    <div className="bg-gray-900 text-white mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center">
          <h3 className="text-lg font-semibold mb-4">About the Model</h3>
          <p className="text-gray-400 max-w-3xl mx-auto mb-6">
            This AI model predicts match liveliness using the "Simple xG" metric 
            (total xG + minimum xG between teams). Trained using 2024/25 Premier League season data 
            with 37 pre-match features including team form, attacking strength, and defensive stats.
          </p>
          <div className="flex justify-center space-x-8 text-sm text-gray-500">
            <div>Model: <span className="text-purple-400">Elastic Net</span></div>
            <div>R²: <span className="text-purple-400">0.82</span></div>
            <div>MAE: <span className="text-purple-400">0.45</span></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Footer;
