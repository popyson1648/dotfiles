syntax on
set encoding=utf-8
set tabstop=4 softtabstop=4 shiftwidth=4 expandtab
set virtualedit+=block
set number incsearch hlsearch showtabline=2
set smartindent nofixendofline
set tabpagemax=1000
set backspace=indent,eol,start
set helplang=ja,en
set fileformat=unix
set statusline=%F
set laststatus=2
set wildignore=*/node_modules/*,*/pnpm-lock.yaml

if $TERM != "linux"
    " Use i-beam cursor in the insert mode.
    let &t_SI = "\<Esc>[6 q"
    let &t_EI = "\<Esc>[2 q"

    " Enable 24-bit colors.
    let &t_8f = "\<Esc>[38;2;%lu;%lu;%lum"
    let &t_8b = "\<Esc>[48;2;%lu;%lu;%lum"

    " Set up color scheme.
    set termguicolors
    colorscheme base16-atelier-dune-light
    command D colorscheme base16-atelier-dune
    command L colorscheme base16-atelier-dune-light
endif

" Enable spell checker.
autocmd BufReadPost * syntax spell toplevel
command   Spell set spell spelllang=en_us complete+=kspell
command NoSpell set nospell
autocmd FileType gitcommit Spell

" Enable commands for tab width.
function! s:set_tabwidth(w)
let &tabstop=a:w
let &softtabstop=a:w
let &shiftwidth=a:w
set expandtab
endfunction
command Tab2 call s:set_tabwidth(2)
command Tab4 call s:set_tabwidth(4)
command Tab8 call s:set_tabwidth(8)
autocmd VimEnter * Tab2

runtime macros/matchit.vim

" Auto-pair <> only in HTML/JSX/TSX
"autocmd FileType html,javascriptreact,typescriptreact let b:AutoPairs = extend(g:AutoPairs, {'<':'>'})

" Add blank line at EOF if missing on save
function! s:AddFinalBlankLine()
  if getline('$') !=# ''
    call append('$', '')
  endif
endfunction

autocmd BufWritePre * call s:AddFinalBlankLine()

" Use clipboard only in WSL (requires win32yank)
if system('uname -r') =~ 'microsoft'
  set clipboard=unnamedplus
endif

" ========================================
" plugin
" ========================================

let s:config_dir = fnamemodify(expand('<sfile>:p'), ':h')
let s:vim_dir = substitute(fnamemodify(s:config_dir . '/.vim', ':p'), '[/\\]$', '', '')
let s:dein_base = s:vim_dir . '/dein'
let s:dein_src = s:dein_base . '/repos/github.com/Shougo/dein.vim'
let g:copilot_chat_data_dir = get(g:, 'copilot_chat_data_dir', s:vim_dir . '/copilot-chat')

" Disable native package loading under this .vim directory because plugins are
" managed through dein.vim.
let s:packpath = split(&packpath, ',')
call filter(s:packpath, {_, v -> substitute(fnamemodify(v, ':p'), '[/\\]$', '', '') !=# s:vim_dir})
let &packpath = join(s:packpath, ',')

if isdirectory(s:dein_src)
  execute 'set runtimepath^=' . fnameescape(s:dein_src)

  if dein#load_state(s:dein_base)
    call dein#begin(s:dein_base)
    call dein#add(s:dein_src)
    call dein#load_toml(s:vim_dir . '/dein.toml', {'lazy': 0})
    call dein#load_toml(s:vim_dir . '/dein_lazy.toml', {'lazy': 1})
    call dein#end()
    call dein#save_state()
  endif
else
  echom 'dein.vim is not installed. Run install_plugins.sh.'
endif

" vim-lsp
let g:lsp_diagnostics_enabled = 0
let g:lsp_diagnostics_signs_enabled = 0
let g:lsp_hover_ui = 'none'
" let g:lsp_hover_auto = 0

" auto-pairs
command! DisableAutoPairs let g:AutoPairsMap = 0 | let g:AutoPairs = 0 | call AutoPairsToggle()
command! EnableAutoPairs  let g:AutoPairsMap = 1 | let g:AutoPairs = 1 | call AutoPairsToggle()

" coc.vim

"" Use K to show documentation in preview window
nnoremap <silent> K :call ShowDocumentation()<CR>

function! ShowDocumentation()
  if CocAction('hasProvider', 'hover')
    call CocActionAsync('doHover')
  else
    call feedkeys('K', 'in')
  endif
endfunction

" Tab で補完メニューの次アイテム選択／補完候補表示
inoremap <silent><expr> <TAB>
  \ coc#pum#visible() ? coc#pum#next(1) :
  \ coc#pum#confirm()

" Shift+Tab で前の候補へ
inoremap <expr><S-TAB> coc#pum#visible() ? coc#pum#prev(1) : "\<C-h>"

filetype plugin indent on
