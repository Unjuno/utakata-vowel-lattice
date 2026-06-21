# Audio Design

The surface output should primarily be instrumental, not human voice. The goal is vowel-like instrumental sound rather than normal singing.

## Principle

A vowel is not a single pitch. It is better represented as a time-varying acoustic event with:

- carrier sound;
- F0 or musical pitch contour;
- formant-like spectral shaping;
- duration;
- energy;
- boundary strength or gap.

## Rendering chain

```text
vowel event
  -> carrier oscillator / sample / instrument model
  -> vowel formant filter
  -> F0 contour
  -> duration and energy envelope
  -> gap / boundary shaping
  -> audio stream
```

## Initial carrier

Start with a synthetic sustained carrier because it is controllable and reproducible. Add flute-like or piano-derived carriers later.

| Carrier | Priority | Reason |
|---|---:|---|
| synthetic sustained tone | 1 | easiest to control |
| flute-like tone | 2 | between voice and instrument |
| stretched piano | 3 | stronger artwork identity, weaker vowel stability |
| human voice | later | strong bias; not the main surface |

## Formant targets

The current implementation uses approximate configurable targets. These are not final phonetic claims and should be treated as synthesis parameters.

```python
{
    "あ": {"F1": 800, "F2": 1200},
    "い": {"F1": 300, "F2": 2200},
    "う": {"F1": 350, "F2": 900},
    "え": {"F1": 500, "F2": 1900},
    "お": {"F1": 500, "F2": 1000},
}
```

## Prosodic continuity

Do not add random rhythm after generation. Prosody should be derived from the same lattice logic as the lexical candidates.

The renderer should consume:

- `F0(t)`;
- `duration`;
- `energy`;
- `gap_after`;
- formant targets.

The system may create phrase-like groups, but those groups should emerge from overlap density and prosody-lattice compatibility, not arbitrary drum-like loops.

## First audio target

The first renderer may produce event JSON only. Audio synthesis can follow after the model is inspectable.
