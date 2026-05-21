# Add Home Link Script

## Goal

Add a Python script that creates the requested home-directory symlinks and checks whether each destination already has the expected link.

## Scope

- Add one Python repository script for creating or checking these links.
- Keep the script idempotent: existing matching symlinks are reported as already correct.
- Detect conflicting existing paths and avoid overwriting them automatically.
- Include the exact link map requested by the user.

## Non-goals

- Do not move existing files or directories.
- Do not delete conflicting paths.
- Do not change unrelated dotfiles.

## Assumptions

- The script should be run from the repository root or be able to find paths relative to the script.
- The left side in the request is the link path under `$HOME`; the right side is the symlink target.
- Relative target `Document/Development` should be preserved as given unless implementation review shows the repository already normalizes targets.

## Steps

- Inspect existing script style and verification setup.
- Add the link script in the appropriate script location.
- Make the script print clear statuses for created, already-correct, missing-target, and conflict cases.
- Add or update lightweight verification if the repository has a suitable pattern.
- Run `python3 scripts/verify.py`.

## Verification

- Run repository verification with `python3 scripts/verify.py`.
- Run the new script in a non-mutating or dry-run/check mode if implemented.

## Open Issues

- None. The user confirmed that links should be created under `$HOME`.
