from src.fetch_data import load_weekly_stats
from src.rank_players import rank_all_players
from src.export_content import export_candidates
import nflreadpy as nfl


SEASON = 2026
WEEK = 1
NUM_CANDIDATES = 10

def main():
    # load weekly player stats and game schedules
    stats = load_weekly_stats(SEASON, WEEK)
    games = nfl.load_schedules(seasons=[SEASON])
    
    # rank players based on their performance this week
    all_players = rank_all_players(stats)

    # export the top candidates with their stats and game context
    export_candidates(
    stats=stats,
    rankings=all_players.head(NUM_CANDIDATES),
    games=games,
    week=WEEK,
    season=SEASON,
    filename="y5_candidates.json"
    )

    print(f"Exported top {NUM_CANDIDATES} Y5 candidates for {SEASON} Week {WEEK}!")

if __name__ == "__main__":
    main()


