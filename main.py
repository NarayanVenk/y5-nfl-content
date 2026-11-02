from src.fetch_data import load_weekly_stats
from src.rank_players import filter_offensive_players


def main():
    stats = load_weekly_stats(2026, 1)
    offensive_players = filter_offensive_players(stats)

    print(offensive_players.select([
        "player_display_name",
        "position",
        "team",
        "fantasy_points_ppr"
    ]).head(20))

    print(f"\nOffensive players: {offensive_players.height}")


if __name__ == "__main__":
    main()

