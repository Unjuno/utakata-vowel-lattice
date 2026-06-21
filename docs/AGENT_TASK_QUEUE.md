# Agent Task Queue

Use this as the implementation queue for local or autonomous coding agents.

## Task 1: Candidate corpus ingestion

Goal: turn a derived CSV into `Candidate` objects.

Existing files:

- `src/utakata_vowel_lattice/corpus_io.py`
- `docs/CORPUS_DESIGN.md`

Implement or improve:

- robust handling of `compressed_vowel`;
- optional `pos_pattern` parsing;
- optional prosody columns;
- validation report output.

Acceptance:

```bash
python scripts/analyze_corpus.py --candidates data/processed/vowel_lattice_corpus.csv
pytest
```

## Task 2: Overlap-edge export

Goal: create `candidate_overlap_edges.csv` from candidates.

Implement:

```text
scripts/build_overlap_edges.py
```

Required output columns:

```csv
from_id,to_id,overlap_ratio,from_vowel,to_vowel
```

Acceptance:

```bash
python scripts/build_overlap_edges.py \
  --candidates data/processed/vowel_lattice_corpus.csv \
  --output data/processed/candidate_overlap_edges.csv
```

## Task 3: Generator uses external corpus

Goal: `generate_events.py` should optionally load candidates from CSV instead of the small demo list.

Add:

```bash
python scripts/generate_events.py \
  --candidates data/processed/vowel_lattice_corpus.csv \
  --seed 20260621 \
  --steps 64 \
  --output outputs/render_events.json
```

Acceptance:

- default demo still works;
- CSV mode works;
- seed produces reproducible JSON.

## Task 4: Prosody-lattice enrichment

Goal: parse prosody columns when available.

Potential columns:

```csv
prosody_id,contour_class,f0_pattern,duration_pattern,energy_pattern,gap_after,boundary_strength
```

Rules:

- missing prosody columns fallback to `DEFAULT_PROSODY`;
- malformed prosody rows should be reported, not silently accepted.

## Task 5: Render-event analysis

Goal: make `scripts/analyze_sequence.py` useful for generated event logs.

Existing:

- `src/utakata_vowel_lattice/analysis.py`
- `scripts/analyze_sequence.py`

Add later:

- repetition window metrics;
- entropy over time windows;
- prosodic discontinuity histogram;
- lexical candidate recurrence report.

## Task 6: Minimal audio renderer

Do this only after event JSON is stable.

Goal:

```text
render_events.json -> simple wav
```

Start with a synthetic carrier. Avoid committing generated wav files.

## Task 7: Local heavy corpus builder

Goal:

```text
source corpus / dictionary table -> vowel_lattice_corpus.csv
```

Keep corpus-specific code isolated. Do not commit source corpus files.

## Task 8: Listener-response schema

Goal: prepare future evaluation.

Potential schema:

```csv
response_id,seed,event_file,listener_id,time_range,heard_text,confidence,scene_description,notes
```

This is not required for the first generator.
