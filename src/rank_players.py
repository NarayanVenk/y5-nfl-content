import polars as pl


def filter_offensive_players(stats: pl.DataFrame) -> pl.DataFrame:
    positions = ["QB", "RB", "WR", "TE"]

    return stats.filter(
        pl.col("position").is_in(positions)
    )


def rank_quarterbacks(stats: pl.DataFrame) -> pl.DataFrame:
    quarterbacks = stats.filter(pl.col("position") == "QB")

    quarterbacks = quarterbacks.with_columns(
        (
            pl.col("passing_yards") * 0.1
            + pl.col("passing_tds") * 15
            + pl.col("rushing_yards") * 0.15
            + pl.col("rushing_tds") * 15
            - pl.col("passing_interceptions") * 10
        ).alias("post_score")
    )

    quarterbacks = quarterbacks.with_columns(
        (
            pl.col("post_score") * 0.8
            + pl.col("fantasy_points") * 3 * 0.2
        ).alias("final_score")
    )

    return quarterbacks.sort("final_score", descending=True)