import nflreadpy as nfl
import polars as pl


def load_weekly_stats(season: int, week: int) -> pl.DataFrame:
    stats = nfl.load_player_stats(seasons=[season], summary_level="week")
    weekly_stats = stats.filter(pl.col("week") == week)
    return weekly_stats