"""
End-to-end test: image → OCR → smart extractor → compare with expected.
"""
import sys
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.reader.ocr import read_image
from backend.reader.extract_smart import extract_smart

# Same test cases as the generator
TEST_CASES = [
    ("test_01.png", 23, 14),
    ("test_02.png", 23, 14),
    ("test_03.png", 23, 14),
    ("test_04.png", 45, 67),
    ("test_05.png", 12, 34),
    ("test_06.png", 56, 78),
    ("test_07.png", 99, 11),
    ("test_08.png", 23, 14),
    ("test_09.png", 10, 20),
    ("test_10.png", 88, 22),
    ("test_11.png", 33, 44),
    ("test_12.png", 15, 25),
    ("test_13.png", 77, 88),
    ("test_14.png", 36, 48),
    ("test_15.png", 91, 13),
    ("test_16.png", 50, 50),
    ("test_17.png", 64, 32),
    ("test_18.png", 27, 39),
    ("test_19.png", 81, 19),
    ("test_20.png", 42, 24),
]


def run_tests():
    print("=" * 70)
    print("PIPELINE TEST: 20 IMAGES")
    print("=" * 70)

    passed = 0
    failed = []

    for filename, expected_a, expected_b in TEST_CASES:
        path = Path("data/sample_books") / filename
        try:
            text = read_image(str(path))
            result = extract_smart(text)

            if result and result["a"] == expected_a and result["b"] == expected_b:
                passed += 1
                status = "✅ PASS"
            else:
                failed.append((filename, text, result, expected_a, expected_b))
                status = "❌ FAIL"
        except Exception as e:
            failed.append((filename, str(e), None, expected_a, expected_b))
            status = "❌ ERROR"
            text = ""

        print(f"{status} | {filename} | expected {expected_a}×{expected_b}")
        print(f"           | OCR: {text!r}")
        print(f"           | Got: {result}")
        print("-" * 70)

    accuracy = (passed / len(TEST_CASES)) * 100

    print()
    print("=" * 70)
    print(f"RESULTS: {passed}/{len(TEST_CASES)} passed ({accuracy:.1f}%)")
    print("=" * 70)

    if failed:
        print("\nFailed cases:")
        for f in failed:
            print(f"  - {f[0]}: expected {f[3]}×{f[4]}, got {f[2]}")


if __name__ == "__main__":
    run_tests()
