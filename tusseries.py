#!/usr/bin/env python
# encoding: utf-8
"""
test.py

Created by Ramon Maria Gallart Escolà on 2012-05-23.
Copyright (c) 2012 ramagaes. All rights reserved.
"""

from bs4 import BeautifulSoup
from constants import PROGRAM, VERSION, INFO, DEBUG, WARNING, ERROR
from utils import print_message
import urllib2
import hashlib
import re

COOKIE_NAME = 'tusseries'

url = 'http://www.tusseries.com/index.php?showtopic=25222'
cookie = 'ipb_stronghold=f51c073a75236c0e3a355e1273ed5352; member_id=222999; pass_hash=c5b30259317e7f631fd09c7af0cb0db3'


def get_digest(url, cookie, do_debug):
    """
    A partir de la url i la cookie d'autentificació retorna un resum md5 dels
    ed2k que conté la pàgina.
    """
    ok = True
    md5hash = ""
    cadena = ""
    user_agent = PROGRAM + ' v.' + VERSION
    req = urllib2.Request(url)
    req.add_header('User-Agent', user_agent)
    req.add_header('Cookie', cookie)
    response = urllib2.urlopen(req)
    html = response.read()
    error_message = ""

    soup = BeautifulSoup(html)
    try:
        links = soup.find_all('a', href=re.compile("ed2k*"))
        print_message(DEBUG, str(links), do_debug)
        for link in links:
            cadena += link.get('href').encode('utf8')
        md5hash = hashlib.md5(cadena).hexdigest()
        print_message(DEBUG, md5hash, do_debug)
    except Exception, e:
        error_message = unicode(e)
        ok = False

    if ok:
        return md5hash
    else:
        raise Exception(error_message)


def main():
    md5hash = get_digest(url, cookie, True)
    print_message(DEBUG, 'Result: ' + md5hash, True)


if __name__ == '__main__':
    main()
