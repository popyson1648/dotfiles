#================================
# Built-in command
#================================
# alias ls='ls -alhF'
alias showpath='echo $PATH | tr ":" "\n"'
alias rm='rm -i'
alias mv='mv -i'

#================================
# External command
#================================
alias ls='eza -alo -F --long --git --icons=automatic'
alias cat='bat --theme="base16"'

alias getignorelist='gh api -H "Accept: application/vnd.github+json" -H "X-GitHub-Api-Version: 2022-11-28" /gitignore/templates --jq ".[]"'

getignore() {
  gh api -H "Accept: application/vnd.github+json" \
         -H "X-GitHub-Api-Version: 2022-11-28" \
         -X GET /gitignore/templates/"$1" \
         --jq .source > .gitignore
}

alias tree='tree -a'

alias code='/mnt/c/Users/popyson/AppData/Local/Programs/Microsoft\ VS\ Code/bin/code'


#================================
# App
#================================
# macOS
alias cot='open -a CotEditor.app'
alias emacs='emacs -nw'

# common
alias v='vim'

#--------------------------------
# WezTerm
#--------------------------------
alias imgcat='wezterm imgcat'
