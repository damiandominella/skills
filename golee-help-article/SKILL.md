---
name: golee-help-article
description: Turn a plain Markdown draft into a published-ready Golee help center article in the HTML that Help Scout imports correctly, adding callouts and working section anchors along the way. Use this skill EVERY TIME someone is preparing an article for the Golee help center or Help Scout. Triggers include "articolo help center", "nuovo articolo di supporto", "convertilo per help scout", "importa su help scout", "il sommario non funziona", "i link alle sezioni non funzionano", "scrivi la guida per questa feature", "documenta questa funzionalità", "help scout html", or whenever someone hands over a Markdown draft, a feature description, a ticket or release notes and wants them published as a support article. Also use when an already-published article needs fixing (dead table-of-contents links, badly rendered headings, missing callouts).
---

# Golee help center articles

The input is a plain Markdown article. It knows nothing about Help Scout, it has no
callouts, and its table of contents (if it has one) is whatever some editor generated.
The output is HTML that Help Scout imports with working anchors and that
help.golee.it styles correctly.

Most of that conversion is mechanical and a script does it. The part that needs
judgement, and the reason this skill is not just a script, is **deciding which
sentences in the draft should become callouts**. Do that first.

Help Scout strips custom heading ids from Markdown imports and generates its own
anchors (`Prima-di-iniziare--N6vvt`), so a Markdown table of contents always ends up
with dead links. Importing HTML keeps the ids. That is why the pipeline exists.

## Workflow

1. **Read the draft and annotate it.** Copy the plain `.md` to a working file and
   insert callout markers where they belong, following "Annotating the draft" below.
   This is the main job. Everything else is automatic.
2. **Convert:**
   ```bash
   python3 scripts/md_to_helpscout.py articolo.md -o articolo.html
   ```
   The script reports the article title it detected and either `ok` or a list of
   problems, exiting non-zero when something is wrong. Fix the Markdown and run again;
   never patch the HTML by hand.
3. **Hand over both files:** the annotated `.md` for the next revision, the `.html`
   for the import.
4. **Import into Help Scout:** Docs, the right collection, new article, paste or
   upload the **HTML**. Set the title to the `# H1` from the Markdown, since the H1 is
   deliberately not rendered into the body. Preview and click one table-of-contents
   link to confirm the anchors resolve.

The `.md` is the source of truth. Don't re-edit the article in Help Scout's visual
editor afterwards, since it can normalise away the custom classes; edit the Markdown
and convert again.

## Annotating the draft

A good help article has a handful of callouts, not one per screen. In a long article
(fifteen sections or so) expect roughly five to eight. If a draft yields none, either
it is very short or something was missed, and the script will warn about it.

A callout is a blockquote with a type marker on its first line:

```markdown
> [!WARNING] L'emissione crea una tessera reale sul portale CSI
> e scala il relativo credito.
```

Turn the existing paragraph into the callout, don't duplicate it. Inline formatting
works inside, which is how "in **BETA**" keeps its bold.

### What to look for

Read the draft asking "which sentences, if the reader skipped them, would cause a
support ticket or an irreversible mistake?" Those are the callouts. There are four
types, and position within the section is a strong signal.

**`[!WARNING]`, yellow, for irreversible or costly actions.** Almost always the lead
paragraph of a section, right after the `##`, framing what the whole section is about
to do: money leaving an account, a write to a federation portal, anything that cannot
be undone from Golee.

> Draft: *L'emissione crea una tessera reale sul portale CSI e scala il relativo
> credito. Si fa dal profilo della persona, uno alla volta.*
> becomes `[!WARNING]`, opening "Come emettere una tessera CSI".

**`[!INFO]`, blue, for the distinction the reader is most likely to get wrong.**
Usually exactly one per article, in the intro. It is the mental model, typically
shaped like "X does this, Y does the opposite".

> Draft: *La sincronizzazione legge il portale e scrive solo in Golee. L'emissione fa
> il contrario: crea una tessera reale sul portale e ne scala il credito.*
> becomes `[!INFO]`, in the intro.

