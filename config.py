# -*- coding: utf-8 -*-
import os
import re
import socket
import subprocess
from re import sub
from subprocess import Popen, PIPE
from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from typing import List  # noqa: F401

mod = "mod4"                                     # Sets mod key to SUPER/WINDOWS
myTerm = "/usr/bin/qterminal"                             # My terminal of choice
myConfig = "/home/kevin/.config/qtile/config.py"    # The Qtile config file location
webdevice=" "
webtext=" "


#evince A\ systematic\ approach\ to\ learning\ robot\ programming\ with\ ros.pdf &
#xsetroot -cursor_name left_ptr -solid '#000000'  : solid black background
# run "xbindkeys --multikey" in home folder to check keybinds 
# suspend session --> sudo pm-suspend

keys = [
         ### The essentials
         Key([mod], "Return",
             lazy.spawn("qterminal"),
             desc='Launches My Terminal'
             ),
         Key([mod, "shift"], "Return",
             lazy.spawn("dmenu_run -p 'Run: '"),
             desc='Dmenu Run Launcher'
             ),
         Key([mod], "Tab",
             lazy.next_layout(),
             desc='Toggle through layouts'
             ),
         Key([mod, "shift"], "c",
             lazy.window.kill(),
             desc='Kill active window'
             ),
         Key([mod, "shift"], "r",
             lazy.restart(),
             desc='Restart Qtile'
             ),
         Key([mod, "shift"], "q",
             lazy.shutdown(),
             desc='Shutdown Qtile'
             ),
         Key(["control", "shift"], "e",
             lazy.spawn(myTerm+" sudo -S ls -l"),
             desc='Doom Emacs'
             ),
         Key([mod, "shift"], "s",
             lazy.spawn("i3lock -ufc 000000")
             ),
         ### Switch focus to specific monitor (out of three)
         Key([mod], "w",
             lazy.to_screen(0),
             desc='Keyboard focus to monitor 1'
             ),
         Key([mod], "e",
             lazy.to_screen(1),
             desc='Keyboard focus to monitor 2'
             ),
         Key([mod], "r",
             lazy.to_screen(2),
             desc='Keyboard focus to monitor 3'
             ),
         ### Switch focus of monitors
         Key([mod], "period",
             lazy.next_screen(),
             desc='Move focus to next monitor'
             ),
         Key([mod], "comma",
             lazy.prev_screen(),
             desc='Move focus to prev monitor'
             ),
         ### Treetab controls
         Key([mod, "control"], "k",
             lazy.layout.section_up(),
             desc='Move up a section in treetab'
             ),
         Key([mod, "control"], "j",
             lazy.layout.section_down(),
             desc='Move down a section in treetab'
             ),
         Key([mod, "control"], "i",
             lazy.layout.move_up(),
             desc='Move down a section in treetab'
             ),
         Key([mod, "control"], "l",
             lazy.layout.move_down(),
             desc='Move down a section in treetab'
             ),
         ### Window controls
         Key([mod], "k",
             lazy.layout.down(),
             desc='Move focus down in current stack pane'
             ),
         Key([mod], "j",
             lazy.layout.up(),
             desc='Move focus up in current stack pane'
             ),
         Key([mod, "shift"], "k",
             lazy.layout.shuffle_down(),
             desc='Move windows down in current stack'
             ),
         Key([mod, "shift"], "j",
             lazy.layout.shuffle_up(),
             desc='Move windows up in current stack'
             ),
         Key([mod], "h",
             lazy.layout.grow(),
             lazy.layout.increase_nmaster(),
             desc='Expand window (MonadTall), increase number in master pane (Tile)'
             ),
         Key([mod], "l",
             lazy.layout.shrink(),
             lazy.layout.decrease_nmaster(),
             desc='Shrink window (MonadTall), decrease number in master pane (Tile)'
             ),
         Key([mod], "n",
             lazy.layout.normalize(),
             desc='normalize window size ratios'
             ),
         Key([mod], "m",
             lazy.layout.maximize(),
             desc='toggle window between minimum and maximum sizes'
             ),
         Key([mod, "shift"], "f",
             lazy.window.toggle_floating(),
             desc='toggle floating'
             ),
         Key([mod, "shift"], "m",
             lazy.window.toggle_fullscreen(),
             desc='toggle fullscreen'
             ),
         ### Stack controls
         Key([mod, "shift"], "space",
             lazy.layout.rotate(),
             lazy.layout.flip(),
             desc='Switch which side main pane occupies (XmonadTall)'
             ),
         Key([mod], "space",
             lazy.layout.next(),
             desc='Switch window focus to other pane(s) of stack'
             ),
         Key([mod, "control"], "Return",
             lazy.layout.toggle_split(),
             desc='Toggle between split and unsplit sides of stack'
             ),
         ### Dmenu scripts launched with ALT + CTRL + KEY
         Key(["mod1", "control"], "e",
             lazy.spawn("./.dmenu/dmenu-edit-configs.sh"),
             desc='Dmenu script for editing config files'
             ),
         Key(["mod1", "control"], "m",
             lazy.spawn("./.dmenu/dmenu-sysmon.sh"),
             desc='Dmenu system monitor script'
             ),
         Key(["mod1", "control"], "p",
             lazy.spawn("passmenu"),
             desc='Passmenu'
             ),
         Key(["mod1", "control"], "r",
             lazy.spawn("./.dmenu/dmenu-reddio.sh"),
             desc='Dmenu reddio script'
             ),
         Key(["mod1", "control"], "s",
             lazy.spawn("./.dmenu/dmenu-surfraw.sh"),
             desc='Dmenu surfraw script'
             ),
        # Key(["mod1", "control"], "t",
        #     lazy.spawn("./.dmenu/dmenu-trading.sh"),
        #     desc='Dmenu trading programs script'
        #     ),
	 Key(["mod1", "control"], "t",
             lazy.spawn("thunar trash:///"),
             desc='Open Trash'
             ),
         ### My applications launched with SUPER + ALT + KEY
         Key([mod, "mod1"], "b",
             #lazy.spawn("tabbed -r 2 surf -pe x '.surf/html/homepage.html'"),
             #desc='lynx browser'
	     lazy.spawn("firefox --new-window  www.google.com"),
             ),
         #Key([], "XF86Explorer", lazy.spawn("firefox --new-window  www.google.com")),

         #Key([], "XF86HomePage", lazy.spawn("thunar")),
	 Key([mod, "mod1"], "d", lazy.spawn("thunar")),

	 #Key([], "XF86Mail", lazy.spawn("gnome-control-center")),

         Key([mod, "mod1"], "l",
             lazy.spawn("firefox --private-window"),
             desc='lynx browser'
             ),
         Key([mod, "mod1"], "n",
             lazy.spawn("gnome-todo"),
             desc='Take Notes'
             ),
         Key([mod, "mod1"], "r",
             lazy.spawn("teamviewer"),
             desc='teamviewer'
             ),
         Key([mod, "mod1"], "e",
             lazy.spawn("/usr/share/sangfor/EasyConnect/EasyConnect"),
             desc='EasyConnect'
             ),
         Key([mod, "mod1"], "m",
             lazy.spawn(myTerm+" -e sh ./scripts/toot.sh"),
             desc='toot mastodon cli'
             ),
         Key([mod, "mod1"], "t",
             lazy.spawn("teams"),
             desc='Microsoft Teams'
             ),
         Key([mod, "mod1"], "f",
             lazy.spawn("flameshot"),
             desc='flameshot'
             ),
         Key([mod, "mod1"], "j",
             lazy.spawn(myTerm+" -e joplin"),
             desc='joplin'
             ),
         Key([mod, "mod1"], "c",
             lazy.spawn("sudo /home/kevin/Desktop/kevin/pycharm-community-2020.3.3/bin/pycharm.sh"),
             desc='Pycharm'
             ),
         Key([mod, "mod1"], "p",
             lazy.spawn("pavucontrol"),
             desc='Volume Control Utility'
             ),
         Key([mod, "mod1"], "s",
             lazy.spawn("xfce4-settings-manager"),
             desc='Settings Manager'
             ),
         #Key([mod, "mod1"], "a",
            # lazy.spawn(myTerm+" -e ncpamixer"),
            # desc='ncpamixer'
            # ),
         Key([mod, "mod1"], "a",
             lazy.spawn("sudo atom --no-sandbox"),
             desc='Atom Editor'
             ),
         Key([mod, "mod1"], "g",
             lazy.spawn("gazebo"),
             desc='gazebo'
             ),
	 Key([mod, "mod1"], "v",
             lazy.spawn("vmware"),
             desc='vmware'
             ),
         Key([mod, "mod1"], "w",
             lazy.spawn("wps"),
             desc='wps'
             ),

	# Audio
	# Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
	# Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -c 2 sset Master 1- unmute")),
	# Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -c 2 sset Master 1+ unmute")),
	# Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    #	 Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    #	 Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
    #	 Key([], "XF86AudioStop", lazy.spawn("playerctl stop")),
    #	# Extras
    #	 Key([], "XF86Calculator", lazy.spawn("gnome-calculator")),
]


