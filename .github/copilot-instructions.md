# Copilot / Coding Agent Instructions

Read these files before implementing anything:

1. `AGENTS.md`
2. `docs/MODEL_DESIGN.md`
3. `docs/IMPLEMENTATION_CONTRACTS.md`
4. `docs/WORK_PACKAGES.md`

## Project invariant

This is not a normal lyric generator. It is a constrained vowel-lattice generative instrument.

The core pipeline is:

```text
source corpora
  -> derived vowel-lattice corpus
  -> constrained overlap Markov lattice model
  -> prosody-lattice field
  -> instrumental formant rendering
  -> listener-side lyric emergence
```

Do not replace this with an opaque decode-only language model.

## How to work

Implement one work package at a time. Prefer small PRs. Do not introduce large dependencies unless the work package explicitly requires them.

Every implementation task should include:

- a CLI or public function with stable input/output;
- unit tests where feasible;
- no committed raw corpus data;
- no committed generated audio;
- no hidden randomness except explicit `seed` arguments.

## Style

- Python 3.11+.
- Keep modules small and inspectable.
- Use JSON/CSV for intermediate artifacts.
- Use dataclasses for stable internal structures.
- Keep error messages concrete.
- Prefer deterministic outputs when a seed is supplied.

## Current near-term target

Make the repository easy to run locally with a derived CSV corpus:

```bash
python scripts/analyze_corpus.py --candidates data/processed/vowel_lattice_corpus.csv
python scripts/build_overlap_edges.py --candidates data/processed/vowel_lattice_corpus.csv --output data/processed/candidate_overlap_edges.csv
python scripts/generate_events.py --candidates data/processed/vowel_lattice_corpus.csv --seed 20260621 --steps 64 --output outputs/render_events.json
python scripts/analyze_sequence.py --input outputs/render_events.json
```
