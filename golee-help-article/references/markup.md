# Markup contract

Everything the converter understands, and what it emits. Read this when an article
needs more than headings, lists and links, or when the output looks wrong.

- [Block elements](#block-elements)
- [Inline elements](#inline-elements)
- [Callouts](#callouts)
- [Generated structure](#generated-structure)
- [Gotchas](#gotchas)

## Block elements

| Markdown | HTML |
|---|---|
| `# Titolo` | nothing in the body; becomes the Help Scout article title, echoed in a comment at the top of the file |
| `## Sezione` | `<h2 id="sezione">Sezione</h2>` |
| `### Sotto` and deeper | `<p><strong>Sotto</strong></p>` |
| paragraph (one or more consecutive lines) | `<p>…</p>`, lines joined with a space |
| `- item` / `* item` / `+ item` | `<ul><li>…</li></ul>` |
| `1. item` | `<ol><li>…</li></ol>` |
| pipe table with a `\|---\|---\|` separator row | `<table>` with `<thead>` and `<tbody>` |
| `---` on its own line | dropped; separators are generated between sections |
| `> [!TYPE] testo` | see [Callouts](#callouts) |

Lists take one item per line. A line indented under an item is appended to it, so a
long bullet can be wrapped in the source. Nested lists are flattened, so avoid them.

## Inline elements

| Markdown | HTML |
|---|---|
| `**testo**` | `<strong>testo</strong>` |
| `*testo*` or `_testo_` | `<em>testo</em>` |
| `` `codice` `` | `<code>codice</code>` |
| `[label](https://…)` | `<a href="…" target="_blank">label</a>` |
| `[label](#ancora)` | `<a href="#ancora">label</a>`, no target |
| `![alt](https://…)` | `<img src="…" alt="alt">` |

`&`, `<` and `>` are escaped, so UI paths like `**Club > Federazioni**` can be written
literally. Inline code is protected from the emphasis rules, so a class name
containing an underscore survives.

## Callouts

Plain drafts arrive without callouts. The markers below are inserted during the
annotation step described in SKILL.md, which is where the judgement about *which*
paragraphs deserve one lives. This section only covers the syntax.

A callout is a blockquote whose first line carries a type marker. Continuation lines
prefixed with `>` are joined into one paragraph.

```markdown
> [!WARNING] L'emissione crea una tessera reale sul portale CSI
> e scala il relativo credito.
```

| Marker | Italian alias | Output |
|---|---|---|
| `[!NOTE]` | `[!NOTA]` | `<div class="callout">` (grey) |
| `[!WARNING]` | `[!ATTENZIONE]` | `<div class="callout-yellow">` |
| `[!INFO]` | | `<div class="callout-blue">` |
| `[!DASHED]` | `[!BREVE]` | `<p class="callout-yellow dashed"><strong>Nota:</strong> …</p>` |

A blockquote with no marker becomes a grey callout. An unknown marker also falls back
to grey, but the script reports it as a problem and exits non-zero, so it will not
pass unnoticed.

Inline formatting works inside callouts, which is how the BETA notice gets its bold:

```markdown
> [!NOTE] Questa funzionalità è in **BETA**.
```

## Generated structure

The converter assembles the page in this order and nothing else goes between:

1. an HTML comment naming the article title
2. the intro blocks, everything before the first `##`
3. `<section class="index-list">` with an `<h4>In questo articolo</h4>` and one link
   per `##` heading
4. each section, preceded by `<hr role="separator">` except the first

The `<h4>` inside the index list is the one exception to the no-H3-or-deeper rule; it
is part of the table-of-contents component and is styled by Golee's Docs CSS.

Any `## In questo articolo` section present in the source is discarded along with the
list that follows it. Editors and Markdown tools like to generate a nested one that
includes the H1 and the TOC itself; leaving it in the source is harmless.

Heading ids come from the heading text: accents folded (`identità` → `identita`),
apostrophes removed (`l'emissione` → `lemissione`), everything else lowercased and
hyphenated. Two sections with the same title would collide, so give them distinct
names.

## Gotchas

**The converter warns when the callout count looks wrong.** No callouts at all in an
article with four or more sections usually means the annotation step was skipped. A
count higher than the number of sections usually means callouts have been sprinkled on
paragraphs that did not need them. These are warnings, not errors, so use judgement.

**The converter exits non-zero when something is wrong.** It checks that every
`href="#…"` has a matching heading id, that no `<h3>`+ escaped into the body, that at
least one section exists, and that every callout marker is known. Fix the Markdown,
not the HTML.

**Import as HTML, not Markdown.** Uploading the `.md` recreates the original bug:
Help Scout regenerates anchors like `Prima-di-iniziare--N6vvt` and the sommario links
go nowhere.

**Do not edit the article in the Help Scout visual editor afterwards.** The custom
classes and ids can be normalised away. Edit the `.md`, convert, replace the body.

**Images need to be uploaded to Help Scout first.** The converter passes `src` through
untouched, so put the final Help Scout URL in the Markdown, or import the article and
insert images afterwards, accepting that the next re-import overwrites them.
