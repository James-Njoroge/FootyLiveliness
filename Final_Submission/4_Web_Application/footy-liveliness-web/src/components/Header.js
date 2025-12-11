import React from 'react';

const Header = ({ onAboutClick, onProjectDetailsClick, onGettingStartedClick, onArchitectureClick }) => {
  return (
    <div className="bg-gradient-to-r from-purple-600 to-purple-800 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Buttons Row */}
        <div className="flex justify-end gap-2 mb-8 flex-wrap">
          <button 
            onClick={onGettingStartedClick}
            className="bg-white bg-opacity-20 hover:bg-opacity-30 text-white px-4 py-2 rounded-lg font-medium transition-all duration-200 flex items-center gap-2 text-sm"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
            </svg>
            Getting Started
          </button>
          <button 
            onClick={onAboutClick}
            className="bg-white bg-opacity-20 hover:bg-opacity-30 text-white px-4 py-2 rounded-lg font-medium transition-all duration-200 flex items-center gap-2 text-sm"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            About
          </button>
          <button 
            onClick={onArchitectureClick}
            className="bg-white bg-opacity-20 hover:bg-opacity-30 text-white px-4 py-2 rounded-lg font-medium transition-all duration-200 flex items-center gap-2 text-sm"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z"></path>
            </svg>
            Architecture
          </button>
          <button 
            onClick={onProjectDetailsClick}
            className="bg-white bg-opacity-20 hover:bg-opacity-30 text-white px-4 py-2 rounded-lg font-medium transition-all duration-200 flex items-center gap-2 text-sm"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
            Project Details
          </button>
        </div>

        {/* Title Section */}
        <div className="text-center">
          <div className="flex items-center justify-center gap-3 mb-4">
            <svg className="w-12 h-12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
              <circle cx="12" cy="12" r="10" fill="white" stroke="currentColor" strokeWidth="1.5"/>
              <path d="M12 2 L12 6 M12 18 L12 22 M2 12 L6 12 M18 12 L22 12" stroke="currentColor" strokeWidth="1.5"/>
              <path d="M12 6 L8 10 L4 8 M12 6 L16 10 L20 8" stroke="currentColor" strokeWidth="1.5" fill="none"/>
              <path d="M8 10 L10 14 L12 18 M16 10 L14 14 L12 18" stroke="currentColor" strokeWidth="1.5" fill="none"/>
              <path d="M4 8 L6 12 L10 14 M20 8 L18 12 L14 14" stroke="currentColor" strokeWidth="1.5" fill="none"/>
            </svg>
            <h1 className="text-5xl font-bold">Footy Liveliness</h1>
          </div>
          <p className="text-xl text-purple-100 mb-2">AI-Powered Premier League Match Rankings</p>
          <p className="text-sm text-purple-200">Predicting the most exciting matches to watch</p>
        </div>
      </div>
    </div>
  );
};

export default Header;
