---
name: breaking-changes
description: Analyze code changes for breaking changes, regressions, and risky modifications by inspecting both the diff AND the codebase. Use this skill whenever the user asks to review a diff for breaking changes, types something like "breaking changes?", "any breaking changes?", "review my diff", "check my changes", "safe to merge?", or pastes a git diff and asks about its impact. Also trigger when the user asks about API compatibility, backward compatibility, or safe-to-deploy checks on code changes.
---

# Breaking Changes Analyzer

Analyze code changes for breaking changes by inspecting the diff, the full files, and the broader codebase. A diff alone is not enough — you must verify how changed symbols are actually used.

## Step 1: Obtain the diff

1. If the user pastes a diff directly, use that.
2. If the user provides no diff, run `git diff` (or `git diff --staged` if they mention staged changes).
3. If comparing branches: `git diff main..HEAD` (or whatever the target branch is).
4. If neither works, ask the user to provide the diff.

## Step 2: Identify candidates

Scan the diff for potential breaking changes. Build a list of **candidates** — symbols, endpoints, fields, configs, types that were removed, renamed, or had their signature/shape changed.

For each candidate, note:
- The symbol name (function, class, endpoint, field, env var, etc.)
- The file it's in
- What changed (removed, renamed, signature change, type change, etc.)

## Step 3: Investigate each candidate (CRITICAL)

Do NOT classify a change as breaking based on the diff alone. For each candidate, actively investigate:

### 3a. Is it public or internal?
Read the full file (not just the diff hunk) to determine visibility:
- Check export statements (`export`, `module.exports`, `__all__`, `pub`, etc.)
- Check if it's in an index/barrel file (`index.ts`, `__init__.py`, `mod.rs`)
- Check access modifiers (`public`, `private`, `protected`, `internal`)
- Check `package.json` exports, API route registration, OpenAPI specs

If a symbol is not exported or is clearly internal, downgrade severity.

### 3b. Who depends on it?
Search the codebase for usages of changed symbols:
```bash
# Use ripgrep if available, fall back to grep
rg "symbolName" --type-add 'src:*.{ts,js,py,rs,go,java}' -t src -l
# or
grep -r "symbolName" --include="*.ts" --include="*.py" -l
```

Count and list callers. If a removed function has 15 callers across the codebase, that's very different from zero callers.

### 3c. Is it referenced in tests?
```bash
rg "symbolName" --glob "*test*" --glob "*spec*" -l
```
Broken tests are a signal but not the full picture — the real concern is production callers.

### 3d. For API/schema changes, check consumers
- Look at API route definitions and middleware
- Check for OpenAPI/Swagger specs that document the endpoint
- Look at database migration files and ORM models
- Check for client SDK or generated types that depend on the shape

### 3e. For dependency changes
- Compare old vs new version in `package.json`, `Cargo.toml`, `requirements.txt`, etc.
- If a major version bump, note it — the transitive API may have changed

## Step 4: Detect the project type

Quickly determine what kind of project this is, as it affects severity:
- **Published library/package**: Any public API change is breaking. Check for semver.
- **Internal service with consumers**: Breaking if other services call it. Check for API clients.
- **Standalone app/monolith**: Most changes are safe unless they affect shared contracts (DB schema, message formats, env vars).
- **Monorepo**: Check cross-package imports. A "private" function might be imported by a sibling package.

Run these checks:
```bash
# Is it a published package?
cat package.json 2>/dev/null | grep -E '"name"|"version"|"private"'
cat setup.py 2>/dev/null | head -5
cat Cargo.toml 2>/dev/null | head -10

# Does it have API routes?
rg -l "router\.|app\.(get|post|put|delete|patch)" --max-depth 3
rg -l "@app\.route|@router\." --max-depth 3
```

## Step 5: Run tests (if quick and available)

If there's an obvious test command and the project is set up for it, run a quick test pass:
```bash
# Only if fast (<30 seconds) and the user hasn't said not to
npm test 2>&1 | tail -20
pytest --tb=short -q 2>&1 | tail -20
cargo test 2>&1 | tail -20
```
If tests take too long or aren't set up, skip this. Don't waste time debugging test infra.

## Step 6: Classify findings

After investigation, classify each candidate:

| Severity | Meaning |
|----------|---------|
| 🔴 BREAKING | Confirmed: exported/public symbol changed + has callers/consumers that will break |
| 🟡 RISKY | Changed symbol is public but no callers found in this repo, OR behavioral change that could break edge cases, OR new required field without default, OR changed defaults |
| 🟢 SAFE | Internal-only change, additive change (new exports, optional fields), refactor with no public surface change, docs, tests |

Key distinction: a removed function with zero callers in the codebase is 🟡 RISKY (might have external consumers), not 🔴 BREAKING. A removed function with 10 callers is 🔴 BREAKING.

## Output format

### Summary
One-line verdict: "X breaking, Y risky changes found" or "No breaking changes detected."

### Findings (if any)
For each finding:
- **Severity**: emoji + label
- **What changed**: concise description
- **Where**: file and line
- **Evidence**: callers found, export status, test impact (show the commands you ran and what they revealed)
- **Impact**: who/what breaks and how
- **Suggestion**: how to make it non-breaking (deprecation, default value, alias, etc.)

Sort by severity (🔴 first, then 🟡).

### Safe changes
Brief summary of 🟢 changes. No need to detail each one unless asked.

### Investigation log
Briefly list the commands you ran and what they found. This builds trust and lets the user verify your work.

## Tone

Be direct. Show your work — the commands you ran and what they revealed. If there are no breaking changes, say so and move on. If the diff is massive, focus on the highest-impact changes first.