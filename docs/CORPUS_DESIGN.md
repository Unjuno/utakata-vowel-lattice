# Corpus Design

The repository should not treat existing corpora as the final material. Existing corpora are source material used to build a derived corpus optimized for vowel-lattice generation.

## Source material

Potential sources:

- word frequency lists;
- morphological dictionaries with readings and part-of-speech information;
- phrase or n-gram tables;
- co-occurrence data;
- manually curated short phrase candidates;
- listener-response data from future tests.

Raw corpus redistribution depends on licensing. Prefer scripts and schema over committing raw data.

## Derived corpus

The central artifact is a vowel-lattice candidate table.

```csv
candidate_id,surface,reading,vowel,compressed_vowel,frequency,pos_pattern,semantic_tags,source,usable_as_node
cand_000001,愛,あい,あい,あい,1000,名詞,affect,bccwj,true
cand_000002,藍,あい,あい,あい,50,名詞,color,bccwj,true
cand_000003,赤い,あかい,ああい,あい,700,形容詞,color,bccwj,true
cand_000004,愛を追う,あいをおう,あいおおう,あいおう,120,名詞+助詞+動詞,action,manual,true
```

## Required columns

| Column | Meaning |
|---|---|
| `candidate_id` | Stable ID |
| `surface` | Original word or phrase |
| `reading` | Reading in kana |
| `vowel` | Strict vowel skeleton |
| `compressed_vowel` | Repeated-vowel compressed skeleton |
| `frequency` | Corpus or derived frequency |
| `pos_pattern` | POS sequence |
| `semantic_tags` | Optional tags, not a hard narrative constraint |
| `source` | Data source |
| `usable_as_node` | Whether candidate can be used in generation |

## Additional tables

### `vowel_frequency_summary.csv`

```csv
vowel,total_frequency,type_count,examples
あい,1850,3,愛|藍|相
ああい,1000,2,赤い|甘い
```

### `candidate_overlap_edges.csv`

```csv
from_id,to_id,overlap_len,overlap_ratio,phonological_similarity
cand_000004,cand_000005,3,0.60,0.82
```

### `prosody_candidates.csv`

```csv
candidate_id,prosody_id,contour_class,duration_pattern,energy_pattern,gap_after,boundary_strength
cand_000004,pros_0001,rise_fall,"0.22 0.18 0.24 0.25 0.31","0.7 0.6 0.75 0.85 0.7",0.12,0.30
```

## Vowelization rules

- `strict_vowel`: extract vowels from the normalized reading.
- `compressed_vowel`: collapse adjacent identical vowels.
- `subsequence_vowel`: optional later extension; do not use in the first corpus because it causes candidate explosion.

Examples:

| Surface | Reading | Strict vowel | Compressed vowel |
|---|---|---|---|
| 愛 | あい | あい | あい |
| 赤い | あかい | ああい | あい |
| 青い家 | あおいいえ | あおいいえ | あおいえ |

## First target

Build a small corpus manually first, then replace it with a source-corpus derived table.
