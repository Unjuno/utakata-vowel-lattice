# Model Design

The first implementable model is a constrained overlap Markov lattice model.

## Model name

```text
Constrained Overlap Markov Lattice Model
```

or, in implementation terms:

```text
OverlapMarkovGenerator
```

## Goal

Generate a vowel-like instrumental event stream by satisfying continuity constraints while maximizing overlap among lexical, phonological, and prosodic candidates.

The model does not optimize for semantic narrative coherence. It optimizes for candidate continuity and controlled ambiguity.

## State

A generator state contains:

```python
state = {
    "vowels": "いいえあいおおう",
    "last_candidates": [...],
    "ngram_counts": {...},
    "entropy": 2.1,
    "prosody_state": {...},
    "time_sec": 12.4,
}
```

## Candidate

Each candidate has lexical, phonological, and prosodic information.

```json
{
  "id": "cand_000123",
  "surface": "愛を追う",
  "reading": "あいをおう",
  "vowel": "あいおおう",
  "frequency": 300,
  "pos_pattern": ["名詞", "助詞", "動詞"],
  "prosody_candidates": ["rise_fall", "level_fall"]
}
```

## Constraints

### Hard constraints

1. Lexical coverage: every output vowel position should be covered by one or more candidates.
2. Lattice connectivity: most adopted candidates should belong to one connected component.
3. Physical prosody: F0, energy, duration, and gap values should remain renderable.

### Soft constraints

1. Maximize vowel overlap.
2. Maximize lexical overlap.
3. Maximize phonological similarity.
4. Maximize prosody-lattice compatibility.
5. Prefer high-frequency candidates.
6. Stay in an entropy band.
7. Penalize isolated candidates.
8. Penalize repetitive patterns.
9. Penalize prosodic discontinuity.

## Objective

For next lexical candidate `c` and prosody candidate `r` under current state `s`:

```text
S(c, r | s)
  = α O_overlap(c, s)
  + β F(c)
  + γ P(c, s)
  + δ K(r, s)
  + η L(c, s)
  + θ E(c, r, s)
  - λ D(r, s)
  - ρ Rep(c, r, s)
```

| Term | Meaning |
|---|---|
| `O_overlap` | Vowel and segment overlap |
| `F` | Frequency score |
| `P` | Phonological similarity |
| `K` | Prosody-lattice compatibility |
| `L` | Lattice connectivity gain |
| `E` | Entropy-band fit |
| `D` | Prosodic discontinuity penalty |
| `Rep` | Repetition penalty |

Selection uses softmax:

```text
p(c, r | s) = exp(S(c,r|s) / τ) / Σ exp(S(c',r'|s) / τ)
```

Temperature `τ` controls determinism.

## Entropy control

Entropy is not maximized. It is kept within a useful band.

Low entropy creates repetition. High entropy creates noise. The target range should depend on mode:

| Mode | Vowel entropy | Prosody entropy | Intended perception |
|---|---:|---:|---|
| stable | low-mid | low-mid | language-like |
| branching | mid | mid | listener-dependent |
| dense | mid-high | mid-high | overlapping meanings |
| collapse | high but bounded | high but bounded | semantic instability |
| reconnect | mid | low-mid | return to legibility |

## Prosody lattice

Prosody is not random rhythm. It is another lattice layer. Candidate phrases carry possible F0, duration, energy, and boundary-strength patterns. The output prosody field should be compatible with many candidate readings without fixing exactly one.

## Output

The model should first output `render_events.json`, not final audio.

```json
{
  "seed": 20260621,
  "events": [
    {
      "time": 0.0,
      "candidate_id": "cand_000001",
      "surface": "いいえ",
      "vowels": "いいえ",
      "f0_hz": [220, 224, 218],
      "duration_sec": [0.24, 0.20, 0.28],
      "energy": [0.6, 0.7, 0.55],
      "gap_after": 0.12
    }
  ]
}
```
