zsh_start_time=$(date +%s%3N)
function log_time() {
  local now=$(date +%s%3N)
  local elapsed=$((now - zsh_start_time))
  echo "[${elapsed} ms] $1"
  zsh_start_time=$now
}

log_time "start .zshrc"

## path
log_time "load path.zsh"
source "$ZRCDIR/path.zsh"

## Aliases
log_time "load alias.zsh"
source "$ZRCDIR/alias.zsh"

## zsh plugins
log_time "load plugins.zsh"
source "$ZRCDIR/plugins.zsh"

## Other plugins
log_time "load pluginconfig .zsh files"
plug_dir="$ZRCDIR/pluginconfig"

# pluginconfig 以下のすべてのサブディレクトリも含めて .zsh ファイルを探し
# 存在する場合に source を実行
while IFS= read -r -d '' f; do
  log_time "  sourcing $f"
  source "$f"
done < <(find "$plug_dir" -type f -name '*.zsh' -print0)


# Wrapper function for `ghq get` that expands shorthand GitHub repository arguments into full SSH URLs.
# Usage:
#   ghq get xxx/yyy
#     -> ghq get git@github.com:xxx/yyy.git
#   ghq get me yyy
#     -> ghq get git@github.com:popyson1648/yyy.git
ghq() {
  if [ "$1" = "get" ] && [ "$2" = "me" ] && [ -n "$3" ] && [ -z "$4" ]; then
    command ghq get "git@github.com:popyson1648/$3.git"
    return
  fi

  if [ "$1" = "get" ] && [ -n "$2" ] && [ -z "$3" ]; then
    case "$2" in
      *@*:*|http://*|https://*)
        command ghq "$@"
        ;;
      *)
        command ghq get "git@github.com:$2.git"
        ;;
    esac
    return
  fi

  command ghq "$@"
}


## SSH keychain（再利用）
log_time "keychain"
keychain_output_file="$HOME/.keychain/$(hostname)-zsh"
if [ -r "$keychain_output_file" ]; then
  log_time "  reusing existing agent"
  source "$keychain_output_file"
else
  log_time "  starting new agent"
  eval "$(keychain --eval --quiet --agents ssh ~/.ssh/id_ed25519)"
fi

# tmux使用時はssh-agentの環境変数をtmuxに共有
if [ -n "$TMUX" ]; then
  log_time "tmux ssh-agent export"
  tmux set-environment -g SSH_AUTH_SOCK "$SSH_AUTH_SOCK"
  tmux set-environment -g SSH_AGENT_PID "$SSH_AGENT_PID"
fi

log_time "end .zshrc"


. "$HOME/.local/share/../bin/env"
