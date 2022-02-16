import os
import subprocess
from libqtile import hook

from typing import List  # noqa: F401

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile import widget

mod = "mod4"
terminal = guess_terminal()


colors = [
    "#277dc2",  # Focus blue
    "#cfe7fa",  # Not focus light blue
    "#1cb850",  # Options green
    "#2aa353",  # Options green 2
    "#2aa37d",  # Options blue
    "#1eba89",  # Options blue 2
]


keys = [
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn("alacritty"), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "d", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod, "shift"], "d", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),

    # Browser
    Key([mod], "b", lazy.spawn("firefox"), desc="Spawn a firefox browser"),

    # Sound
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn(
        "amixer -c 0 sset Master 1- unmute")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn(
        "amixer -c 0 sset Master 1+ unmute")),

    # Brightness
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +5%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 5%-")),

    # Screenshots
    Key([mod], "s", lazy.spawn("scrot"), desc="Lauch scrot to take screenshots"),
    Key([mod, "shift"], "s", lazy.spawn("scrot -s"),
        desc="Lauch scrot to take screenshots for selected area"),

    # Screen lock (temporary)
    Key([mod], "x", lazy.spawn("dm-tool switch-to-greeter"),
        desc="Lauches a screen locker"),
]


groups = [Group(i) for i in [
    "   ", "   ", "   ", "   ", "  ", "   ", "   ", "   "
]]

for i, group in enumerate(groups):
    actual_key = str(i + 1)
    keys.extend([
        # Switch to workspace N
        Key([mod], actual_key, lazy.group[group.name].toscreen()),
        # Send window to workspace N
        Key([mod, "shift"], actual_key, lazy.window.togroup(group.name))
    ])

layouts = [
    # layout.MonadTall(margin=4, border_focus=colors[4], border_normal=colors[1], border_width=2),
    layout.Columns(border_focus=colors[4], border_normal=colors[1], margin=3, border_width=2),    
    # layout.MonadTall(),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(border_normal=colors[1], border_width=2, border_focus=colors[4], margin=4),
    # layout.Matrix(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()


def separator(bg="#000000", fg="#ffffff"):
    return widget.TextBox(
        font='UbuntuMono Nerd Font',
        text="",  # Icon: nf-oct-triangle_left
        fontsize=39,
        padding=-3,
        foreground=fg,
        background=bg
    )


def icon(bg="#000000", icon=""):
    return widget.TextBox(
        font='UbuntuMono Nerd Font',
        text=icon,  # Icon: nf-oct-triangle_left
        fontsize=16,
        foreground="ffffff",
        background=bg
    )


colors = [
    "#277dc2",  # Focus blue
    "#cfe7fa",  # Not focus light blue
    "#1cb850",  # Options green
    "#2aa353",  # Options green 2
    "#2aa37d",  # Options blue
    "#1eba89",  # Options blue 2
]


screens = [
    Screen(
        top=bar.Bar(
            [
                # widget.CurrentLayout(),
                widget.GroupBox(
                    font='UbuntuMono Nerd Font',
                    fontsize=16,
                    border_width=1,
                    background="#171717",
                    highlight_method="line",
                    rounded=True,
                    spacing=3,
                    highlight_color=[colors[4], colors[4]],
                ),
                widget.Prompt(),
                widget.WindowName(fontsize=0),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                # widget.Memory(),
                separator("", "#06c947"),
                widget.CheckUpdates(fontsize=24, no_update_string="", colour_have_updates="#e3051b",
                                    format='Updates: {updates}', colour_no_updates="#ffffff", background="#06c947"),
                separator("#06c947", colors[2]),
                icon(colors[2], " "),
                widget.DF(fontsize=12,
                          visible_on_warn=False, format='{uf} {m} - {r:.0f}%', background="#1cb850", padding_x=15),
                separator(colors[2], colors[3]),
                icon(colors[3], "直 "),
                widget.Net(interface="wlp2s0",
                           format='{down} ↓↑ {up}  ', background=colors[3]),
                separator(colors[3], colors[5]),
                icon(colors[5], " "),
                widget.Clock(format="%d/%m/%Y |",
                             padding=5, background=colors[5]),
                icon(colors[5], " "),
                widget.Clock(format="%I:%M:%S %p ",
                             padding=5, background=colors[5]),
                separator(colors[5], colors[4]),
                widget.Systray(background=colors[4]),
                # widget.QuickExit(),
            ],
            25,
            opacity=0.85,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~')
    subprocess.Popen([home + '/.config/qtile/autostart.sh'])
