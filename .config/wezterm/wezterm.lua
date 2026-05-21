local wezterm = require 'wezterm'
--local keybindings = require 'keybindings'

--require 'format'
--require 'status'

local hour = tonumber(os.date("%H"))
local darkSchemes = {
	"BlulocoDark",
	"CGA",
}
local lightSchemes = {
	"Builtin Solarized Light",
	"Catppuccin Latte",
}
local selectedScheme

if hour >= 6 and hour < 17 then
	selectedScheme = lightSchemes[2]
else
	selectedScheme = darkSchemes[1]
end

return {
	color_scheme = selectedScheme,
	window_background_opacity = 1.00,
	font = wezterm.font("HackGen Console NF"),
	font_size = 13.0,
	status_update_interval = 1000,
	window_decorations = 'RESIZE',
	use_ime = true,
	adjust_window_size_when_changing_font_size = false,
	tab_bar_at_bottom = true,
--	leader = { key="a", mods="CTRL", timeout_milliseconds=1001 },
	keys = keybindings.keybindings,
}
