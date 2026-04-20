# Lessons Learned

This directory captures debugging insights, non-obvious behaviors, and architectural patterns discovered during development. It is a core part of the **compound learning loop**.

## The Compound Learning Loop

1. **Consult** (during Planning): Before starting any implementation or debugging task, search this directory for relevant prior knowledge. Ask: "Have we solved a similar problem before? Are there known pitfalls in this area?"

2. **Capture** (after Debugging/Fixing): After resolving any non-trivial bug or unexpected behavior, write a lesson-learned doc. If the root cause was surprising or non-obvious, always capture it.

3. **Promote** (when a pattern recurs): If a lesson represents a universal rule that should be enforced on every task, add a concise rule to `CLAUDE.md`. Not every lesson needs promotion — only persistent traps or architectural patterns.

## When to Write a Lesson

Write a lesson when:
- A bug took significant investigation to diagnose
- The root cause was non-obvious or counter-intuitive
- The same mistake has been made more than once
- A pattern/anti-pattern emerged that future work should know about
- An integration or library behaves unexpectedly

Do NOT write a lesson for:
- Typos or trivial fixes
- One-off configuration issues
- Things already well-documented in library docs

## Lesson Format

Use the template in [TEMPLATE.md](TEMPLATE.md). Each lesson should be a standalone document that future developers can find via keyword search and understand without additional context.

## Searching Lessons

```bash
# Search by keyword
grep -r "keyword" docs/lessons-learned/

# List all lessons
ls docs/lessons-learned/
```

## When to Promote to CLAUDE.md

A lesson should be promoted to a rule in `CLAUDE.md` when:
- The mistake has occurred **more than once** across different tasks
- It involves a project-specific convention that isn't obvious from the code
- Violating it causes **production issues** or hard-to-debug failures
- It's a pattern that every agent session should check automatically

Promotion format: Add a concise section to `CLAUDE.md` with the rule, a wrong/correct example, and a link back to the full lesson-learned doc.
