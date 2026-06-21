from utakata_vowel_lattice.phonology import (
    compress_repeated_vowels,
    extract_vowels,
    ngrams,
    overlap_length,
    overlap_ratio,
)


def test_extract_vowels_basic():
    assert extract_vowels("あい") == "あい"
    assert extract_vowels("アオイ") == "あおい"
    assert extract_vowels("あかい") == "ああい"
    assert extract_vowels("あいをおう") == "あいおおう"


def test_compress_repeated_vowels():
    assert compress_repeated_vowels("ああい") == "あい"
    assert compress_repeated_vowels("あいおおう") == "あいおう"


def test_ngrams():
    assert ngrams("あいおう", 2) == ["あい", "いお", "おう"]


def test_overlap():
    assert overlap_length("あいおおう", "おおうあおい") == 3
    assert overlap_ratio("あいおおう", "おおうあおい") == 3 / 5
