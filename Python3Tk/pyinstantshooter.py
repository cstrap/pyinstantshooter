#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
App     : pyInstantShooter2.0 - cross platform (Tkinter version)
Author  : Strap
Website : http://www.strap.it
Year    : 2009 (ported to Python 3 / Tkinter)
License : http://creativecommons.org/licenses/by-nc-sa/3.0/
E-mail  : pyinstantshooter@strap.it
"""

import atexit
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
import tkinter as tk
from tkinter import ttk

import plugin.Plugin as loadPlugin

PLATFORM = os.name


def _plugins_dir():
    # PyInstaller frozen binary
    if getattr(sys, "frozen", False):
        return os.path.join(sys._MEIPASS, "plugins")
    # zipapp .pyz
    exe = os.path.abspath(sys.argv[0])
    if os.path.isfile(exe) and zipfile.is_zipfile(exe):
        with zipfile.ZipFile(exe) as zf:
            has_plugins = any(n.startswith("plugins/") for n in zf.namelist())
        if has_plugins:
            tmpdir = tempfile.mkdtemp(prefix="pyis_plugins_")
            atexit.register(shutil.rmtree, tmpdir, ignore_errors=True)
            with zipfile.ZipFile(exe) as zf:
                for member in zf.namelist():
                    if member.startswith("plugins/"):
                        zf.extract(member, tmpdir)
            return os.path.join(tmpdir, "plugins")
        # fallback: plugins accanto al .pyz
        return os.path.join(os.path.dirname(exe), "plugins")
    # Normal script inside Python3Tk/
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "plugins"
    )


PLUGINS_DIR = _plugins_dir()

BUTTONS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

buttons = {}
images = {}
combo = None


def playWave(fileName):
    """Play a wave file cross platform."""
    if PLATFORM == "nt":
        from winsound import PlaySound, SND_FILENAME, SND_ASYNC

        PlaySound(fileName, SND_FILENAME | SND_ASYNC)
        return

    if sys.platform == "darwin":
        subprocess.Popen(["afplay", fileName])
        return

    # Linux/POSIX: try common players in order
    for player in ("paplay", "aplay", "ffplay"):
        path = shutil.which(player)
        if path:
            args = [path, fileName]
            if player == "ffplay":
                args = [path, "-nodisp", "-autoexit", "-loglevel", "quiet", fileName]
            subprocess.Popen(args)
            return

    print("No audio player found (tried paplay, aplay, ffplay).")


def sound(name):
    """Button click callback — play the sound for the given button name."""
    play_file = os.path.join(PLUGINS_DIR, combo.get(), "sounds", "%s.wav" % name)
    print(play_file)
    playWave(play_file)


def icon_file(plugin, name):
    return os.path.join(PLUGINS_DIR, plugin, "icons", "%s.png" % name)


def update_icons(plugin_name):
    """Refresh all button icons for the given plugin, falling back to Default."""
    for name in BUTTONS:
        path = icon_file(plugin_name, name)
        if not os.path.isfile(path):
            path = icon_file("Default", name)
        img = tk.PhotoImage(file=path)
        images[name] = img  # keep reference to prevent GC
        buttons[name].config(image=img)


def on_plugin_change(event=None):
    """Combobox selection callback."""
    selected = combo.get()
    print("Plugin selected:", selected)
    update_icons(selected)


def main():
    global combo

    root = tk.Tk()
    root.title("Instant Shooter")
    root.resizable(False, False)

    frame = tk.Frame(root, padx=5, pady=5)
    frame.pack()

    # Build 3x3 button grid with Default icons pre-loaded
    for i, name in enumerate(BUTTONS):
        default_icon = icon_file("Default", name)
        img = tk.PhotoImage(file=default_icon)
        images[name] = img
        btn = tk.Button(
            frame,
            image=img,
            padx=8,
            pady=8,
            command=lambda n=name: sound(n),
        )
        btn.grid(row=i // 3, column=i % 3, padx=2, pady=2)
        buttons[name] = btn

    # Plugin selector
    combo = ttk.Combobox(frame, state="readonly")
    combo["values"] = loadPlugin.loader(PLUGINS_DIR)
    combo.current(0)
    combo.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(4, 0))
    combo.bind("<<ComboboxSelected>>", on_plugin_change)

    root.mainloop()


if __name__ == "__main__":
    main()
