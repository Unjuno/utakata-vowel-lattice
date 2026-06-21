# Resource Collection

The repository assumes that the user collects required data and tools locally. Do not commit raw external corpora unless redistribution is explicitly permitted.

## Collection principle

Collect resources locally, then transform them into the repository contracts:

```text
raw source material
  -> local processing
  -> data/processed/vowel_lattice_corpus.csv
  -> data/processed/candidate_overlap_edges.csv
  -> outputs/render_events.json
```

The repository should only need the derived CSV/JSON contracts to run.

## Minimum resources to collect

### 1. Lexical frequency data

Purpose:

- prioritize words and phrases that are likely to be perceptually recoverable;
- avoid low-probability candidate clutter;
- compute frequency scores for the Markov generator.

Needed fields:

```csv
surface,reading,frequency,pos_pattern,source
```

Notes:

- Frequency can be corpus count, normalized frequency, or a manually assigned proxy.
- Keep raw source tables under `data/raw/` or outside the repository.
- Commit only derived small fixtures or processed tables when license permits.

### 2. Readings and morphological metadata

Purpose:

- convert surface forms to vowel skeletons;
- support POS-pattern constraints;
- generate candidate words and short phrases.

Needed fields:

```csv
surface,reading,pos,lemma,source
```

Notes:

- The first implementation only requires `surface`, `reading`, and `frequency`.
- POS and lemma become useful when phrase candidates are added.

### 3. Candidate phrase data

Purpose:

- move beyond isolated words;
- create overlapping phrase-level lattice nodes;
- prevent the output from becoming single-word fragments.

Needed fields:

```csv
candidate_id,surface,reading,vowel,frequency,pos_pattern,source
```

Notes:

- Phrase candidates may be corpus-derived or hand-curated.
- Hand-curated rows are acceptable for early experiments.

### 4. Prosody candidates

Purpose:

- add F0, duration, energy, and boundary candidates;
- make prosody overlap part of generation rather than random rhythm.

Recommended fields:

```csv
candidate_id,contour_class,f0_pattern,duration_pattern,energy_pattern,gap_after,boundary_strength
```

Pattern format:

```text
220 224 219
0.22 0.20 0.28
0.60 0.70 0.58
```

### 5. Instrument carriers

Purpose:

- render vowel-like sound without ordinary human singing;
- test synthetic, flute-like, and stretched-piano carriers.

Suggested local paths:

```text
assets/carriers/synth/
assets/carriers/flute/
assets/carriers/piano_stretched/
```

Do not commit large audio assets unless licensing and size are acceptable.

### 6. Listener-response data

Purpose:

- evaluate whether listeners infer different lyrics, sentences, scenes, or meanings.

Future schema:

```csv
response_id,seed,event_file,listener_id,time_range,heard_text,confidence,scene_description,notes
```

## Local path convention

```text
data/raw/             raw source files, ignored by Git
data/interim/         temporary transformed tables, ignored by Git
data/processed/       derived corpus and edge tables, ignored by Git by default
outputs/              generated event logs, reports, and audio, ignored by Git
assets/               optional local carrier sounds, should usually stay ignored
```

## What to commit

Commit:

- scripts;
- schemas;
- small hand-written fixtures;
- configuration;
- markdown reports;
- small generated JSON examples only when useful.

Do not commit by default:

- raw corpora;
- licensed dictionary dumps;
- large frequency tables;
- generated WAV files;
- private listener-response data;
- large instrument sample libraries.

## First practical collection target

Create this file locally first:

```text
data/processed/vowel_lattice_corpus.csv
```

Minimum valid example:

```csv
candidate_id,surface,reading,vowel,frequency,pos_pattern,source
cand_0001,いいえ,いいえ,いいえ,1200,応答,manual
cand_0002,良い絵,よいえ,おいえ,430,形容詞+名詞,manual
cand_0003,愛を追う,あいをおう,あいおおう,300,名詞+助詞+動詞,manual
cand_0004,藍を覆う,あいをおおう,あいおおう,70,名詞+助詞+動詞,manual
cand_0005,青い家,あおいいえ,あおいいえ,220,形容詞+名詞,manual
```

Then run:

```bash
python scripts/analyze_corpus.py --candidates data/processed/vowel_lattice_corpus.csv
```

## Agent handoff

When handing work to an agent, provide:

1. which collected resource exists;
2. local path;
3. license status;
4. intended derived output;
5. acceptance command.

Example:

```text
Resource: hand-curated candidate CSV
Path: data/processed/vowel_lattice_corpus.csv
License: original/manual, OK to use locally
Task: implement CSV-backed generation
Acceptance: python scripts/generate_events.py --candidates data/processed/vowel_lattice_corpus.csv --seed 20260621 --steps 64
```
