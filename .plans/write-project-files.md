# Write Project Files

## Goal

Fill the `.project/` documentation with concise, repository-specific guidance for this dotfiles repository.

## Scope

- Update the existing `.project/*.md` files in English.
- Update `.project/verification.toml` so `python3 scripts/verify.py` can run against the current repository.
- Leave unrelated dotfile changes untouched.

## Non-goals

- Do not reorganize dotfiles.
- Do not change tracked application configuration.
- Do not merge or publish the branch.

## Assumptions

- This repository is the source of selected personal dotfiles under `.config/`.
- Verification should be lightweight and runnable in local hooks and CI.
- Secret scanning policy is documented because dotfiles can easily contain credentials.

## Steps

- Create a dedicated branch.
- Replace placeholder `.project/` sections with project-specific content.
- Configure verification phases with currently runnable commands.
- Run `python3 scripts/verify.py`.
- Review the final diff.

## Verification

- Run `python3 scripts/verify.py`.
- Check `git diff -- .project .plans/write-project-files.md`.

## Open Issues

- None.
