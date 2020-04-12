#!/usr/bin/python3
'''
a Fabric script (based on the file 1-pack_web_static.py)
that distributes an archive to your web servers,
using the function
'''
from fabric.api import *
import os
env.hosts = ['35.231.60.179', '34.228.186.160']


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


def do_deploy(archive_path):
    '''
    define do_deploy() function
    '''
    if os.path.isfile(archive_path) is False:
        return False
    try:
        archive = archive_path.split("/")[-1]
        path = "/data/web_static/releases"
        put("{}".format(archive_path), "/tmp/{}".format(archive))
        folder = archive.split(".")
        run("mkdir -p {}/{}/".format(path, folder[0]))
        new_archive = '.'.join(folder)
        run("tar -xzf /tmp/{} -C {}/{}/"
            .format(new_archive, path, folder[0]))
        run("rm /tmp/{}".format(archive))
        run("mv {}/{}/web_static/* {}/{}/"
            .format(path, folder[0], path, folder[0]))
        run("rm -rf {}/{}/web_static".format(path, folder[0]))
        run("rm -rf /data/web_static/current")
        run("ln -sf {}/{} /data/web_static/current"
            .format(path, folder[0]))
        return True
    except:
        return False


def deploy():
    '''
    define deploy() function
    '''
    d = do_pack()
    if d is None:
        return False
    return do_deploy(d)
