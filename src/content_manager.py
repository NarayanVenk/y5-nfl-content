import json


def load_content(filename: str) -> list[dict]:
    with open(filename, "r", encoding="utf-8") as file:
        content = json.load(file)

    return content



def get_approved_posts(content: list[dict]) -> list[dict]:
    approved_posts = []

    for post in content:
        if post["approved"]:
            approved_posts.append(post)

    return approved_posts



def combine_content(
    candidates: list[dict],
    approved_posts: list[dict]
) -> list[dict]:
    combined_posts = []

    for post in approved_posts:
        for player in candidates:
            if (
                post["player"] == player["player"]
                and post["season"] == player["season"]
                and post["week"] == player["week"]
            ):
                combined = player.copy()
                combined.update(post)
                combined_posts.append(combined)
                break

    return combined_posts
