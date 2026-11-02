from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

GRAPHIC_WIDTH = 1080
GRAPHIC_HEIGHT = 1350


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


if __name__ == "__main__":
    background = create_background(
        "assets/player_images/calebwilliams.png"
    )

    background = add_dark_overlay(background)
    background = add_y5_logo(background)
    background = add_team_logo(background, "CHI")
    background = add_stats_panel(
        background,
        [
            ("269", "PASS YDS"),
            ("2", "PASS TD"),
            ("65", "RUSH YDS"),
            ("2", "RUSH TD")
        ]
    )
    background = add_headline(background, "Caleb Williams is Elite?")
    background = add_watermark(background)
    background.save("test_background.png")
    print("Created test_background.png!")