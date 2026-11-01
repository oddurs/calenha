import pytest

from calenha.cli import main
from calenha.generate import euphony, generate
from calenha.language import Language
from calenha.render import collate, line_html, markdown, stressed_html
from calenha.sound_change import evolve


@pytest.fixture(scope="module")
def language(lang_path):
    return Language.load(lang_path)


# -- sound change -----------------------------------------------------------------


@pytest.mark.parametrize(
    ("old", "word", "changes"),
    [
        ("kalenia", "calenha", ["the old k", "the palatal glide"]),
        ("alkamar", "algamar", ["the old k", "softening after l"]),
        ("thaliire", "thalírë", ["the long vowels", "the lifted ending"]),
        ("miran", "mirão", ["the nasal close"]),
        ("nevona", "nevoã", ["the fading n"]),
        ("*keele", "célë", ["the old k", "the long vowels", "the lifted ending"]),
    ],
)
def test_evolve(language, old, word, changes):
    result = evolve(old, language)
    assert result.word == word
    assert [s.change.name for s in result.steps] == changes


def test_long_vowels_come_before_the_glide(language):
    # if the glide ran first, *thaliire would become thalhirë
    assert evolve("thaliire", language).word != "thalhirë"


# -- generation -------------------------------------------------------------------


def test_generated_words_obey_the_phonology(language):
    for candidate in generate(language, n=40, seed=1, attempts=400):
        assert language.phonology.problems(candidate.word.text) == []
        assert not candidate.word.text.endswith("u")
        assert not language.lookup(candidate.word.text)


def test_generated_verbs_invite(language):
    for candidate in generate(language, n=10, seed=2, kind="verb"):
        assert candidate.word.text.endswith("u")


def test_generation_is_repeatable(language):
    first = [c.word.text for c in generate(language, seed=5)]
    assert first == [c.word.text for c in generate(language, seed=5)]


def test_the_ear_prefers_soft_words(language):
    p = language.phonology
    assert euphony(p.syllabify("solenha"), p) > euphony(p.syllabify("pedralta"), p)
    assert euphony(p.syllabify("miraluma"), p) > euphony(p.syllabify("chechë"), p)


# -- rendering --------------------------------------------------------------------


def test_collation_ignores_accents():
    assert collate("célë") == "cele"


def test_stress_mark_survives_capitals_and_breaths(language):
    p = language.phonology
    assert stressed_html(p.syllabify("Miraluma"), "Miraluma") == 'Mira<span class="st">lu</span>ma'
    assert stressed_html(p.syllabify("mirão"), "mi·rão") == 'mi·<span class="st">rão</span>'


def test_markdown_lists_every_word(language):
    text = markdown(language)
    for entry in language.entries:
        assert f"**{entry.word}**" in text


def test_line_links_words(language):
    html = line_html("velu zuma", language, href=lambda w: f"word/{w}.html")
    assert 'href="word/velu.html"' in html
    assert 'href="word/zuma.html"' in html  # the line renderer trusts its linker


# -- the command line -------------------------------------------------------------


def test_cli_check(lang_path, capsys):
    assert main(["--lang", str(lang_path), "check"]) == 0
    assert "calenha is well" in capsys.readouterr().out


def test_cli_read_flags_unknown_words(lang_path, capsys):
    assert main(["--lang", str(lang_path), "read", "velu zuma"]) == 1
    assert "zuma" in capsys.readouterr().out


def test_cli_build_writes_the_markdown_dictionary(lang_path, tmp_path, monkeypatch):
    monkeypatch.setattr("calenha.cli.DATA", tmp_path / "language.json")
    assert main(["--lang", str(lang_path), "build", "--out", str(tmp_path)]) == 0
    assert (tmp_path / "dictionary.md").exists()
