---
name: naming
description: Help choose good variable, function, component, hook, type, and file names. Use this skill whenever the user asks for naming help, says things like "what should I name this", "name this variable", "naming suggestions", "better name for", "rename this", or is clearly struggling to name something in their code. Also trigger when reviewing code and a name is unclear or misleading. Optimized for TypeScript, React, and Next.js conventions.
---

# Naming Advisor

Help the user choose precise, idiomatic names for variables, functions, components, hooks, types, files, and routes. Provide multiple options with trade-off analysis and a clear recommendation.

## Step 1: Understand what's being named

Ask only if truly ambiguous. Otherwise infer from context:
- What is it? (variable, function, component, hook, type, constant, file, route, API endpoint)
- What does it hold or do? (its purpose, not its implementation)
- Where does it live? (component scope, module scope, global, shared util, API layer)
- What type is it? (boolean, array, record, callback, Promise, React node, etc.)

## Step 2: Apply naming conventions

### TypeScript general
- `camelCase` for variables, functions, parameters, methods
- `PascalCase` for types, interfaces, enums, classes
- `UPPER_SNAKE_CASE` for true constants (config values, magic numbers, env keys)
- Prefix interfaces with nothing — no `I` prefix. Use `Props`, `State`, `Config` suffixes when appropriate
- Generic type params: `T`, `K`, `V` for simple cases; descriptive like `TResponse`, `TItem` for complex ones

### Booleans
- Prefix with `is`, `has`, `can`, `should`, `was`, `will` — always a yes/no question
- `isLoading` not `loading` (avoids ambiguity: is `loading` a verb or adjective?)
- `hasPermission` not `permission` (is it the permission object or a flag?)
- `canEdit` not `editable` (clearer intent in conditionals)
- For props: `isDisabled`, `isOpen`, `hasError` — keep the prefix even in JSX

