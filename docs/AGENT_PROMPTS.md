# Agent Prompts

Copy one of these prompts into a coding agent. Each prompt is intentionally narrow.

## Prompt: WP-001 overlap edges

Implement `WP-001: Export overlap edges` from `docs/WORK_PACKAGES.md`.

Read first:

- `AGENTS.md`
- `docs/IMPLEMENTATION_CONTRACTS.md`
- `src/utakata_vowel_lattice/corpus_io.py`
- `src/utakata_vowel_lattice/analysis.py`

Task:

- Create `scripts/build_overlap_edges.py`.
- Input: `--candidates` CSV path.
- Output: `--output` CSV path.
- Optional: `--min-overlap`, default `0.2`.
- Required output columns: `from_id,to_id,overlap_ratio,from_vowel,to_vowel`.
- Add a small fixture if needed, but do not commit raw external corpus data.
- Add or update tests if feasible.

Acceptance:

```bash
python scripts/build_overlap_edges.py --candidates tests/fixtures/vowel_lattice_corpus.small.csv --output outputs/test_edges.csv
pytest
```

## Prompt: WP-002 CSV-backed generation

Implement `WP-002: Let generator read candidate CSV` from `docs/WORK_PACKAGES.md`.

Read first:

- `AGENTS.md`
- `docs/IMPLEMENTATION_CONTRACTS.md`
- `scripts/generate_events.py`
- `src/utakata_vowel_lattice/corpus_io.py`

Task:

- Add optional `--candidates` to `scripts/generate_events.py`.
- If omitted, keep the current demo-candidate behavior.
- If supplied, load candidates with `load_candidates_csv`.
- Preserve deterministic output for identical seed and input.
- Produce concrete errors for missing or invalid CSV files.

Acceptance:

```bash
python scripts/generate_events.py --seed 20260621 --steps 16 --output outputs/demo_events.json
python scripts/generate_events.py --candidates tests/fixtures/vowel_lattice_corpus.small.csv --seed 20260621 --steps 16 --output outputs/csv_events.json
pytest
```

## Prompt: WP-003 small fixture

Implement `WP-003: Add small demo candidate fixture` from `docs/WORK_PACKAGES.md`.

Task:

- Create `tests/fixtures/vowel_lattice_corpus.small.csv`.
- Use 5-10 hand-written rows only.
- Include required columns: `candidate_id,surface,reading,vowel,frequency`.
- Include `pos_pattern` if useful.
- Ensure at least one suffix-prefix overlap and at least one shared vowel pattern.
- Do not use external corpus data.

Acceptance:

```bash
python scripts/analyze_corpus.py --candidates tests/fixtures/vowel_lattice_corpus.small.csv
pytest
```

## Prompt: WP-006 prosody parsing

Implement `WP-006: Prosody parsing from CSV` from `docs/WORK_PACKAGES.md`.

Read first:

- `src/utakata_vowel_lattice/prosody_lattice.py`
- `src/utakata_vowel_lattice/corpus_io.py`
- `docs/IMPLEMENTATION_CONTRACTS.md`

Task:

- Parse optional columns: `contour_class,f0_pattern,duration_pattern,energy_pattern,gap_after,boundary_strength`.
- Space-separated float patterns are acceptable.
- Missing columns fallback to `DEFAULT_PROSODY`.
- Malformed values should appear in validation reports.

Acceptance:

```bash
pytest
python scripts/analyze_corpus.py --candidates tests/fixtures/vowel_lattice_corpus.small.csv
```

## Prompt: WP-008 CI

Implement `WP-008: GitHub Actions CI` from `docs/WORK_PACKAGES.md`.

Task:

- Add `.github/workflows/ci.yml`.
- Use Python 3.11.
- Install the package with `pip install -e .`.
- Run `pytest`.
- Do not download external corpora.

Acceptance:

- Workflow file is valid YAML.
- Local `pytest` passes.
