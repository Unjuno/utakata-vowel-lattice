# Work Packages

These are small implementation units for coding agents. Each package should be implementable in one focused PR.

## WP-001: Export overlap edges

### Goal

Create `scripts/build_overlap_edges.py`.

### Inputs

```text
data/processed/vowel_lattice_corpus.csv
```

### Outputs

```text
data/processed/candidate_overlap_edges.csv
```

Required CSV columns:

```csv
from_id,to_id,overlap_ratio,from_vowel,to_vowel
```

### Implementation notes

- Use `load_candidates_csv` from `corpus_io.py`.
- Use `build_overlap_edges` from `analysis.py`.
- Add `--min-overlap` argument, default `0.2`.
- Write UTF-8 CSV.

### Acceptance

```bash
python scripts/build_overlap_edges.py \
  --candidates data/processed/vowel_lattice_corpus.csv \
  --output data/processed/candidate_overlap_edges.csv
python scripts/analyze_corpus.py --candidates data/processed/vowel_lattice_corpus.csv
pytest
```

## WP-002: Let generator read candidate CSV

### Goal

Extend `scripts/generate_events.py` with `--candidates`.

### Current behavior

Without `--candidates`, it uses demo candidates.

### Required behavior

With `--candidates`, load candidates via `load_candidates_csv`.

```bash
python scripts/generate_events.py \
  --candidates data/processed/vowel_lattice_corpus.csv \
  --seed 20260621 \
  --steps 64 \
  --output outputs/render_events.json
```

### Acceptance

- Demo mode still works.
- CSV mode works.
- Same seed and same input produce identical JSON.
- Missing candidate file gives a concrete error.

## WP-003: Add small demo candidate fixture

### Goal

Add a small committed fixture for local tests.

### Path

```text
tests/fixtures/vowel_lattice_corpus.small.csv
```

### Requirements

- 5-10 rows.
- Valid required columns.
- At least one duplicated vowel pattern.
- At least one suffix-prefix overlap.
- No external corpus data.

### Acceptance

```bash
python scripts/analyze_corpus.py --candidates tests/fixtures/vowel_lattice_corpus.small.csv
python scripts/build_overlap_edges.py --candidates tests/fixtures/vowel_lattice_corpus.small.csv --output outputs/test_edges.csv
pytest
```

## WP-004: Strengthen corpus validation

### Goal

Make `validate_candidate_csv` report warnings without rejecting usable files.

### Add checks

- missing `reading`;
- missing `surface`;
- frequency < 0;
- `usable_as_node=false` support;
- `compressed_vowel` invalid when present.

### Acceptance

- Valid fixture passes.
- Invalid fixture fails with precise row numbers.

## WP-005: Windowed sequence analysis

### Goal

Extend sequence analysis with sliding-window metrics.

### Metrics

- 2-gram entropy over windows;
- 3-gram entropy over windows;
- candidate recurrence over recent windows;
- F0 jump summary;
- boundary-strength summary.

### Output

Add fields to JSON report, keeping existing fields stable.

## WP-006: Prosody parsing from CSV

### Goal

Parse optional prosody columns into `ProsodyCandidate`.

### Columns

```csv
contour_class,f0_pattern,duration_pattern,energy_pattern,gap_after,boundary_strength
```

Pattern format may be space-separated floats.

### Acceptance

- Missing prosody columns fallback to `DEFAULT_PROSODY`.
- Malformed patterns return validation errors.

## WP-007: Minimal audio renderer

### Goal

Render event JSON to a simple WAV file.

### Constraints

- Do not commit generated WAV files.
- Start with a synthetic carrier.
- Use `formant.py` metadata but keep rendering simple.
- Put generated audio under ignored `outputs/audio/`.

### CLI

```bash
python scripts/render_audio.py \
  --input outputs/render_events.json \
  --output outputs/audio/render.wav
```

## WP-008: GitHub Actions CI

### Goal

Add a lightweight CI workflow.

### Requirements

- Python 3.11.
- Install package editable.
- Run `pytest`.
- No corpus downloads.

## WP-009: Listener-response schema

### Goal

Add schema and docs for future listening tests.

### Output path

```text
docs/LISTENER_RESPONSE_SCHEMA.md
```

### Include

```csv
response_id,seed,event_file,listener_id,time_range,heard_text,confidence,scene_description,notes
```

## WP-010: Mode profiles

### Goal

Make `stable`, `branching`, `dense`, `collapse`, `reconnect` modes usable in generation.

### Requirements

- Read from `configs/generation.yml` or a small internal default.
- Mode controls target entropy and temperature.
- Existing explicit weight arguments should override mode defaults when present.
