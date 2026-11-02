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



def get_game_context(
    games: pl.DataFrame,
    team: str,
    week: int
) -> dict:
    game = games.filter(
        (pl.col("week") == week)
        & (
            (pl.col("home_team") == team)
            | (pl.col("away_team") == team)
        )
    )

    if game.is_empty():
        raise ValueError(f"No game found for {team} in Week {week}")

    game_data = game.row(0, named=True)

    if game_data["home_team"] == team:
        opponent = game_data["away_team"]
        team_score = game_data["home_score"]
        opponent_score = game_data["away_score"]
    else:
        opponent = game_data["home_team"]
        team_score = game_data["away_score"]
        opponent_score = game_data["home_score"]

    if team_score > opponent_score:
        result = "W"
    elif team_score < opponent_score:
        result = "L"
    else:
        result = "T"

    return {
        "opponent": opponent,
        "team_score": team_score,
        "opponent_score": opponent_score,
        "result": result
    }



def generate_readable_stat_line(player: dict) -> str:
    position = player["position"]

    if position == "QB":
        total_yards = player["passing_yards"] + player["rushing_yards"]
        total_tds = player["passing_tds"] + player["rushing_tds"]

        return (
            f"{total_yards} total yards | "
            f"{total_tds} total TD | "
            f"{player['interceptions']} INT"
        )

    
    elif position == "RB":
        total_tds = player["rushing_tds"] + player["receiving_tds"]

        return (
            f"{player['rushing_yards']} RUSH YDS | "
            f"{player['receptions']} REC | "
            f"{player['receiving_yards']} REC YDS | "
            f"{total_tds} total TD"
        )

    else:
        total_tds = player["receiving_tds"] + player["rushing_tds"]

        return (
            f"{player['receptions']} REC | "
            f"{player['receiving_yards']} REC YDS | "
            f"{total_tds} total TD"
        )


def generate_caption(player: dict) -> str:
    name = player["player"]
    stat_line = generate_readable_stat_line(player)

    headline = f"{name.upper()} WENT OFF 🔥"

    caption = (
        f"{headline}\n\n"
        f"{name} put up an impressive performance this week:\n\n"
        f"{stat_line}\n\n"
        f"What did you think of the performance from {name}? 👀"
    )

    return caption