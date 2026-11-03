from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from src.content_manager import load_content, get_approved_posts, combine_content
from main import SEASON, WEEK


GRAPHIC_WIDTH = 1080
GRAPHIC_HEIGHT = 1350

TEAM_COLORS = {
    "ARI": "#97233F",
    "ATL": "#A71930",
    "BAL": "#241773",
    "BUF": "#00338D",
    "CAR": "#0085CA",
    "CHI": "#0B162A",
    "CIN": "#FB4F14",
    "CLE": "#311D00",
    "DAL": "#003594",
    "DEN": "#FB4F14",
    "DET": "#0076B6",
    "GB": "#203731",
    "HOU": "#03202F",
    "IND": "#002C5F",
    "JAX": "#006778",
    "KC": "#E31837",
    "LAC": "#0080C6",
    "LAR": "#003594",
    "LV": "#A5ACAF",
    "MIA": "#008E97",
    "MIN": "#4F2683",
    "NE": "#002244",
    "NO": "#D3BC8D",
    "NYG": "#0B2265",
    "NYJ": "#125740",
    "PHI": "#004C54",
    "PIT": "#FFB612",
    "SEA": "#002244",
    "SF": "#AA0000",
    "TB": "#D50A0A",
    "TEN": "#0C2340",
    "WAS": "#5A1414"
}


def create_background(player_image_path: str) -> Image.Image:
    image = Image.open(player_image_path).convert("RGB")

    # Resize while maintaining the aspect ratio
    scale = max(
        GRAPHIC_WIDTH / image.width,
        GRAPHIC_HEIGHT / image.height
    )

    new_width = round(image.width * scale)
    new_height = round(image.height * scale)

    image = image.resize(
        (new_width, new_height),
        Image.Resampling.LANCZOS
    )

    # Crop the center to match Instagram's portrait dimensions
    left = (new_width - GRAPHIC_WIDTH) // 2
    top = (new_height - GRAPHIC_HEIGHT) // 2

    return image.crop((
        left,
        top,
        left + GRAPHIC_WIDTH,
        top + GRAPHIC_HEIGHT
    ))


def add_dark_overlay(image: Image.Image) -> Image.Image:
    # Create a dark blue overlay with the same dimensions
    overlay = Image.new("RGB", image.size, (10, 20, 50))

    # Blend 20% of the overlay with 80% of the original photo
    return Image.blend(image, overlay, 0.20)


def add_team_gradient(image: Image.Image, team: str) -> Image.Image:
    color = TEAM_COLORS.get(team, "#101820")

    rgb = tuple(
        int(color[i:i + 2], 16)
        for i in (1, 3, 5)
    )

    gradient = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(gradient)

    start_y = int(image.height * 0.45)

    for y in range(start_y, image.height):
        progress = (y - start_y) / (image.height - start_y)
        alpha = int(210 * progress ** 1.5)

        draw.line(
            [(0, y), (image.width, y)],
            fill=(*rgb, alpha)
        )

    return Image.alpha_composite(
        image.convert("RGBA"),
        gradient
    ).convert("RGB")


def add_y5_logo(image: Image.Image) -> Image.Image:
    logo = Image.open("assets/y5_logo_transparent.png").convert("RGBA")

    # Resize logo while preserving its aspect ratio
    logo.thumbnail((160, 160), Image.Resampling.LANCZOS)

    # Paste logo in the upper-left corner
    image.paste(logo, (25, 20), logo)

    return image



def add_team_logo(image: Image.Image, team: str) -> Image.Image:
    logo_path = Path("assets/team_logos") / f"{team}.png"

    logo = Image.open(logo_path).convert("RGBA")

    # Resize while preserving the logo's aspect ratio
    logo.thumbnail((250, 250), Image.Resampling.LANCZOS)

    # Center the logo horizontally near the bottom
    x = (GRAPHIC_WIDTH - logo.width) // 2
    y = 850

    image.paste(logo, (x, y), logo)

    return image



