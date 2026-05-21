1. https://emacsformacosx.com から .zip をダウンロード

2. Emacs.app を /Applications に入れる

3. CLI 用にシンボリックリンクを貼る：

ln -s /Applications/Emacs.app/Contents/MacOS/Emacs /usr/local/bin/emacs

4. Alias を設定する:

alias emacs='emacs -nw'
