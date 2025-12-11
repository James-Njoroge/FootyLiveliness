export const getTeamLogo = (teamName) => {
  const teamLogos = {
    'Arsenal': 'https://images.fotmob.com/image_resources/logo/teamlogo/9825_small.png',
    'Aston Villa': 'https://images.fotmob.com/image_resources/logo/teamlogo/10252_small.png',
    'AFC Bournemouth': 'https://images.fotmob.com/image_resources/logo/teamlogo/8678_small.png',
    'Brentford': 'https://images.fotmob.com/image_resources/logo/teamlogo/9937_small.png',
    'Brighton & Hove Albion': 'https://images.fotmob.com/image_resources/logo/teamlogo/10204_small.png',
    'Brighton': 'https://images.fotmob.com/image_resources/logo/teamlogo/10204_small.png',
    'Chelsea': 'https://images.fotmob.com/image_resources/logo/teamlogo/8455_small.png',
    'Crystal Palace': 'https://images.fotmob.com/image_resources/logo/teamlogo/9826_small.png',
    'Everton': 'https://images.fotmob.com/image_resources/logo/teamlogo/8668_small.png',
    'Fulham': 'https://images.fotmob.com/image_resources/logo/teamlogo/9879_small.png',
    'Ipswich Town': 'https://images.fotmob.com/image_resources/logo/teamlogo/10233_small.png',
    'Leicester City': 'https://images.fotmob.com/image_resources/logo/teamlogo/8197_small.png',
    'Liverpool': 'https://images.fotmob.com/image_resources/logo/teamlogo/8650_small.png',
    'Manchester City': 'https://images.fotmob.com/image_resources/logo/teamlogo/8456_small.png',
    'Manchester United': 'https://images.fotmob.com/image_resources/logo/teamlogo/10260_small.png',
    'Newcastle United': 'https://images.fotmob.com/image_resources/logo/teamlogo/10261_small.png',
    'Nottingham Forest': 'https://images.fotmob.com/image_resources/logo/teamlogo/10203_small.png',
    'Southampton': 'https://images.fotmob.com/image_resources/logo/teamlogo/8466_small.png',
    'Tottenham Hotspur': 'https://images.fotmob.com/image_resources/logo/teamlogo/8586_small.png',
    'Tottenham': 'https://images.fotmob.com/image_resources/logo/teamlogo/8586_small.png',
    'West Ham United': 'https://images.fotmob.com/image_resources/logo/teamlogo/8654_small.png',
    'West Ham': 'https://images.fotmob.com/image_resources/logo/teamlogo/8654_small.png',
    'Wolverhampton Wanderers': 'https://images.fotmob.com/image_resources/logo/teamlogo/8602_small.png',
    'Wolves': 'https://images.fotmob.com/image_resources/logo/teamlogo/8602_small.png'
  };
  
  return teamLogos[teamName] || '';
};
