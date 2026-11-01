import json

import pytest

from calenha.cli import main
from calenha.export import environment, export
from calenha.language import Language
from calenha.mdown import inline, render


@pytest.fixture(scope="module")
def data(lang_path):
    return export(Language.load(lang_path), lang_path.parent, built="2026-01-01")


def test_it_is_plain_json(data):
    assert json.loads(json.dumps(data, ensure_ascii=False)) == data


def test_every_entry_is_whole(data):
    for e in data["entries"]:
        assert "".join(e["syllables"]) == e["word"]
        assert 0 <= e["stress"] < len(e["syllables"])
        assert e["ipa"] and e["short"] and e["label"]


def test_slugs_are_unique_and_readable(data):
    slugs = [e["slug"] for e in data["entries"]]
    assert len(slugs) == len(set(slugs))
    by_word = {e["word"]: e["slug"] for e in data["entries"]}
    assert by_word["thalírë"] == "thalire"
    assert by_word["nã"] == "nan"


def test_references_point_at_real_things(data):
    slugs = {e["slug"] for e in data["entries"]}
    roots = {r["slug"] for r in data["roots"]}
    texts = {t["slug"] for t in data["texts"]}
    for e in data["entries"]:
        assert set(e["family"]) <= slugs
        assert set(e["texts"]) <= texts
        assert all(0 <= i < len(data["phrases"]) for i in e["phrases"])
        for p in e["parts"]:
            if p["kind"] == "root":
                assert p["target"] in roots
            if p["kind"] == "word":
                assert p["target"] in slugs
    for change in data["changes"]:
        assert set(change["shaped"]) <= slugs


def test_word_story(data):
    calenha = next(e for e in data["entries"] if e["word"] == "calenha")
    assert calenha["old"] == "kalenia"
    assert [h["change"] for h in calenha["history"]] == ["the old k", "the palatal glide"]
    assert "calenhi" in calenha["family"]


def test_docs_are_rendered_with_relative_links(data):
    assert set(data["docs"]) == {"grammar", "sounds", "world", "principles"}
    assert 'href="grammar"' in data["docs"]["world"]["html"]


def test_unspoken_words_are_new(data):
    words = {e["word"] for e in data["entries"]}
    for c in data["unspoken"]["things"] + data["unspoken"]["invitations"]:
        assert c["text"] not in words


def test_cli_export(lang_path, tmp_path):
    out = tmp_path / "language.json"
    assert main(["--lang", str(lang_path), "export", "--out", str(out)]) == 0
    assert json.loads(out.read_text(encoding="utf-8"))["schema"] == 1


@pytest.mark.parametrize(
    ("when", "words"),
    [
        ("l_", "after l"),
        ("_V", "before a vowel"),
        ("_#", "at the end of a word"),
        ("V_#", "after a vowel, at the end of a word"),
        ("", ""),
    ],
)
def test_environment_in_words(when, words):
    assert environment(when) == words


# -- the markdown renderer --------------------------------------------------------


def test_markdown_inline():
    assert inline("**velu** and *calu*") == "<strong>velu</strong> and <em>calu</em>"
    assert inline("*\\*kalenia*") == "<em>*kalenia</em>"
    assert inline("see `docs/grammar.md`", link={"docs/grammar.md": "grammar"}.get) == (
        'see <a href="grammar"><code>docs/grammar.md</code></a>'
    )


def test_markdown_blocks():
    doc = render(
        "# title\n\npara one\nstill one\n\n> a\n>\n> b\n\n"
        "| x | y |\n|---|---|\n| 1 | 2 |\n\n- one\n- two"
    )
    assert doc.title == "title"
    assert "<p>para one still one</p>" in doc.html
    assert "<blockquote><p>a</p><p>b</p></blockquote>" in doc.html
    assert "<td>1</td><td>2</td>" in doc.html
    assert "<ul><li>one</li><li>two</li></ul>" in doc.html
