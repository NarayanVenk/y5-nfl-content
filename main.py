from src.fetch_data import load_weekly_stats
from src.rank_players import rank_quarterbacks, rank_running_backs, rank_receivers, rank_all_players
from src.player_content import get_player_stats, generate_readable_stat_line, generate_caption, get_game_context
from src.export_content import export_candidates
import polars as pl
import nflreadpy as nfl

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

    print("\nCALEB WILLIAMS CONTENT DATA")
    print(get_player_stats(stats, "Caleb Williams"))

    print("\nJALEN COKER CONTENT DATA")
    print(get_player_stats(stats, "Jalen Coker"))

    caleb = get_player_stats(stats, "Caleb Williams")
    coker = get_player_stats(stats, "Jalen Coker")

    print(generate_readable_stat_line(caleb))
    print(generate_readable_stat_line(coker))

    print("\nCALEB WILLIAMS CAPTION")
    print(generate_caption(caleb))

    games = nfl.load_schedules(seasons=[2026])
    export_candidates(
    stats,
    all_players.head(10),
    games,
    1,
    "y5_candidates.json"
    )

    print("Exported top 10 Y5 candidates!")


    
    print("\nCALEB WILLIAMS GAME CONTEXT")
    print(get_game_context(games, "CHI", 1))

    print("\nJALEN COKER GAME CONTEXT")
    print(get_game_context(games, "CAR", 1))


if __name__ == "__main__":
    main()


