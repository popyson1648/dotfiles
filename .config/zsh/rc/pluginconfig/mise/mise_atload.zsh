mise_bin="$(command -v mise 2>/dev/null)"
if [ -z "$mise_bin" ]; then
  mise_candidates=("$HOME/.local/bin/mise")

  if [ "$(uname -s)" = "Darwin" ]; then
    mise_candidates=(
      "/opt/homebrew/bin/mise"
      "/usr/local/bin/mise"
      "$mise_candidates[@]"
    )
  fi

  for mise_candidate in "${mise_candidates[@]}"; do
    if [ -x "$mise_candidate" ]; then
      mise_bin="$mise_candidate"
      break
    fi
  done
fi

if [ -n "$mise_bin" ] && [ -x "$mise_bin" ]; then
  eval "$("$mise_bin" activate zsh)"
fi
