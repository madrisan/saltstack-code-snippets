# -*- coding: utf-8 -*-
'''
SaltStack code snippets
Modulr for managing system CPUs

Copyright (C) 2017 Davide Madrisan <davide.madrisan.gmail.com>

'''

# Import 3rd-party libs
import os

# Import salt libs
import salt.utils
import salt.utils.fsutils
from salt.exceptions import CommandExecutionError

__virtualname__ = 'cpuinfo'
proc_cpuinfo = '/proc/cpuinfo'

def __virtual__():
    if not os.path.exists(proc_cpuinfo):
        return (False, 'The {0} file cannot be found.'.format(proc_cpuinfo))
    return True

def _lscpu():
    '''
    Get available CPU information.
    '''
    try:
        out = __salt__['cmd.run_all']("lscpu")
    except:
        return None
    salt.utils.fsutils._verify_run(out)
    data = dict()
    for descr, value in [elm.split(":", 1) for elm in out['stdout'].split(os.linesep)]:
        data[descr.strip()] = value.strip()

    cpus = data.get('CPU(s)')
    sockets = data.get('Socket(s)')
    cores = data.get('Core(s) per socket')

    return (cpus, sockets, cores)

def _proc():
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

    if cores == 0 and sockets == 0:
        # FIXME: assume that one core is installed
        cores = 1
        sockets = cpus

    return (cpus, sockets, cores)

def lscpu(*args):
    '''
    Return the number of core, logical, and CPU sockets, by parsing
    the lscpu command and following back to /proc/cpuinfo when this tool
    is not available.

    CLI Example:

        .. code-block:: bash

            salt '*' cpuinfo.lscpu
            salt '*' cpuinfo.lscpu logicals
    '''
    (cpus, sockets, cores) = _lscpu() or _proc()

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
