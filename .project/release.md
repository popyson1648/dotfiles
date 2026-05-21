# Release

## When Release Is Needed

This repository normally does not produce formal software releases. A release is
only needed when a stable dotfile snapshot must be shared, tagged, or restored
across machines.

## Release Steps

1. Confirm the working tree contains only intended changes.
2. Run repository verification:

   ```sh
   python3 scripts/verify.py
   ```

3. Review the diff for secrets and machine-local files.
4. Commit on a dedicated branch.
5. Push the branch and open a pull request or review it manually.
6. Tag only after review confirms the snapshot is safe to reuse.

## Required Checks

- `python3 scripts/verify.py`.
- Manual review of newly added dotfiles.
- Secret review for any file that may contain credentials, tokens, cookies, or
  cloud authentication material.

## Rollback Or Recovery Notes

- Revert the specific commit that introduced a bad configuration when possible.
- If a secret is committed, rotate the secret immediately, remove it from the
  repository history through the chosen remediation process, and document the
  decision in `.decisions/`.
- Keep machine-specific recovery steps out of tracked files unless they are safe
  and broadly reusable.
