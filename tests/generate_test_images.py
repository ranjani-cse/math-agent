"""
Generate 20 test images with various math problem formats.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUTPUT_DIR = Path("data/sample_books")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Test cases: (text_to_render, expected_a, expected_b)
TEST_CASES = [
    ("23 x 14 = ?", 23, 14),
    ("23 X 14", 23, 14),
    ("23 * 14 = ?", 23, 14),
    ("45 x 67 = ?", 45, 67),
    ("12 x 34", 12, 34),
    ("56 x 78 = ?", 56, 78),
    ("99 x 11 = ?", 99, 11),
    ("What is 23 x 14?", 23, 14),
    ("10 x 20 = ?", 10, 20),
    ("88 x 22", 88, 22),
    ("33 x 44 = ?", 33, 44),
    ("15 x 25 = ?", 15, 25),
    ("77 x 88", 77, 88),
    ("36 x 48 = ?", 36, 48),
    ("91 x 13 = ?", 91, 13),
    ("50 x 50 = ?", 50, 50),
    ("64 x 32", 64, 32),
    ("27 x 39 = ?", 27, 39),
    ("81 x 19 = ?", 81, 19),
    ("42 x 24 = ?", 42, 24),
]


def make_image(text: str, filename: str):
    """Create an image with the given text."""
    img = Image.new("RGB", (500, 150), color="white")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
    except Exception:
        font = ImageFont.load_default()

    draw.text((30, 50), text, fill="black", font=font)
    img.save(OUTPUT_DIR / filename)


if __name__ == "__main__":
    print("Generating 20 test images...")
    for i, (text, _, _) in enumerate(TEST_CASES, start=1):
        filename = f"test_{i:02d}.png"
        make_image(text, filename)
        print(f"  ✅ {filename}: {text!r}")
    print(f"\n✅ Generated {len(TEST_CASES)} images in {OUTPUT_DIR}/")
