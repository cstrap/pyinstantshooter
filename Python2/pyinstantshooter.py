#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
App     : pyInstantShooter2.0 - cross platform
Author  : Strap
Website : http://www.strap.it
Year    : 2009
License : http://creativecommons.org/licenses/by-nc-sa/3.0/
E-mail  : pyinstantshooter@strap.it
"""

import os
import sys

try:
    import gtk
    import gtk.glade
except:
    print "Text mode not ready yet, sorry!"
    sys.exit(0)

# Use gnome environment if it's possible, otherwise... IOError if the /dev/dsp is busy
try:
    import gnome
    gnome.sound_init('localhost')
    SOUND_ENV = 'gnome'
except:
    # Mabye have a IOError - know bug in env != gnome and win
    SOUND_ENV = 'standard'

import plugin.Plugin as loadPlugin

# Directory of this version (holds gui/) and the shared plugins directory
# (one level up, shared with the other Python version).
APP_DIR = os.path.dirname(os.path.abspath(__file__))
PLUGINS_DIR = os.path.join(os.path.dirname(APP_DIR), 'plugins')

def playWave(fileName):
    """ Play wave file cross platform """
    if PLATFORM == 'nt':
        from winsound import PlaySound, SND_FILENAME, SND_ASYNC
        PlaySound(fileName, SND_FILENAME|SND_ASYNC)
    elif PLATFORM == 'posix' and SOUND_ENV == 'standard':
        from wave import open as waveOpen
        from ossaudiodev import open as ossOpen
        s = waveOpen(fileName, 'rb')
        (nc, sw, fr, nf, comptype, compname) = s.getparams()
        dsp = ossOpen('/dev/dsp2', 'w')
        from ossaudiodev import AFMT_S16_LE
        dsp.setparameters(AFMT_S16_LE, nc, fr)
        data = s.readframes(nf)
        s.close()
        dsp.writeall(data)
        dsp.close()

def sound(button):
    """ Gtk callback for all button """
    playFile = os.path.join(PLUGINS_DIR, ui.get_widget('selectPlugin').get_active_text(), 'sounds', '%s.wav' % button.get_name())
    print playFile
    if SOUND_ENV == 'gnome':
        gnome.sound_play(playFile)
    else:
        playWave(playFile)

def populateSelectWithPlugin():
    """ Populate select whit plugin name """
    print 'Populate select'
    select = ui.get_widget('selectPlugin')
    for plug in loadPlugin.loader(PLUGINS_DIR):
        select.append_text(plug)
    select.set_active(0) # default
    onChangeSelect(ui.get_widget('selectPlugin'))

def onChangeSelect(button):
    """ Gtk callback, refreshing buttons icons """
    def imageFile(plug, number):
        return os.path.join(PLUGINS_DIR, plug, 'icons', '%s.png' % number)
    selectedPlugin = button.get_active_text()
    print "Plugin selected: ", selectedPlugin
    for item in ['img_one', 'img_two', 'img_three', 'img_four', 'img_five', 'img_six', 'img_seven', 'img_eight', 'img_nine']:
        number = item.split('_')[1]
        if os.path.isfile(imageFile(selectedPlugin, number)):
            ui.get_widget(item).set_from_file(imageFile(selectedPlugin, number))
        else:
            # Set default image
            ui.get_widget(item).set_from_file(imageFile('Default', number))

def exit(window):
    print "Exit"
    gtk.main_quit()

if __name__ == "__main__":
        print "init"
        # Settings for import customplugin
        PLATFORM,SELECTED_PLUGIN  = os.name, 'default'
        ui = gtk.glade.XML(os.path.join(APP_DIR, "gui", "pyinstantshooter.glade"))
        populateSelectWithPlugin()
        ui.signal_autoconnect(locals())
        gtk.main()
