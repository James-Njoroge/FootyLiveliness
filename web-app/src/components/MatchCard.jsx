import React from 'react';
import { Flame, TrendingUp, Shield, Target, Clock, ExternalLink, Calendar } from 'lucide-react';

const MatchCard = ({ match, rank }) => {
  const getLivelinessColor = (score) => {
    if (score >= 5.5) return 'from-yellow-300 to-yellow-400';
    if (score >= 4.5) return 'from-yellow-400 to-green-300';
    if (score >= 3.5) return 'from-green-300 to-green-400';
    return 'from-green-400 to-emerald-500';
  };

  const getLivelinessLabel = (score) => {
    if (score >= 5.5) return '🔥 Very Lively';
    if (score >= 4.5) return '⚡ Exciting';
    if (score >= 3.5) return '✨ Moderate';
    return '😴 Calm';
  };

  const getRankBadge = (rank) => {
    if (rank === 1) return '🥇';
    if (rank === 2) return '🥈';
    if (rank === 3) return '🥉';
    return `#${rank}`;
  };

  const getRankColor = (rank) => {
    if (rank === 1) return 'bg-yellow-400';
    if (rank === 2) return 'bg-silver';
    if (rank === 3) return 'bg-orange-500';
    return 'bg-white/20';
  };

  const handleViewMatch = (e) => {
    e.stopPropagation();
    const url = match.matchUrl || `https://www.fotmob.com/leagues/47/matches/premier-league`;
    window.open(url, '_blank', 'noopener,noreferrer');
  };

  return (
    <div className="bg-gradient-to-br from-green-900/90 to-emerald-950/90 rounded-lg p-4 shadow-lg hover:shadow-xl transition-all duration-300 border border-yellow-500/30 hover:border-yellow-400/50 backdrop-blur-sm">
      {/* Rank Badge */}
      <div className="flex items-center justify-between mb-3">
        {/* Rank Badge */}
        <div className={`text-2xl font-bold px-4 py-2 rounded-lg ${
          rank <= 3 ? 'bg-gradient-to-r from-yellow-400 to-yellow-500 text-green-900' : 'bg-green-800/50 text-white'
        }`}>
          {getRankBadge(rank)}
        </div>

        {/* Liveliness Score */}
        <div className="text-right">
          <div className="text-xs text-white/90 font-medium">Score</div>
          <div className={`bg-gradient-to-r ${getLivelinessColor(match.predictedLiveliness)} bg-clip-text text-transparent text-2xl font-extrabold drop-shadow-lg`}>
            {match.predictedLiveliness.toFixed(1)}
          </div>
          <div className="text-sm text-white font-medium mt-1">
            {getLivelinessLabel(match.predictedLiveliness)}
          </div>
        </div>
      </div>

      {/* Teams */}
      <div className="flex items-center justify-between gap-3 mb-3">
        {/* Home Team */}
        <div className="flex items-center gap-2 flex-1 min-w-0">
          <div className="w-10 h-10 flex-shrink-0 bg-white/10 rounded-full flex items-center justify-center overflow-hidden">
            <img 
              src={`https://images.fotmob.com/image_resources/logo/teamlogo/${match.homeTeamId}_small.png`}
              alt={match.homeTeam}
              className="w-8 h-8 object-contain"
              onError={(e) => {
                e.target.style.display = 'none';
                e.target.parentElement.innerHTML = `<span class="text-white text-xs font-bold">${match.homeTeam.substring(0, 3).toUpperCase()}</span>`;
              }}
            />
          </div>
          <div className="min-w-0 flex-1">
            <div className="font-semibold text-white text-sm truncate">{match.homeTeam}</div>
            <div className="text-xs text-white/80">{match.homeForm}</div>
          </div>
        </div>

        {/* VS Divider */}
        <div className="flex-shrink-0 px-2">
          <div className="text-xl font-bold text-white/50">vs</div>
        </div>

        {/* Away Team */}
        <div className="flex items-center gap-2 flex-1 min-w-0 justify-end">
          <div className="min-w-0 flex-1 text-right">
            <div className="font-semibold text-white text-sm truncate">{match.awayTeam}</div>
            <div className="text-xs text-white/80">{match.awayForm}</div>
          </div>
          <div className="w-10 h-10 flex-shrink-0 bg-white/10 rounded-full flex items-center justify-center overflow-hidden">
            <img 
              src={`https://images.fotmob.com/image_resources/logo/teamlogo/${match.awayTeamId}_small.png`}
              alt={match.awayTeam}
              className="w-8 h-8 object-contain"
              onError={(e) => {
                e.target.style.display = 'none';
                e.target.parentElement.innerHTML = `<span class="text-white text-xs font-bold">${match.awayTeam.substring(0, 3).toUpperCase()}</span>`;
              }}
            />
          </div>
        </div>
      </div>

      {/* Match Details */}
      <div className="grid grid-cols-2 gap-4 mb-4 pt-4 border-t border-white/30">
        <div className="flex items-center gap-1.5 text-xs text-white/90">
          <Calendar className="w-3.5 h-3.5" />
          <span>{match.kickoffTime}</span>
        </div>
        <div className="flex items-center gap-2 text-white/90">
          <Target className="w-4 h-4" />
          <span className="text-sm">Round {match.round}</span>
        </div>
      </div>

      {/* Match Info */}
      <div className="space-y-1.5 mb-3">
        <p className="text-xs text-white/80 font-semibold mb-2">KEY FACTORS:</p>
        
        <div className="flex items-center gap-2 text-sm text-white/95">
          <TrendingUp className="w-4 h-4 text-green-300" />
          <span>Form: {match.homeForm} (H) vs {match.awayForm} (A)</span>
        </div>
        
        <div className="flex items-center gap-2 text-sm text-white/95">
          <Shield className="w-4 h-4 text-blue-300" />
          <span>League Position: {match.homePosition} vs {match.awayPosition}</span>
        </div>
      </div>

      {/* High Stakes Badge */}
      {match.isHighStakes && (
        <div className="flex items-center gap-1.5 text-xs text-yellow-300 font-semibold mb-2">
          <Flame className="w-3.5 h-3.5" />
          <span>High Stakes</span>
        </div>
      )}

      {/* Confidence Indicator */}
      <div className="mt-3 pt-3 border-t border-yellow-500/30">
        <div className="flex items-center justify-between text-xs text-white/90">
          <span title="Based on model R², data quality, and prediction certainty">Confidence</span>
          <span className="font-semibold text-yellow-200">{match.confidence}%</span>
        </div>
        <div className="w-full bg-green-950/50 rounded-full h-1.5 mt-1.5">
          <div 
            className="bg-gradient-to-r from-yellow-400 to-green-400 h-1.5 rounded-full transition-all duration-500"
            style={{ width: `${match.confidence}%` }}
          ></div>
        </div>
      </div>

      {/* View Match Button */}
      <button
        onClick={handleViewMatch}
        className="mt-3 w-full bg-gradient-to-r from-yellow-500 to-green-500 hover:from-yellow-400 hover:to-green-400 text-green-950 font-semibold py-2 px-3 rounded-lg transition-all duration-300 flex items-center justify-center gap-2 group text-sm"
      >
        <span>View Details</span>
        <ExternalLink className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
      </button>
    </div>
  );
};

export default MatchCard;
