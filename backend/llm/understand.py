"""
LLM Understander (Groq)
Uses Groq's free LLM API to extract math problems from messy OCR text.
"""

import os
import json
from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Point the OpenAI client to Groq's API
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)


def extract_math_with_llm(text: str) -> Optional[dict]:
    """
    Use Groq's LLM to extract a 2-digit multiplication problem from OCR text.
    """
    prompt = f"""Extract any 2-digit multiplication problem from the text below.

Text: {text!r}

Return ONLY a JSON object with:
- "a": first number (integer)
- "b": second number (integer)
- "op": "x" for multiplication

If no multiplication problem is found, return: {{"found": false}}

Examples:
Input: "23 x 14 = ?"
Output: {{"a": 23, "b": 14, "op": "x"}}

Input: "What is 45 times 67?"
Output: {{"a": 45, "b": 67, "op": "x"}}

Input: "Hello world"
Output: {{"found": false}}

Return ONLY JSON, no explanation."""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()

    try:
        result = json.loads(raw)
        if result.get("found") is False:
            return None
        return result
    except json.JSONDecodeError:
        return None


if __name__ == "__main__":
    test_cases = [
        "23x14=?",
        "What is 23 times 14?",
        "Calculate forty-five multiplied by sixty-seven",
        "Hello world",
    ]

    print("=" * 60)
    print("LLM EXTRACTOR TEST (Groq)")
    print("=" * 60)

    for tc in test_cases:
        result = extract_math_with_llm(tc)
        print(f"Input:  {tc!r}")
        print(f"Output: {result}")
        print("-" * 60)
