#!/usr/bin/python3
'''
generates a .tgz archive from the contents of
the web_static folder of your AirBnB Clone repo,
using the function do_pack.
'''
from fabric.api import local
from datetime import datetime


def do_pack():
    '''
    define do_pack function
    '''
    t = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    f = "versions/web_static_{}.tgz".format(t)
    try:
        local("mkdir -p ./versions")
        local("tar --create --verbose -z --file={} ./web_static"
              .format(f))
        return f
    except:
        return None
