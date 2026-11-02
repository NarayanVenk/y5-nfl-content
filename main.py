from src.fetch_data import load_weekly_stats
from src.rank_players import rank_quarterbacks
import polars as pl

pl.Config.set_tbl_cols(-1)

def main():
    stats = load_weekly_stats(2026, 1)
    quarterbacks = rank_quarterbacks(stats)

    print(
        quarterbacks.select([
            "player_display_name",
            "team",
            "passing_yards",
            "passing_tds",
            "rushing_yards",
            "rushing_tds",
            "passing_interceptions",
            "fantasy_points",
            "post_score",
            "final_score"
        ]).head(10)
    )


if __name__ == "__main__":
    main()


