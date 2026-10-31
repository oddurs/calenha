"""A very small Markdown renderer for the language's own documents.

It covers what the docs use — headings, paragraphs, quotes, lists, tables, code,
emphasis and links — and nothing more, so the toolkit stays free of dependencies.
"""

from __future__ import annotations

import html
import re
from collections.abc import Callable
from dataclasses import dataclass

_CODE = re.compile(r"`([^`]+)`")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
_BOLD = re.compile(r"\*\*(?!\s)(.+?)(?<!\s)\*\*")
_ITALIC = re.compile(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])")
_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
_FENCE = "```"


@dataclass(frozen=True)
class Document:
    title: str
    html: str


def slug(text: str) -> str:
    plain = re.sub(r"<[^>]+>|[*`]", "", text).lower()
    return re.sub(r"[^\w]+", "-", plain, flags=re.UNICODE).strip("-")


def inline(text: str, link: Callable[[str], str | None] | None = None) -> str:
    """Emphasis, code and links within a line. ``link`` may turn a code span into a link."""
    stash: list[str] = []

    def keep(fragment: str) -> str:
        stash.append(fragment)
        return f"\x00{len(stash) - 1}\x00"

    def code(m: re.Match[str]) -> str:
        body = m.group(1)
        target = link(body) if link else None
        tag = f"<code>{html.escape(body)}</code>"
        return keep(f'<a href="{html.escape(target)}">{tag}</a>' if target else tag)

    text = _CODE.sub(code, text)
    text = text.replace("\\*", keep("*"))
    text = html.escape(text, quote=False)
    text = _LINK.sub(lambda m: keep(f'<a href="{html.escape(m.group(2))}">{m.group(1)}</a>'), text)
    text = _BOLD.sub(r"<strong>\1</strong>", text)
    text = _ITALIC.sub(r"<em>\1</em>", text)
    return re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m.group(1))], text)


def render(text: str, link: Callable[[str], str | None] | None = None) -> Document:
    """Render a document. Its first ``#`` heading becomes the title, not part of the body."""
    lines = text.splitlines()
    out: list[str] = []
    title = ""
    para: list[str] = []
    i = 0

    def flush() -> None:
        if para:
            out.append(f"<p>{inline(' '.join(para), link)}</p>")
            para.clear()

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            flush()
            i += 1
        elif stripped.startswith(_FENCE):
            flush()
            body = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith(_FENCE):
                body.append(lines[i])
                i += 1
            out.append(f"<pre><code>{html.escape(chr(10).join(body))}</code></pre>")
            i += 1
        elif m := _HEADING.match(stripped):
            flush()
            level, body = len(m.group(1)), m.group(2)
            if level == 1 and not title:
                title = body
            else:
                out.append(f'<h{level} id="{slug(body)}">{inline(body, link)}</h{level}>')
            i += 1
        elif stripped.startswith("|"):
            flush()
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i].strip())
                i += 1
            out.append(_table(rows, link))
        elif stripped.startswith(">"):
            flush()
            quote: list[str] = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip()[1:].strip())
                i += 1
            paragraphs = " ".join(q if q else "\n" for q in quote).split("\n")
            body = "".join(f"<p>{inline(p.strip(), link)}</p>" for p in paragraphs if p.strip())
            out.append(f"<blockquote>{body}</blockquote>")
        elif re.match(r"^[-*]\s+", stripped) or re.match(r"^\d+\.\s+", stripped):
            flush()
            ordered = bool(re.match(r"^\d+\.", stripped))
            items: list[str] = []
            while i < len(lines):
                current = lines[i]
                if re.match(r"^\s*([-*]|\d+\.)\s+", current) and not current.startswith("   "):
                    items.append(re.sub(r"^\s*([-*]|\d+\.)\s+", "", current))
                elif current.startswith("  ") and current.strip() and items:
                    items[-1] += " " + current.strip()
                else:
                    break
                i += 1
            tag = "ol" if ordered else "ul"
            body = "".join(f"<li>{inline(item, link)}</li>" for item in items)
            out.append(f"<{tag}>{body}</{tag}>")
        else:
            para.append(stripped)
            i += 1

    flush()
    return Document(title, "\n".join(out))


def _table(rows: list[str], link: Callable[[str], str | None] | None) -> str:
    cells = [[c.strip() for c in row.strip("|").split("|")] for row in rows]
    head, body = cells[0], [r for r in cells[1:] if not all(set(c) <= set("-: ") for c in r)]
    thead = "".join(f"<th>{inline(c, link)}</th>" for c in head)
    tbody = "".join(
        "<tr>" + "".join(f"<td>{inline(c, link)}</td>" for c in row) + "</tr>" for row in body
    )
    return f'<div class="table"><table><thead><tr>{thead}</tr></thead><tbody>{tbody}</tbody></table></div>'
