import React from 'react';
import { getTeamLogo } from '../utils/teamLogos';

const MatchCard = ({ match, index }) => {
  const livelinessScore = match.predicted_liveliness;
  const livelinessPercent = Math.min(100, (livelinessScore / 8) * 100);
  
  // Check if match is finished and has actual data
  const isFinished = match.status === 'finished';
  const hasActualData = match.actualXG && match.actualXG.simple_xg;
  const actualLiveliness = hasActualData ? match.actualXG.simple_xg : null;
  
  // Calculate accuracy if we have actual data
  let accuracy = null;
  let accuracyColor = '';
  if (actualLiveliness !== null) {
    const diff = Math.abs(livelinessScore - actualLiveliness);
    const percentDiff = (diff / actualLiveliness) * 100;
    accuracy = 100 - Math.min(100, percentDiff);
    
    if (accuracy >= 90) accuracyColor = 'text-green-600';
    else if (accuracy >= 75) accuracyColor = 'text-blue-600';
    else if (accuracy >= 60) accuracyColor = 'text-yellow-600';
    else accuracyColor = 'text-red-600';
  }

  let rankBadge = '';
  let rankClass = '';
  
  if (index === 0) {
    rankBadge = <span className="fire-icon text-lg">🔥</span>;
    rankClass = 'text-red-600';
  } else if (index === 1) {
    rankBadge = <span className="text-lg">⭐</span>;
    rankClass = 'text-orange-600';
  } else if (index === 2) {
    rankBadge = <span className="text-lg">✨</span>;
    rankClass = 'text-yellow-600';
  }

  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    const options = { weekday: 'short', month: 'short', day: 'numeric' };
    return date.toLocaleDateString('en-US', options);
  };

  // Generate FotMob URL if matchId is available
  const fotmobUrl = match.matchId ? `https://www.fotmob.com/match/${match.matchId}` : null;

  return (
    <div className="bg-white rounded-lg shadow-md p-4 hover:shadow-lg transition-all duration-300 hover:-translate-y-1">
      <div className="flex items-center justify-between gap-4">
        {/* Rank & Badge */}
        <div className="flex items-center gap-2 min-w-[60px]">
          <div className={`text-xl font-bold ${rankClass || 'text-gray-400'}`}>
            #{match.rank}
          </div>
          {rankBadge}
        </div>

        {/* Teams */}
        <div className="flex items-center justify-center flex-1 gap-3">
          <div className="flex items-center justify-end gap-2 flex-1">
            <div className="text-base font-bold text-gray-900 text-right truncate">
              {match.home}
            </div>
            <img 
              src={getTeamLogo(match.home)} 
              alt={match.home} 
              className="w-7 h-7 object-contain"
              onError={(e) => e.target.style.display = 'none'}
            />
          </div>
          <div className="text-lg font-bold text-gray-400 px-2">vs</div>
          <div className="flex items-center justify-start gap-2 flex-1">
            <img 
              src={getTeamLogo(match.away)} 
              alt={match.away} 
              className="w-7 h-7 object-contain"
              onError={(e) => e.target.style.display = 'none'}
            />
            <div className="text-base font-bold text-gray-900 text-left truncate">
              {match.away}
            </div>
          </div>
        </div>

        {/* Liveliness Score - Show Predicted vs Actual for finished matches */}
        <div className="flex flex-col gap-2 min-w-[200px]">
          {/* Predicted Score */}
          <div className="flex items-center gap-3">
            <div className="text-xs text-gray-500 w-16">Predicted:</div>
            <div className="flex-1">
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-gradient-to-r from-purple-500 to-pink-500 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${livelinessPercent}%` }}
                />
              </div>
            </div>
            <div className="text-sm font-bold text-purple-600 min-w-[50px] text-right">
              {livelinessScore.toFixed(2)}
            </div>
          </div>
          
          {/* Actual Score (if finished) */}
          {isFinished && hasActualData && (
            <div className="flex items-center gap-3">
              <div className="text-xs text-gray-500 w-16">Actual:</div>
              <div className="flex-1">
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-gradient-to-r from-green-500 to-emerald-500 h-2 rounded-full transition-all duration-500"
                    style={{ width: `${Math.min(100, (actualLiveliness / 8) * 100)}%` }}
                  />
                </div>
              </div>
              <div className="text-sm font-bold text-green-600 min-w-[50px] text-right">
                {actualLiveliness.toFixed(2)}
              </div>
            </div>
          )}
          
          {/* Accuracy Badge (if finished) */}
          {isFinished && hasActualData && accuracy !== null && (
            <div className="flex items-center gap-2 justify-end">
              <span className="text-xs text-gray-500">Accuracy:</span>
              <span className={`text-xs font-bold ${accuracyColor}`}>
                {accuracy.toFixed(0)}%
              </span>
            </div>
          )}
        </div>

        {/* Date & Time */}
        <div className="text-right min-w-[100px]">
          <div className="text-xs text-gray-500">{formatDate(match.date)}</div>
          <div className="text-xs font-medium text-gray-700">{match.time}</div>
        </div>

        {/* FotMob Link Button */}
        {fotmobUrl && (
          <div className="min-w-[100px]">
            <a
              href={fotmobUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors shadow-sm hover:shadow-md"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path>
              </svg>
              Details
            </a>
          </div>
        )}
      </div>
    </div>
  );
};

export default MatchCard;
