#!/usr/bin/env bash

set -eu

script_dir=$(
  CDPATH= cd -- "$(dirname -- "$0")"
  pwd
)

dein_src="$script_dir/.vim/dein/repos/github.com/Shougo/dein.vim"
base16_src="$script_dir/.vim/pack/colors/start/base16-vim"

if [ ! -d "$base16_src" ]; then
  mkdir -p "$(dirname "$base16_src")"
  git clone --depth 1 https://github.com/chriskempson/base16-vim.git "$base16_src"
fi

if [ ! -d "$dein_src" ]; then
  mkdir -p "$(dirname "$dein_src")"
  git clone --depth 1 https://github.com/Shougo/dein.vim "$dein_src"
fi

vim -Nu "$script_dir/.vimrc" -n -es -i NONE \
  "+try | call dein#install() | finally | qall! | endtry"
