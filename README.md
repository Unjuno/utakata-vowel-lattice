# utakata-vowel-lattice

`utakata-vowel-lattice` is a research-stage project for building a corpus-driven generative instrument from Japanese vowel structures.

The system does **not** sing fixed lyrics. It generates overlapping vowel-lattice structures from Japanese lexical and phonological data, then renders them as non-human instrumental sound with vowel-like formant profiles. The intended result is an audio stream where lyrics, sentences, scenes, or meanings emerge differently in each listener.

## Core idea

```text
source corpora
  -> word / phrase / reading / frequency data
  -> vowelized candidate corpus
  -> overlap-maximizing Markov lattice model
  -> prosody-lattice field
  -> instrument carrier + vowel formant rendering
  -> listener-side lyric emergence
```

The project treats lyrics as a latent structure rather than a surface text. The surface is a stream of vowel-like instrumental sound. The underlying model keeps lexical candidates, vowel overlap, phonological similarity, corpus frequency, entropy targets, and prosodic continuity in play at the same time.

## Current design decision

The first model should be an **entropy-controlled weighted Markov lattice generator**, not a decode-only language model. The reasons are practical: it is lightweight, inspectable, seedable, and allows explicit control over overlap, repetition, frequency, phonology, prosody, and entropy.

## Main constraints

1. **Lexical coverage**: each vowel position should be covered by at least one candidate word or phrase.
2. **Boundary bridging**: candidate boundaries should often be crossed by other candidates, preventing hard segmentation.
3. **Lattice connectivity**: adopted candidates should mostly belong to one connected lattice.
4. **Prosodic continuity**: F0, duration, energy, and boundary strength should not break arbitrarily.
5. **Ambiguity preservation**: the model should avoid collapsing into one fixed lyric.
6. **Entropy band control**: vowel, lexical-path, and prosodic entropy should stay within a useful range, neither repetitive nor random.

## Repository status

Concept: fixed enough to implement.  
Method: under research.  
Implementation: scaffold phase.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python scripts/generate_events.py --seed 20260621 --steps 16
```

This writes a small `outputs/render_events.json` file containing generated vowel/prosody events. It is not the final audio renderer yet.

## For coding agents

Start here:

- [`AGENTS.md`](AGENTS.md): non-negotiable project rules and local-heavy pipeline
- [`.github/copilot-instructions.md`](.github/copilot-instructions.md): concise coding-agent entrypoint
- [`docs/IMPLEMENTATION_CONTRACTS.md`](docs/IMPLEMENTATION_CONTRACTS.md): stable CSV, JSON, CLI, and object contracts
- [`docs/WORK_PACKAGES.md`](docs/WORK_PACKAGES.md): small implementation tasks with acceptance criteria
- [`docs/AGENT_PROMPTS.md`](docs/AGENT_PROMPTS.md): copyable prompts for autonomous coding agents
- [`docs/RESOURCE_COLLECTION.md`](docs/RESOURCE_COLLECTION.md): what to collect locally and how to hand resources to agents

## Documents

- [`docs/CONCEPT.md`](docs/CONCEPT.md): project concept
- [`docs/CORPUS_DESIGN.md`](docs/CORPUS_DESIGN.md): derived corpus schema
- [`docs/MODEL_DESIGN.md`](docs/MODEL_DESIGN.md): constrained overlap Markov model
- [`docs/AUDIO_DESIGN.md`](docs/AUDIO_DESIGN.md): instrumental formant rendering plan
- [`docs/LOCAL_ANALYSIS_PLAN.md`](docs/LOCAL_ANALYSIS_PLAN.md): local-heavy analysis plan
- [`docs/RESOURCE_COLLECTION.md`](docs/RESOURCE_COLLECTION.md): local resource checklist

## Data policy

Do not commit raw external corpora unless their license explicitly permits redistribution. This repository should contain scripts, schemas, small examples, generated metadata, and reproducible processing steps.
