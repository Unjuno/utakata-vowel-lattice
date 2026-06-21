#!/usr/bin/env python
"""Analyze render-events JSON."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from utakata_vowel_lattice.analysis import (
    load_event_payload,
    report_to_dict,
    summarize_sequence,
    write_report_markdown,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--json-report", default=None)
    parser.add_argument("--md-report", default=None)
    args = parser.parse_args()

    payload = load_event_payload(args.input)
    report = summarize_sequence(payload)
    data = report_to_dict(report)
    print(json.dumps(data, ensure_ascii=False, indent=2))

    if args.json_report:
        out = Path(args.json_report)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.md_report:
        write_report_markdown(report, args.md_report, title="Sequence Analysis")


if __name__ == "__main__":
    main()
