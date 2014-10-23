#!/usr/bin/env python
# -*- encoding: utf8 -*-
"""
test.py

Created by Ramon Maria Gallart Escolà on 2012-11-25.
Copyright (c) 2012 www.ramagaes.com. All rights reserved.
"""
import hashlib

from bs4 import BeautifulSoup
import requests

from settings.constants import PROGRAM, VERSION, DEBUG

COOKIE_NAME = 'todohdtv'


def get_digest(url):
    """
    Busquem el primer h2 amb la classe 'header'. Aquest h2 s'actualitza
    cada cop que es puja un nou capítol indicant si hi ha hagut novetats.
    """
    md5hash = ""
    user_agent = PROGRAM + ' v.' + VERSION
    headers = {'User-Agent': user_agent}

    r = requests.get(url, headers=headers)
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.content)
        h2s = soup.find_all('h2', {'class': 'header'})
        md5hash = hashlib.md5(repr(h2s[0]).encode('utf-8')).hexdigest()

    return md5hash
