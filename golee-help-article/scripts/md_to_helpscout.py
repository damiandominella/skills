#!/usr/bin/env python3
"""
md_to_helpscout.py — convert a Golee help article from Markdown to the HTML
that Help Scout's import accepts and that help.golee.it styles correctly.

Usage:
    python md_to_helpscout.py article.md               # writes article.html
    python md_to_helpscout.py article.md -o out.html
    python md_to_helpscout.py article.md --stdout

Why this exists: Help Scout strips custom heading ids from Markdown imports and
regenerates its own anchors, so a Markdown table of contents always ends up with
dead links. Importing HTML keeps the ids we write, so the TOC survives.

Stdlib only, no dependencies.
"""

import argparse
import re
import sys
import unicodedata
from pathlib import Path

# ---------------------------------------------------------------- callouts

# marker -> (wrapper, css class, inline prefix)
# "block" renders as <div class="..."><p>…</p></div>
# "inline" renders as <p class="..."><strong>Nota:</strong> …</p>
CALLOUTS = {
    "NOTE":       ("block",  "callout",              None),
    "NOTA":       ("block",  "callout",              None),
    "WARNING":    ("block",  "callout-yellow",       None),
    "ATTENZIONE": ("block",  "callout-yellow",       None),
    "INFO":       ("block",  "callout-blue",         None),
    "DASHED":     ("inline", "callout-yellow dashed", "Nota:"),
    "BREVE":      ("inline", "callout-yellow dashed", "Nota:"),
}
DEFAULT_CALLOUT = "NOTE"

TOC_HEADING = "In questo articolo"
SEPARATOR = '<hr role="separator">'

# ---------------------------------------------------------------- helpers


def slugify(text: str) -> str:
    """Heading text -> anchor id.

    Accents are folded and apostrophes are dropped, so "Dati richiesti per
    l'emissione" becomes "dati-richiesti-per-lemissione" and "identita" never
    ends up percent-encoded in an href.
    """
    text = re.sub(r"<[^>]+>", "", text)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.replace("'", "").replace("\u2019", "")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def inline(text: str) -> str:
    """Escape, then apply the inline Markdown we allow."""
    text = esc(text.strip())

    # code first, so its contents are not touched by the emphasis rules
    codes: list[str] = []

    def stash_code(m):
        codes.append(m.group(1))
        return f"\x00CODE{len(codes) - 1}\x00"

    text = re.sub(r"`([^`]+)`", stash_code, text)

    # images before links: same syntax with a leading !
    text = re.sub(
        r"!\[([^\]]*)\]\(([^)\s]+)\)",
        lambda m: f'<img src="{m.group(2)}" alt="{m.group(1)}">',
        text,
    )

    def link(m):
        label, href = m.group(1), m.group(2)
        target = "" if href.startswith("#") else ' target="_blank"'
        return f'<a href="{href}"{target}>{label}</a>'

    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, text)

    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<em>\1</em>", text)
    text = re.sub(r"(?<![\w_])_([^_\n]+)_(?![\w_])", r"<em>\1</em>", text)

    for i, code in enumerate(codes):
        text = text.replace(f"\x00CODE{i}\x00", f"<code>{code}</code>")

    return text


# ---------------------------------------------------------------- parsing


class Block:
    def __init__(self, kind, **kw):
        self.kind = kind
        self.__dict__.update(kw)


def parse(md: str):
    """Markdown -> (title, [Block]). Raises ValueError on unknown callout types."""
    lines = md.replace("\r\n", "\n").split("\n")
    title = None
    blocks: list[Block] = []
    i = 0
    errors: list[str] = []

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # horizontal rules in the source are dropped; separators are generated
        if re.fullmatch(r"(-{3,}|\*{3,}|_{3,})", stripped):
            i += 1
            continue

        # headings
        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            level, text = len(m.group(1)), m.group(2).strip()
            if level == 1 and title is None:
                title = text
            elif level == 2:
                blocks.append(Block("h2", text=text))
            else:
                # h3 and deeper are rendered as bold paragraphs: the Golee help
                # center restyles real <h3> badly.
                blocks.append(Block("subhead", text=text))
            i += 1
            continue

        # callouts: > [!TYPE] first line, then further "> " lines
        if stripped.startswith(">"):
            body: list[str] = []
            kind = None
            while i < len(lines) and lines[i].strip().startswith(">"):
                content = re.sub(r"^\s*>\s?", "", lines[i])
                mk = re.match(r"^\s*\[!([A-Za-z\-]+)\]\s*(.*)$", content)
                if mk and kind is None:
                    kind = mk.group(1).upper()
                    content = mk.group(2)
                if content.strip():
                    body.append(content.strip())
                i += 1
            kind = kind or DEFAULT_CALLOUT
            if kind not in CALLOUTS:
                errors.append(
                    f"unknown callout type [!{kind}] "
                    f"(use one of: {', '.join(sorted(CALLOUTS))})"
                )
                kind = DEFAULT_CALLOUT
            blocks.append(Block("callout", ctype=kind, text=" ".join(body)))
            continue

        # tables
        if stripped.startswith("|") and i + 1 < len(lines) and re.match(
            r"^\s*\|[\s:\-|]+\|\s*$", lines[i + 1]
        ):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            header, body_rows = rows[0], rows[2:]
            blocks.append(Block("table", header=header, rows=body_rows))
            continue

        # lists
        m = re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$", line)
        if m:
            ordered = not m.group(2)[0] in "-*+"
            items: list[str] = []
            while i < len(lines):
                mi = re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$", lines[i])
                if mi:
                    items.append(mi.group(3).strip())
                    i += 1
                elif lines[i].strip() and lines[i].startswith((" ", "\t")) and items:
                    items[-1] += " " + lines[i].strip()  # lazy continuation
                    i += 1
                else:
                    break
            blocks.append(Block("list", ordered=ordered, items=items))
            continue

        # paragraph: consume until a blank line or another block starts
        para = []
        while i < len(lines):
            cur = lines[i]
            if not cur.strip():
                break
            if re.match(r"^\s*(#{1,6}\s|>|\||[-*+]\s|\d+[.)]\s)", cur):
                break
            if re.fullmatch(r"(-{3,}|\*{3,}|_{3,})", cur.strip()):
                break
            para.append(cur.strip())
            i += 1
        if para:
            blocks.append(Block("para", text=" ".join(para)))

    return title, blocks, errors


