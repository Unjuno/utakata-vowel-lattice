"""Lightweight analysis utilities for generated vowel-lattice events."""

from __future__ import annotations

import json
from collections import Counter, defaultdict, deque
from dataclasses import asdict, dataclass
from itertools import combinations
from pathlib import Path
from typing import Any

from .entropy import ngram_entropy
from .overlap_markov import Candidate
from .phonology import overlap_ratio


@dataclass(frozen=True)
class OverlapEdge:
    """Suffix-prefix overlap edge between two candidates."""

    from_id: str
    to_id: str
    overlap_ratio: float
    from_vowel: str
    to_vowel: str


@dataclass(frozen=True)
class OverlapReport:
    """Summary of candidate overlap graph."""

    candidate_count: int
    edge_count: int
    isolated_count: int
    largest_component_ratio: float
    average_overlap_ratio: float


@dataclass(frozen=True)
class SequenceReport:
    """Summary of a generated event sequence."""

    event_count: int
    approximate_duration_sec: float
    vowel_stream_length: int
    vowel_entropy_2gram: float
    vowel_entropy_3gram: float
    repeated_candidate_count: int
    repeated_vowel_count: int
    average_gap_after: float
    average_boundary_strength: float
    max_f0_jump_hz: float
    max_energy_jump: float


def build_overlap_edges(candidates: list[Candidate], min_ratio: float = 0.2) -> list[OverlapEdge]:
    """Build directed suffix-prefix overlap edges."""
    edges: list[OverlapEdge] = []
    for left, right in combinations(candidates, 2):
        lr = overlap_ratio(left.vowel, right.vowel)
        if lr >= min_ratio:
            edges.append(OverlapEdge(left.candidate_id, right.candidate_id, lr, left.vowel, right.vowel))
        rl = overlap_ratio(right.vowel, left.vowel)
        if rl >= min_ratio:
            edges.append(OverlapEdge(right.candidate_id, left.candidate_id, rl, right.vowel, left.vowel))
    return edges


def summarize_overlap(candidates: list[Candidate], edges: list[OverlapEdge]) -> OverlapReport:
    """Summarize an overlap graph."""
    ids = {c.candidate_id for c in candidates}
    connected: dict[str, set[str]] = {candidate_id: set() for candidate_id in ids}
    for edge in edges:
        connected.setdefault(edge.from_id, set()).add(edge.to_id)
        connected.setdefault(edge.to_id, set()).add(edge.from_id)

    seen: set[str] = set()
    largest = 0
    for candidate_id in ids:
        if candidate_id in seen:
            continue
        queue = deque([candidate_id])
        seen.add(candidate_id)
        size = 0
        while queue:
            current = queue.popleft()
            size += 1
            for neighbor in connected.get(current, set()):
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
        largest = max(largest, size)

    isolated_count = sum(1 for candidate_id in ids if not connected.get(candidate_id))
    average_overlap = sum(edge.overlap_ratio for edge in edges) / len(edges) if edges else 0.0
    largest_ratio = largest / len(ids) if ids else 0.0
    return OverlapReport(
        candidate_count=len(ids),
        edge_count=len(edges),
        isolated_count=isolated_count,
        largest_component_ratio=largest_ratio,
        average_overlap_ratio=average_overlap,
    )


def load_event_payload(path: str | Path) -> dict[str, Any]:
    """Load a generated render-events JSON payload."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def summarize_sequence(payload: dict[str, Any]) -> SequenceReport:
    """Analyze generated render events."""
    events = payload.get("events", [])
    vowel_stream = payload.get("vowel_stream") or "".join(event.get("vowels", "") for event in events)
    candidate_counts = Counter(event.get("candidate_id") for event in events)
    vowel_counts = Counter(event.get("vowels") for event in events)

    gaps: list[float] = []
    boundaries: list[float] = []
    f0_jumps: list[float] = []
    energy_jumps: list[float] = []
    prev_f0: float | None = None
    prev_energy: float | None = None
    last_time = 0.0

    for event in events:
        prosody = event.get("prosody", {})
        gaps.append(float(prosody.get("gap_after", 0.0)))
        boundaries.append(float(prosody.get("boundary_strength", 0.0)))
        f0 = [float(x) for x in prosody.get("f0_hz", [])]
        energy = [float(x) for x in prosody.get("energy", [])]
        if prev_f0 is not None and f0:
            f0_jumps.append(abs(f0[0] - prev_f0))
        if prev_energy is not None and energy:
            energy_jumps.append(abs(energy[0] - prev_energy))
        if f0:
            prev_f0 = f0[-1]
        if energy:
            prev_energy = energy[-1]
        last_time = max(last_time, float(event.get("time", 0.0)) + sum(float(x) for x in prosody.get("duration_sec", [])) + float(prosody.get("gap_after", 0.0)))

    return SequenceReport(
        event_count=len(events),
        approximate_duration_sec=last_time,
        vowel_stream_length=len(vowel_stream),
        vowel_entropy_2gram=ngram_entropy(vowel_stream, 2),
        vowel_entropy_3gram=ngram_entropy(vowel_stream, 3),
        repeated_candidate_count=sum(count - 1 for count in candidate_counts.values() if count > 1),
        repeated_vowel_count=sum(count - 1 for count in vowel_counts.values() if count > 1),
        average_gap_after=sum(gaps) / len(gaps) if gaps else 0.0,
        average_boundary_strength=sum(boundaries) / len(boundaries) if boundaries else 0.0,
        max_f0_jump_hz=max(f0_jumps) if f0_jumps else 0.0,
        max_energy_jump=max(energy_jumps) if energy_jumps else 0.0,
    )


def report_to_dict(report: OverlapReport | SequenceReport) -> dict[str, Any]:
    """Convert a report dataclass to a JSON-friendly dictionary."""
    return asdict(report)


def write_report_markdown(report: OverlapReport | SequenceReport, path: str | Path, title: str) -> None:
    """Write a small markdown report."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# {title}", ""]
    for key, value in asdict(report).items():
        lines.append(f"- `{key}`: {value}")
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
