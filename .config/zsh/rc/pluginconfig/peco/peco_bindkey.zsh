function peco-history-selection() {
function peco-history-selection() {
  BUFFER=$(fc -rl 1 | tac | awk '!a[$0]++' | peco)
  CURSOR=$#BUFFER
  zle reset-prompt
}

zle -N peco-history-selection
bindkey '^R' peco-history-selection

  BUFFER=$(fc -rl 1 | tac | awk '!a[$0]++' | peco)
  CURSOR=$#BUFFER
  zle reset-prompt
}

zle -N peco-history-selection
bindkey '^R' peco-history-selection
