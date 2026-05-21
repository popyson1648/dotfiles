# Add CI Scripts Validation

## Goal

Ensure CI verifies the contents of the `scripts/` directory.

## Scope

- Add verification phases for shell and Python scripts under `scripts/`.
- Keep local pre-commit, pre-push, and CI behavior aligned.
- Update testing documentation.

## Non-goals

- Do not change CI workflow structure unless the verification runner cannot
  cover the checks.
- Do not add generated files or external hook dependencies.
- Do not rewrite existing scripts.

## Assumptions

- GitHub Actions already runs `python3 scripts/verify.py --mode ci`.
- Script syntax checks should avoid writing `__pycache__` or other generated
  files.
- Current script checks should be lightweight enough for pre-commit.

## Steps

- Add a shell syntax phase for `scripts/*.sh`.
- Add a Python syntax phase for `scripts/*.py`.
- Mark both phases for edit, pre-commit, pre-push, and CI modes.
- Document the script checks.
- Run CI mode and local hook verification.

## Verification

- `python3 scripts/verify.py --mode ci`
- `pre-commit run --all-files`
- `pre-commit run --hook-stage pre-push --all-files`
- `git diff --check`

## Open Issues

- None.