group_names = [(" ", {'layout': 'monadtall'}),               
               (" ", {'layout': 'ratiotile'}),
               (" ", {'layout': 'monadtall'}),
               (" ", {'layout': 'monadtall'}),
               (" ", {'layout': 'zoomy'}),
               (" ", {'layout': 'monadtall'}),
               (" ", {'layout': 'monadtall'}),
               (" ", {'layout': 'treetab'}),
               (" ", {'layout': 'monadtall'})]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name))) # Send current window to another group

layout_theme = {"border_width": 2,
                "margin": 6,
                "border_focus": "117af0",
                "border_normal": "1D2330"
                }

layouts = [
    layout.MonadWide(**layout_theme),
    #layout.Bsp(**layout_theme),
    #layout.Stack(stacks=2, **layout_theme),
    #layout.Columns(**layout_theme),
    layout.RatioTile(**layout_theme),
    layout.VerticalTile(**layout_theme),
    layout.Matrix(**layout_theme),
    layout.Zoomy(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Tile(shift_windows=True, **layout_theme),
    layout.Stack(num_stacks=2),
    layout.TreeTab(
         font = "UbuntuMono Nerd Font",
         fontsize = 10,
         sections = ["FIRST", "SECOND"],
         section_fontsize = 11,
         bg_color = "141414",
         active_bg = "90C435",
         active_fg = "000000",
         inactive_bg = "384323",
         inactive_fg = "a0a0a0",
         padding_y = 5,
         section_top = 10,
         panel_width = 320
         ),
    layout.Floating(**layout_theme)
]

colors = [["#000000", "#000000"], # panel background#292d3e
          ["#434758", "#434758"], # background for current screen tab
          ["#ffffff", "#ffffff"], # font color for group names
          ["#80b2ea", "#80b2ea"], # border line color for current tab ff5555
          ["#6441a5", "#6441a5"], # border line color for other tab and odd widgets
          ["#668bd7", "#668bd7"], # color for the even widgets
          ["#117af0", "#117af0"]] # window name e1acff c411f0
          
colors2 = [["#114ef0", "#114ef0"], # panel background#292d3e
          ["#d8f011", "#d8f011"], # background for current screen tab
          ["#11f018", "#11f018"], # font color for group names
          ["#11f08e", "#11f08e"], # border line color for current tab 11f08e
          ["#11dff0", "#11dff0"], # border line color for other tab and odd widgets 11dff0
          ["#11c1f0", "#11c1f0"], # color for the even widgets
          ["#117af0", "#117af0"]] # window name e1acff c411f0


prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

def get_my_net():
  import subprocess
  datanet=subprocess.Popen(["nmcli","-g","general.state","device","show","eth0"],stdout=subprocess.PIPE).communicate()
  datanetp=datanet[0].decode("utf-8");
  res = datanetp.split()
  datanet1=res[0]
  datanet2=res[1]
  
  #import subprocess
  #datawifi=subprocess.Popen(["nmcli","-g","general.state","device","show","wlan0"],stdout=subprocess.PIPE).communicate()
  #datawifip=datawifi[0].decode("utf-8");
  #res2 = datawifip.split()
  #datawifi1=res2[0]
  #datawifi2=res2[1]
  if datanet2=="(connected)":
    setdevice=("eth0","")
  #elif datawifi2=="(connected)":
  #  setdevice=("wlan0","")
  else:
    setdevice=("","睊   ")
  return setdevice

#def get_my_gpu_temp():
 # import subprocess
  #data = subprocess.Popen(["nvidia-smi","--query-gpu=temperature.gpu","--format=csv"],stdout=subprocess.PIPE).communicate()
  #return "{} °C".format(sub("\D", "", str(data)))


import subprocess
subprocess.call(['xsetroot', '-cursor_name', 'left_prt', '-solid', '#000000'])


##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    #font="Ubuntu Mono",
    font="UbuntuMono Nerd Font",
    fontsize = 12,
    padding = 0,
    background=colors[2]
)
extension_defaults = widget_defaults.copy()

