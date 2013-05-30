#!/usr/bin/env python
# encoding: utf-8
"""
vagos.py

Created by Ramon Maria Gallart Escolà on 2012-05-24.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""
from bs4 import BeautifulSoup
from constants import PROGRAM, VERSION, INFO, DEBUG, WARNING, ERROR
from utils import print_message
import urllib2
import hashlib
import re

COOKIE_NAME = 'vagos'

url = 'http://www.vagos.es/showthread.php?t=1783293'
cookie = 'bb1_lastvisit=1337875225; bb1_lastactivity=0; __utma=150572209.361459416.1337875227.1337875227.1337875227.1; __utmb=150572209.3.10.1337875227; __utmc=150572209; __utmz=150572209.1337875227.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); kcc_undefined1=24; __qca=P0-1610319199-1337875228950; bb1_sessionhash=b4c7aaf0b1c1e97d43c145f5b71bae8d'


def get_digest(url, cookie, do_debug):
    ok = True
    user_agent = PROGRAM + ' v.' + VERSION
    req = urllib2.Request(url)
    req.add_header('User-Agent', user_agent)
    req.add_header('Cookie', cookie)
    response = urllib2.urlopen(req)
    html = response.read()
    error_message = ""

    soup = BeautifulSoup(html)
    try:
        quotes = soup.find_all('blockquote', 'lastedited')
        print_message(DEBUG, str(quotes), do_debug)
        md5hash = hashlib.md5(str(quotes)).hexdigest()
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
