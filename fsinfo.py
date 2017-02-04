# -*- coding: utf-8 -*-
'''
SaltStack code snippets
Return some informations about the configured file systems.

Copyright (C) 2017 Davide Madrisan <davide.madrisan.gmail.com>

'''

import salt.utils

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

    filesystems_infos = __salt__['disk.usage']()
    infos = {}
    for fs in filesystems_infos:
        try:
            name = __salt__['disk.fstype'](fs)
            device = filesystems_infos[fs].get('filesystem')
            if not device.startswith('/dev/'):
                continue

            # example:
            #  Filesystem Type 1024-blocks   Used Available Capacity Mounted on
            #  /dev/vg/lv ext4     1998672 352472   1541344      19% /var
            df_out = __salt__['cmd.run']('df -PTk {0}'.format(fs)).splitlines()
            filesystem_infos = df_out[1].split()
            fstype, size, used, available = \
                list(filesystem_infos[i] for i in range(1,5))
            infos[fs] = {
                'available': _sizeof_fmt(int(available)),
                'device': device,
                'size': _sizeof_fmt(int(size)),
                'type': fstype,
                'used': _sizeof_fmt(int(used))
            }
            fs_class = 'system' if fs in fs_system else 'other'
            infos[fs].update({ 'class': fs_class })

            # check whether 'device' is configured for automount in fstab
            automount = __salt__['file.grep']('/etc/fstab', '^%s\s' % device)
            infos[fs].update({ 'automount': 'true' if automount else 'false' })
        except:
            continue

    return infos
