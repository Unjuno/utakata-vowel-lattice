"""Phonological utilities for Japanese vowel-lattice generation."""

from __future__ import annotations

import re
from collections.abc import Iterable

VOWELS = "あいうえお"

KATAKANA_OFFSET = ord("ァ") - ord("ぁ")

# Basic kana-to-vowel map. This is intentionally compact and can be expanded
# when corpus ingestion begins.
KANA_TO_VOWEL: dict[str, str] = {
    **dict.fromkeys(list("あかさたなはまやらわがざだばぱゃぁ"), "あ"),
    **dict.fromkeys(list("いきしちにひみりぎじぢびぴぃ"), "い"),
    **dict.fromkeys(list("うくすつぬふむゆるぐずづぶぷゅぅゔ"), "う"),
    **dict.fromkeys(list("えけせてねへめれげぜでべぺぇ"), "え"),
    **dict.fromkeys(list("おこそとのほもよろをごぞどぼぽょぉ"), "お"),
}

DIGRAPH_VOWEL = {
    "ゃ": "あ",
    "ゅ": "う",
    "ょ": "お",
    "ぁ": "あ",
    "ぃ": "い",
    "ぅ": "う",
    "ぇ": "え",
    "ぉ": "お",
}


def kata_to_hira(text: str) -> str:
    """Convert full-width katakana to hiragana, leaving other chars unchanged."""
    chars: list[str] = []
    for ch in text:
        code = ord(ch)
        if ord("ァ") <= code <= ord("ヶ"):
            chars.append(chr(code - KATAKANA_OFFSET))
        else:
            chars.append(ch)
    return "".join(chars)


def normalize_reading(reading: str) -> str:
    """Normalize a kana reading for vowel extraction."""
    text = kata_to_hira(reading.strip())
    text = text.replace("ー", "")
    text = re.sub(r"\s+", "", text)
    return text


def extract_vowels(reading: str) -> str:
    """Extract a strict vowel skeleton from a kana reading.

    Unknown symbols are ignored rather than guessed.
    """
    text = normalize_reading(reading)
    vowels: list[str] = []
    for ch in text:
        if ch in VOWELS:
            vowels.append(ch)
        elif ch in DIGRAPH_VOWEL:
            if vowels:
                # Small ya/yu/yo normally modifies the preceding consonant kana.
                # Replace the last vowel with the digraph vowel.
                vowels[-1] = DIGRAPH_VOWEL[ch]
            else:
                vowels.append(DIGRAPH_VOWEL[ch])
        elif ch == "ん" or ch == "っ":
            continue
        elif ch in KANA_TO_VOWEL:
            vowels.append(KANA_TO_VOWEL[ch])
    return "".join(vowels)


def compress_repeated_vowels(vowels: str) -> str:
    """Collapse adjacent repeated vowels."""
    if not vowels:
        return ""
    out = [vowels[0]]
    for ch in vowels[1:]:
        if ch != out[-1]:
            out.append(ch)
    return "".join(out)


def is_vowel_string(text: str) -> bool:
    """Return true if text consists only of Japanese vowels."""
    return bool(text) and all(ch in VOWELS for ch in text)


def ngrams(text: str, n: int) -> list[str]:
    """Return character n-grams."""
    if n <= 0:
        raise ValueError("n must be positive")
    if len(text) < n:
        return []
    return [text[i : i + n] for i in range(len(text) - n + 1)]


def overlap_length(left: str, right: str) -> int:
    """Longest suffix-prefix overlap length between two strings."""
    max_len = min(len(left), len(right))
    for k in range(max_len, 0, -1):
        if left[-k:] == right[:k]:
            return k
    return 0


def overlap_ratio(left: str, right: str) -> float:
    """Normalized suffix-prefix overlap."""
    denom = min(len(left), len(right))
    if denom == 0:
        return 0.0
    return overlap_length(left, right) / denom


def levenshtein_distance(a: str, b: str) -> int:
    """Small dependency-free Levenshtein distance."""
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)

    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        curr = [i]
        for j, cb in enumerate(b, start=1):
            cost = 0 if ca == cb else 1
            curr.append(min(curr[-1] + 1, prev[j] + 1, prev[j - 1] + cost))
        prev = curr
    return prev[-1]


def normalized_similarity(a: str, b: str) -> float:
    """Return 1 - normalized edit distance."""
    denom = max(len(a), len(b))
    if denom == 0:
        return 1.0
    return 1.0 - levenshtein_distance(a, b) / denom


def count_items(items: Iterable[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    return counts
