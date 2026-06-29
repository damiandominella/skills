---
name: ticket-formatter
description: Convert any brief, raw note, Slack thread, bug report, feature request, or unstructured description into a standardized engineering ticket with user story, acceptance criteria as checkboxes, and to-do sections split by Design/Backend/Frontend. ALWAYS use this skill when the user pastes a brief, situation description, bug report, or any unstructured text and asks to "format it", "turn it into a ticket", "make a ticket", "fittalo nel formato", "trasforma in task", or provides the target template explicitly. Trigger even if the user doesn't mention the word "ticket" — any request to convert prose into a structured Description / Acceptance criteria / To Do format should activate this skill.
---

# Ticket Formatter

Convert unstructured briefs into a consistent engineering-ticket format with user story, checkbox acceptance criteria, and discipline-split to-dos.

## Output format (strict)

Output the ticket as a single markdown code block so the user can copy-paste cleanly. Use this exact structure:

```markdown
## 📜 Description

"As a [persona],

I want [output],

so that [outcome]."

## ✅ Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## 📝 To Do

- [ ] High-level cross-cutting task (only if it doesn't belong to a specific discipline)

### 📐 Design

- [ ] Design task

### 🔙 Backend

- [ ] Backend task

### 💻 Frontend

- [ ] Frontend task
```

### Language

Match the language of the brief. If the brief is in Italian, write the ticket in Italian (e.g. "Come [persona], vorrei [output], così da [outcome]."). If in English, use English. Do not mix languages within a ticket.

## Rules

### Description (user story)

- Always use the "As a / I want / so that" three-line format, with a blank line between each clause and quotes wrapping the whole thing.
- Persona must be the actual end-user affected (e.g. "user signing up from mobile", "admin managing workspaces", "customer browsing the catalog"). Never use vague personas like "user" alone if the brief specifies context — be specific.
- The "I want" is the desired *capability or outcome*, not the implementation. "I want legal documents to open inline" not "I want an iframe modal".
- The "so that" is the user's underlying goal, not the engineering goal. "so I can complete onboarding without losing state" not "so the auth state remains valid".

### Acceptance criteria

- **Every item MUST start with `- [ ] `** (checkbox syntax). This is non-negotiable.
- Criteria describe *observable behavior*, not implementation. Write what a tester or PM could verify.
- Cover happy path, edge cases mentioned in the brief, and cross-platform/device considerations if relevant.
- If the brief mentions specific environments (mobile webview, in-app browsers, specific OS, specific browsers), include at least one criterion that explicitly covers them.
- Aim for 4–8 criteria. If you have fewer than 3, the brief was probably underspecified — surface that. If more than 10, you're mixing in implementation details — cut them.

### To Do sections

- **Sections are optional.** Omit any section that doesn't apply. Don't include empty sections with placeholder bullets.
- Decision rule for omitting:
  - **No Design section** if the change is purely backend/data, has no UI surface, or the UI is trivially derived from existing patterns.
  - **No Backend section** if the change is purely client-side (styling, copy, frontend-only state, animations, etc.).
  - **No Frontend section** if the change is purely backend (API, infra, jobs, migrations, internal tooling without UI).
  - **No top-level "📝 To Do" parent bullet** unless there's a genuinely cross-cutting task that doesn't fit any discipline (e.g. "Reproduce the bug", "Investigate root cause", "Document decision in ADR"). If everything maps to a discipline, omit the parent bullets entirely and just keep the sub-sections.
- Every to-do item starts with `- [ ] `.
- To-dos are *engineering work items*, not requirements. "Implement `<LegalModal>` component" not "the modal should work".
- Be concrete. Prefer "Add `GET /legal/privacy-policy` endpoint returning Markdown" over "Add legal endpoint".

### Order of sections (always)

1. Description
2. Acceptance criteria
3. To Do (with sub-sections in this order: Design → Backend → Frontend)

Never reorder. Never rename emojis or headers.

## Inferring missing information

Briefs are often incomplete. When something is missing:

- **Persona unclear**: infer from context. A bug in signup flow → "user registering from [context]". A dashboard issue → "[role] viewing the dashboard". If genuinely ambiguous, pick the most affected user and note the assumption *outside the code block* in a brief follow-up.
- **Outcome unclear**: ask yourself "why would the user care about this being fixed?" That's the "so that".
- **Acceptance criteria thin**: derive them from the bug symptoms (each symptom → at least one criterion that asserts its absence) and from the proposed solution (each behavior → one criterion).
- **Discipline split unclear**: read the brief for technical signals. Mentions of API/DB/auth/state → backend. Mentions of UI/modal/styling/components → frontend. Mentions of UX/flow/mockups → design.

If the brief is severely underspecified (e.g. one sentence with no context), produce the best-effort ticket and flag specific gaps to the user *after* the code block, not inside it.

## Pushback

When the brief contains questionable technical decisions (e.g. "let's just use an iframe", "we'll hardcode the copy"), the ticket itself should remain neutral and capture the *requirement*, not the debated solution. Then, *after* the code block, briefly raise the concern with a better alternative. The user asked for a ticket, not a code review — keep the artifact clean and put the opinion outside it.

## Anti-patterns to avoid

- ❌ Filling every section just because the template has it. Empty sections are worse than absent sections.
- ❌ Acceptance criteria that restate the to-do list. ACs = observable outcomes; to-dos = work items.
- ❌ Implementation details inside the user story ("I want a React modal with an iframe").
- ❌ Vague to-dos ("Fix the bug", "Make it work on mobile"). Always concrete.
- ❌ Translating the user's language. If they wrote in Italian, the ticket is in Italian.
- ❌ Adding sections, emojis, or headers not in the template.
- ❌ Forgetting `- [ ]` on acceptance criteria — they MUST be checkboxes.

## Example

**Input brief (Italian):**
> Gli utenti si lamentano che quando ricevono la mail di reset password, il link scade troppo in fretta (15 min) e spesso devono richiederlo 2-3 volte. Portiamolo a 1 ora. Anche la mail è bruttina, vediamo se il design può rifarla.

**Output:**

```markdown
## 📜 Description

"Come utente che ha dimenticato la password,

vorrei avere abbastanza tempo per usare il link di reset dopo averlo ricevuto via email,

così da non dover richiedere il reset più volte e completare il recupero account al primo tentativo."

## ✅ Acceptance criteria

- [ ] Il link di reset password ha una validità di 60 minuti dal momento dell'invio
- [ ] Dopo la scadenza, l'utente vede un messaggio chiaro che invita a richiedere un nuovo link
- [ ] La mail di reset ha un design aggiornato e coerente con il resto delle comunicazioni transazionali
- [ ] Il link continua a essere single-use (invalidato dopo il primo utilizzo)

## 📝 To Do

### 📐 Design

- [ ] Redesign del template email di reset password

### 🔙 Backend

- [ ] Aggiornare la durata del token di reset da 15 a 60 minuti
- [ ] Verificare che la logica di invalidazione single-use rimanga intatta
- [ ] Aggiornare eventuali test che verificano la scadenza del token
```

Note: nessuna sezione Frontend perché il cambio è interamente backend + email template (gestita dal design system, non da codice frontend dell'app).
