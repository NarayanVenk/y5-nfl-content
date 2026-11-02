from src.fetch_data import load_weekly_stats
from src.rank_players import rank_quarterbacks, rank_running_backs, rank_receivers, rank_all_players
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

    running_backs = rank_running_backs(stats)

    print(
        running_backs.select([
            "player_display_name",
            "team",
            "carries",
            "rushing_yards",
            "receiving_yards",
            "receptions",
            "rushing_tds",
            "receiving_tds",
            "fantasy_points_ppr",
            "post_score",
            "final_score"
        ]).head(10)
    )

    wide_receivers = rank_receivers(stats, "WR")
    tight_ends = rank_receivers(stats, "TE")

    columns = [
        "player_display_name",
        "team",
        "receptions",
        "receiving_yards",
        "receiving_tds",
        "fantasy_points_ppr",
        "post_score",
        "final_score"
    ]

    print("\nTOP WIDE RECEIVERS")
    print(wide_receivers.select(columns).head(10))

    print("\nTOP TIGHT ENDS")
    print(tight_ends.select(columns).head(10))

    all_players = rank_all_players(stats)

    print("\nTOP Y5 POST CANDIDATES")
    with pl.Config(tbl_rows=20):
        print(all_players.head(20))



if __name__ == "__main__":
    main()


