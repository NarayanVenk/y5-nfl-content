from src.fetch_data import load_weekly_stats
from src.rank_players import rank_all_players
from src.export_content import export_candidates
import nflreadpy as nfl
from src.content_manager import load_content, get_approved_posts, combine_content


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




    candidates = load_content("y5_candidates.json")
    content = load_content("y5_content.json")

    approved_posts = get_approved_posts(content)
    combined_posts = combine_content(candidates, approved_posts)

    print("\nCOMBINED Y5 POSTS")
    for post in combined_posts:
        print("Player:", post["player"])
        print("Headline:", post["graphic_headline"])
        print("Stats:", post["stat_line"])
        print("Caption:", post["caption"])


if __name__ == "__main__":
    main()


