# Import Local Dotfiles

## Goal

Initialize this directory as the source for `popyson1648/dotfiles` without overwriting existing remote history.

## Steps

- Fetch the existing `origin/main` history.
- Create an import branch from `origin/main`.
- Add selected local dotfiles and ignore generated caches, logs, and credentials.
- Run the secret scanner before committing.
- Push the import branch to GitHub.
