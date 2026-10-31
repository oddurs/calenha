import re
from pathlib import Path

import pytest

from calenha.language import Language
from calenha.site import Site, build, environment
from calenha.site.mdown import inline, render


@pytest.fixture(scope="module")
def built(lang_path, tmp_path_factory):
    out = tmp_path_factory.mktemp("site")
    build(Language.load(lang_path), lang_path.parent, out)
    return out


def test_every_word_has_a_page(lang_path, built):
    language = Language.load(lang_path)
    assert len(list((built / "word").glob("*.html"))) == len(language.entries)


@pytest.mark.parametrize(
    "page",
    ["index", "words", "roots", "grammar", "sounds", "history", "world", "principles", "unspoken"],
)
def test_pages_exist_and_are_whole(built, page):
    html = (built / f"{page}.html").read_text(encoding="utf-8")
    assert html.startswith("<!doctype html>")
    assert "<title>" in html and "site.css" in html


def test_no_link_is_broken(built):
    ids = {
        f.resolve(): set(re.findall(r'id="([^"]+)"', f.read_text(encoding="utf-8")))
        for f in built.rglob("*.html")
    }
    broken = []
    for page in built.rglob("*.html"):
        markup = re.sub(r"<script.*?</script>", "", page.read_text(encoding="utf-8"), flags=re.S)
        for href in re.findall(r'href="([^"]+)"', markup):
            if href.startswith(("http", "#")):
                continue
            path, _, anchor = href.partition("#")
            target = (page.parent / path).resolve()
            if not target.exists() or (anchor and anchor not in ids.get(target, set())):
                broken.append(f"{page.relative_to(built)} → {href}")
    assert broken == []


def test_word_page_tells_the_story(built):
    html = (built / "word" / "calenha.html").read_text(encoding="utf-8")
    assert "*kalenia" in html  # the old form
    assert "the palatal glide" in html  # the change that shaped it
    assert "calenhi.html" in html  # its family


def test_fragment_home_has_no_shell(lang_path, tmp_path):
    build(Language.load(lang_path), lang_path.parent, tmp_path, fragment_home=True)
    assert not (tmp_path / "index.html").read_text(encoding="utf-8").startswith("<!doctype")
    assert (tmp_path / "words.html").read_text(encoding="utf-8").startswith("<!doctype")


def test_slugs_are_unique(lang_path):
    site = Site(Language.load(lang_path), lang_path.parent)
    slugs = list(site.slugs.values())
    assert len(slugs) == len(set(slugs))


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


def test_markdown_inline():
    assert inline("**velu** and *calu*") == "<strong>velu</strong> and <em>calu</em>"
    assert inline("*\\*kalenia*") == "<em>*kalenia</em>"
    assert inline("see `docs/grammar.md`", link={"docs/grammar.md": "grammar.html"}.get) == (
        'see <a href="grammar.html"><code>docs/grammar.md</code></a>'
    )


def test_markdown_blocks():
    doc = render(
        "# title\n\npara one\nstill one\n\n> a\n>\n> b\n\n| x | y |\n|---|---|\n| 1 | 2 |\n\n- one\n- two"
    )
    assert doc.title == "title"
    assert "<p>para one still one</p>" in doc.html
    assert "<blockquote><p>a</p><p>b</p></blockquote>" in doc.html
    assert "<td>1</td><td>2</td>" in doc.html
    assert "<ul><li>one</li><li>two</li></ul>" in doc.html


def test_the_real_documents_render(lang_path):
    for source in ["docs/grammar.md", "docs/phonology.md", "context/world.md"]:
        doc = render((Path(lang_path).parent / source).read_text(encoding="utf-8"))
        assert doc.title and "<p>" in doc.html


def test_texts_have_pages_and_glosses(lang_path, built):
    language = Language.load(lang_path)
    for text in language.texts:
        html = (built / "text" / f"{text.slug}.html").read_text(encoding="utf-8")
        assert 'class="ilin"' in html  # word-by-word glosses
        assert text.english in html


def test_reader_carries_the_lexicon(lang_path, built):
    html = (built / "reader.html").read_text(encoding="utf-8")
    payload = re.search(r'<script type="application/json" id="lexicon">(.*?)</script>', html, re.S)
    import json

    data = json.loads(payload.group(1))
    assert data["thalírë"]["g"] == "river"
    assert data["velu"]["g"] == "wander"


def test_phrases_page_groups_by_topic(built):
    html = (built / "phrases.html").read_text(encoding="utf-8")
    for topic in ["greetings", "the hours", "the heart", "land and sea", "sayings"]:
        assert f">{topic}</h2>" in html
