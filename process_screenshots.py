"""Crop Android status/system navigation bars from the app screenshots.

Original JPGs stay untouched in assets/. Cropped, purpose-named JPGs are
written to assets/site/ and are used by the website.
"""

from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parent
SOURCE_DIR = ROOT / "assets"
OUTPUT_DIR = SOURCE_DIR / "site"

# The screenshots are 1080 x 2340. These fixed insets remove Android's top
# status/notification bar and bottom system navigation area while preserving
# the app's own content and in-app navigation.
TOP_CROP = 125
BOTTOM_CROP = 130

SCREENSHOTS = {
    "jornada": "Screenshot_20261016_194107.jpg",
    "livros": "Screenshot_20261016_194114.jpg",
    "missoes": "Screenshot_20261016_194123.jpg",
    "reflexao-do-dia": "Screenshot_20261016_194132.jpg",
    "perfil": "Screenshot_20261016_194139.jpg",
    "compartilhamento": "Screenshot_20261016_194142.jpg",
    "conquistas": "Screenshot_20261016_194147.jpg",
    "perfil-detalhe": "Screenshot_20261016_194156.jpg",
    "leitura": "Screenshot_20261016_194209.jpg",
    "quiz": "Screenshot_20261016_194315.jpg",
    "capitulo-concluido": "Screenshot_20261016_194411.jpg",
    "recompensa": "Screenshot_20261016_194416.jpg",
}


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for purpose, filename in SCREENSHOTS.items():
        source = SOURCE_DIR / filename
        if not source.exists():
            raise FileNotFoundError(f"Screenshot não encontrado: {source}")

        with Image.open(source) as image:
            image = ImageOps.exif_transpose(image).convert("RGB")
            if image.height <= TOP_CROP + BOTTOM_CROP:
                raise ValueError(f"Imagem pequena demais para o crop: {source}")
            cropped = image.crop(
                (0, TOP_CROP, image.width, image.height - BOTTOM_CROP)
            )
            destination = OUTPUT_DIR / f"{purpose}.jpg"
            cropped.save(
                destination,
                "JPEG",
                quality=94,
                optimize=True,
                progressive=True,
                subsampling=0,
            )
            print(f"{source.name} → {destination.relative_to(ROOT)} {cropped.size}")


if __name__ == "__main__":
    main()
