"""CSV I/O for derived vowel-lattice corpora."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from .overlap_markov import Candidate
from .phonology import extract_vowels, is_vowel_string
from .prosody_lattice import DEFAULT_PROSODY

REQUIRED_COLUMNS = {"candidate_id", "surface", "reading", "vowel", "frequency"}


@dataclass(frozen=True)
class CorpusValidationReport:
    """Validation summary for a candidate corpus."""

    path: str
    row_count: int
    missing_columns: tuple[str, ...]
    duplicate_ids: tuple[str, ...]
    invalid_vowel_rows: tuple[int, ...]
    empty_vowel_rows: tuple[int, ...]
    frequency_error_rows: tuple[int, ...]

    @property
    def ok(self) -> bool:
        return not (
            self.missing_columns
            or self.duplicate_ids
            or self.invalid_vowel_rows
            or self.empty_vowel_rows
            or self.frequency_error_rows
        )


def validate_candidate_csv(path: str | Path) -> CorpusValidationReport:
    """Validate a derived vowel-lattice candidate CSV."""
    csv_path = Path(path)
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = set(reader.fieldnames or [])
        missing_columns = tuple(sorted(REQUIRED_COLUMNS - fieldnames))
        seen: set[str] = set()
        duplicate_ids: list[str] = []
        invalid_vowel_rows: list[int] = []
        empty_vowel_rows: list[int] = []
        frequency_error_rows: list[int] = []
        row_count = 0
        for row_index, row in enumerate(reader, start=2):
            row_count += 1
            candidate_id = (row.get("candidate_id") or "").strip()
            if candidate_id in seen:
                duplicate_ids.append(candidate_id)
            seen.add(candidate_id)

            vowel = (row.get("vowel") or "").strip()
            if not vowel:
                empty_vowel_rows.append(row_index)
            elif not is_vowel_string(vowel):
                invalid_vowel_rows.append(row_index)

            try:
                float((row.get("frequency") or "0").strip())
            except ValueError:
                frequency_error_rows.append(row_index)

    return CorpusValidationReport(
        path=str(csv_path),
        row_count=row_count,
        missing_columns=missing_columns,
        duplicate_ids=tuple(duplicate_ids),
        invalid_vowel_rows=tuple(invalid_vowel_rows),
        empty_vowel_rows=tuple(empty_vowel_rows),
        frequency_error_rows=tuple(frequency_error_rows),
    )


def load_candidates_csv(path: str | Path) -> list[Candidate]:
    """Load candidates from a derived corpus CSV.

    This loader is intentionally small. Prosody-specific columns can be added
    later; for now each candidate receives DEFAULT_PROSODY.
    """
    report = validate_candidate_csv(path)
    if report.missing_columns:
        raise ValueError(f"missing required columns: {', '.join(report.missing_columns)}")

    candidates: list[Candidate] = []
    with Path(path).open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            reading = (row.get("reading") or "").strip()
            vowel = (row.get("vowel") or "").strip() or extract_vowels(reading)
            if not is_vowel_string(vowel):
                continue
            frequency = float((row.get("frequency") or "1").strip())
            pos_pattern = tuple(
                item.strip()
                for item in (row.get("pos_pattern") or "").replace("+", "|").split("|")
                if item.strip()
            )
            candidates.append(
                Candidate(
                    candidate_id=(row.get("candidate_id") or "").strip(),
                    surface=(row.get("surface") or "").strip(),
                    reading=reading,
                    vowel=vowel,
                    frequency=frequency,
                    pos_pattern=pos_pattern,
                    prosody_candidates=(DEFAULT_PROSODY,),
                )
            )
    return candidates
