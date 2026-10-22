# Worker brief and return contract

Provide a compact concrete brief, filling only the fields relevant to the worker:

- **Task and done criteria:** requested artifact or review, intended audience/environment, actual pass conditions and scope limits.
- **Instructions:** absolute `SKILL.md` path(s), required relevant references, project root/current README and applicable instructions. Require reading them, not just acknowledging skill names.
- **Inputs:** source, reference roles, selected voice, map/config versions, exact file paths/hashes and important uncertainty. Point to raw evidence rather than copying large histories or secrets.
- **Ownership:** exclusive write paths/modules, read-only boundaries, staging output names and who can update shared manifests. Record handoff before another worker edits owned files.
- **Dependencies:** needed upstream versions, work that can proceed independently and actions blocked on missing evidence/authorization. Report any input changing during execution.
- **Resources:** existing permitted destination/actions, allotted cumulative credits or other ceiling, outstanding requests and retry limit. No global credentials in briefs; use the established secure provider path.
- **Verification:** required technical and perceptual checks, evidence paths, final hash bindings and what must remain held if tools are unavailable.
- **Return:** actual outputs/hashes, methods/tests actually run and observed results, coverage/limitations, defects, receipts/cost/unknown requests and readiness for the next stage.

For a fresh adversarial or independent checker, supply the edit contract, raw inputs, frozen final artifacts and required checks. Withhold the producer's proposed verdict and suspected diagnosis until the checker has made observations. Sharing necessary provenance/known scope is appropriate; hiding a prerequisite or giving an intentionally incomplete input set is not independence.

## Coordinator ledger

Keep a compact run record containing stage ID/owner, current state, input/output hashes, map/reference/config versions, required checks, actual evidence, reservations/spend, unresolved issues and downstream dependents. Reuse a project-approved run receipt format if it exists. Do not maintain a second canonical plan or claim worker completion from a queued dispatch alone.

Wait for actual results using the available bounded coordination tools; monitor meaningful changes and communicate findings. Do not busy-poll unchanged workers or block all useful work on one missing answer. Release ownership/resources only after their state is reconciled; an unknown paid request remains outstanding.
