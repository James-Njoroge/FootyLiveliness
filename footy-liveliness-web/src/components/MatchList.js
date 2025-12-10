import React from 'react';
import MatchCard from './MatchCard';

const MatchList = ({ matches }) => {
  return (
    <div>
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Upcoming Fixtures</h2>
        <p className="text-gray-600">Ranked by predicted match liveliness</p>
      </div>

      <div className="space-y-2">
        {matches.map((match, index) => (
          <MatchCard key={match.rank || index} match={match} index={index} />
        ))}
      </div>
    </div>
  );
};

export default MatchList;
