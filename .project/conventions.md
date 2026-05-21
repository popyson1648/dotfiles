# Conventions

## Naming

- Keep dotfiles in the same relative path as their home-directory location when
  practical, especially under `.config/`.
- Use lowercase names for repository documentation and scripts unless an
  external tool requires another name.
- Name plans after the task, for example `.plans/import-local-dotfiles.md`.
- Name decisions after the policy or structure they record.

## Code Style

- Keep shell scripts POSIX-friendly where practical; use Bash only when the
  script declares Bash explicitly.
- Keep Python scripts compatible with Python 3.11.
- Prefer small, direct configuration files over generated or machine-specific
  output.
- Avoid broad rewrites of unrelated tool configuration during focused changes.

## Review Expectations

- Explain why new dotfiles are useful and where their owning tool reads them.
- Check for secrets before adding or moving configuration files.
- Add local credential paths to `.gitignore`; the secret scanner fails when
  sensitive-looking local file names are not ignored.
- Keep `.project/verification.toml`, `.pre-commit-config.yaml`, and
  `.github/workflows/ci.yml` aligned when verification behavior changes.
- Update `.project/` when workflows, structure, or required commands change.

## Forbidden Patterns

- Do not commit credentials, private keys, tokens, cookies, local browser
  profiles, cloud auth databases, or machine-only caches.
- Do not add temporary files to the repository root.
- Do not add `.tmp/` to `.gitignore`; use `.git/info/exclude` for local
  temporary work.
- Do not make unrelated formatting or organization changes while updating a
  specific tool configuration.
