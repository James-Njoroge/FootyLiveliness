import React, { useState, useEffect } from 'react';
import { Flame, TrendingUp, Info, Calendar, Trophy, Activity, AlertCircle, ChevronDown } from 'lucide-react';
import MatchCard from './components/MatchCard';
import ModelInfo from './components/ModelInfo';
import { predictMatches, upcomingMatches } from './utils/predictor';
import { api } from './utils/api';

function App() {
  const [matches, setMatches] = useState([]);
  const [showInfo, setShowInfo] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [useBackend, setUseBackend] = useState(false);
  const [apiStatus, setApiStatus] = useState('checking');
  const [selectedRound, setSelectedRound] = useState('all');
  const [selectedTeam, setSelectedTeam] = useState('all');

  useEffect(() => {
    checkAPIAndLoadMatches();
  }, []);

  async function checkAPIAndLoadMatches() {
    try {
      // Try to connect to backend API
      await api.healthCheck();
      setApiStatus('connected');
      setUseBackend(true);
      await loadMatchesFromAPI();
    } catch (err) {
      // Fallback to client-side predictions
      console.warn('Backend API not available, using client-side predictions');
      setApiStatus('offline');
      setUseBackend(false);
      loadMatchesClientSide();
    }
  }

  async function loadMatchesFromAPI() {
    try {
      setLoading(true);
      setError(null);
      const response = await api.predictBatch(upcomingMatches);
      setMatches(response.predictions);
    } catch (err) {
      setError('Failed to load predictions from server');
      console.error(err);
      // Fallback to client-side
      loadMatchesClientSide();
    } finally {
      setLoading(false);
    }
  }

  function loadMatchesClientSide() {
    setTimeout(() => {
      const predictions = predictMatches(upcomingMatches);
      setMatches(predictions);
      setLoading(false);
    }, 1000);
  }

  // Get unique rounds and teams for filters
  const rounds = [...new Set(matches.map(m => m.round))].sort((a, b) => a - b);
  const allTeams = [...new Set(matches.flatMap(m => [m.homeTeam, m.awayTeam]))].sort();
  
  // Filter matches by selected round and team
  let filteredMatches = matches;
  
  if (selectedRound !== 'all') {
    filteredMatches = filteredMatches.filter(m => m.round === parseInt(selectedRound));
  }
  
  if (selectedTeam !== 'all') {
    filteredMatches = filteredMatches.filter(m => 
      m.homeTeam === selectedTeam || m.awayTeam === selectedTeam
    );
  }
  
  // Group matches by round
  const matchesByRound = matches.reduce((acc, match) => {
    if (!acc[match.round]) {
      acc[match.round] = [];
    }
    acc[match.round].push(match);
    return acc;
  }, {});

  const topMatch = filteredMatches[0];
  const avgLiveliness = filteredMatches.length > 0 
    ? (filteredMatches.reduce((sum, m) => sum + m.predictedLiveliness, 0) / filteredMatches.length).toFixed(2)
    : 0;

  return (
    <div className="min-h-screen football-field py-8 px-4">
      <div className="max-w-7xl mx-auto relative z-10">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center gap-4 mb-4">
            <Flame className="w-16 h-16 text-yellow-400 animate-pulse" />
            <h1 className="text-6xl font-bold bg-gradient-to-r from-yellow-300 via-green-400 to-emerald-300 bg-clip-text text-transparent">
              Footy Liveliness
            </h1>
            <Trophy className="w-16 h-16 text-yellow-400" />
          </div>
          <p className="text-xl text-white/80 mb-2">
            AI-Powered Premier League Match Excitement Predictor
          </p>
          <p className="text-sm text-white/60">
            Powered by Ridge Regression ML Model (R² = 0.088, 67% recommendation accuracy)
          </p>
          
          <button
            onClick={() => setShowInfo(true)}
            className="bg-yellow-500/20 hover:bg-yellow-500/30 text-white px-6 py-3 rounded-lg transition-all duration-300 flex items-center gap-2 mx-auto backdrop-blur-sm border border-yellow-400/30"
          >
            <Info className="w-5 h-5" />
            <span>How It Works</span>
          </button>
        </div>

        {/* API Status Banner */}
        {apiStatus === 'offline' && (
          <div className="mb-6 glass-effect rounded-lg p-4 border-l-4 border-yellow-400">
            <div className="flex items-center gap-3 text-white">
              <AlertCircle className="w-5 h-5 text-yellow-400" />
              <div>
                <p className="font-semibold">Running in Demo Mode</p>
                <p className="text-sm text-white/80">
                  Backend API not available. Using client-side predictions with simplified model.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="mb-6 glass-effect rounded-lg p-4 border-l-4 border-red-400">
            <div className="flex items-center gap-3 text-white">
              <AlertCircle className="w-5 h-5 text-red-400" />
              <p>{error}</p>
            </div>
          </div>
        )}

        {/* Model Info Modal */}
        {showInfo && <ModelInfo onClose={() => setShowInfo(false)} apiStatus={apiStatus} />}

        {/* Filters */}
        <div className="mb-8">
          <div className="glass-effect rounded-xl p-6">
            <div className="flex items-center gap-4 flex-wrap">
              {/* Round Filter */}
              <div className="flex items-center gap-2">
                <ChevronDown className="w-5 h-5 text-yellow-400" />
                <label className="text-white font-semibold">Round:</label>
              </div>
              
              <select
                value={selectedRound}
                onChange={(e) => setSelectedRound(e.target.value)}
                className="bg-green-900/50 text-white px-4 py-2 rounded-lg border border-yellow-500/30 focus:border-yellow-400 focus:outline-none backdrop-blur-sm"
              >
                <option value="all">All Rounds</option>
                {rounds.map(round => (
                  <option key={round} value={round} className="bg-green-900">Round {round}</option>
                ))}
              </select>

              {/* Team Filter */}
              <div className="flex items-center gap-2 ml-4">
                <Trophy className="w-5 h-5 text-yellow-400" />
                <label className="text-white font-semibold">Team:</label>
              </div>
              
              <select
                value={selectedTeam}
                onChange={(e) => setSelectedTeam(e.target.value)}
                className="bg-green-900/50 text-white px-4 py-2 rounded-lg border border-yellow-500/30 focus:border-yellow-400 focus:outline-none backdrop-blur-sm min-w-[200px]"
              >
                <option value="all">All Teams</option>
                {allTeams.map(team => (
                  <option key={team} value={team} className="bg-green-900">{team}</option>
                ))}
              </select>

              {/* Clear Filters */}
              {(selectedRound !== 'all' || selectedTeam !== 'all') && (
                <button
                  onClick={() => {
                    setSelectedRound('all');
                    setSelectedTeam('all');
                  }}
                  className="bg-yellow-500/20 hover:bg-yellow-500/30 text-yellow-200 px-4 py-2 rounded-lg transition-colors border border-yellow-400/30 ml-auto"
                >
                  Clear Filter
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="glass-effect rounded-xl p-6 text-white">
            <div className="flex items-center gap-3 mb-2">
              <Trophy className="w-6 h-6 text-yellow-300" />
              <h3 className="text-lg font-semibold">Top Match</h3>
            </div>
            {topMatch ? (
              <div>
                <p className="text-2xl font-bold">
                  {topMatch.homeTeam} vs {topMatch.awayTeam}
                </p>
                <p className="text-sm text-white/60 mt-1">Round {topMatch.round}</p>
              </div>
            ) : (
              <p className="text-gray-300">Loading...</p>
            )}
          </div>

          <div className="glass-effect rounded-xl p-6 text-white">
            <div className="flex items-center gap-3 mb-2">
              <Activity className="w-6 h-6 text-green-400" />
              <h3 className="text-lg font-semibold">Avg Liveliness</h3>
            </div>
            <p className="text-2xl font-bold">{avgLiveliness} / 10</p>
            <p className="text-sm text-white/60 mt-1">
              {selectedRound === 'all' && selectedTeam === 'all' 
                ? 'All matches' 
                : selectedRound !== 'all' && selectedTeam !== 'all'
                ? `Round ${selectedRound} • ${selectedTeam}`
                : selectedRound !== 'all' 
                ? `Round ${selectedRound}` 
                : selectedTeam}
            </p>
          </div>

          <div className="glass-effect rounded-xl p-6 text-white">
            <div className="flex items-center gap-3 mb-2">
              <Calendar className="w-6 h-6 text-blue-400" />
              <h3 className="text-lg font-semibold">
                {selectedRound === 'all' ? 'Total Matches' : 'Matches in Round'}
              </h3>
            </div>
            <p className="text-2xl font-bold">{filteredMatches.length}</p>
            <p className="text-sm text-white/60 mt-1">
              {selectedRound === 'all' ? `${rounds.length} rounds` : `of ${matches.length} total`}
            </p>
          </div>
        </div>

        {/* Match Rankings */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-6">
            <TrendingUp className="w-8 h-8 text-white" />
            <h2 className="text-3xl font-bold text-white">
              {selectedRound === 'all' && selectedTeam === 'all'
                ? 'Match Rankings - All Matches'
                : selectedRound !== 'all' && selectedTeam !== 'all'
                ? `Match Rankings - Round ${selectedRound} • ${selectedTeam}`
                : selectedRound !== 'all'
                ? `Match Rankings - Round ${selectedRound}`
                : `Match Rankings - ${selectedTeam}`}
            </h2>
          </div>

          {loading ? (
            <div className="text-center py-12">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-white/30 border-t-white"></div>
              <p className="text-white mt-4">Analyzing matches...</p>
            </div>
          ) : filteredMatches.length === 0 ? (
            <div className="text-center py-12 glass-effect rounded-xl">
              <Calendar className="w-16 h-16 text-white/40 mx-auto mb-4" />
              <p className="text-white text-xl">No matches found for this round</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {filteredMatches.map((match, index) => (
                <MatchCard key={match.id} match={match} rank={index + 1} />
              ))}
            </div>
          )}
        </div>

        {/* Footer */}
        <footer className="text-center text-white/60 text-sm mt-12 pb-8">
          <p>
            Built with React + TailwindCSS | Data from FotMob | 
            <a 
              href="https://github.com" 
              className="text-white/80 hover:text-white ml-1 underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              View on GitHub
            </a>
          </p>
          <p className="mt-2">
            CS 506 - Data Science | Boston University | Fall 2025
          </p>
        </footer>
      </div>
    </div>
  );
}

export default App;
