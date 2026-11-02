
from pathlib import Path
from urllib.request import urlopen
from PIL import Image
from io import BytesIO
import ssl
import certifi

TEAM_ABBREVIATIONS = [
    "ARI", "ATL", "BAL", "BUF", "CAR", "CHI", "CIN", "CLE",
    "DAL", "DEN", "DET", "GB", "HOU", "IND", "JAX", "KC",
    "LAC", "LAR", "LV", "MIA", "MIN", "NE", "NO", "NYG",
    "NYJ", "PHI", "PIT", "SEA", "SF", "TB", "TEN", "WAS"
]

LOGO_DIRECTORY = Path("assets/team_logos")
BASE_URL = "https://a.espncdn.com/i/teamlogos/nfl/500"


def download_team_logos() -> None:
    LOGO_DIRECTORY.mkdir(parents=True, exist_ok=True)

    for team in TEAM_ABBREVIATIONS:
        url = f"{BASE_URL}/{team.lower()}.png"
        filename = LOGO_DIRECTORY / f"{team}.png"

        ssl_context = ssl.create_default_context(cafile=certifi.where())
        try:
            with urlopen(url, timeout=15, context=ssl_context) as response:
                image_data = response.read()

            image = Image.open(BytesIO(image_data))
            image = image.convert("RGBA")
            image.save(filename)

            print(f"Downloaded {team}.png")

        except Exception as error:
            print(f"Failed to download {team}: {error}")


if __name__ == "__main__":
    download_team_logos()
