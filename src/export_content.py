import json
import polars as pl

from src.player_content import get_player_stats, generate_readable_stat_line, get_game_context



def export_candidates(
    stats: pl.DataFrame,
    rankings: pl.DataFrame,
    games: pl.DataFrame,
    week: int,
    season: int,
    filename: str
) -> None:
    candidates = []

    for row in rankings.iter_rows(named=True):
        player = get_player_stats(stats, row["player_display_name"])

        player["position_rank"] = row["position_rank"]
        player["final_score"] = round(row["final_score"], 2)
        player["stat_line"] = generate_readable_stat_line(player)
        player["season"] = season
        player["week"] = week

        game_context = get_game_context(games, player["team"], week)
        player.update(game_context)

        candidates.append(player)

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(candidates, file, indent=4)

