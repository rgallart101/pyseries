#!/usr/bin/env python
# encoding: utf-8
"""
test.py

Created by Ramon Maria Gallart Escolà on 2012-11-25.
Copyright (c) 2012 www.ramagaes.com. All rights reserved.
"""

from bs4 import BeautifulSoup
from constants import PROGRAM, VERSION, DEBUG
from utils import print_message
import urllib2
import hashlib


COOKIE_NAME = 'todohdtv'
url = "http://foro.todohdtv.com/the-newsroom-temporada-1-720p-ac3-spanish-2012-05-10-t18667.html"
cookie = ''


def get_digest(url, cookie=None, do_debug=False):
    """
    Busquem el primer h2 amb la classe 'header'. Aquest h2 s'actualitza
    cada cop que es puja un nou capítol indicant si hi ha hagut novetats.
    """
    ok = True
    md5hash = ""
    user_agent = PROGRAM + ' v.' + VERSION
    req = urllib2.Request(url)
    req.add_header('User-Agent', user_agent)
    if cookie:
        req.add_header('Cookie', cookie)
    response = urllib2.urlopen(req)
    html = response.read()

    if do_debug:
        f = open('cookie-test.html', 'w')
        f.write(html)
        f.close()

    error_message = ""

    soup = BeautifulSoup(html)
    try:
        h2s = soup.find_all('h2', {'class': 'header'})
        print_message(DEBUG, repr(h2s[0]), do_debug)
        md5hash = hashlib.md5(repr(h2s[0])).hexdigest()
        print_message(DEBUG, md5hash, do_debug)
    except Exception, e:
        error_message = unicode(e)
        ok = False

    if ok:
        return md5hash
    else:
        raise Exception(error_message)


def main(do_debug=False):
    md5hash = get_digest(url, cookie, do_debug)
    print_message(DEBUG, 'Result: ' + md5hash, do_debug)


if __name__ == '__main__':
    import sys

    do_debug = False
    if len(sys.argv) > 1:
        do_debug = True

    main(do_debug)
