import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import StatsBar from './components/StatsBar';
import MatchList from './components/MatchList';
import AboutModal from './components/AboutModal';
import ProjectDetailsModal from './components/ProjectDetailsModal';
import ArchitectureDiagram from './components/ArchitectureDiagram';
import GettingStartedModal from './components/GettingStartedModal';
import Footer from './components/Footer';
import { fetchUpcomingMatches } from './services/api';

function App() {
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [showAboutModal, setShowAboutModal] = useState(false);
  const [showProjectDetailsModal, setShowProjectDetailsModal] = useState(false);
  const [showArchitectureDiagram, setShowArchitectureDiagram] = useState(false);
  const [showGettingStarted, setShowGettingStarted] = useState(false);

  useEffect(() => {
    loadMatches();
    
    // Refresh every 5 minutes
    const interval = setInterval(loadMatches, 5 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  const loadMatches = async () => {
    try {
      setLoading(true);
      setError(false);
      const data = await fetchUpcomingMatches();
      setMatches(data);
    } catch (err) {
      console.error('Error loading matches:', err);
      setError(true);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-gray-50 min-h-screen">
      <Header 
        onAboutClick={() => setShowAboutModal(true)}
        onProjectDetailsClick={() => setShowProjectDetailsModal(true)}
        onGettingStartedClick={() => setShowGettingStarted(true)}
        onArchitectureClick={() => setShowArchitectureDiagram(true)}
      />
      <StatsBar />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {loading && (
          <div className="text-center py-20">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-lime-600"></div>
            <p className="mt-4 text-gray-600">Loading upcoming fixtures...</p>
          </div>
        )}

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
            <p className="text-red-600 font-medium">Failed to load predictions</p>
            <p className="text-red-500 text-sm mt-2">Make sure the API server is running on http://localhost:5001</p>
          </div>
        )}

        {!loading && !error && <MatchList matches={matches} />}
      </div>

      <Footer />
      
      {showAboutModal && (
        <AboutModal onClose={() => setShowAboutModal(false)} />
      )}

      {showProjectDetailsModal && (
        <ProjectDetailsModal 
          onClose={() => setShowProjectDetailsModal(false)}
        />
      )}

      {showArchitectureDiagram && (
        <ArchitectureDiagram onClose={() => setShowArchitectureDiagram(false)} />
      )}

      {showGettingStarted && (
        <GettingStartedModal onClose={() => setShowGettingStarted(false)} />
      )}
    </div>
  );
}

export default App;
