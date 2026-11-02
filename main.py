from src.fetch_data import load_weekly_stats


def main():
    stats = load_weekly_stats(2026, 1)

    print(stats.head(10))
    print(f"\nTotal rows: {stats.height}")
    print(f"\nColumns: {stats.columns}")


if __name__ == "__main__":
    main()
