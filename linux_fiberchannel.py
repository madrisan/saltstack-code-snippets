# -*- coding: utf-8 -*-
'''
SaltStack code snippets
Module for managing fiber channel hardware.

Copyright (C) 2017 Davide Madrisan <davide.madrisan.gmail.com>
'''

# Import 3rd-party libs
import os

# Import salt libs
import salt.utils
import salt.utils.fsutils
from salt.exceptions import CommandExecutionError

__virtualname__ = 'linux_fiberchannel'

def __virtual__():
    '''
    Only run on Linux systems
    '''
    if __grains__['kernel'] != 'Linux':
        return (False, 'The {0} execution module cannot be loaded: '
                       'only available on Linux systems.'.format(
                       __virtualname__))
    if not salt.utils.which('systool'):
        return (False, 'The systool binary is not in the path.')
    return True

sysfs_fc_host = '/sys/class/fc_host'

def _fc_host_list():
    '''
    Return the list of fiber channel hosts
    '''
    sysfs_fc_hosts = __salt__['file.find'](
        sysfs_fc_host,
        mindepth=1,
        maxdepth=1
    )
    hosts = [os.path.basename(syspath) for syspath in sysfs_fc_hosts]
    return hosts

def show(*args):
    '''
    View system fiber channel device information.

    CLI Example:

        .. code-block:: bash

            salt '*' linux_fiberchannel.show
            salt '*' linux_fiberchannel.show host12
    '''
    def _parse_output(output):
        data = dict()
        for descr, value in [elm.split('=', 1) for elm in
                output.split(os.linesep) if elm.strip()]:
            data[descr.strip()] = value.strip().strip('"')
        return data

    data = dict()
    if not os.path.exists(sysfs_fc_host):
        return data

    hosts = _fc_host_list()
    for host in hosts:
        cmd = ['systool', '-c', 'fc_host', '-av', host]
        out = __salt__['cmd.run_all'](
                cmd,
                output_loglevel='trace',
                ignore_retcode=True,
                python_shell=False
            )
        if out['retcode'] == 0:
            data[host] = _parse_output(out['stdout'])

    if not args:
        return data
    try:
        ret = dict((arg, data[arg]) for arg in args)
    except:
        raise CommandExecutionError(
            'Invalid flag passed to {0}.show'.format(__virtualname__)
        )
    return ret
