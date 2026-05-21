# Rewrite Sensitive Scan In Python

## Goal

Replace the shell implementation of the sensitive file scanner with Python.

## Scope

- Add `scripts/scan-secrets.py`.
- Point verification to the Python scanner.
- Remove the shell scanner that was introduced under `scripts/`.
- Update documentation that shows direct scanner commands.

## Non-goals

- Do not change the scanner policy.
- Do not remove local credential files.
- Do not change unrelated dotfiles.

## Assumptions

- Python 3.11 or newer is available wherever verification runs.
- Tracked file content scanning should not print secret values.
- Sensitive-looking local file names should fail only when not ignored by Git.

## Steps

- Port the current scanner behavior to Python.
- Keep output labels stable enough for hook logs.
- Update `.project/verification.toml`.
- Update `.project/testing.md`.
- Run direct scanner, CI mode, pre-commit, pre-push, and diff checks.

## Verification

- `python3 scripts/scan-secrets.py`
- `python3 scripts/verify.py --mode ci`
- `pre-commit run --all-files`
- `pre-commit run --hook-stage pre-push --all-files`
- `git diff --check`

## Open Issues

- None.
