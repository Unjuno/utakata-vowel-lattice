# Agent Instructions

This repository is a research scaffold for a corpus-driven vowel-lattice generative instrument.

Agents should preserve the core design:

```text
source corpora
  -> derived vowel-lattice corpus
  -> constrained overlap Markov lattice model
  -> prosody-lattice field
  -> instrumental formant rendering
  -> listener-side lyric emergence
```

## Non-negotiable constraints

1. Do not replace the core model with an opaque decode-only text generator.
2. Do not commit raw external corpora unless redistribution is explicitly permitted.
3. Keep heavy corpus parsing and large analysis local; commit scripts, schemas, small fixtures, and reports only.
4. Preserve seedability and event logs for reproducibility.
5. Keep lexical overlap and prosodic overlap separate but jointly scored.
6. Do not treat rhythm as random post-processing. Prosody should be derived from candidate overlap and prosody-lattice compatibility.

## Preferred implementation style

- Small modules.
- Dependency-light Python first.
- Pure functions where possible.
- JSON/CSV I/O for generated intermediate artifacts.
- Tests for phonology, entropy, overlap, corpus loading, and analysis functions.
- Avoid hidden state outside explicit seed and config.

## Local-heavy pipeline

Raw corpus data should live outside Git or under ignored paths such as `data/raw/`.

Expected local flow:

```bash
python scripts/build_corpus.py --input data/raw/source.csv --output data/processed/vowel_lattice_corpus.csv
python scripts/build_overlap_edges.py --candidates data/processed/vowel_lattice_corpus.csv --output data/processed/candidate_overlap_edges.csv
python scripts/generate_events.py --seed 20260621 --steps 64 --output outputs/render_events.json
python scripts/analyze_sequence.py --input outputs/render_events.json
```

## Priority tasks

1. Implement robust CSV loading for `vowel_lattice_corpus.csv`.
2. Implement overlap-edge generation.
3. Implement sequence analysis reports.
4. Implement event-to-audio rendering only after event JSON is inspectable.
5. Add optional dependencies only when the analysis requires them.

## Definition of done for a change

- `pytest` passes.
- New scripts have `--help` and clear input/output arguments.
- No large corpus files or generated audio are committed.
- Any new metric is documented in `docs/` or a module docstring.
