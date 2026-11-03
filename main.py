from src.fetch_data import load_weekly_stats
from src.rank_players import rank_all_players
from src.export_content import export_candidates
import nflreadpy as nfl
from src.content_manager import load_content, get_approved_posts, combine_content
from pathlib import Path
import json


SEASON = 2026
WEEK = 1
NUM_CANDIDATES = 10

def main():
    # create a directory for this season's data
    data_dir = Path("data") / str(SEASON)
    data_dir.mkdir(parents=True, exist_ok=True)

    # create filenames for the selected week
    candidates_file = data_dir / f"week{WEEK}_candidates.json"
    content_file = data_dir / f"week{WEEK}_content.json"

    
    # load weekly player stats and game schedules
    stats = load_weekly_stats(SEASON, WEEK)
    games = nfl.load_schedules(seasons=[SEASON])    
    
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
    filename=str(candidates_file)
    )

    print(f"Exported top {NUM_CANDIDATES} Y5 candidates for {SEASON} Week {WEEK}!")




    candidates = load_content(str(candidates_file))
    # create an empty content file for a new week
    if not content_file.exists():
        with open(content_file, "w", encoding="utf-8") as file:
            json.dump([], file, indent=4)

        print(f"Created new content file: {content_file}")

    # load the week's approved content
    content = load_content(str(content_file))

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


