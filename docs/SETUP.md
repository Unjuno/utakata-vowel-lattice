# Setup

This document describes the local setup path. The repository is designed so that installation and basic checks are automatic, while heavy corpus resources remain local.

## Requirements

- Python 3.11 or newer
- POSIX shell for `scripts/bootstrap.sh` or `make`

## Fast setup

```bash
./scripts/bootstrap.sh
```

Equivalent Makefile command:

```bash
make setup
```

This will:

1. create `.venv`;
2. upgrade `pip`;
3. install the package in editable mode with development dependencies;
4. run `scripts/doctor.py`.

## Manual setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e ".[dev]"
python scripts/doctor.py
pytest
```

## Local directories

`doctor.py` creates these directories if missing:

```text
data/raw/
data/interim/
data/processed/
outputs/
outputs/analysis/
outputs/audio/
assets/carriers/
```

These are local working directories. Most are ignored by Git.

## Common commands

```bash
make doctor        # check local environment
make test          # run tests
make demo          # generate outputs/render_events.json
make analyze-demo  # generate demo events and sequence analysis
make clean         # remove outputs and caches
```

Without Make:

```bash
python scripts/generate_events.py --seed 20260621 --steps 16 --output outputs/render_events.json
python scripts/analyze_sequence.py --input outputs/render_events.json --json-report outputs/analysis/sequence.json --md-report outputs/analysis/sequence.md
```

## Local resources

The user collects raw resources locally. Start with:

```text
data/processed/vowel_lattice_corpus.csv
```

Minimum columns:

```csv
candidate_id,surface,reading,vowel,frequency
```

Recommended columns:

```csv
compressed_vowel,pos_pattern,semantic_tags,source,usable_as_node
```

See `docs/RESOURCE_COLLECTION.md` for the complete resource checklist.

## Agent workflow

After setup, an implementation agent should work from:

1. `AGENTS.md`
2. `.github/copilot-instructions.md`
3. `docs/IMPLEMENTATION_CONTRACTS.md`
4. `docs/WORK_PACKAGES.md`
5. `docs/AGENT_PROMPTS.md`

Recommended first tasks:

```text
WP-003 small fixture
WP-001 overlap-edge export
WP-002 CSV-backed generation
WP-008 CI
```

## Do not commit

- raw corpora;
- licensed dictionary dumps;
- generated WAV files;
- large instrument samples;
- private listener-response data;
- `.env`;
- `.venv`.
