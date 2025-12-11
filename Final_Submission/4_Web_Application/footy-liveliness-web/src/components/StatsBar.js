import React from 'react';

const StatsBar = () => {
  const stats = [
    { value: '82%', label: 'Prediction Accuracy' },
    { value: 'Elastic Net', label: 'ML Model' },
    { value: 'Trained on 24/25', label: 'Season Data' }
  ];

  return (
    <div className="bg-white border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {stats.map((stat, index) => (
            <div key={index} className="text-center">
              <div className="text-3xl font-bold text-lime-600">{stat.value}</div>
              <div className="text-sm text-gray-600 mt-1">{stat.label}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default StatsBar;
