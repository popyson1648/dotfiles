# Configure Pre-commit

## Goal

Configure local pre-commit hooks so repository verification runs before commits
and pushes.

## Scope

- Update `.pre-commit-config.yaml`.
- Update `.project/` documentation that describes local checks.
- Install local Git hook entrypoints when possible.

## Non-goals

- Do not add network-fetched hook repositories.
- Do not change dotfile contents unrelated to verification.
- Do not commit or merge changes.

## Assumptions

- `pre-commit` is installed locally.
- `scripts/verify.py` is the source of truth for verification phases.
- Hook commands should not create generated files in the working tree.

## Steps

- Add explicit pre-commit and pre-push local hooks.
- Keep both hooks routed through `scripts/verify.py`.
- Document install and run commands.
- Run `pre-commit run --all-files`.
- Run repository verification and whitespace checks.

## Verification

- `pre-commit run --all-files`
- `pre-commit run --hook-stage pre-push --all-files`
- `python3 scripts/verify.py`
- `git diff --check`

## Open Issues

- None.
