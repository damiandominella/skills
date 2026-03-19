---
name: twig-to-tiptap
description: Convert Twig HTML templates into TipTap-compatible JSON and vice versa. Use this skill whenever the user wants to convert a Twig/HTML template to TipTap JSON format, migrate templates to a TipTap editor, convert TipTap JSON back to Twig HTML, or asks about mapping HTML structures to ProseMirror nodes. Also trigger when the user pastes HTML containing Twig syntax ({{ }}, {% %}) and wants it in a structured editor-friendly JSON format, or when they mention "tiptap", "prosemirror", "twig template", or "template migration". This skill should be used even when the user just pastes HTML and asks to convert it to TipTap JSON without explicitly naming the skill.
---

# Twig ↔ TipTap JSON Converter

Convert Twig HTML templates into TipTap-compatible ProseMirror JSON, maximizing editable content while preserving Twig logic.

## Core Principle

Make as much content editable as possible. Only use `fixedBlock` nodes for things that genuinely cannot be represented in TipTap's document model (images, tables, Twig conditionals/loops, complex layout wrapping non-text content). Plain text in any wrapper element should be extracted and made editable.

## Before Starting

Read the schema reference to understand the exact JSON structures:
```
/references/tiptap-schema.md
```

## Conversion Rules (Twig HTML → TipTap JSON)

### Step 1: Extract body content
If the input is a full HTML document, extract only the inner content of `<body>`. Discard `<head>`, `<html>`, `<style>`, `<script>`, and `<meta>` tags entirely.

### Step 2: Identify Twig block regions
Before processing individual elements, identify and isolate Twig block regions:
- `{% if ... %}...{% endif %}` (including `{% else %}` / `{% elseif %}`)
- `{% for ... %}...{% endfor %}`

Each complete block region becomes a single `fixedBlock` with `blockType: "twigBlock"` and the entire original HTML (including the Twig tags) stored in `rawHtml`.

**Important:** If a `<p>` or other element contains a mix of regular text AND `{% %}` syntax inline, the entire element becomes a fixedBlock. Don't try to split inline conditionals.

### Step 3: Process remaining elements

Walk through top-level elements and convert them:

#### Unwrap layout wrappers
Elements like `<section>`, `<article>`, `<div>` (without Twig block syntax) that only contain text-based children: **unwrap them** and process each child individually. The wrapper tag and its CSS classes are dropped (except alignment — see mapping below).