### Arrays and collections
- Always plural: `users`, `items`, `selectedIds`
- For a list that will be rendered: `items`, not `itemList` or `itemArray` (the type already says it's an array)
- Maps/Records: name by the lookup pattern — `usersById`, `permissionsByRole`, `priceMap`

### Functions
- Start with a verb: `getUser`, `createOrder`, `validateEmail`, `formatDate`
- Event handlers: `handleClick`, `handleSubmit`, `handleChange` — or `onItemClick` if passed as a prop
- Async functions: name by what they return, not the mechanism — `fetchUser` not `callUserApi`
- Transformers/mappers: `toDisplayName`, `fromApiResponse`, `parseConfig`
- Predicates (return boolean): `isValid`, `hasAccess`, `canProceed` — same rules as boolean variables

### React components
- `PascalCase`, always
- Name by what it renders, not how: `UserProfile` not `UserProfileRenderer`
- Avoid redundant suffixes: `UserCard` not `UserCardComponent`
- Layout components: `Sidebar`, `Header`, `PageLayout`, `Container`
- Pages in Next.js: the file path IS the name — focus on the directory structure

### React hooks
- Always `use` prefix: `useAuth`, `useDebounce`, `useLocalStorage`
- Name by what they provide, not how they work: `useUser` not `useFetchUserFromApiAndCache`
- Return value naming: `{ data, error, isLoading }` pattern for async hooks
- If a hook is specific to a feature: `useCartItems`, `useInvoiceFilters`

### Props and types
- Component props: `ComponentNameProps` — e.g., `ButtonProps`, `UserCardProps`
- Callback props: `onAction` pattern — `onSubmit`, `onClick`, `onChange`, `onDismiss`
- Render props: `renderItem`, `renderHeader`, `renderEmpty`
- Generic types: `ApiResponse<T>`, `Paginated<T>`, `WithId<T>`
- Discriminated unions: use a `type` or `kind` field — `{ kind: 'success', data: T } | { kind: 'error', error: E }`

### Next.js specific
- API routes: verb-oriented — `/api/users/create`, `/api/auth/login`
- Server actions: `createUser`, `deletePost` — plain verbs, they're functions
- Route params: match the domain — `[slug]`, `[userId]`, `[teamId]`
- Middleware and config: `middleware.ts`, `next.config.ts` — follow Next.js conventions exactly
- Server vs client components: no naming convention needed, the `"use client"` directive is enough

### Constants and config
- `UPPER_SNAKE_CASE` for static values: `MAX_RETRIES`, `API_BASE_URL`, `DEFAULT_PAGE_SIZE`
- Enum-like objects: `const STATUS = { ACTIVE: 'active', INACTIVE: 'inactive' } as const`
- Feature flags: `ENABLE_NEW_CHECKOUT`, `SHOW_BETA_FEATURES`

## Step 3: Generate options

Provide 3-4 naming options. For each option:

**Name**: the proposed name
**Style**: which convention it follows
**Pros**: what makes it good (clarity, brevity, idiomaticity, searchability)
**Cons**: what's not ideal (too long, ambiguous, unconventional, could be confused with X)

## Step 4: Recommend one

Pick the best option and explain why in one sentence. Optimize for this priority order:

1. **Clarity** — a reader unfamiliar with the code understands what it is
2. **Convention** — it follows TypeScript/React/Next.js idioms
3. **Brevity** — shorter is better, but never at the cost of clarity
4. **Searchability** — easy to grep for, distinct from similar names in the codebase
5. **Consistency** — matches patterns already used in the user's code (if visible)

## Quick decision tree

```
Is it a boolean?
├─ Yes → is/has/can/should prefix
└─ No → Is it a function?
    ├─ Yes → Start with verb (get, create, handle, fetch, parse, validate)
    └─ No → Is it a React hook?
        ├─ Yes → use prefix (useAuth, useDebounce)
        └─ No → Is it a React component?
            ├─ Yes → PascalCase noun (UserCard, Sidebar)
            └─ No → Is it a constant?
                ├─ Yes → UPPER_SNAKE_CASE (MAX_RETRIES, API_BASE_URL)
                └─ No → Descriptive noun, camelCase (currentUser, selectedItems)
```

## Acceptable abbreviations

These are universally understood — don't expand them:

`id`, `url`, `api`, `html`, `css`, `db`, `io`, `ui`, `src`, `dest`, `config`, `env`, `auth`, `admin`, `dev`, `prod`, `min`, `max`, `ref`, `props`, `params`, `args`

**Context-specific (acceptable only in their domain):**
`req`, `res` (HTTP handlers), `err` (error handling), `ctx` (context), `el` (DOM elements), `i`, `j`, `k` (loop counters), `e` (event handlers), `fn` (higher-order function params)

**Everything else — spell it out.** `usr` → `user`, `btn` → `button`, `msg` → `message`, `calc` → `calculate`.

## Anti-patterns to flag

If the user's current name has any of these problems, call it out:
- **Type-in-name**: `userArray`, `nameString`, `isLoadingBoolean` — the type system handles this
- **Hungarian notation**: `strName`, `arrItems`, `bIsValid` — not idiomatic in TS
- **Implementation leak**: `fetchAndCacheUser` — name the WHAT, not the HOW
- **Negated booleans**: `isNotReady`, `hasNoPermission` — hard to read in conditionals (`if (!isNotReady)`)
- **Generic names**: `data`, `info`, `result`, `temp`, `stuff` — almost always too vague
- **Abbreviations**: `usr`, `btn`, `msg` — spell it out unless it's a universally known abbreviation (`id`, `url`, `api`)
- **Redundant context**: `UserComponent` inside a `components/` folder, `IUserInterface` — the structure already tells you

## Output format

Keep it tight. Example:

---

**Naming: function that fetches the current user's subscription status**

| # | Name | Pros | Cons |
|---|------|------|------|
| 1 | `getSubscriptionStatus` | Clear, verb-first, standard | Doesn't specify "current user" |
| 2 | `fetchCurrentSubscription` | Implies async, scoped to current user | `fetch` suggests network call — fine if it is one |
| 3 | `useSubscription` | Idiomatic if it's a hook | Only valid inside a React component |
| 4 | `checkSubscription` | Short | `check` is vague — returns status or boolean? |

**→ Recommended: `getSubscriptionStatus`** — clear, greppable, and works whether it's sync or async. Use `useSubscription` if it's a hook.

---

## Tone

Be opinionated. The user is asking because they want a good answer, not a diplomatic non-answer. If their current name is bad, say so and say why.