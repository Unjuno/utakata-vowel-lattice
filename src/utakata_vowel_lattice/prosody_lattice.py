"""Prosody-lattice primitives.

Prosody is represented as a field that can overlap across lexical candidates.
It is not random rhythm added after generation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from math import sqrt


@dataclass(frozen=True)
class ProsodyCandidate:
    """A possible prosodic realization for a lexical candidate."""

    contour_class: str = "level"
    f0_pattern: tuple[float, ...] = field(default_factory=tuple)
    duration_pattern: tuple[float, ...] = field(default_factory=tuple)
    energy_pattern: tuple[float, ...] = field(default_factory=tuple)
    gap_after: float = 0.0
    boundary_strength: float = 0.0


def _vector_similarity(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    if not a or not b:
        return 0.5
    n = min(len(a), len(b))
    if n == 0:
        return 0.5
    diff = sqrt(sum((a[i] - b[i]) ** 2 for i in range(n)) / n)
    return 1.0 / (1.0 + diff)


def prosody_similarity(a: ProsodyCandidate, b: ProsodyCandidate) -> float:
    """Similarity of two prosody candidates.

    This rewards compatible contour, duration, energy, and boundary behavior.
    """
    contour = 1.0 if a.contour_class == b.contour_class else 0.5
    f0 = _vector_similarity(a.f0_pattern, b.f0_pattern)
    duration = _vector_similarity(a.duration_pattern, b.duration_pattern)
    energy = _vector_similarity(a.energy_pattern, b.energy_pattern)
    gap = 1.0 / (1.0 + abs(a.gap_after - b.gap_after))
    boundary = 1.0 / (1.0 + abs(a.boundary_strength - b.boundary_strength))
    return 0.20 * contour + 0.25 * f0 + 0.20 * duration + 0.15 * energy + 0.10 * gap + 0.10 * boundary


def continuity_penalty(previous: ProsodyCandidate | None, current: ProsodyCandidate) -> float:
    """Penalty for abrupt prosodic discontinuity."""
    if previous is None:
        return 0.0
    prev_f0 = previous.f0_pattern[-1] if previous.f0_pattern else 0.0
    curr_f0 = current.f0_pattern[0] if current.f0_pattern else prev_f0
    prev_energy = previous.energy_pattern[-1] if previous.energy_pattern else 0.0
    curr_energy = current.energy_pattern[0] if current.energy_pattern else prev_energy
    f0_jump = abs(curr_f0 - prev_f0) / 100.0
    energy_jump = abs(curr_energy - prev_energy)
    gap = current.gap_after + current.boundary_strength
    return f0_jump + energy_jump + 0.25 * gap


DEFAULT_PROSODY = ProsodyCandidate(
    contour_class="level",
    f0_pattern=(220.0, 222.0, 220.0),
    duration_pattern=(0.22, 0.22, 0.22),
    energy_pattern=(0.65, 0.68, 0.65),
    gap_after=0.08,
    boundary_strength=0.15,
)
