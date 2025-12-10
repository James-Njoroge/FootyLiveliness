import pickle

# Load team stats
with open('team_stats.pkl', 'rb') as f:
    team_stats = pickle.load(f)

print(f"Total teams: {len(team_stats)}")
print(f"\nTeams: {list(team_stats.keys())}")

# Show Liverpool's stats as example
if 'Liverpool' in team_stats:
    liverpool = team_stats['Liverpool']
    print(f"\nLiverpool has {len(liverpool)} features:")
    print("\nFirst 15 features:")
    for i, (k, v) in enumerate(list(liverpool.items())[:15]):
        print(f"  {k}: {v}")
