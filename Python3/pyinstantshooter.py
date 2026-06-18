#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
App     : pyInstantShooter2.0 - cross platform
Author  : Strap
Website : http://www.strap.it
Year    : 2009 (ported to Python 3 / GTK 3)
License : http://creativecommons.org/licenses/by-nc-sa/3.0/
E-mail  : pyinstantshooter@strap.it
"""

import os
import sys
import shutil
import subprocess

try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
except (ImportError, ValueError):
    print("GTK 3 (PyGObject) is required. Text mode not ready yet, sorry!")
    sys.exit(0)

import plugin.Plugin as loadPlugin


def playWave(fileName):
    """ Play a wave file cross platform. """
    if PLATFORM == 'nt':
        from winsound import PlaySound, SND_FILENAME, SND_ASYNC
        PlaySound(fileName, SND_FILENAME | SND_ASYNC)
        return

    # POSIX: use whichever common player is available.
    for player in ('paplay', 'aplay', 'ffplay'):
        path = shutil.which(player)
        if path:
            args = [path, fileName]
            if player == 'ffplay':
                args = [path, '-nodisp', '-autoexit', '-loglevel', 'quiet', fileName]
            subprocess.Popen(args)
            return

    print("No audio player found (tried paplay, aplay, ffplay).")


def sound(button):
    """ Gtk callback for all buttons. """
    name = Gtk.Buildable.get_name(button)
    playFile = "%s/plugin/%s/sounds/%s.wav" % (
        os.getcwd(), ui.get_object('selectPlugin').get_active_text(), name)
    print(playFile)
    playWave(playFile)


def populateSelectWithPlugin():
    """ Populate the combo box with the plugin names. """
    print('Populate select')
    select = ui.get_object('selectPlugin')
    for plug in loadPlugin.loader():
        select.append_text(plug)
    select.set_active(0)  # default
    onChangeSelect(select)


def onChangeSelect(button):
    """ Gtk callback, refreshing the button icons. """
    imageFile = os.getcwd() + "/plugin/%s/icons/%s.png"
    selectedPlugin = button.get_active_text()
    print("Plugin selected: ", selectedPlugin)
    for item in ['img_one', 'img_two', 'img_three', 'img_four', 'img_five',
                 'img_six', 'img_seven', 'img_eight', 'img_nine']:
        number = item.split('_')[1]
        if selectedPlugin and os.path.isfile(imageFile % (selectedPlugin, number)):
            ui.get_object(item).set_from_file(imageFile % (selectedPlugin, number))
        else:
            # Set default image
            ui.get_object(item).set_from_file(imageFile % ('Default', number))


def exit(window):
    print("Exit")
    Gtk.main_quit()


if __name__ == "__main__":
    print("init")
    # Settings for importing custom plugins
    PLATFORM, SELECTED_PLUGIN = os.name, 'default'
    ui = Gtk.Builder()
    ui.add_from_file("gui/pyinstantshooter.ui")
    populateSelectWithPlugin()
    ui.connect_signals({
        'sound': sound,
        'onChangeSelect': onChangeSelect,
        'exit': exit,
    })
    ui.get_object('main_window').show_all()
    Gtk.main()
