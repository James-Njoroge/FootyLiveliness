# 24-25_PL_Data

Detailed documentation for the 2024/25 Premier League dataset used by this project.

## Overview

- **Location**: `data/14-25_PL_Data_raw/` (Obtained from unzipping `data/24-25_PL_Data_raw.zip`)
- **Source**: Scraped from FotMob public endpoints (see project notebooks and scripts in `data/`).
- **Purpose**: Provide full match-level details for all fixtures in the 2024/25 season to support modeling and analysis of match liveliness.

## Structure

- **`index.json`**: Manifest listing each round and its 10 matches with fields:
  - `round` (0-based)
  - `matches`: `{ matchId, matchUrl, home, away, jsonPath }`
- **`round_0` … `round_37`**: 38 folders, one per Premier League round.
  - Note: Folders are 0-indexed, i.e., `round_0` corresponds to Round 1, `round_37` to Round 38.
  - Each folder contains 10 files named: `<matchId>_matchDetails_<Home>-vs-<Away>.json`.

## Match JSON schema

High-level keys present in each per-match JSON:

- **`general`**: Match metadata
  - `matchId`, `matchName`, `matchRound` (1-based string), `leagueId`, `leagueName`, `countryCode`
  - `homeTeam`/`awayTeam` (IDs, names)
  - `coverageLevel` (e.g., `"xG"` if shot-level xG is available)
  - `matchTimeUTC`/`matchTimeUTCDate`, flags: `started`, `finished`

- **`header`**: Score/status and key events
  - `teams`: names, IDs, scores, logos
  - `status`: kickoff time, half start/end timestamps, FT flag, score string
  - `events`: goals and cards per team; goal entries include a `shotmapEvent` with:
    - coordinates (`x`, `y`), `expectedGoals`, `expectedGoalsOnTarget`, `shotType`, `situation`, `period`, and whether from inside box

- **`nav`**: Available tabs (e.g., `matchfacts`, `liveticker`, `lineup`, `stats`)

- **`content.matchFacts`**: Highlights and player-of-the-match + grouped player stats
  - `highlights`: YouTube link and thumbnail
  - `playerOfTheMatch`: player ID/name, team, rating
  - Player stat groups: "Top stats", "Attack", "Defense", "Duels" with typed values (integers, fractions with percentage, fantasy points)

- **`content.lineup`**: Team formations and player-level info
  - `homeTeam` / `awayTeam`: `formation`, team `rating`
  - `starters` and `subs`: per-player `id`, `name`, `age`, `positionId`, `shirtNumber`, `country`, `marketValue`
  - `performance`: rating, events (e.g., `goal`, `assist`, `yellowCard`), `substitutionEvents` (minute, type, reason), fantasy score
  - `coach` info; `unavailable` players (injuries/suspensions); aggregate `averageStarterAge`, `totalStarterMarketValue`

- **`content.stats`**: Aggregated team-vs-team match stats
  - Grouped by period (e.g., `Periods -> All`) with standard metrics (shots, shots on target, duels, tackles, etc.)

## Using the data

- Iterate via manifest: Load `index.json` and traverse each match using `jsonPath`.
- Round mapping: Treat folder `round_k` as human-friendly Round `k + 1`.
- Common analyses:
  - Shot maps and xG timelines from `header.events`
  - Formations/ratings/substitutions from `content.lineup`
  - Team aggregates by period from `content.stats`

## Scraping the dataset with the notebook

- Notebook: `data/fotmob_scraping.ipynb`
- Overview: The notebook demonstrates how to query FotMob public endpoints and save outputs into `data/24-25_PL_Data_raw/` (including `index.json` and per-round match JSON files).
- How to run (high level):
  - Open the notebook and follow the setup cells for any dependencies and configuration.
  - Execute the scraping cells to fetch rounds and matches; results are written to the folder structure described above.
  - Refer to the notebook for detailed parameters, rate-limiting guidance, and incremental update tips.

## Notes

- This dataset mirrors what is visible on FotMob match pages for the 2024/25 season.