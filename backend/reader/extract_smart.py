"""
Smart Math Extractor
Tries regex first (fast), falls back to LLM (smart).
"""

from backend.reader.extract import extract_math as extract_regex
from backend.llm.understand import extract_math_with_llm


def extract_smart(text: str) -> dict:
    """
    Extract a math problem from text using the best available method.

    Strategy:
    1. Try regex (fast, free, deterministic)
    2. If regex fails, use LLM (handles word problems, messy OCR)

    Returns:
        dict with keys: a, b, op, method
        None if nothing found.
    """
    # Step 1: Try regex
    regex_result = extract_regex(text)
    if regex_result:
        return {
            "a": regex_result["a"],
            "b": regex_result["b"],
            "op": "×",
            "method": "regex",
        }

    # Step 2: Fall back to LLM
    llm_result = extract_math_with_llm(text)
    if llm_result:
        return {
            "a": llm_result["a"],
            "b": llm_result["b"],
            "op": "×",
            "method": "llm",
        }

    # Nothing found
    return None


if __name__ == "__main__":
    test_cases = [
        "23x14=?",                          # regex handles
        "What is 23 times 14?",             # regex handles
        "Calculate forty-five times sixty-seven",  # LLM handles
        "twenty-three multiplied by fourteen",     # LLM handles
        "Hello world",                      # nothing
    ]

    print("=" * 70)
    print("SMART EXTRACTOR TEST")
    print("=" * 70)

    for tc in test_cases:
        result = extract_smart(tc)
        if result:
            print(f"Input:  {tc!r}")
            print(f"Output: a={result['a']}, b={result['b']}, method={result['method']}")
        else:
            print(f"Input:  {tc!r}")
            print(f"Output: None")
        print("-" * 70)
