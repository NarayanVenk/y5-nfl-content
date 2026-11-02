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


def rank_running_backs(stats: pl.DataFrame) -> pl.DataFrame:
    running_backs = stats.filter(pl.col("position") == "RB")

    running_backs = running_backs.with_columns(
        (
            pl.col("rushing_yards") * 0.15
            + pl.col("receiving_yards") * 0.15
            + pl.col("receptions") * 2
            + pl.col("rushing_tds") * 15
            + pl.col("receiving_tds") * 15
        ).alias("post_score")
    )

    running_backs = running_backs.with_columns(
        (
            pl.col("post_score") * 0.8
            + pl.col("fantasy_points_ppr") * 3 * 0.2
        ).alias("final_score")
    )

    return running_backs.sort("final_score", descending=True)



def rank_receivers(stats: pl.DataFrame, position: str) -> pl.DataFrame:
    receivers = stats.filter(pl.col("position") == position)

    receivers = receivers.with_columns(
        (
            pl.col("receiving_yards") * 0.2
            + pl.col("receptions") * 2
            + pl.col("receiving_tds") * 15
            + pl.col("rushing_yards") * 0.15
            + pl.col("rushing_tds") * 15
        ).alias("post_score")
    )

    receivers = receivers.with_columns(
        (
            pl.col("post_score") * 0.8
            + pl.col("fantasy_points_ppr") * 3 * 0.2
        ).alias("final_score")
    )

    return receivers.sort("final_score", descending=True)



def rank_all_players(stats: pl.DataFrame) -> pl.DataFrame:
    quarterbacks = rank_quarterbacks(stats)
    running_backs = rank_running_backs(stats)
    wide_receivers = rank_receivers(stats, "WR")
    tight_ends = rank_receivers(stats, "TE")

    rankings = []

    for players in [
        quarterbacks,
        running_backs,
        wide_receivers,
        tight_ends
    ]:
        players = players.with_columns(
            pl.col("final_score")
            .rank(method="ordinal", descending=True)
            .alias("position_rank")
        )

        rankings.append(
            players.select([
                "player_display_name",
                "team",
                "position",
                "final_score",
                "position_rank"
            ])
        )

    return pl.concat(rankings).sort(
        ["position_rank", "final_score"],
        descending=[False, True]
    )
