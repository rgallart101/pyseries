#!/usr/bin/env python
# -*- encoding: utf8 -*-
"""
utils.py

Created by Ramon Maria Gallart Escolà on 2012-05-24.
Copyright (c) 2012 ramagaes. All rights reserved.
"""

from settings.constants import INFO, DEBUG, WARNING, ERROR


def print_message(level, msg):
    """
    Donat un nivell d'informació imprimeix per stdout un missatge. Per defecte
    La funció té a False el debugar.
    """
    data = ""

    if level == INFO:
        data = "[INFO] {}"
    elif level == DEBUG:
        data = "[DEBUG] {}"
    elif level == WARNING:
        data = "[WARNING] {}"
    elif level == ERROR:
        data = "[ERROR] {}"

    print(data.format(msg))