def drop_source_toc(blocks):
    """Remove a hand-written or editor-generated 'In questo articolo' section.

    The TOC is regenerated from the h2s, so whatever was in the Markdown, however
    nested, is thrown away.
    """
    out = []
    skipping = False
    for b in blocks:
        if b.kind in ("h2", "subhead") and slugify(b.text) == slugify(TOC_HEADING):
            skipping = True
            continue
        if skipping:
            if b.kind in ("list", "para"):
                continue
            skipping = False
        out.append(b)
    return out


# ---------------------------------------------------------------- rendering


def render_block(b) -> str:
    if b.kind == "para":
        return f"<p>{inline(b.text)}</p>"

    if b.kind == "subhead":
        return f"<p><strong>{inline(b.text)}</strong></p>"

    if b.kind == "list":
        tag = "ol" if b.ordered else "ul"
        items = "\n".join(f"  <li>{inline(it)}</li>" for it in b.items)
        return f"<{tag}>\n{items}\n</{tag}>"

    if b.kind == "table":
        head = "".join(f"<th>{inline(c)}</th>" for c in b.header)
        body = "\n".join(
            "    <tr>" + "".join(f"<td>{inline(c)}</td>" for c in row) + "</tr>"
            for row in b.rows
        )
        return (
            "<table>\n  <thead>\n    <tr>"
            + head
            + "</tr>\n  </thead>\n  <tbody>\n"
            + body
            + "\n  </tbody>\n</table>"
        )

    if b.kind == "callout":
        style, css, prefix = CALLOUTS[b.ctype]
        text = inline(b.text)
        if style == "inline":
            body = f"<strong>{prefix}</strong> {text}" if prefix else text
            return f'<p class="{css}">{body}</p>'
        return f'<div class="{css}">\n  <p>{text}</p>\n</div>'

    if b.kind == "h2":
        return f'<h2 id="{slugify(b.text)}">{inline(b.text)}</h2>'

    return ""


def render_toc(headings) -> str:
    items = "\n".join(
        f'    <li><a href="#{slug}">{inline(text)}</a></li>' for slug, text in headings
    )
    return (
        '<section class="index-list">\n'
        f"  <h4>{TOC_HEADING}</h4>\n"
        "  <ul>\n"
        f"{items}\n"
        "  </ul>\n"
        "</section>"
    )


def convert(md: str):
    title, blocks, errors = parse(md)
    blocks = drop_source_toc(blocks)

    headings = [(slugify(b.text), b.text) for b in blocks if b.kind == "h2"]

    parts: list[str] = []
    if title:
        parts.append(f"<!-- Import in Help Scout as HTML. Article title: {title} -->")

    first_h2_index = next((i for i, b in enumerate(blocks) if b.kind == "h2"), len(blocks))

    # intro, before the first section
    for b in blocks[:first_h2_index]:
        parts.append(render_block(b))

    if headings:
        parts.append(render_toc(headings))

    for idx, b in enumerate(blocks[first_h2_index:]):
        if b.kind == "h2" and idx > 0:
            parts.append(SEPARATOR)
        parts.append(render_block(b))

    html = "\n\n".join(p for p in parts if p) + "\n"

    # validation
    ids = set(re.findall(r'<h2 id="([^"]+)"', html))
    for anchor in set(re.findall(r'href="#([^"]+)"', html)):
        if anchor not in ids:
            errors.append(f"TOC link #{anchor} has no matching heading id")
    body_only = re.sub(r'<section class="index-list">.*?</section>', "", html, flags=re.S)
    if re.search(r"<h[3-6]\b", body_only):
        errors.append("output contains an <h3>+ heading, which the help center misstyles")
    if not headings:
        errors.append("no <h2> sections found, so no table of contents was generated")

    warnings: list[str] = []
    n_callouts = len(re.findall(r'class="callout', html))
    if n_callouts == 0 and len(headings) >= 4:
        warnings.append(
            "no callouts in this article: the annotation step was probably skipped "
            "(see 'Annotating the draft' in SKILL.md)"
        )
    elif n_callouts > max(6, len(headings)):
        warnings.append(
            f"{n_callouts} callouts for {len(headings)} sections: that is a lot, and "
            "callouts stop standing out when there are too many"
        )

    return title, html, errors, warnings


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", help="Markdown source file")
    ap.add_argument("-o", "--output", help="output .html path (default: alongside input)")
    ap.add_argument("--stdout", action="store_true", help="print HTML instead of writing")
    args = ap.parse_args()

    src = Path(args.input)
    title, html, errors, warnings = convert(src.read_text(encoding="utf-8"))

    if args.stdout:
        print(html)
    else:
        dest = Path(args.output) if args.output else src.with_suffix(".html")
        dest.write_text(html, encoding="utf-8")
        print(f"wrote {dest}")

    print(f"title: {title or '(no H1 found)'}", file=sys.stderr)
    for w in warnings:
        print(f"warning: {w}", file=sys.stderr)
    if errors:
        print("problems:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)
    print("ok: anchors resolve, no h3+ in output", file=sys.stderr)


if __name__ == "__main__":
    main()
