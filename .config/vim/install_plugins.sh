#!/usr/bin/env bash

set -eu

script_dir=$(
  CDPATH= cd -- "$(dirname -- "$0")"
  pwd
)

dein_src="$script_dir/.vim/dein/repos/github.com/Shougo/dein.vim"

if [ ! -d "$dein_src" ]; then
  mkdir -p "$(dirname "$dein_src")"
  git clone --depth 1 https://github.com/Shougo/dein.vim "$dein_src"
fi

vim -Nu "$script_dir/.vimrc" -n -es -i NONE \
  "+try | call dein#install() | finally | qall! | endtry"
