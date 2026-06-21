# Local Analysis Plan

This project should support heavy local analysis without committing heavy raw data.

## Why local analysis

Corpus-scale processing can become large quickly:

- morphological dictionary expansion;
- source-corpus frequency tables;
- candidate phrase extraction;
- all-pairs overlap computation;
- generated-event analysis;
- audio feature analysis.

These should run locally against ignored data paths. Git should contain code, schemas, small fixtures, and summarized reports.

## Artifact flow

```text
data/raw/*                         ignored source data
  -> data/interim/*.csv             optional intermediate tables
  -> data/processed/*.csv           derived candidate/edge tables
  -> outputs/render_events.json     generated event logs
  -> outputs/analysis/*.json|md     analysis reports
```

## Core analysis functions

### Corpus validation

Check that `vowel_lattice_corpus.csv` has required fields:

- `candidate_id`
- `surface`
- `reading`
- `vowel`
- `frequency`

Report:

- missing columns;
- empty vowels;
- duplicate candidate IDs;
- invalid vowel strings;
- frequency parse failures.

### Overlap analysis

Compute suffix-prefix overlap among candidate vowel strings.

Report:

- number of candidates;
- number of overlap edges;
- average overlap ratio;
- largest connected component ratio;
- isolated candidate count.

### Generated-sequence analysis

Analyze `render_events.json`.

Report:

- total events;
- approximate duration;
- final vowel-stream length;
- vowel n-gram entropy;
- repeated candidate IDs;
- repeated vowel patterns;
- prosodic discontinuity estimates;
- gap and boundary-strength summaries.

### Prosody analysis

Measure continuity across adjacent events:

- F0 jump;
- energy jump;
- duration-pattern jump;
- gap strength;
- boundary strength.

This does not decide whether the music is good. It checks whether the sequence violates the current design constraints.

## Heavy analysis policy

Keep large derived results out of Git by default. Commit only:

- schemas;
- scripts;
- small demo fixtures;
- small markdown summaries;
- reproducible configuration.

## Next implementation targets

1. `src/utakata_vowel_lattice/corpus_io.py`
2. `src/utakata_vowel_lattice/analysis.py`
3. `scripts/analyze_sequence.py`
4. `scripts/build_overlap_edges.py`
