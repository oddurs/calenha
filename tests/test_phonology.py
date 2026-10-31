import pytest

from calenha.phonology import PhonologyError


@pytest.mark.parametrize(
    ("word", "syllables", "stressed"),
    [
        ("solenha", ["so", "le", "nha"], "le"),
        ("thalírë", ["tha", "lí", "rë"], "lí"),
        ("mirão", ["mi", "rão"], "rão"),
        ("velu", ["ve", "lu"], "ve"),
        ("aswen", ["as", "wen"], "as"),
        ("miraluma", ["mi", "ra", "lu", "ma"], "lu"),
        ("algamar", ["al", "ga", "mar"], "ga"),
        ("ouressa", ["ou", "res", "sa"], "res"),
        ("nevoã", ["ne", "vo", "ã"], "ã"),
        ("brisalma", ["bri", "sal", "ma"], "sal"),
        ("solouro", ["so", "lou", "ro"], "lou"),
        ("pedralta", ["pe", "dral", "ta"], "dral"),
        ("sol", ["sol"], "sol"),
    ],
)
def test_syllables_and_stress(phonology, word, syllables, stressed):
    analysed = phonology.syllabify(word)
    assert [s.text for s in analysed.syllables] == syllables
    assert analysed.syllables[analysed.stress].text == stressed


def test_digraphs_are_single_sounds(phonology):
    assert [s.text for s in phonology.tokenize("calenha")] == ["c", "a", "l", "e", "nh", "a"]
    assert [s.text for s in phonology.tokenize("thalírë")] == ["th", "a", "l", "í", "r", "ë"]


def test_capitals_are_not_spelling(phonology):
    assert phonology.syllabify("Solmara").text == "solmara"


def test_breath_mark_is_ignored_by_sound(phonology):
    assert phonology.syllabify("mi·rão").text == "mirão"


@pytest.mark.parametrize(
    ("word", "ipa"),
    [
        ("calenha", "ka.ˈlɛ.ɲa"),
        ("thalírë", "θa.ˈliː.ɾe"),
        ("mirão", "mi.ˈɾɐ̃w̃"),
        ("brisalma", "bɾi.ˈzal.ma"),  # lone s between vowels is voiced
        ("ouressa", "ow.ˈɾɛ.sa"),  # ss is said once, and stays [s]
        ("sol", "sɔl"),
    ],
)
def test_ipa(phonology, word, ipa):
    assert phonology.syllabify(word).ipa() == ipa


def test_hyphenated_raises_the_stress(phonology):
    assert phonology.syllabify("thalírë").hyphenated() == "tha·LÍ·rë"


@pytest.mark.parametrize(
    ("word", "complaint"),
    [
        ("kalenha", "not a letter"),
        ("nhalo", "cannot begin"),
        ("solt", "cannot end"),
        ("anstra", "cannot sit between"),
        ("thrth", "at least one vowel"),
        ("álí", "only one vowel"),
    ],
)
def test_impossible_words(phonology, word, complaint):
    with pytest.raises(PhonologyError, match=complaint):
        phonology.syllabify(word)


def test_final_e_is_written_with_diaeresis(phonology):
    assert phonology.problems("thalire") == ["a final e is written ë"]
    assert phonology.problems("tëla") == ["ë may only end a word"]
    assert phonology.problems("thalírë") == []
