# -*- coding: utf-8 -*-
'''
SaltStack code snippets.
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

# Define the module's virtual name
__virtualname__ = 'fsinfo'

def _sizeof_fmt(tok, factor=1024.0, skip=1, suffix='B'):
    '''
    Divide 'num' to its best unit and append it to the output.
    '''
    try:
        num = int(tok)
    except ValueError:
        return tok

    units = ['', 'k','M','G','T','P']
    for unit in units[skip:]:
        if num < factor:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= factor
    return "%.1f%s%s" % (num, 'p', suffix)

def usage(human_readable=True):
    '''
    Return informations about the existing filesystems

    CLI Example:
        .. code-block:: bash
            salt '*' fsinfo.usage

    '''
    # we will ignore all the filesystem with a fstype not in this list
    fs_check_types = [
        'autofs',
        'ext2', 'ext3', 'ext4',
        'nfs', 'nfs4',
        'xfs' ]
    fs_networkfs = ['nfs', 'nfs4']  # FIXME: cifs fs unsupported

    if not os.path.isfile('/etc/mtab'):
        log.error('df cannot run without /etc/mtab')
        return {}
    if not os.path.isfile('/etc/fstab'):
        log.error('file not found: /etc/fstab')
        return {}

    cmd = 'df -PTk'
    cmd += ''.join([' -t %s' % fstype for fstype in fs_check_types])

    out = __salt__['cmd.run'](cmd, python_shell=False).splitlines()

    # example:
    #  Filesystem Type 1024-blocks   Used Available Capacity Mounted on
    #  /dev/vg/lv ext4     1998672 352472   1541344      19% /var
    #  ...
    cols = ('filesystem', 'fstype', 'blocks', 'used',
            'available', 'capacity', 'mountpoint')
    FileSystem = collections.namedtuple("Filesystem", cols)

    header = lambda line: line.startswith('Filesystem')
    error = lambda line: line.startswith('df:')
    data = (FileSystem(*line.split()) for line in out
        if not header(line) and not error(line))
    bool2str = lambda b: 'true' if b else 'false'
    fsscope = lambda fs: 'lan' if fs.fstype in fs_networkfs else 'Unknown' # FIXME

    def automount(device):
        '''Check whether 'device' is configured for automount in fstab'''
        return __salt__['file.grep']('/etc/fstab', '^%s\s' % device)

    fmt = lambda num: _sizeof_fmt(num) if human_readable else int(num)
    def fsinfos(fs):
        '''Return a dictionary containing the filesystem informations'''
        return {
            'autofs': bool2str(fs.fstype == 'autofs'),
            'automount': 'true' if automount(fs.filesystem) else 'false',
            'available': fmt(fs.available),
            'device': fs.filesystem,
            'fstype': fs.fstype,
            'mountpoint': fs.mountpoint,
            'scope': fsscope(fs),
            'size': fmt(fs.blocks),
            'used': fmt(fs.used)}

    return dict((fs.mountpoint, fsinfos(fs)) for fs in data)
