import shutil

import pytest

from calenha.language import Language
from calenha.morphology import join
from calenha.validate import ERROR, check, errors, words_of


@pytest.fixture(scope="module")
def language(lang_path):
    return Language.load(lang_path)


def test_the_real_language_is_clean(language):
    assert [str(i) for i in errors(check(language))] == []


def test_every_root_has_children(language):
    lonely = [i for i in check(language) if "no word grows" in i.message]
    assert lonely == []


@pytest.mark.parametrize(
    ("parts", "word"),
    [
        (["thal", "-írë"], "thalírë"),
        (["mir", "-a-", "lum", "-a"], "miraluma"),
        (["calenha", "-i"], "calenhi"),  # the last vowel gives way
        (["sol", "ouro"], "solouro"),  # roots and words join plainly
        (["vel", "-u"], "velu"),
    ],
)
def test_join(phonology, parts, word):
    assert join(parts, phonology) == word


def test_lookup_ignores_capitals(language):
    assert language.lookup("Miraluma")[0].gloss == "redwood"


def test_children_follow_words_back_to_roots(language):
    children = {e.word for e in language.children("cal")}
    assert {"calenha", "calenhi", "calmarë", "calu", "calma"} <= children


def test_words_of_strips_breath_and_punctuation():
    assert words_of("lë Miraluma miru.") == ["lë", "miraluma", "miru"]
    assert words_of("mi·rão dë lar") == ["mirão", "dë", "lar"]


# -- the validator catches mistakes ---------------------------------------------


@pytest.fixture
def scratch(lang_path, tmp_path):
    """A disposable copy of the language to break."""
    target = tmp_path / "lang"
    shutil.copytree(lang_path, target)
    return target


def _add(scratch, toml: str) -> list[str]:
    (scratch / "lexicon" / "zz.toml").write_text(toml, encoding="utf-8")
    return [i.message for i in check(Language.load(scratch)) if i.level == ERROR]


def test_catches_unpronounceable_words(scratch):
    found = _add(scratch, '[[word]]\nword = "solt"\ngloss = "x"\npos = "noun"\n')
    assert any("cannot end" in m for m in found)


def test_catches_verbs_without_the_invitation(scratch):
    found = _add(scratch, '[[word]]\nword = "vela"\ngloss = "to x"\npos = "verb"\n')
    assert any("every verb ends in -u" in m for m in found)


def test_catches_nouns_that_look_like_verbs(scratch):
    found = _add(scratch, '[[word]]\nword = "solu"\ngloss = "x"\npos = "noun"\n')
    assert any("only verbs may end in -u" in m for m in found)


def test_catches_etymology_that_does_not_compile(scratch):
    found = _add(
        scratch, '[[word]]\nword = "solira"\ngloss = "x"\npos = "noun"\nfrom = ["sol", "-a"]\n'
    )
    assert any("gives 'sola'" in m for m in found)


def test_catches_unknown_morphemes(scratch):
    found = _add(
        scratch, '[[word]]\nword = "zola"\ngloss = "x"\npos = "noun"\nfrom = ["zol", "-a"]\n'
    )
    assert any("'zol' is not a root" in m for m in found)


def test_catches_unknown_words_in_phrases(scratch):
    path = scratch / "phrases.toml"
    path.write_text(
        path.read_text(encoding="utf-8")
        + '\n[[phrase]]\ntext = "velu zuma"\nliteral = "x"\ntranslation = "x"\n',
        encoding="utf-8",
    )
    found = [i.message for i in check(Language.load(scratch)) if i.level == ERROR]
    assert "'zuma' is not a word" in found
