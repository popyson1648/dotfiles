-- WezTermの設定スクリプトを読み込み
local wezterm = require 'wezterm';

-- カラースキームの定義
local colors = {
  white = '#f5f1e6',
  black = '#1c2121',
  yellow = '#f4cc20',
  gray = '#5d5c57'
};

-- パワーラインスタイルの記号定義
local SOLID_LEFT_ARROW = utf8.char(0xe0b6);

-- 表示項目の定義
local status_items = {
  {
    name = 'hostname',
    fg = colors.white,
    bg = colors.gray,
    arrow_fg = colors.gray,    -- ホスト名項目の矢印の前景色（自身の背景色）
    arrow_bg = colors.black,   -- ホスト名項目の矢印の背景色（次の項目の背景色）
  },
  {
    name = 'date',
    fg = colors.white,
    bg = colors.black,
    arrow_fg = colors.black,   -- 日付項目の矢印の前景色（自身の背景色）
    arrow_bg = colors.gray,    -- 日付項目の矢印の背景色（次の項目の背景色）
  },
  {
    name = 'battery',
    fg = colors.white,
    bg = colors.gray,
    -- バッテリー項目は最後なので矢印は不要です
  }
};

-- 右側のステータスバーを更新するためのイベントを定義
wezterm.on('update-right-status', function(window, pane)
  local elements = {};

  -- 各項目の情報を取得し、フォーマットする
  for index, item in ipairs(status_items) do
    local text;
    if item.name == 'hostname' then
      text = wezterm.hostname():gsub("%.local$", "");
    elseif item.name == 'date' then
      text = wezterm.strftime '%a %b %-d %H:%M';
    elseif item.name == 'battery' then
      for _, b in ipairs(wezterm.battery_info()) do
        text = string.format('%.0f%%', b.state_of_charge * 100);
      end
    end

    -- セル間の矢印を設定
    if index > 1 then
      local prev_item = status_items[index - 1];
      table.insert(elements, { Foreground = { Color = prev_item.arrow_fg } });
      table.insert(elements, { Background = { Color = prev_item.arrow_bg } });
      table.insert(elements, { Text = SOLID_LEFT_ARROW });
    end

    -- セルの内容を追加
    table.insert(elements, { Foreground = { Color = item.fg } });
    table.insert(elements, { Background = { Color = item.bg } });
    table.insert(elements, { Text = ' ' .. text .. ' ' });
  end

  -- 最終的なステータスバーを設定
  window:set_right_status(wezterm.format(elements));
end);
