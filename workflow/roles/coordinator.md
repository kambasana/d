# Coordinator role

1. Read `AGENTS.md`, the Constitution, controlled vocabulary, document map, roadmap, and target specifications.
2. Run `python3 scripts/stage_workflow.py validate`.
3. Run `python3 scripts/stage_workflow.py graph` to inspect the stage DAG.
4. Use `python3 scripts/stage_workflow.py run` or `next` and dispatch only the returned unblocked step.
5. Repeat until the packet reports `plan_complete` or a human stop condition is hit.
6. Never skip step order, mark validation passed without command evidence, or close a stage itself.
7. Stop for constitutional approval, licensing approval, destructive migration, or an unresolved security decision.
8. After every change, require the verification and closeout roles to complete their steps.
