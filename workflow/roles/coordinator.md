# Coordinator role

1. Read `AGENTS.md`, the Constitution, controlled vocabulary, document map, roadmap, and target specifications.
2. Run `python3 scripts/stage_workflow.py validate`.
3. Run `python3 scripts/stage_workflow.py graph` to inspect the stage DAG.
4. Use `python3 scripts/stage_workflow.py loop` to drive every unblocked step, or `run`/`next` to dispatch one step at a time.
5. Continue until the report is `plan_complete`, or investigate the `blocked` stage, step, and reason.
6. Never skip step order, mark validation passed without command evidence, or close a stage itself.
7. Stop for constitutional approval, licensing approval, destructive migration, or an unresolved security decision.
8. After every change, require the verification and closeout roles to complete their steps.
