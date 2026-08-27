---
name: commit-chunks
description: Analyze a dirty Git working tree and turn it into small, coherent commits with copy-paste git add and git commit commands. Use when the user asks to split work into commits, prepare commit chunks, or wants a commit guide without having the agent commit.
disable-model-invocation: true
---

# Commit chunks

Produce a copy-paste commit guide. Never stage, commit, restore, reset, clean, stash, or otherwise mutate Git state.

## Inspect the work

For each requested repository:

1. Run `git status --short`.
2. Inspect staged and unstaged diffs, including untracked files.
3. Read recent commit subjects with `git log -8 --oneline`.
4. Use conversation context to distinguish work produced in this session from unrelated user changes.
5. If repository scope is ambiguous, ask which repository to process first.

Do not read likely secret files such as `.env`, credentials, keys, or tokens. Warn if one appears in the working tree.

## Design the commits

- Group files by one user-visible behavior or technical concern.
- Keep implementation and its tests in the same commit.
- Keep tightly coupled files together.
- Order foundation commits before their consumers.
- Aim for commits that compile independently.
- Do not split merely to make commits smaller.
- Do not mix unrelated cleanup into a feature commit.
- Account for already staged changes explicitly.
- Never use `git add .` or `git add -A`.

Prefer file-level staging. If one file contains changes for multiple proposed commits:

1. Keep those concerns together when that still produces a coherent commit.
2. Otherwise use `git add -p <file>` and explain which hunks belong in that commit.
3. State clearly that interactive hunk staging is not a single blind copy-paste operation.

Call out modified files intentionally left out of the guide.

## Commit messages

Match the repository's recent style. If it uses Conventional Commits, choose the accurate type and scope:

- `feat` for new behavior.
- `fix` for corrected behavior or access control.
- `refactor` for behavior-preserving restructuring.
- `test`, `docs`, or `chore` only when they accurately describe the whole commit.

Keep the subject concise and explain the purpose, not the file operations.

## Output

Start with the repository in which the commands must run. Then provide numbered commits in dependency order.

For each commit, output one directly copyable Bash block:

```bash
git add \
  path/to/file-one \
  path/to/file-two

git commit -m "feat(scope): describe the outcome"
```

Use exact repository-relative paths. End with a short note listing unrelated or intentionally uncommitted files.

Do not execute any command from the generated guide.
