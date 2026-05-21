# Project Guide

## What This Project Is

This repository stores selected personal dotfiles and developer tool configuration.
Most managed files live under `.config/`, with repository metadata, verification
scripts, plans, decisions, and project documentation kept at the repository root.

Treat this repository as configuration source, not as a general backup of a home
directory. Add only files that are useful to recreate or review the development
environment.

## Where To Start

- Read `AGENTS.md` for repository rules before changing files.
- Read `.project/structure.md` to understand the directory layout.
- Read `.project/testing.md` before reporting work as complete.
- Use `.plans/` for task plans and `.decisions/` for lasting project decisions.

## Minimum Setup

- Git.
- Python 3.11 or newer for `scripts/verify.py`.
- `pre-commit` when running the local hook workflow.
- Tool-specific applications only when editing their configuration, such as
  Neovim, WezTerm, tmux, zsh, mise, or Karabiner.

## Related Documents

- `.project/structure.md`: repository layout and ownership boundaries.
- `.project/conventions.md`: naming, style, review, and forbidden patterns.
- `.project/testing.md`: verification expectations.
- `.project/build.md`: setup and run notes.
- `.project/release.md`: publication and rollback notes.
- `.project/verification.toml`: verification phase configuration.
