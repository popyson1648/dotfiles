function ghq-cd() {
  local dir
  dir=$(ghq list --full-path | peco) && cd "$dir"
}