For inner elements like `<p class="text-center font-semibold">`:
- Map `text-center` → `textAlign: "center"` on the paragraph node
- Map `font-bold` / `font-semibold` → apply `bold` mark to all text content
- Map `italic` → apply `italic` mark to all text content
- Drop all other Tailwind/CSS classes (they're presentational)

#### Convert native elements
- `<p>` → `paragraph` node
- `<h1>`–`<h6>` → `heading` node with corresponding level
- `<ul>` → `bulletList`, `<ol>` → `orderedList`
- `<blockquote>` → `blockquote`
- `<hr>` → `horizontalRule`
- `<strong>`, `<b>` → `bold` mark on text
- `<em>`, `<i>` → `italic` mark on text
- `<s>`, `<del>` → `strike` mark
- `<code>` → `code` mark
- `style="text-align: center"` → `textAlign: "center"` attr

#### Convert Twig variables
Every `{{ expression }}` becomes a `mention` node:
- `id` = the expression (trimmed, without braces)
- `key` = same as id
- `label` = human-readable name derived from the expression's last segment, or from a user-provided label map
- `mentionSuggestionChar` = `"@"`

If the variable was inside `<strong>`, apply `bold` mark to the mention.

#### Wrap non-representable elements as fixedBlock
- `<img>` → fixedBlock, blockType: `"image"`
- `<table>` → fixedBlock, blockType: `"table"`
- `<input>`, `<select>`, `<textarea>` → fixedBlock, blockType: `"generic"`
- `<div>` with complex content (not just paragraphs) → fixedBlock, blockType: `"layout"`

The `rawHtml` attribute stores the original HTML verbatim.

### Step 4: Output valid JSON
Produce a valid TipTap document JSON with `type: "doc"` and a `content` array.

## Conversion Rules (TipTap JSON → Twig HTML)

### Serialize each node:
- `fixedBlock` → output `rawHtml` directly (this preserves all Twig syntax, images, tables, etc.)
- `mention` → output `{{ key }}`
- `paragraph` → `<p>` with optional `style="text-align: ..."` if textAlign is set
- `heading` → `<h1>`–`<h6>`
- `bulletList` / `orderedList` → `<ul>` / `<ol>` with `<li>` children
- `bold` mark → `<strong>`, `italic` → `<em>`, `strike` → `<s>`, `code` → `<code>`
- `horizontalRule` → `<hr>`

## Example

### Input (Twig HTML):
```html
<section class="my-4">
  <p class="text-center font-semibold">UOSD MEDICINA DELLO SPORT</p>
  <p class="text-center italic">Dipartimento di Prevenzione AST Ancona</p>
</section>

<p>Per l'atleta <strong>{{ orgPerson.name }} {{ orgPerson.surname }}</strong></p>

<img src="logo.png" style="height:90px">

<p>CF: {% if orgPerson.fiscalCode %}<strong>{{ orgPerson.fiscalCode }}</strong>{% else %} ___ {% endif %}</p>
```

### Output (TipTap JSON):
```json
{
  "type": "doc",
  "content": [
    {
      "type": "paragraph",
      "attrs": { "textAlign": "center" },
      "content": [
        { "type": "text", "text": "UOSD MEDICINA DELLO SPORT", "marks": [{ "type": "bold" }] }
      ]
    },
    {
      "type": "paragraph",
      "attrs": { "textAlign": "center" },
      "content": [
        { "type": "text", "text": "Dipartimento di Prevenzione AST Ancona", "marks": [{ "type": "italic" }] }
      ]
    },
    {
      "type": "paragraph",
      "attrs": { "textAlign": null },
      "content": [
        { "type": "text", "text": "Per l'atleta " },
        {
          "type": "mention",
          "attrs": { "id": "orgPerson.name", "label": "Name", "key": "orgPerson.name", "mentionSuggestionChar": "@" },
          "marks": [{ "type": "bold" }]
        },
        { "type": "text", "text": " ", "marks": [{ "type": "bold" }] },
        {
          "type": "mention",
          "attrs": { "id": "orgPerson.surname", "label": "Surname", "key": "orgPerson.surname", "mentionSuggestionChar": "@" },
          "marks": [{ "type": "bold" }]
        }
      ]
    },
    {
      "type": "fixedBlock",
      "attrs": {
        "blockType": "image",
        "rawHtml": "<img src=\"logo.png\" style=\"height:90px\">"
      }
    },
    {
      "type": "fixedBlock",
      "attrs": {
        "blockType": "twigBlock",
        "rawHtml": "<p>CF: {% if orgPerson.fiscalCode %}<strong>{{ orgPerson.fiscalCode }}</strong>{% else %} ___ {% endif %}</p>"
      }
    }
  ]
}
```

Notice how the `<section>` was unwrapped — its children became editable paragraphs with `textAlign` and marks inferred from CSS classes. The `<img>` and the paragraph with inline Twig conditionals stayed as fixedBlocks.

## Common Mistakes to Avoid

1. **Don't wrap entire `<section>` / `<div>` as fixedBlock** when the content inside is just paragraphs and headings. Unwrap them.
2. **Don't drop Twig variables.** Every `{{ }}` must become a mention node.
3. **Don't split `{% if %}...{% endif %}` across multiple nodes.** The entire region is one fixedBlock.
4. **Don't invent attrs** that aren't in the schema. Only use `textAlign` on paragraphs/headings.
5. **Don't forget marks.** If text was in `<strong>` or has class `font-bold`, it needs a `bold` mark.
6. **Don't add `textAlign` when it's null.** If no alignment is specified, use `null`, not `"left"`.
7. **Don't include the `<section>`/`<div>` wrapper tag in rawHtml** when unwrapping — only when the whole thing is a fixedBlock.

## User-Provided Label Map

If the user provides a label map (mapping twig variable paths to display labels), use it for mention nodes. If not, auto-generate labels from the variable key's last segment using these rules:
- Split on `.`, take the last part
- Convert camelCase to separate words: `birthDate` → `Birth Date`
- Convert snake_case to separate words: `birth_date` → `Birth Date`
- Capitalize first letter of each word
