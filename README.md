# dotfiles

macOS、Linux、WSLへ共通の設定を導入するリポジトリです。

## 導入

GitとPython 3.10以降を用意し、継続して使う場所へリポジトリをcloneします。

```sh
git clone https://github.com/popyson1648/dotfiles.git ~/dotfiles
cd ~/dotfiles
```

変更内容を確認します。

```sh
python3 scripts/link-home.py --dry-run
```

`conflict`が表示された場合は、該当する既存ファイルを退避してから再確認します。

設定へのシンボリックリンクを作成します。

```sh
python3 scripts/link-home.py
```

導入結果を検証します。

```sh
python3 scripts/link-home.py --check
```

WSLでWindowsのホームディレクトリを指定する場合は、次のように実行します。

```sh
python3 scripts/link-home.py --windows-home /mnt/c/Users/<Windowsユーザー名>
```
