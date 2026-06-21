"""Entropy utilities for controlled stochastic generation."""

from __future__ import annotations

import math
from collections import Counter
from collections.abc import Iterable

from .phonology import ngrams


def shannon_entropy(items: Iterable[str]) -> float:
    """Compute Shannon entropy in nats for an iterable of discrete items."""
    counts = Counter(items)
    total = sum(counts.values())
    if total == 0:
        return 0.0
    entropy = 0.0
    for count in counts.values():
        p = count / total
        entropy -= p * math.log(p)
    return entropy


def ngram_entropy(text: str, n: int = 3) -> float:
    """Entropy of character n-grams in a string."""
    return shannon_entropy(ngrams(text, n))


def entropy_band_score(value: float, target: float, width: float) -> float:
    """Score how close an entropy value is to a target band.

    Returns 1.0 inside the band center and decays linearly outside.
    """
    if width <= 0:
        raise ValueError("width must be positive")
    distance = abs(value - target)
    return max(0.0, 1.0 - distance / width)
