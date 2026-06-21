#!/usr/bin/env python
"""Generate a small render-events JSON payload from the scaffold model."""

from __future__ import annotations

import argparse
from pathlib import Path

from utakata_vowel_lattice.overlap_markov import Candidate, GeneratorWeights, OverlapMarkovGenerator
from utakata_vowel_lattice.prosody_lattice import ProsodyCandidate


def demo_candidates() -> list[Candidate]:
    return [
        Candidate(
            candidate_id="cand_0001",
            surface="いいえ",
            reading="いいえ",
            vowel="いいえ",
            frequency=1200,
            pos_pattern=("応答",),
            prosody_candidates=(
                ProsodyCandidate("level", (220, 222, 219), (0.22, 0.20, 0.28), (0.60, 0.70, 0.58), 0.08, 0.15),
                ProsodyCandidate("fall", (224, 220, 216), (0.20, 0.22, 0.30), (0.70, 0.65, 0.55), 0.12, 0.25),
            ),
        ),
        Candidate(
            candidate_id="cand_0002",
            surface="良い絵",
            reading="よいえ",
            vowel="おいえ",
            frequency=430,
            pos_pattern=("形容詞", "名詞"),
            prosody_candidates=(
                ProsodyCandidate("rise", (218, 222, 226), (0.20, 0.22, 0.26), (0.55, 0.65, 0.76), 0.06, 0.12),
            ),
        ),
        Candidate(
            candidate_id="cand_0003",
            surface="愛を追う",
            reading="あいをおう",
            vowel="あいおおう",
            frequency=300,
            pos_pattern=("名詞", "助詞", "動詞"),
            prosody_candidates=(
                ProsodyCandidate("rise_fall", (218, 224, 231, 227, 220), (0.22, 0.18, 0.20, 0.25, 0.30), (0.65, 0.70, 0.78, 0.82, 0.60), 0.10, 0.22),
            ),
        ),
        Candidate(
            candidate_id="cand_0004",
            surface="藍を覆う",
            reading="あいをおおう",
            vowel="あいおおう",
            frequency=70,
            pos_pattern=("名詞", "助詞", "動詞"),
            prosody_candidates=(
                ProsodyCandidate("level_fall", (219, 221, 222, 219, 215), (0.24, 0.18, 0.22, 0.26, 0.32), (0.60, 0.66, 0.72, 0.80, 0.58), 0.09, 0.20),
            ),
        ),
        Candidate(
            candidate_id="cand_0005",
            surface="青い家",
            reading="あおいいえ",
            vowel="あおいいえ",
            frequency=220,
            pos_pattern=("形容詞", "名詞"),
            prosody_candidates=(
                ProsodyCandidate("fall", (226, 224, 220, 218, 216), (0.24, 0.20, 0.18, 0.22, 0.30), (0.72, 0.70, 0.68, 0.60, 0.52), 0.14, 0.30),
            ),
        ),
        Candidate(
            candidate_id="cand_0006",
            surface="葵、家",
            reading="あおい、いえ",
            vowel="あおいいえ",
            frequency=40,
            pos_pattern=("名詞", "名詞"),
            prosody_candidates=(
                ProsodyCandidate("wave", (220, 225, 221, 223, 218), (0.20, 0.21, 0.22, 0.20, 0.26), (0.60, 0.72, 0.62, 0.68, 0.55), 0.10, 0.18),
            ),
        ),
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20260621)
    parser.add_argument("--steps", type=int, default=16)
    parser.add_argument("--output", default="outputs/render_events.json")
    args = parser.parse_args()

    weights = GeneratorWeights(target_entropy=2.0, entropy_width=1.0, temperature=0.75)
    generator = OverlapMarkovGenerator(demo_candidates(), weights=weights, seed=args.seed)
    generator.write_json(Path(args.output), steps=args.steps)
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
