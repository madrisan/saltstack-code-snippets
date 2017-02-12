# -*- coding: utf-8 -*-
'''
Module for managing system clusters

Copyright (C) 2017 Davide Madrisan <davide.madrisan.gmail.com>

'''

# Import python libs
from os.path import basename as basename

# Import salt libs
import salt.utils

__virtualname__ = 'cluster'

def __virtual__():
    '''
    Confine this execution module on Red Hat systems
    '''
    if not __grains__.get('os_family') == 'RedHat':
        return (False, 'Unsopported os.')
    return True

def is_active():
    '''
    Check if a system cluster is running on this node.

    CLI Example:

        .. code-block:: bash

            salt '*' cluster.is_active

    '''
    first = lambda x: x.split()[0]
    cmd = lambda infos: first(infos.get('cmd'))
    kernel_proc = lambda c: c.startswith('[')
    procs_info = __salt__['status.procs']()
    procs_cmds = list(basename(cmd(p))
        for p in procs_info.values() if not kernel_proc(cmd(p)))

    rh_cluster_suite = lambda procs: 'clurgmgrd' in procs
    pacemaker_cluster = lambda procs: 'pacemakerd' in procs
    
    if rh_cluster_suite(procs_cmds):
        return (True, 'Red Hat Cluster Suite')
    elif pacemaker_cluster (procs_cmds):
        return (True, 'Pacemaker Cluster')

    return (False, 'Not a cluster node')