a=get_my_net()
webdevice=a[0]
webtext=a[1]

def init_widgets_list():
    widgets_list = [
              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[2],
                       background = colors[0]
                       ),
              widget.GroupBox(
                       #font = "Ubuntu Bold",
                       font = "UbuntuMono Nerd Font",
                       fontsize = 19,
                       margin_y = 4,
                       margin_x = 2,
                       padding_y = 8,
                       padding_x = 10,
                       borderwidth = 1,
                       active = colors[2],
                       inactive = colors[2],
                       rounded = False,
                       highlight_color = colors[1],
                       highlight_method = "block",
                       this_current_screen_border = colors[6],
                       this_screen_border = colors2 [3],
                       other_current_screen_border = colors[0],
                       other_screen_border = colors[0],
                       foreground = colors[2],
                       background = colors[0]
                       ),
              widget.Prompt(
                       prompt = prompt,
                       font = "UbuntuMono Nerd Font",
                       padding = 10,
                       foreground = colors[3],
                       background = colors[1]
                       ),
              widget.Sep(
                       linewidth = 0,
                       padding = 40,
                       foreground = colors[2],
                       background = colors[0]
                       ),
              widget.WindowName(
                       foreground = colors[6],
                       background = colors[0],
                       padding = 0
                       ),
              widget.TextBox(
                       text = '',
                       background = colors[0],
                       foreground = colors2[3],
                       padding = -2,
                       fontsize = 37
                       ),
              widget.TextBox(
                       text = "ﴑ",
                       font = 'UbuntuMono Nerd Font',
                       fontsize = 19,
                       padding = 0,
                       foreground = colors[0],
                       background = colors2[3]
                       ),
              widget.BitcoinTicker(
              	       currency="EUR",
                       foreground = colors[0],
                       background = colors2[3],
                       padding = 5
                       ),
              widget.TextBox(
                       text = '',
                       background = colors2[3],
                       foreground = colors2[4],
                       padding = -2,
                       fontsize = 37
                       ),
              widget.TextBox(
                       text = "CPU:",
                       padding = 0,
                       foreground = colors[0],
                       background = colors2[4],
                       fontsize = 12
                       ),
              widget.ThermalSensor(
                       foreground = colors[0],
                       background = colors2[4],
                       threshold = 90,
                       tag_sensor = "Core 0", #Tdie
                       padding = 2
                       ),

	      widget.TextBox(
	               text="GPU:",
	               padding = 2,                       
                       foreground = colors[0],
                       background = colors2[4]
                       ),
             # widget.GenPollText(
              #         func=get_my_gpu_temp,
               #        update_interval=1,
	        #       padding = 5,
	         #      background = colors[5],
                  #     foreground = colors[2]
                   #    ),
              widget.ThermalSensor(
                       foreground = colors[0],
                       background = colors2[4],
                       threshold = 90,
                       tag_sensor = "temp1", #Tdie
                       padding = 2
                       ),
              widget.TextBox(
                       text = '',
                       background = colors2[4],
                       foreground = colors2[3],
                       padding = -2,
                       fontsize = 37
                       ),
              widget.TextBox(
                       text = "",
                       foreground = colors[0],
                       background = colors2[3],
                       padding = 0,
                       fontsize = 20
                       ),
              widget.Memory(
                       foreground = colors[0],
                       background = colors2[3],
                       mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn(myTerm + ' -e htop')},
                       padding = 5
                       ),
              widget.TextBox(
                       text='',
                       background = colors2[3],
                       foreground = colors2[4],
                       padding = -2,
                       fontsize = 37
                       ),
              widget.TextBox(
					   text=webtext,
                       foreground = colors[0],
                       background = colors2[4],
                       padding = 5,
                       fontsize = 15
                       ),
              widget.Net(
                       #interface = "enp34s0", #ethernet
                       #interface = "wlo1",	#wifi
                       interface = webdevice,
                       format = '{down} ↓↑ {up}',
                       foreground = colors[0],
                       background = colors2[4],
                       padding = 5
                       ),
              widget.TextBox(
                       text = '',
                       background = colors2[4],
                       foreground = colors2[3],
                       padding = -2,
                       fontsize = 37
                       ),
              widget.TextBox(
                       text ="",
                       foreground = colors[0],
                       background = colors2[3],
                       fontsize = 20,
                       padding = 9
                       ),
              widget.Volume(                       
                       #cardid = 2,
                       #device = 'hw:2',
                       foreground = colors[0],
                       background = colors2[3],
                       padding = 5
                       ),
              widget.TextBox(
                       text = '',
                       background = colors2[3],
                       foreground = colors2[4],
                       padding = -2,
                       fontsize = 37
                       ),
              widget.CurrentLayoutIcon(
                       custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                       foreground = colors[0],
                       background = colors2[4],
                       padding = 0,
                       scale = 0.7
                       ),
              widget.CurrentLayout(
                       foreground = colors[0],
                       background = colors2[4],
                       padding = 5
                       ),
              widget.TextBox(
                       text = '',
                       background = colors2[4],
                       foreground = colors2[3],
                       padding = -2,
                       fontsize = 37
                       ),
              widget.Clock(
                       padding = 3,
                       foreground = colors[0],
                       background = colors2[3],
                       format = '%d/%m/%Y - %H:%M:%S '
                       ),
              widget.Sep(
                       linewidth = 0,
                       padding = 10,
                       foreground = colors[0],
                       background = colors2[3]
                       ),
              widget.Systray(
                       background = colors[0],
                       padding = 5
                       ),
              ]
    return widgets_list

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1                       # Slicing removes unwanted widgets on Monitors 1,3

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2                       # Monitor 2 will display all widgets in widgets_list

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=20)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=1.0, size=20)),
            Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=20))]

if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