def add_stats_panel(image: Image.Image, stats: list[tuple]) -> Image.Image:
    # Create a transparent layer for the panel
    panel = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(panel)

    # Panel dimensions
    x1, y1 = 35, 160
    x2 = 440
    y2 = y1 + 35 + len(stats) * 85

    # Semi-transparent dark background
    draw.rounded_rectangle(
        (x1, y1, x2, y2),
        radius=15,
        fill=(10, 15, 30, 125)
    )

    # Load fonts
    font_path = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
    number_font = ImageFont.truetype(font_path, 65)
    label_font = ImageFont.truetype(font_path, 45)

    # Draw each statistic
    for i, (value, label) in enumerate(stats):
        y = y1 + 25 + i * 85

        draw.text((x1 + 25, y), str(value), font=number_font, fill="#FF7900")

        # Position label after the number
        number_width = draw.textlength(str(value), font=number_font)

        draw.text(
            (x1 + 40 + number_width, y + 12),
            label,
            font=label_font,
            fill="white"
        )

    # Combine the transparent panel with the photo
    return Image.alpha_composite(image.convert("RGBA"), panel).convert("RGB")



def add_headline(image: Image.Image, headline: str) -> Image.Image:
    draw = ImageDraw.Draw(image)

    # Headline box dimensions
    x1, y1 = 45, 1120
    x2, y2 = 1035, 1280

    # Black background with white border
    draw.rectangle(
        (x1, y1, x2, y2),
        fill="black",
        outline="white",
        width=5
    )

    # Load headline font
    font_path = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
    font_size = 100
    max_text_width = (x2 - x1) - 60

    while font_size >= 30:
        font = ImageFont.truetype(font_path, font_size)

        if draw.textlength(headline, font=font) <= max_text_width:
            break

        font_size -= 2

    # Center the headline
    bbox = draw.textbbox((0, 0), headline, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    text_x = (GRAPHIC_WIDTH - text_width) // 2 - bbox[0]
    text_y = (y1 + y2 - text_height) // 2 - bbox[1]

    draw.text(
        (text_x, text_y),
        headline,
        font=font,
        fill="#FF914D"
    )

    return image



def add_watermark(image: Image.Image) -> Image.Image:
    draw = ImageDraw.Draw(image)

    font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
    font = ImageFont.truetype(font_path, 32)

    draw.text(
        (20, GRAPHIC_HEIGHT - 45),
        "@yazdaddy5",
        font=font,
        fill=(220, 220, 220)
    )

    return image



def get_graphic_stats(player: dict) -> list[tuple]:
    position = player["position"]

    if position == "QB":
        total_tds = player["passing_tds"] + player["rushing_tds"]

        stats = [
            (player["passing_yards"], "PASS YDS"),
            (total_tds, "TOTAL TD")
        ]

        if player["rushing_yards"] >= 30:
            stats.append((player["rushing_yards"], "RUSH YDS"))
        else:
            stats.append((player["interceptions"], "INT"))

        return stats

    
    
    elif position == "RB":
        total_yards = player["rushing_yards"] + player["receiving_yards"]
        total_tds = player["rushing_tds"] + player["receiving_tds"]

        stats = [
            (total_yards, "TOTAL YDS"),
            (total_tds, "TOTAL TD")
        ]

        if player["receptions"] >= 4:
            stats.append((player["receptions"], "REC"))
        else:
            stats.append((player["carries"], "CAR"))

        return stats



    elif position in ["WR", "TE"]:
        total_tds = player["rushing_tds"] + player["receiving_tds"]
        return [
            (player["receptions"], "REC"),
            (player["receiving_yards"], "REC YDS"),
            (total_tds, "TD")
        ]

    return []



def generate_player_graphic(post: dict, player_image_path: str) -> None:
    background = create_background(player_image_path)
    background = add_dark_overlay(background)
    background = add_team_gradient(background, post["team"])

    background = add_y5_logo(background)
    background = add_team_logo(background, post["team"])

    stats = get_graphic_stats(post)
    background = add_stats_panel(background, stats)

    background = add_headline(background, post["graphic_headline"])
    background = add_watermark(background)

    
    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)

    player_name = post["player"].lower().replace(" ", "_")
    season = post["season"]
    week = post["week"]

    filename = f"{player_name}_{season}_week{week}.png"
    output_path = output_dir / filename

    background.save(output_path)

    print(f"Created {output_path}!")





if __name__ == "__main__":
    data_dir = Path("data") / str(SEASON)

    candidates_file = data_dir / f"week{WEEK}_candidates.json"
    content_file = data_dir / f"week{WEEK}_content.json"

    candidates = load_content(str(candidates_file))
    content = load_content(str(content_file))

    approved_posts = get_approved_posts(content)
    posts = combine_content(candidates, approved_posts)

    for post in posts:
        player_name = post["player"].lower().replace(" ", "")
        image_path = Path("assets/player_images") / f"{player_name}.png"

        if not image_path.exists():
            print(f"Skipping {post['player']}: no player image found.")
            continue

        generate_player_graphic(post, str(image_path))
