#!/usr/bin/env python
"""Validate and analyze a vowel-lattice candidate CSV."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from utakata_vowel_lattice.analysis import build_overlap_edges, report_to_dict, summarize_overlap, write_report_markdown
from utakata_vowel_lattice.corpus_io import load_candidates_csv, validate_candidate_csv


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", required=True)
    parser.add_argument("--min-overlap", type=float, default=0.2)
    parser.add_argument("--json-report", default=None)
    parser.add_argument("--md-report", default=None)
    args = parser.parse_args()

    validation = validate_candidate_csv(args.candidates)
    if not validation.ok:
        print(json.dumps({"validation": asdict(validation)}, ensure_ascii=False, indent=2))
        raise SystemExit(1)

    candidates = load_candidates_csv(args.candidates)
    edges = build_overlap_edges(candidates, min_ratio=args.min_overlap)
    overlap = summarize_overlap(candidates, edges)
    data = {
        "validation": asdict(validation),
        "overlap": report_to_dict(overlap),
    }
    print(json.dumps(data, ensure_ascii=False, indent=2))

    if args.json_report:
        out = Path(args.json_report)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.md_report:
        write_report_markdown(overlap, args.md_report, title="Corpus Overlap Analysis")


if __name__ == "__main__":
    main()
