"""utakata-vowel-lattice.

A scaffold for constrained overlap Markov lattice generation and
vowel-like instrumental rendering.
"""

from .phonology import compress_repeated_vowels, extract_vowels, ngrams, overlap_length
from .overlap_markov import Candidate, GeneratorWeights, OverlapMarkovGenerator

__all__ = [
    "Candidate",
    "GeneratorWeights",
    "OverlapMarkovGenerator",
    "compress_repeated_vowels",
    "extract_vowels",
    "ngrams",
    "overlap_length",
]
