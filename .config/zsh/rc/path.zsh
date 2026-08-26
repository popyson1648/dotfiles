#--------------------
# go
#--------------------
# "~/.local/share/mise/installs/go/latest" は、~/go に相当する
export GOPATH=~/.local/share/mise/installs/go/latest
export PATH=$PATH:$GOPATH/bin
export PATH=$PATH:~/.cargo/bin

if [[ -d /opt/homebrew/opt/postgresql@16/bin ]]; then
  export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"
fi
