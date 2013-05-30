#!/usr/bin/env python
# encoding: utf-8
"""
test.py

Created by Ramon Maria Gallart Escolà on 2012-05-23.
Copyright (c) 2012 www.ramagaes.com. All rights reserved.
"""

from bs4 import BeautifulSoup
from constants import PROGRAM, VERSION, DEBUG
from utils import print_message
import urllib2
import hashlib


COOKIE_NAME = 'tusseries'
url = "http://www.tusseries.com/index.php?showtopic=25880"
# url = 'http://www.tusseries.com/index.php?showtopic=25222'
cookie = 'ipb_stronghold=e7239be8fc82676e86a96b801ed545d1; member_id=222999; pass_hash=34cab994d8eebaa30b0140671373f7a0'


def get_digest(url, cookie=None, do_debug=False):
    """
    Busquem el primer div amb la classe 'maintitle'. Aquest div s'actualitza
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
        divs = soup.find_all('div', {'class': 'maintitle'})
        print_message(DEBUG, str(divs), do_debug)
        md5hash = hashlib.md5(repr(divs[0])).hexdigest()
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
