import React from 'react';
import { getTeamLogo } from '../utils/teamLogos';

const MatchCard = ({ match, index }) => {
  const livelinessScore = match.predicted_liveliness;
  const livelinessPercent = Math.min(100, (livelinessScore / 8) * 100);

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

        {/* Liveliness Score */}
        <div className="flex items-center gap-3 min-w-[140px]">
          <div className="flex-1">
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-gradient-to-r from-purple-500 to-pink-500 h-2 rounded-full transition-all duration-500"
                style={{ width: `${livelinessPercent}%` }}
              />
            </div>
          </div>
          <div className="text-base font-bold text-purple-600 min-w-[60px] text-right">
            {livelinessScore.toFixed(4)}
          </div>
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
