import React from 'react';

const Footer = () => {
  return (
    <div className="bg-gray-900 text-white mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* About the Model */}
        <div className="text-center mb-10">
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

        {/* Contributors */}
        <div className="border-t border-gray-800 pt-8 mb-8">
          <h3 className="text-lg font-semibold text-center mb-6">Contributors</h3>
          <div className="grid md:grid-cols-3 gap-6 max-w-4xl mx-auto">
            <div className="text-center">
              <div className="text-purple-400 font-semibold">James Njoroge</div>
              <a 
                href="https://jnjoroge.dev/" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-purple-300 text-xs transition-colors"
              >
                (jnjoroge.dev)
              </a>
              <p className="text-gray-500 text-sm mt-1">Data Collection & Feature Engineering</p>
            </div>
            <div className="text-center">
              <div className="text-purple-400 font-semibold">Muhammad Raka Zuhdi</div>
              <p className="text-gray-500 text-sm mt-1">Model Training & Web Development</p>
            </div>
            <div className="text-center">
              <div className="text-purple-400 font-semibold">Fola Oladipo</div>
              <p className="text-gray-500 text-sm mt-1">Model Evaluation & Documentation</p>
            </div>
          </div>
        </div>

        {/* Course & Acknowledgments */}
        <div className="border-t border-gray-800 pt-8 text-center">
          <p className="text-gray-400 mb-2">
            <span className="font-semibold text-white">CS 506 - Data Science</span>
            <span className="mx-2">•</span>
            Boston University
            <span className="mx-2">•</span>
            Fall 2025
          </p>
          <p className="text-gray-500 text-sm">
            Special thanks to Professor{' '}
            <a 
              href="https://gallettilance.github.io/" 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-purple-400 hover:text-purple-300 transition-colors"
            >
              Lance Galletti
            </a>
          </p>
        </div>

        {/* Copyright */}
        <div className="border-t border-gray-800 mt-8 pt-6 text-center text-gray-500 text-sm">
          <p>© 2025 Footy Liveliness. Built with React, Flask, and scikit-learn.</p>
        </div>
      </div>
    </div>
  );
};

export default Footer;
