import React, { useState } from 'react';
import MatchCard from './MatchCard';
import ComparisonView from './ComparisonView';

const MatchList = ({ matches }) => {
  const [weekOffset, setWeekOffset] = useState(0); // 0 = current week, 1 = next week, -1 = last week
  const [viewMode, setViewMode] = useState('normal'); // 'normal' or 'comparison'

  // Get week's date range (Sunday to Saturday) with offset
  const getWeekRange = (offset = 0) => {
    const today = new Date();
    const currentDay = today.getDay(); // 0 = Sunday, 6 = Saturday
    
    // Start of current week (last Sunday or today if Sunday)
    const weekStart = new Date(today);
    weekStart.setDate(today.getDate() - currentDay + (offset * 7));
    weekStart.setHours(0, 0, 0, 0);
    
    // End of current week (next Saturday)
    const weekEnd = new Date(weekStart);
    weekEnd.setDate(weekStart.getDate() + 6);
    weekEnd.setHours(23, 59, 59, 999);
    
    return { weekStart, weekEnd };
  };

  const { weekStart, weekEnd } = getWeekRange(weekOffset);

  // Filter matches to only show this week's fixtures
  const thisWeekMatches = matches.filter(match => {
    const matchDate = new Date(match.date);
    return matchDate >= weekStart && matchDate <= weekEnd;
  });

  // Format date range for display
  const formatDateRange = () => {
    const options = { month: 'short', day: 'numeric' };
    const startStr = weekStart.toLocaleDateString('en-US', options);
    const endStr = weekEnd.toLocaleDateString('en-US', options);
    return `${startStr} - ${endStr}`;
  };

  // Check if there are matches in previous/next weeks
  const hasPreviousWeek = () => {
    const { weekStart } = getWeekRange(weekOffset - 1);
    return matches.some(match => {
      const matchDate = new Date(match.date);
      const { weekStart: prevStart, weekEnd: prevEnd } = getWeekRange(weekOffset - 1);
      return matchDate >= prevStart && matchDate <= prevEnd;
    });
  };

  const hasNextWeek = () => {
    const { weekStart } = getWeekRange(weekOffset + 1);
    return matches.some(match => {
      const matchDate = new Date(match.date);
      const { weekStart: nextStart, weekEnd: nextEnd } = getWeekRange(weekOffset + 1);
      return matchDate >= nextStart && matchDate <= nextEnd;
    });
  };

  const getWeekTitle = () => {
    if (weekOffset === 0) return "This Week's Fixtures";
    if (weekOffset === 1) return "Next Week's Fixtures";
    if (weekOffset === -1) return "Last Week's Fixtures";
    if (weekOffset > 1) return `${weekOffset} Weeks Ahead`;
    return `${Math.abs(weekOffset)} Weeks Ago`;
  };

  // Check if this week has finished matches with actual data
  const hasFinishedMatches = thisWeekMatches.some(
    match => match.status === 'finished' && match.actualXG && match.actualXG.simple_xg
  );

  return (
    <div>
      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-3xl font-bold text-gray-900">{getWeekTitle()}</h2>
          
          {/* Week Navigation Buttons */}
          <div className="flex items-center gap-3">
            <button
              onClick={() => setWeekOffset(weekOffset - 1)}
              disabled={!hasPreviousWeek()}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all ${
                hasPreviousWeek()
                  ? 'bg-purple-600 hover:bg-purple-700 text-white shadow-md hover:shadow-lg'
                  : 'bg-gray-200 text-gray-400 cursor-not-allowed'
              }`}
              title="Previous week"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 19l-7-7 7-7"></path>
              </svg>
              Previous
            </button>

            {weekOffset !== 0 && (
              <button
                onClick={() => setWeekOffset(0)}
                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-all shadow-md hover:shadow-lg"
              >
                This Week
              </button>
            )}

            <button
              onClick={() => setWeekOffset(weekOffset + 1)}
              disabled={!hasNextWeek()}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all ${
                hasNextWeek()
                  ? 'bg-purple-600 hover:bg-purple-700 text-white shadow-md hover:shadow-lg'
                  : 'bg-gray-200 text-gray-400 cursor-not-allowed'
              }`}
              title="Next week"
            >
              Next
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7"></path>
              </svg>
            </button>
          </div>
        </div>
        
        <div className="flex items-center justify-between">
          <p className="text-gray-600">
            {formatDateRange()} • {thisWeekMatches.length} matches • Ranked by predicted liveliness
          </p>
          
          {/* View Mode Toggle (only show for weeks with finished matches) */}
          {hasFinishedMatches && (
            <div className="flex items-center gap-2 bg-gray-100 rounded-lg p-1">
              <button
                onClick={() => setViewMode('normal')}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-all ${
                  viewMode === 'normal'
                    ? 'bg-white text-purple-600 shadow-sm'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                📊 Normal View
              </button>
              <button
                onClick={() => setViewMode('comparison')}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-all ${
                  viewMode === 'comparison'
                    ? 'bg-white text-green-600 shadow-sm'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                ⚖️ Comparison View
              </button>
            </div>
          )}
        </div>
      </div>

      {thisWeekMatches.length > 0 ? (
        viewMode === 'comparison' && hasFinishedMatches ? (
          <ComparisonView matches={thisWeekMatches} />
        ) : (
          <div className="space-y-2">
            {thisWeekMatches.map((match, index) => {
              // Create a new match object with updated rank for this week
              const weekMatch = {
                ...match,
                rank: index + 1  // Rank within this week (1, 2, 3...)
              };
              return <MatchCard key={match.rank || index} match={weekMatch} index={index} />;
            })}
          </div>
        )
      ) : (
        <div className="bg-blue-50 border-l-4 border-blue-500 p-6 rounded-lg">
          <p className="text-blue-800 font-medium">
            📅 No matches scheduled for this week ({formatDateRange()})
          </p>
          <p className="text-blue-600 text-sm mt-2">
            Check back later or view all upcoming fixtures in the API.
          </p>
        </div>
      )}
    </div>
  );
};

export default MatchList;
