---
name: Work package
description: A narrow implementation task for a coding agent
title: "WP-XXX: "
labels: ["work-package"]
body:
  - type: textarea
    id: goal
    attributes:
      label: Goal
      description: What should be implemented?
    validations:
      required: true
  - type: textarea
    id: files
    attributes:
      label: Files to read first
      description: List relevant docs and source files.
      value: |
        - AGENTS.md
        - docs/IMPLEMENTATION_CONTRACTS.md
        - docs/WORK_PACKAGES.md
    validations:
      required: true
  - type: textarea
    id: contract
    attributes:
      label: Input / output contract
      description: CLI, function, CSV, JSON, or file contract.
    validations:
      required: true
  - type: textarea
    id: acceptance
    attributes:
      label: Acceptance commands
      description: Commands that must pass.
      value: |
        ```bash
        pytest
        ```
    validations:
      required: true
  - type: checkboxes
    id: constraints
    attributes:
      label: Constraints
      options:
        - label: Do not commit raw external corpus data.
          required: true
        - label: Do not commit generated audio.
          required: true
        - label: Preserve seedability for stochastic outputs.
          required: true
        - label: Keep lexical and prosodic overlap separate but jointly scored.
          required: true
---
