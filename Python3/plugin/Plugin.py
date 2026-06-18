#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re


def loader(directory):
    """Return the sorted plugin names found in the shared plugins directory."""
    plugin_list = []
    c = re.compile(r"(.(\.py|\.pyc)$)|(Default)|(\.svn)|(__pycache__)")

    for plug in os.listdir(directory):
        if not c.findall(plug):
            print("Adding", plug)
            plugin_list.append(plug)
    plugin_list.sort()
    plugin_list.insert(0, "Default")

    return plugin_list


if __name__ == "__main__":
    loader(".")
