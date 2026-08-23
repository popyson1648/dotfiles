# Plan

## Goal

Fix zsh startup errors related to mise initialization and startup timing logs.

## Scope

- zsh startup files under `.config/zsh/`.
- Resolve mise from `PATH` first, then known macOS install locations.
- Guard optional local environment loading while checking known local paths.
- Make startup timing logs compatible with macOS zsh.
- Update the local Homebrew-managed mise version and keep supported mise settings.
- Verify the shell starts without the reproduced errors.

## Non-goals

- Installing mise or changing the user's selected tool versions.
- Refactoring the full zsh plugin setup.
- Changing unrelated shell aliases, plugins, or keychain behavior.

## Assumptions

- On macOS, mise may be installed by Homebrew at `/usr/local/bin/mise` or `/opt/homebrew/bin/mise`, or by the official installer at `~/.local/bin/mise`.
- The repository should prefer the user's active `PATH` when it can resolve `mise`.
- The installed mise version is Homebrew-managed and can be updated before validating `settings.idiomatic_version_file_enable_tools`.
- Startup logging can keep millisecond precision when a compatible timestamp source is available.

## Steps

1. Update `.config/zsh/.zshrc` so `log_time` uses a macOS-compatible millisecond timestamp source.
2. Update `.config/zsh/rc/pluginconfig/mise/mise_atload.zsh` to resolve `mise` with `command -v`, then fall back to known macOS locations.
3. Check the trailing local environment source in `.config/zsh/.zshrc` and load the readable candidate path.
4. Update the Homebrew-managed `mise` installation.
5. Restore `idiomatic_version_file_enable_tools = []` in `.config/mise/config.toml`.
6. Run `zsh -ic 'exit'` to confirm the startup errors are gone.
7. Run repository verification with `python3 scripts/verify.py`.

## Verification

- `zsh -ic 'exit'`
- `python3 scripts/verify.py`

## Open Issues

- None.
