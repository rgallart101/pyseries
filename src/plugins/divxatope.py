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


def get_digest(url):
    """
    Busquem el primer div amb la classe 'torrent-container-2'. Aquest div 
    s'actualitza cada cop que es puja un nou capítol indicant si hi ha hagut
    novetats.
    """
    md5hash = ""
    user_agent = PROGRAM + ' v.' + VERSION
    headers = {'User-Agent': user_agent}

    r = requests.get(url, headers=headers)
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.content)
        elems = soup.find_all('div', {'class': 'torrent-container-2'})
        a = elems[0].find('h4').next_element
        md5hash = hashlib.md5(repr(a).encode("utf-8")).hexdigest()

    return md5hash
