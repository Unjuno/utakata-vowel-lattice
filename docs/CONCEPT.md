# Concept

This project creates a generative audio system where Japanese vowel structures are rendered as non-human instrumental sound. The goal is not to output a single correct lyric. The goal is to create conditions where different listeners infer different lyrics, sentences, scenes, or meanings from the same or related vowel-like sound streams.

## Updated concept

The surface sound should not be ordinary human singing. Human voice introduces strong biases: age, gender, vocal identity, accent, breath, AI voice artifacts, and expectations that a fixed lyric exists. Instead, the system should primarily use instrumental carriers shaped by vowel-like formant profiles.

```text
surface: instrumental sound
structure: Japanese vowel lattice
latent layer: overlapping lexical and prosodic candidates
listener layer: perceived lyric / sentence / scene / meaning
```

## What this is not

- Not a normal lyric generator.
- Not a fixed Japanese sentence generator.
- Not a random `a i u e o` sequence.
- Not an AI singer singing hidden lyrics.
- Not a simple mapping from vowels to pitches.

## What this is

A corpus-driven generative instrument that:

1. builds a derived corpus of vowelized Japanese words and phrases;
2. maximizes overlap among lexical, phonological, and prosodic candidates;
3. controls entropy to avoid both repetition and noise;
4. renders the result as instrumental sound with vowel-like formant structure;
5. records seed, model settings, candidate logs, and audio-event logs for reproducibility.

## Work title

`utakata-vowel-lattice`: a vowel-lattice generative instrument.
