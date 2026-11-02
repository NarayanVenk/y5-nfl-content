import polars as pl

def get_player_stats(stats: pl.DataFrame, player_name: str) -> dict:
    player = stats.filter(
        pl.col("player_display_name") == player_name
    )

    if player.is_empty():
        raise ValueError(f"Player not found: {player_name}")

    player_data = player.row(0, named=True)

    position = player_data["position"]

    result = {
        "player": player_data["player_display_name"],
        "team": player_data["team"],
        "position": position
    }

    if position == "QB":
        result.update({
            "passing_yards": player_data["passing_yards"],
            "passing_tds": player_data["passing_tds"],
            "rushing_yards": player_data["rushing_yards"],
            "rushing_tds": player_data["rushing_tds"],
            "interceptions": player_data["passing_interceptions"]
        })

    elif position in ["RB", "WR", "TE"]:
        result.update({
            "receptions": player_data["receptions"],
            "receiving_yards": player_data["receiving_yards"],
            "receiving_tds": player_data["receiving_tds"],
            "rushing_yards": player_data["rushing_yards"],
            "rushing_tds": player_data["rushing_tds"]
        })

    return result
