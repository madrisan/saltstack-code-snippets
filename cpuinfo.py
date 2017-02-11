# -*- coding: utf-8 -*-
'''
SaltStack code snippets.
Module for managing system CPUs.
Copyright (C) 2017 Davide Madrisan <davide.madrisan.gmail.com>
'''
# Import 3rd-party libs
import os

# Import salt libs
import salt.utils
from salt.exceptions import CommandExecutionError

# Define the module's virtual name
__virtualname__ = 'cpuinfo'

proc_cpuinfo = '/proc/cpuinfo'

def __virtual__():
    if not os.path.exists(proc_cpuinfo):
        return (False, 'The {0} file cannot be found.'.format(proc_cpuinfo))
    return True

def proc(*args):
    '''
    Return the number of core, logical, and CPU sockets, by parsing
    the file /proc/cpuinfo.

    CLI Example:

        .. code-block:: bash

            salt '*' cpuinfo.proc
            salt '*' cpuinfo.proc logicals
    '''
    cpus, cpu_core_id, cpu_physical_id = 0, set(), set()

    with salt.utils.fopen(proc_cpuinfo, 'r') as fp_:
        for line in fp_:
            if line.startswith('processor'):
                cpus += 1
            elif line.startswith('core id'):
                cpu_core_id.update([line.split(':')[1].strip()])
            elif line.startswith('physical id'):
                cpu_physical_id.update([line.split(':')[1].strip()])
        cores = len(cpu_core_id)
        sockets = len(cpu_physical_id)

    infos = {
        'cores': cores, 
        'logicals': cpus,
        'sockets': sockets
    }

    if not args:
        return infos

    try:
        ret = dict((arg, infos[arg]) for arg in args)
    except:
        raise CommandExecutionError(
            'Invalid flag passed to {0}.proc'.format(__virtualname__)
        )
    return ret
