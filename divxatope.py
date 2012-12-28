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


COOKIE_NAME = 'divxatope'
url = ""
cookie = ''


def get_digest(url, cookie=None, do_debug=False):
    """
    Busquem el primer div amb la classe 'torrent-container-2'. Aquest div 
    s'actualitza cada cop que es puja un nou capítol indicant si hi ha hagut
    novetats.
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
        elems = soup.find_all('div', {'class': 'torrent-container-2'})
        print_message(DEBUG, repr(elems[0]), do_debug)
        a = elems[0].find('h4').next_element
        md5hash = hashlib.md5(repr(a)).hexdigest()
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

