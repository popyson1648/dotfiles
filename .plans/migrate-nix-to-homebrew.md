# Migrate Nix Tools to Homebrew

## Goal

Replace the local Nix-managed toolchain with Homebrew while retaining the
repository's dotfiles and the current local WezTerm configuration changes.

## Scope

- Declare the current general-purpose command-line tools in `Brewfile`.
- Initialize Homebrew from the portable zsh configuration.
- Remove the obsolete Nix-specific dotfile.
- Preserve and relink existing configuration safely during the machine migration.

## Non-goals

- Preserve Nix-only formatting and linting tools after Nix is removed.
- Change the current local WezTerm configuration choices.

## Assumptions

- Homebrew uses its supported Apple Silicon prefix, `/opt/homebrew`.
- Language runtimes remain managed by `mise` using `.config/mise/config.toml`.

## Steps

1. Inventory the active Nix and Home Manager packages.
2. Add equivalent Homebrew formulae and casks.
3. Relink the repository while preserving conflicts and WezTerm changes.
4. Remove nix-darwin and the Nix installation.
5. Verify shell startup and representative tools.

## Verification

- Run `brew bundle check --file Brewfile`.
- Run `python3 scripts/link-home.py --check`.
- Run `python3 scripts/verify.py`.
- Start a clean zsh and confirm that its tool paths do not reference `/nix`.

## Open Issues

- None.
