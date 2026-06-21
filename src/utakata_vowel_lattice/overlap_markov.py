"""Constrained overlap Markov lattice generator."""

from __future__ import annotations

import json
import math
import random
from dataclasses import dataclass, field
from pathlib import Path

from .entropy import entropy_band_score, ngram_entropy
from .phonology import normalized_similarity, overlap_ratio
from .prosody_lattice import DEFAULT_PROSODY, ProsodyCandidate, continuity_penalty, prosody_similarity


@dataclass(frozen=True)
class Candidate:
    """Lexical/phonological candidate node."""

    candidate_id: str
    surface: str
    reading: str
    vowel: str
    frequency: float = 1.0
    pos_pattern: tuple[str, ...] = field(default_factory=tuple)
    prosody_candidates: tuple[ProsodyCandidate, ...] = (DEFAULT_PROSODY,)

    @property
    def frequency_score(self) -> float:
        return math.log1p(max(self.frequency, 0.0))


@dataclass(frozen=True)
class GeneratorWeights:
    """Scoring weights for candidate selection."""

    overlap: float = 1.5
    frequency: float = 1.0
    phonology: float = 1.0
    prosody: float = 1.0
    entropy: float = 1.2
    continuity_penalty: float = 1.0
    repetition_penalty: float = 1.4
    target_entropy: float = 2.0
    entropy_width: float = 1.0
    temperature: float = 0.7


@dataclass
class GeneratorState:
    """Mutable generation state."""

    vowels: str = ""
    selected: list[Candidate] = field(default_factory=list)
    selected_prosody: list[ProsodyCandidate] = field(default_factory=list)
    time_sec: float = 0.0


class OverlapMarkovGenerator:
    """Weighted Markov generator for overlapping vowel candidates.

    This is intentionally small and inspectable. It does not try to be a
    natural language model. It scores candidates by overlap, frequency,
    phonological similarity, prosody compatibility, entropy-band fit, and
    repetition avoidance.
    """

    def __init__(
        self,
        candidates: list[Candidate],
        weights: GeneratorWeights | None = None,
        seed: int | None = None,
    ) -> None:
        if not candidates:
            raise ValueError("candidates must not be empty")
        self.candidates = candidates
        self.weights = weights or GeneratorWeights()
        self.rng = random.Random(seed)
        self.seed = seed

    def score(self, state: GeneratorState, candidate: Candidate, prosody: ProsodyCandidate) -> float:
        prev = state.selected[-1] if state.selected else None
        prev_prosody = state.selected_prosody[-1] if state.selected_prosody else None

        if prev is None:
            overlap = 0.0
            phonology = 0.5
            prosody_fit = 0.5
        else:
            overlap = overlap_ratio(prev.vowel, candidate.vowel)
            phonology = normalized_similarity(prev.vowel, candidate.vowel)
            prosody_fit = prosody_similarity(prev_prosody or DEFAULT_PROSODY, prosody)

        next_vowels = self._merged_vowels(state.vowels, candidate.vowel)
        entropy_value = ngram_entropy(next_vowels, n=3)
        entropy_fit = entropy_band_score(
            entropy_value,
            target=self.weights.target_entropy,
            width=self.weights.entropy_width,
        )
        repetition = self._repetition_penalty(state, candidate)
        discontinuity = continuity_penalty(prev_prosody, prosody)

        return (
            self.weights.overlap * overlap
            + self.weights.frequency * candidate.frequency_score
            + self.weights.phonology * phonology
            + self.weights.prosody * prosody_fit
            + self.weights.entropy * entropy_fit
            - self.weights.continuity_penalty * discontinuity
            - self.weights.repetition_penalty * repetition
        )

    def step(self, state: GeneratorState) -> tuple[Candidate, ProsodyCandidate, float]:
        """Select and apply the next candidate/prosody pair."""
        options: list[tuple[Candidate, ProsodyCandidate, float]] = []
        for candidate in self.candidates:
            for prosody in candidate.prosody_candidates or (DEFAULT_PROSODY,):
                options.append((candidate, prosody, self.score(state, candidate, prosody)))

        candidate, prosody, score = self._softmax_choice(options)
        state.vowels = self._merged_vowels(state.vowels, candidate.vowel)
        state.selected.append(candidate)
        state.selected_prosody.append(prosody)
        state.time_sec += sum(prosody.duration_pattern) + prosody.gap_after
        return candidate, prosody, score

    def generate(self, steps: int) -> dict:
        if steps <= 0:
            raise ValueError("steps must be positive")
        state = GeneratorState()
        events = []
        current_time = 0.0
        for _ in range(steps):
            candidate, prosody, score = self.step(state)
            events.append(
                {
                    "time": round(current_time, 4),
                    "candidate_id": candidate.candidate_id,
                    "surface": candidate.surface,
                    "reading": candidate.reading,
                    "vowels": candidate.vowel,
                    "score": round(score, 6),
                    "prosody": {
                        "contour_class": prosody.contour_class,
                        "f0_hz": list(prosody.f0_pattern),
                        "duration_sec": list(prosody.duration_pattern),
                        "energy": list(prosody.energy_pattern),
                        "gap_after": prosody.gap_after,
                        "boundary_strength": prosody.boundary_strength,
                    },
                }
            )
            current_time = state.time_sec
        return {
            "seed": self.seed,
            "steps": steps,
            "vowel_stream": state.vowels,
            "vowel_entropy_3gram": ngram_entropy(state.vowels, n=3),
            "events": events,
        }

    def write_json(self, path: str | Path, steps: int) -> None:
        payload = self.generate(steps)
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def _softmax_choice(
        self, options: list[tuple[Candidate, ProsodyCandidate, float]]
    ) -> tuple[Candidate, ProsodyCandidate, float]:
        temperature = max(self.weights.temperature, 1e-6)
        max_score = max(score for _, _, score in options)
        weights = [math.exp((score - max_score) / temperature) for _, _, score in options]
        total = sum(weights)
        pick = self.rng.random() * total
        acc = 0.0
        for option, weight in zip(options, weights, strict=True):
            acc += weight
            if acc >= pick:
                return option
        return options[-1]

    def _merged_vowels(self, current: str, next_vowels: str) -> str:
        if not current:
            return next_vowels
        overlap = 0
        max_len = min(len(current), len(next_vowels))
        for k in range(max_len, 0, -1):
            if current[-k:] == next_vowels[:k]:
                overlap = k
                break
        return current + next_vowels[overlap:]

    def _repetition_penalty(self, state: GeneratorState, candidate: Candidate) -> float:
        if not state.selected:
            return 0.0
        recent = state.selected[-4:]
        same = sum(1 for item in recent if item.vowel == candidate.vowel)
        similar = sum(1 for item in recent if normalized_similarity(item.vowel, candidate.vowel) > 0.85)
        return 0.5 * same + 0.25 * similar
