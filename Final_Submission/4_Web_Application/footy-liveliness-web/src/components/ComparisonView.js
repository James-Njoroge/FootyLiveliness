import React from 'react';
import { getTeamLogo } from '../utils/teamLogos';

const ComparisonView = ({ matches }) => {
  // Filter only finished matches with actual xG data
  const finishedMatches = matches.filter(
    match => match.status === 'finished' && match.actualXG && match.actualXG.simple_xg
  );

  if (finishedMatches.length === 0) {
    return (
      <div className="bg-yellow-50 border-l-4 border-yellow-500 p-6 rounded-lg">
        <p className="text-yellow-800 font-medium">
          ⏰ No finished matches with actual data for this week
        </p>
        <p className="text-yellow-600 text-sm mt-2">
          Navigate to past weeks (August-December) to see predicted vs actual comparisons
        </p>
      </div>
    );
  }

  // Create two lists: sorted by predicted vs sorted by actual
  const predictedRanking = [...finishedMatches].sort(
    (a, b) => b.predicted_liveliness - a.predicted_liveliness
  );

  const actualRanking = [...finishedMatches].sort(
    (a, b) => b.actualXG.simple_xg - a.actualXG.simple_xg
  );

  // Calculate overall accuracy
  const accuracies = finishedMatches.map(match => {
    const predicted = match.predicted_liveliness;
    const actual = match.actualXG.simple_xg;
    const diff = Math.abs(predicted - actual);
    const percentDiff = (diff / actual) * 100;
    return 100 - Math.min(100, percentDiff);
  });
  const avgAccuracy = accuracies.reduce((a, b) => a + b, 0) / accuracies.length;

  const MatchRow = ({ match, rank, showActual = false }) => {
    const predicted = match.predicted_liveliness;
    const actual = match.actualXG.simple_xg;
    const diff = Math.abs(predicted - actual);
    const percentDiff = (diff / actual) * 100;
    const accuracy = 100 - Math.min(100, percentDiff);

    let accuracyColor = '';
    if (accuracy >= 90) accuracyColor = 'text-green-600 bg-green-50';
    else if (accuracy >= 75) accuracyColor = 'text-blue-600 bg-blue-50';
    else if (accuracy >= 60) accuracyColor = 'text-yellow-600 bg-yellow-50';
    else accuracyColor = 'text-red-600 bg-red-50';

    const score = showActual ? actual : predicted;
    const barColor = showActual ? 'from-green-500 to-emerald-500' : 'from-purple-500 to-pink-500';

    return (
      <div className="flex items-center gap-3 p-3 bg-white rounded-lg hover:shadow-md transition-shadow">
        {/* Rank */}
        <div className="text-lg font-bold text-gray-400 min-w-[40px]">
          #{rank}
        </div>

        {/* Teams */}
        <div className="flex items-center gap-2 flex-1 min-w-0">
          <img 
            src={getTeamLogo(match.home)} 
            alt={match.home} 
            className="w-6 h-6 object-contain flex-shrink-0"
            onError={(e) => e.target.style.display = 'none'}
          />
          <div className="text-sm font-semibold text-gray-900 truncate">
            {match.home}
          </div>
          <div className="text-xs text-gray-400 flex-shrink-0">vs</div>
          <img 
            src={getTeamLogo(match.away)} 
            alt={match.away} 
            className="w-6 h-6 object-contain flex-shrink-0"
            onError={(e) => e.target.style.display = 'none'}
          />
          <div className="text-sm font-semibold text-gray-900 truncate">
            {match.away}
          </div>
        </div>

        {/* Score Bar */}
        <div className="flex items-center gap-2 min-w-[120px]">
          <div className="flex-1">
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className={`bg-gradient-to-r ${barColor} h-2 rounded-full transition-all duration-500`}
                style={{ width: `${Math.min(100, (score / 8) * 100)}%` }}
              />
            </div>
          </div>
          <div className={`text-sm font-bold min-w-[45px] text-right ${showActual ? 'text-green-600' : 'text-purple-600'}`}>
            {score.toFixed(2)}
          </div>
        </div>

        {/* Accuracy Badge */}
        <div className={`px-3 py-1 rounded-full text-xs font-bold ${accuracyColor} min-w-[60px] text-center`}>
          {accuracy.toFixed(0)}%
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-6">
      {/* Summary Stats */}
      <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg p-6 border border-purple-200">
        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <div className="text-3xl font-bold text-purple-600">{finishedMatches.length}</div>
            <div className="text-sm text-gray-600">Matches Analyzed</div>
          </div>
          <div>
            <div className="text-3xl font-bold text-blue-600">{avgAccuracy.toFixed(1)}%</div>
            <div className="text-sm text-gray-600">Average Accuracy</div>
          </div>
          <div>
            <div className="text-3xl font-bold text-green-600">
              {accuracies.filter(a => a >= 75).length}
            </div>
            <div className="text-sm text-gray-600">Good Predictions (75%+)</div>
          </div>
        </div>
      </div>

      {/* Side by Side Comparison */}
      <div className="grid grid-cols-2 gap-6">
        {/* Predicted Ranking */}
        <div>
          <div className="mb-4">
            <h3 className="text-xl font-bold text-purple-600 flex items-center gap-2">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
              </svg>
              Predicted Ranking
            </h3>
            <p className="text-sm text-gray-600">Sorted by model predictions</p>
          </div>
          <div className="space-y-2">
            {predictedRanking.map((match, index) => (
              <MatchRow key={`pred-${match.matchId}`} match={match} rank={index + 1} showActual={false} />
            ))}
          </div>
        </div>

        {/* Actual Ranking */}
        <div>
          <div className="mb-4">
            <h3 className="text-xl font-bold text-green-600 flex items-center gap-2">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              Actual Ranking
            </h3>
            <p className="text-sm text-gray-600">Sorted by actual liveliness</p>
          </div>
          <div className="space-y-2">
            {actualRanking.map((match, index) => (
              <MatchRow key={`actual-${match.matchId}`} match={match} rank={index + 1} showActual={true} />
            ))}
          </div>
        </div>
      </div>

      {/* Legend */}
      <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
        <h4 className="text-sm font-bold text-gray-700 mb-2">Accuracy Legend:</h4>
        <div className="flex flex-wrap gap-4 text-xs">
          <div className="flex items-center gap-2">
            <div className="w-12 h-6 bg-green-50 border border-green-200 rounded flex items-center justify-center text-green-600 font-bold">90%+</div>
            <span className="text-gray-600">Excellent</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-12 h-6 bg-blue-50 border border-blue-200 rounded flex items-center justify-center text-blue-600 font-bold">75%+</div>
            <span className="text-gray-600">Good</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-12 h-6 bg-yellow-50 border border-yellow-200 rounded flex items-center justify-center text-yellow-600 font-bold">60%+</div>
            <span className="text-gray-600">Fair</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-12 h-6 bg-red-50 border border-red-200 rounded flex items-center justify-center text-red-600 font-bold">&lt;60%</div>
            <span className="text-gray-600">Poor</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ComparisonView;
