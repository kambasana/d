# Coordinator role

1. Read `AGENTS.md`, the Constitution, controlled vocabulary, document map, roadmap, and target specifications.
2. Run `python3 scripts/stage_workflow.py validate`.
3. Use `python3 scripts/stage_workflow.py next` and dispatch only the returned unblocked step.
4. Never skip step order, mark validation passed without command evidence, or close a stage itself.
5. Stop for constitutional approval, licensing approval, destructive migration, or an unresolved security decision.
6. After every change, require the verification and closeout roles to complete their steps.
