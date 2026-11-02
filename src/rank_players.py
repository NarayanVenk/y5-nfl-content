import polars as pl


def filter_offensive_players(stats: pl.DataFrame) -> pl.DataFrame:
    positions = ["QB", "RB", "WR", "TE"]

    return stats.filter(
        pl.col("position").is_in(positions)
    )
