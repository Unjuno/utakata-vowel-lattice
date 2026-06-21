# Implementation Contracts

This file defines stable interfaces for coding agents. Treat these as contracts unless a task explicitly changes them.

## 1. Candidate corpus CSV

Path convention:

```text
data/processed/vowel_lattice_corpus.csv
```

Required columns:

```csv
candidate_id,surface,reading,vowel,frequency
```

Recommended columns:

```csv
compressed_vowel,pos_pattern,semantic_tags,source,usable_as_node
```

Rules:

- `candidate_id` must be unique.
- `vowel` must contain only `あいうえお`.
- `frequency` must parse as a non-negative float.
- `surface` and `reading` must not be silently discarded.
- If `vowel` is missing, code may derive it from `reading`, but the validation report must mention missing values.

## 2. Candidate object

Current implementation:

```python
Candidate(
    candidate_id: str,
    surface: str,
    reading: str,
    vowel: str,
    frequency: float,
    pos_pattern: tuple[str, ...],
    prosody_candidates: tuple[ProsodyCandidate, ...],
)
```

Do not make this object depend on external corpus libraries.

## 3. Prosody candidate

Current implementation:

```python
ProsodyCandidate(
    contour_class: str,
    f0_pattern: tuple[float, ...],
    duration_pattern: tuple[float, ...],
    energy_pattern: tuple[float, ...],
    gap_after: float,
    boundary_strength: float,
)
```

Interpretation:

- `f0_pattern`: local F0 contour in Hz.
- `duration_pattern`: per-vowel or per-control-point durations in seconds.
- `energy_pattern`: normalized 0-1 values.
- `gap_after`: gap after candidate, in seconds or relative render units.
- `boundary_strength`: perceived boundary strength, 0-1 preferred.

## 4. Overlap-edge CSV

Path convention:

```text
data/processed/candidate_overlap_edges.csv
```

Required columns:

```csv
from_id,to_id,overlap_ratio,from_vowel,to_vowel
```

Recommended columns:

```csv
overlap_len,phonological_similarity,prosody_similarity
```

Rules:

- Directed edges are allowed.
- Suffix-prefix overlap is the first required edge type.
- Do not compute all-pairs overlap in memory for very large corpora without chunking or indexing.

## 5. Generated event JSON

Path convention:

```text
outputs/render_events.json
```

Required top-level keys:

```json
{
  "seed": 20260621,
  "steps": 64,
  "vowel_stream": "...",
  "events": []
}
```

Each event should contain:

```json
{
  "time": 0.0,
  "candidate_id": "cand_0001",
  "surface": "...",
  "reading": "...",
  "vowels": "あいお",
  "score": 1.23,
  "prosody": {
    "contour_class": "level",
    "f0_hz": [220, 222, 219],
    "duration_sec": [0.2, 0.2, 0.2],
    "energy": [0.6, 0.7, 0.6],
    "gap_after": 0.08,
    "boundary_strength": 0.15
  }
}
```

## 6. CLI contracts

### `scripts/analyze_corpus.py`

Required:

```bash
python scripts/analyze_corpus.py --candidates data/processed/vowel_lattice_corpus.csv
```

Optional:

```bash
--min-overlap 0.2
--json-report outputs/analysis/corpus.json
--md-report outputs/analysis/corpus.md
```

### `scripts/build_overlap_edges.py`

Required future contract:

```bash
python scripts/build_overlap_edges.py \
  --candidates data/processed/vowel_lattice_corpus.csv \
  --output data/processed/candidate_overlap_edges.csv
```

### `scripts/generate_events.py`

Current demo mode:

```bash
python scripts/generate_events.py --seed 20260621 --steps 16 --output outputs/render_events.json
```

Future CSV mode:

```bash
python scripts/generate_events.py \
  --candidates data/processed/vowel_lattice_corpus.csv \
  --seed 20260621 \
  --steps 64 \
  --output outputs/render_events.json
```

### `scripts/analyze_sequence.py`

Required:

```bash
python scripts/analyze_sequence.py --input outputs/render_events.json
```

Optional:

```bash
--json-report outputs/analysis/sequence.json
--md-report outputs/analysis/sequence.md
```

## 7. Testing contract

Minimum test command:

```bash
pytest
```

If heavy dependencies are added, tests that require them must be explicitly marked or skipped when unavailable.
