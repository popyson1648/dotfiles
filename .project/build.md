# Build

## Prerequisites

- Python 3.11 or newer.
- Git.
- `pre-commit` for local hook checks.
- The target tool when validating a specific dotfile manually.

## Setup

This repository does not require a build step. Clone it, inspect the files to be
used, and link or copy selected configuration into the expected home-directory
locations outside this repository.

Install local hooks when needed:

```sh
pre-commit install
```

Install both configured hook types explicitly:

```sh
pre-commit install --hook-type pre-commit --hook-type pre-push
```

## Build

No build artifact is produced. The closest equivalent to a build is repository
verification:

```sh
python3 scripts/verify.py
```

## Run

Dotfiles are consumed by their owning tools after they are placed in the normal
configuration paths. Examples include:

- zsh reads `.config/zsh/.zshrc` and related files.
- Neovim reads `.config/nvim/init.lua`.
- tmux reads `.config/tmux/.tmux.conf`.
- WezTerm reads `.config/wezterm/wezterm.lua`.

Validate tool behavior with the tool itself after changing its configuration.

## Common Failures

- `python3` is too old: use Python 3.11 or newer.
- A local hook cannot find `python3`: ensure Python is on `PATH`.
- `pre-commit` is missing: install it before enabling local hooks.
- A tool does not read a changed file: confirm the file is linked or copied to
  the location expected by that tool.
- A configuration file contains machine-local paths: document the assumption or
  keep the value out of the tracked file.
