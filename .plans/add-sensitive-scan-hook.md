# Add Sensitive Scan Hook

## Goal

Run secret scanning through the repository verification workflow and fail when
sensitive-looking local files are not ignored by Git.

## Scope

- Update the repository secret scanner.
- Add a secrets verification phase.
- Document the hook behavior in `.project/`.

## Non-goals

- Do not inspect or print secret values.
- Do not remove local credential files.
- Do not change unrelated dotfiles.

## Assumptions

- Git ignore rules are the source of truth for local credential directories.
- Secret pattern scanning should inspect tracked files only.
- Sensitive-looking local file names should be allowed only when ignored or
  explicitly allowed as repository tooling.

## Steps

- Scan tracked files for secret-like content patterns.
- Scan all local file names for sensitive names.
- Use `git check-ignore` to verify sensitive local file names are ignored.
- Add the scanner to `.project/verification.toml`.
- Run the scanner and pre-commit checks.

## Verification

- `python3 scripts/scan-secrets.py`
- `pre-commit run --all-files`
- `pre-commit run --hook-stage pre-push --all-files`
- `python3 scripts/verify.py`
- `git diff --check`

## Open Issues

- None.
