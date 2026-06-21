"""Approximate vowel-formant rendering metadata."""

from __future__ import annotations

from dataclasses import dataclass

VOWEL_FORMANT_TARGETS: dict[str, dict[str, float]] = {
    "あ": {"F1": 800.0, "F2": 1200.0},
    "い": {"F1": 300.0, "F2": 2200.0},
    "う": {"F1": 350.0, "F2": 900.0},
    "え": {"F1": 500.0, "F2": 1900.0},
    "お": {"F1": 500.0, "F2": 1000.0},
}


@dataclass(frozen=True)
class VowelEvent:
    """A renderable vowel-like event."""

    time: float
    vowel: str
    duration: float
    f0_hz: float
    energy: float
    f1_hz: float
    f2_hz: float
    candidate_id: str | None = None
    surface: str | None = None


def formants_for_vowel(vowel: str) -> dict[str, float]:
    """Return approximate formant targets for a Japanese vowel."""
    if vowel not in VOWEL_FORMANT_TARGETS:
        raise ValueError(f"unsupported vowel: {vowel!r}")
    return VOWEL_FORMANT_TARGETS[vowel]
