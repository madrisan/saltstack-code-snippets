# -*- coding: utf-8 -*-
'''
SaltStack code snippets
Return some informations about the configured file systems.

Copyright (C) 2017 Davide Madrisan <davide.madrisan.gmail.com>

'''
# Import python libs
import collections
import logging
import os

# Import salt libs
import salt.utils

log = logging.getLogger(__name__)

__virtualname__ = 'fsinfo'

def _sizeof_fmt(num, factor=1024.0, skip=1, suffix='B'):
    '''
    Divide 'num' to its best unit and append it to the output.
    '''
    units = ['', 'k','M','G','T','P']
    for unit in units[skip:]:
        if num < factor:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= factor
    return "%.1f%s%s" % (num, 'p', suffix)

def usage():
    '''
    Return informations about the existing filesystems

    CLI Example:
        .. code-block:: bash
            salt '*' fsinfo.usage

    '''
    fs_system = [
        '/',
        '/boot',
        '/home',
        '/images',
        '/opt', '/opt/bladelogic',
        '/root',
        '/tmp',
        '/usr', '/usr/openv',
        '/var', '/var/cache', '/var/log' ]

    if not os.path.isfile('/etc/mtab'):
        log.error('df cannot run without /etc/mtab')
        return {}
    if not os.path.isfile('/etc/fstab'):
        log.error('file not found: /etc/fstab')
        return {}

    out = __salt__['cmd.run']('df -aPTk', python_shell=False).splitlines()

    cols = ('filesystem', 'fstype', 'blocks', 'used',
            'available', 'capacity', 'mountpoint')
    # example:
    #  Filesystem Type 1024-blocks   Used Available Capacity Mounted on
    #  /dev/vg/lv ext4     1998672 352472   1541344      19% /var
    #  ...
    FileSystem = collections.namedtuple("Filesystem", cols)

    header = lambda line: line.startswith('Filesystem')
    dummy = lambda line: not line.startswith('/dev')
    data = (FileSystem(*line.split()) for line in out
        if not header(line) and not dummy(line))

    def automount(device):
        '''
        Check whether 'device' is configured for automount in fstab
        '''
        return __salt__['file.grep']('/etc/fstab', '^%s\s' % device)

    return dict(
        (fs.filesystem, {
            'automount': 'true' if automount(fs.filesystem) else 'false',
            'available': _sizeof_fmt(int(fs.available)),
            'class': 'system' if fs.mountpoint in fs_system else 'other',
            'device': fs.filesystem,
            'size': _sizeof_fmt(int(fs.blocks)),
            'type': fs.fstype,
            'used': _sizeof_fmt(int(fs.used))})
        for fs in data)
