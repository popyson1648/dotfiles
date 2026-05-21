# Structure

## Top-level Directories

- `.config/`: tracked application and shell configuration.
- `.decisions/`: decision records for durable repository policies.
- `.github/workflows/`: GitHub Actions workflow files.
- `.plans/`: task plans.
- `.project/`: current project documentation and verification config.
- `.template/`: source templates for project docs and workflow files.
- `scripts/`: repository verification and maintenance scripts.

## Important Modules

- `scripts/verify.py`: reads `.project/verification.toml` and runs selected
  verification phases.
- `.project/verification.toml`: defines local, pre-commit, pre-push, and CI
  verification commands.
- `.pre-commit-config.yaml`: runs the verification script in pre-commit mode.
- `.github/workflows/ci.yml`: runs the verification script in CI mode.

## Where To Make Changes

- Tool configuration changes belong under that tool's existing `.config/`
  directory.
- Repository process changes belong in `.project/`, `.template/`, or
  `AGENTS.md`, depending on their scope.
- Reusable maintenance commands belong under `scripts/`.
- Plans belong under `.plans/`; durable decisions belong under `.decisions/`.

## Areas That Require Extra Care

- Files from cloud tools, browsers, password managers, SSH, GPG, and API clients
  often contain credentials and should not be tracked.
- Shell startup files can affect every terminal session; test them before
  treating changes as complete.
- Generated caches and logs should remain untracked.
- Verification workflow files must stay aligned with `.project/verification.toml`.