**`[!NOTE]`, grey, for neutral state and scope.** BETA notices, what a feature does
not touch, what a status word means. Not warnings, just things the reader has to hold
in mind.

> Draft: *Questa funzionalità è in BETA.* becomes
> `> [!NOTE] Questa funzionalità è in **BETA**.` (bold the status word)
>
> Draft: *La sincronizzazione importa i tesseramenti dal portale verso Golee. Non
> crea, modifica o cancella tessere sul portale, e non importa foto o documenti.*
>
> Draft: *Un tesseramento allineato al portale compare sul profilo come Tesseramento
> certificato. Non è modificabile a mano.*

**`[!DASHED]`, inline yellow, for a short caveat attached to what precedes it.**
Typically the last paragraph of a section, one or two lines, a limit or a permission
requirement. It renders with a bold "Nota:" prefix, so the sentence should read
naturally after it and start lowercase.

> Draft: *Senza il CSI tra le federazioni della società, o senza i permessi per
> gestire federazioni e tesseramenti, non vedi le azioni di collegamento.*
> becomes `> [!DASHED] senza il CSI tra le federazioni della società, o senza…`
>
> Draft: *Il rinnovo in blocco dalla lista atleti non è disponibile.*
>
> Draft: *Un'emissione confermata non può essere annullata da Golee.*

The yellow/dashed split is about weight, not topic. A destructive action the reader is
about to perform gets the full yellow block at the top of the section. A limitation
they should know about afterwards gets the dashed one-liner at the bottom.

### What not to touch

Leave the rest of the draft alone. In particular, don't convert these by hand, because
the script already handles them and doing both produces a mess:

- the `# H1`, which becomes the Help Scout title and is dropped from the body
- any `## In questo articolo` section, however nested, which is discarded and
  regenerated from the `##` headings
- `---` separator lines, which are dropped and re-inserted between sections
- `###` and deeper headings, which become bold paragraphs (see below)
- `>` characters inside UI paths like `**Club > Federazioni ed Enti**`, escaped for you

If the draft is missing structure altogether, or its sections are titled like labels
rather than questions, fix the headings while you are in there. See "Writing from
scratch".

### Never use H3 as a real heading

The Golee help center restyles `<h3>` badly, so `###` is rendered as a bold paragraph.
This is intentional: FAQ entries and small sub-sections read as bold lines, and only
real sections appear in the sommario. If a `###` genuinely deserves to be in the
sommario, promote it to `##` rather than leaving it as a heading.

The CSS behind the callout classes lives in Golee's Docs custom stylesheet, not in the
article. If a callout renders unstyled, a class was renamed there.

## Writing from scratch

When the input is a feature description, a ticket or release notes rather than a
draft, write the Markdown first, then annotate it. Structure matters more than prose,
because these articles also feed the Beacon AI agent and it retrieves by section.

- One question per `##` section, phrased the way a club secretary would ask it: "Come
  collegare Golee al portale CSI", not "Configurazione integrazione".
- Open with what the feature lets you do as a short bulleted list, then the single
  most important distinction as a blue callout. A reader who stops after the first
  screen should still come away with the right mental model.
- Front-load prerequisites in "Prima di iniziare". Most tickets are people missing one.
- Close with "Cosa non fa" and "Problemi comuni". "Cosa non fa" prevents tickets, and
  "Problemi comuni" should mirror the actual error messages the product shows, since
  that is the text people paste into search.
- Bold UI paths and button labels exactly as they appear in the product.
- Italian, second person, present tense. No em dashes.

## Reference files

- `references/markup.md`, everything the converter understands and what it emits, plus
  the failure modes. Read it when the article uses tables, images, or anything beyond
  headings, lists and links.
- `references/esempio-input.md`, a plain draft, the kind of input this skill gets.
- `references/esempio-annotato.md`, the same draft after annotation.
- `references/esempio-output.html`, what the script produces from it.

## Fixing an existing article

If a live article has dead section links, it was imported as Markdown. Copy its body
back into a `.md`, run the pipeline, and replace the article body with the HTML rather
than re-importing the Markdown.
