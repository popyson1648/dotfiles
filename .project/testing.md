# Testing

## Test Types

- Repository verification through `python3 scripts/verify.py`.
- Syntax checks for shell and Python files under `scripts/`.
- Secret scanning of tracked files and sensitive-looking local file names.
- Manual tool checks for changed dotfiles when automated checks are not
  available.
- Secret review before adding or moving configuration files.

## Minimum Checks Before Completion

Run:

```sh
python3 scripts/verify.py
```

Then review the final diff for unrelated changes and sensitive data.

Before committing, run the local hook set directly:

```sh
pre-commit run --all-files
```

## Checks By Change Type

- Python scripts: run `python3 scripts/verify.py`; CI parses every
  `scripts/*.py` file without writing cache files.
- Shell scripts: run `python3 scripts/verify.py`; CI runs `bash -n` for every
  `scripts/*.sh` file.
- zsh, tmux, Neovim, WezTerm, mise, or other tool config: run repository
  verification and manually start or reload the affected tool when practical.
- Documentation-only changes: run repository verification and review the
  rendered Markdown structure.
- New dotfiles: run repository verification and perform a focused secret review.
- New credential-like local paths: add the path to `.gitignore` before running
  verification.

## How To Run Verification

Run all enabled phases:

```sh
python3 scripts/verify.py
```

List phases selected for CI:

```sh
python3 scripts/verify.py --mode ci --list
```

Run the pre-commit subset:

```sh
python3 scripts/verify.py --mode pre-commit
```

Run the configured pre-commit hook against all files:

```sh
pre-commit run --all-files
```

Run the configured pre-push hook against all files:

```sh
pre-commit run --hook-stage pre-push --all-files
```

Run the secret scanner directly:

```sh
python3 scripts/scan-secrets.py
```

Run the CI-selected verification phases locally:

```sh
python3 scripts/verify.py --mode ci
```
