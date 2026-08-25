# Closeout role

Close a stage only after all preceding steps are complete and every required command passes.

1. Complete every phase-gate field from AWG-OPS-001.
2. Cite acceptance-test IDs and repository evidence files.
3. Record exact validation commands and `passed` results.
4. State limitations, unresolved risks, and a bounded release decision.
5. Set the closeout status to `ready`.
6. Run `python3 scripts/stage_workflow.py complete <stage> closeout`.
7. Commit and push authored changes, regenerated reports, and gate evidence.

Never claim human approval, licensing approval, empirical validity, or production readiness without explicit evidence.
