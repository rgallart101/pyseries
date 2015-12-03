#!/usr/bin/env python
# -*- encoding: utf8 -*-
"""
test.py

Created by Ramon Maria Gallart Escolà on 2015-12-03.
Copyright (c) 2015 www.ramagaes.com. All rights reserved.
"""
import hashlib

from bs4 import BeautifulSoup
import requests


COOKIE_NAME = 'mundoteam'


def get_digest(url):
    """
    Busquem el primer h2 amb la classe 'title icon'. Aquest h2 s'actualitza
    cada cop que es puja un nou capítol indicant si hi ha hagut novetats.
    """
    md5hash = ""

    r = requests.get(url)
    if r.ok:
        soup = BeautifulSoup(r.content)
        h2s = soup.find_all('h2', {'class': 'title icon'})
        md5hash = hashlib.md5(repr(h2s[0]).encode('utf-8')).hexdigest()

    return md5hash
