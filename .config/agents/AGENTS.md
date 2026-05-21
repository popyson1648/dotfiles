# Global Working Rules

## Scope

This file defines cross-repository working rules.

Repository-specific structure, workflows, verification config, and documentation rules belong in the project-level AGENTS.md.

## Before Starting Work

- Read the project-level AGENTS.md when it exists.
- Create a plan before implementation when the task is not trivial.
- Do not start implementation until the user has reviewed and approved the plan.

## Research

- If specifications, framework behavior, library behavior, CLI behavior, or implementation details are unclear, verify them before proceeding.
- Prefer official documentation and primary sources.

## File Creation Rules

- Do not create temporary files or directories in the project root.
- Store temporary working files under `.tmp/` when they must be kept inside the project.
- When `.tmp/` is used, add `.tmp/` to `.git/info/exclude` if it is not already listed.
- Do not create new files or directories in the project root unless they are directly required for the repository source, build, test, documentation, or tool configuration.
- If a new root-level file or directory is necessary, tell the user what needs to be created, why it is needed, and where it should be placed.
- Tool-generated files and directories may be created at the project root only when that location is the normal and expected location for the tool.
- Do not add `.tmp/` to `.gitignore`.
- `.tmp/` is for temporary working files only.
- Do not commit files under `.tmp/`.
- Do not keep temporary files longer than necessary.

## Branch Policy

- Create and switch to a dedicated Git branch before starting work.
- Never work directly on the main branch.
- Keep unrelated changes out of the same branch.

## Implementation

- Keep implementation aligned with the approved plan.
- Keep code changes, config changes, test changes, and documentation changes consistent with each other.
- If the change requires tests, add or update them.

## Verification

- Verify every change before treating the task as complete.
- Run the appropriate checks for the change.
- Do not report completion if verification is incomplete or if required checks fail.
- For UI-related changes, use appropriate UI verification methods.

## Final Review

- Before finishing, review the completed work for correctness, consistency, regressions, code quality and maintainability, and performance risk.
- If an issue is found, fix it and rerun the necessary verification.

## Completion

- In the completion report, state:
  - what changed
  - what was verified
  - how it was verified
  - whether any known concern remains
- Never merge automatically.
- Ask the user before merging.

## Security

- Do not expose secrets, credentials, or private keys.
- Be careful with commands that modify files, Git history, or system state.
- Prefer transparent and reviewable changes.
