# -*- coding: utf-8 -*-
'''
SaltStack code snippets
Provides an interface for querying information about the system CPUs

Copyright (C) 2017 Davide Madrisan <davide.madrisan.gmail.com>

'''

import salt.utils
import os

__virtualname__ = 'cpuinfo'
proc_cpuinfo = '/proc/cpuinfo'

def __virtual__():
    if os.path.exists(proc_cpuinfo):
        return True
    return False

def proc():
    '''
    Return the number of core, logical, and CPU sockets, by parsing
    the file /proc/cpuinfo.

    CLI Example:

        .. code-block:: bash

            salt '*' cpuinfo.proc
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

    return {
        'cores': cores,
        'logicals': cpus,
        'sockets': sockets
    }
