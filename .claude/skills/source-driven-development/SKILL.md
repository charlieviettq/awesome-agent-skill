---
name: source-driven-development
description: "Ground framework and library decisions in official documentation—detect versions, fetch relevant docs, cite sources, flag unverified patterns. Use when API correctness matters for React, Next.js, Python libs, cloud SDKs, or unfamiliar stacks."
allowed-tools: Read, Glob, Grep
---

# Source-driven development

## When to use

- Framework-specific code (React, Next, FastAPI, sklearn, etc.)
- User wants documented, version-correct patterns
- Unsure if training-data API is current

## When to relax

- Pure logic with no external API
- User explicitly wants speed over doc verification

## Process

```
DETECT versions -> FETCH official docs -> IMPLEMENT -> CITE or FLAG unverified
```

1. Read dependency files (`package.json`, `pyproject.toml`, etc.)
2. Fetch the **specific doc page** for the feature (not homepages)
3. Match signatures and patterns from docs
4. Cite URL for non-obvious choices; flag gaps as **UNVERIFIED**

## Source priority

1. Official documentation
2. Official changelog / migration guide
3. Web standards (MDN, etc.)
4. Not primary: blogs, Stack Overflow, training memory alone

## Conflicts

If docs conflict with existing codebase, surface options—do not silently pick one.

## Output

Brief citation in comments or PR for framework decisions; UNVERIFIED callouts when docs missing.
